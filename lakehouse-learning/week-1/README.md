# Week 1: Ingestion & Storage

## Goals

- Understand the lakehouse architecture
- Install and configure local lakehouse tooling
- Build a local ingestion flow with NiFi and RustFS
- See how raw data lands in object storage

## Topics

- Lakehouse vs data lake vs data warehouse
- Medallion architecture (Bronze / Silver / Gold)
- NiFi flow basics and FlowFile concepts
- RustFS object storage setup

---

## 🏗️ Architecture & Data Flow

The environment is a tiny **lakehouse** — the three classic building blocks of a modern data platform, separated so each can scale independently:

| Layer | Component | Role |
|-------|-----------|------|
| **Storage** | RustFS | S3-compatible object store — where *all* data actually lives (the "lake") |
| **Compute** | Spark (Jupyter) | Reads/writes data in the lake, does the transformation work (the "engine") |
| **Metadata** | Iceberg REST Catalog | Tracks table schemas + file locations so Spark can treat files as tables (the "brain") |

### How the containers talk to each other

```
                         ┌─────────────────────────────────────────────────┐
                         │             LOCALHOST (your machine)             │
                         │                                                 │
 Browser ──► http://localhost:9001 ──► RustFS Console   (create buckets)    │
 Browser ──► http://localhost:8888 ──► Jupyter          (run notebooks)    │
 Browser ──► http://localhost:8181 ──► Iceberg REST      (JSON API, no UI)  │
                         │                                                 │
                         └───────────────────┬─────────────────────────────┘
                                             │
                  ┌──────────────────────────┼──────────────────────────┐
                  │        container network (services resolve by name) │
                  │                          │                          │
                  ▼                          ▼                          ▼
             ┌─────────┐   s3a://   ┌──────────────┐   catalog   ┌──────────────┐
             │  Spark  │◄──────────►│   RustFS     │◄───────────►│ Iceberg REST │
             │ (engine)│  Parquet   │   (storage)  │   via HTTP   │  (metadata)  │
             └─────────┘   files    └──────────────┘              └──────────────┘
```

**Inside the container network, services talk to each other by *service name*** (e.g. `http://rustfs:9000`), not by `localhost`. Your scripts only need the S3 endpoint — the metadata catalog is wired to the same store, so Spark and Iceberg always agree on where data lives.

### Where Spark runs and how it connects to your code

Spark runs **inside the `lakehouse-spark` container** (the `jupyter/pyspark-notebook` image). It is *not* a separate process on your host — when you run:

```bash
podman-compose exec spark python /home/week-1/bronze_silver_gold.py
```

`podman exec` sends that command into the **already-running container**, so the script executes inside the container's filesystem and Python environment — the exact same runtime that hosts the Jupyter server on `:8888`. Jupyter notebooks and CLI scripts are the *same* PySpark runtime, just entered through different doors.

Inside, a `SparkSession` runs the classic **driver–executor** model:

```
                     driver (inside container)
                 ┌────────────────────────────┐
                 │  SparkContext / UI at :4040│
                 │  your Python code runs     │  ← plans the work
                 └─────────────┬──────────────┘
                               │  distributes stages/tasks
                 ┌─────────────▼──────────────┐
                 │  executors (same container) │  ← actually read/write Parquet
                 │  via S3A → rustfs:9000      │
                 └────────────────────────────┘
```

- The `s3a://` scheme in `bronze_silver_gold.py` tells Spark to use **S3A**, its S3-compatible filesystem client, enabled by the `hadoop-aws` + `aws-java-sdk-bundle` jars the container downloads at startup.
- S3A reads the endpoint + credentials from the Spark config and talks to RustFS over HTTP at `http://rustfs:9000` (service-name resolution on the compose network).
- The **Spark UI at `http://localhost:4040`** is the *driver's* web UI — you can watch each stage and task as the pipeline runs.

> This is the same architecture used in production: a driver plans the DAG, executors do the file I/O. In this local setup everything shares one container; in a real cluster (covered later in the plan — see "Spark architecture & execution internals" days) the driver and executors are separate processes across many machines.

### Data flow through the pipeline

```
  simulate trades  ──► BRONZE (raw, append-only)  ──►  SILVER (clean + dedup)  ──►  GOLD (aggregates)
  (100 fake rows)       s3a://bronze/trades             s3a://silver/trades          s3a://gold/daily_symbol_summary
                        partitioned by date             validated, deduplicated      daily per-symbol stats
```

1. **Generate** — 100 simulated trade records (with *intentional duplicates* to test dedup).
2. **Bronze** — write everything exactly as-is, partitioned by `event_date`. Nothing is filtered or cleaned. This is your immutable source of truth.
3. **Silver** — read Bronze, drop the raw payload, keep only valid rows, and deduplicate on `trade_id` (keeping the latest event). Production-ready data.
4. **Gold** — read Silver and build business aggregates: daily per-symbol buy/sell volume + price stats.

Each step reads its input *from* the lake and writes its output *back to* the lake — the lake is the only place data is ever stored.

### Where each piece is used

| Piece | Used by |
|-------|---------|
| S3 API on `:9000` | Spark reads/writes Parquet; Iceberg stores table files |
| Console on `:9001` | You — inspect buckets, files, and what each layer produced |
| `rustfs-init` | One-shot job that creates the 5 buckets at startup |
| Iceberg REST on `:8181` | Spark connects as its `rest` catalog (metadata) |

---

## 🚀 Local Environment Setup

This week's environment consists of **RustFS** (object storage) + **Spark** (compute) + **Iceberg REST Catalog** (table metadata). All run via **Podman Compose** (Docker-compatible).

### Prerequisites

- Podman + podman-compose installed (see below)
- ~4GB free RAM for the containers

### 0. Install Podman (if not installed)

```bash
sudo apt update && sudo apt install -y podman podman-compose
```

### 1. Start the Environment

```bash
# From the project root
cd lakehouse-learning
podman-compose up -d
```

This starts:

| Service | Purpose | URL |
|---------|---------|-----|
| RustFS | Object storage (S3-compatible) | http://localhost:9001 (console) |
| Spark | PySpark compute + Jupyter | http://localhost:8888 |
| Iceberg REST | Table metadata catalog (JSON API) | http://localhost:8181/v1/config |

**Credentials:** `admin` / `password` (RustFS console + S3 API)

> **Iceberg REST has no web UI.** It is a JSON API consumed by Spark and other Iceberg clients — there is nothing to "browse" in a browser. Opening `http://localhost:8181/` returns `400 No route for request`, which is expected. To confirm it is healthy, open `http://localhost:8181/v1/config` — you should see a JSON list of API endpoints. The real endpoints Spark uses live under `/v1/{prefix}/namespaces` and `/v1/{prefix}/namespaces/{namespace}/tables`.

> ⚠️ **Rootless podman note**: If `podman-compose up -d` complains about binding ports, run with `sudo` or configure rootless networking.

### 2. Verify Everything is Up

```bash
podman-compose ps
```

You should see all containers with status `Up` / `healthy`.

### 3. Test the RustFS Buckets

The startup script auto-creates buckets: `raw`, `bronze`, `silver`, `gold`, `warehouse`.
Open http://localhost:9001 → log in → you should see all 5 buckets in the console.

---

## 🧪 Hands-On: Day 1 — Bronze / Silver / Gold

The script `bronze_silver_gold.py` demonstrates the full medallion pipeline:

```bash
# From the project root, exec into the Spark container
podman-compose exec spark python /home/week-1/bronze_silver_gold.py
```

### What it does

1. **Generates** 100 simulated trade records (with intentional duplicates)
2. **Bronze layer** → writes raw data partition-by-date to `s3a://bronze/trades`
3. **Silver layer** → reads Bronze, drops raw payload, validates, dedupes on `trade_id`, writes to `s3a://silver/trades`
4. **Gold layer** → aggregates daily per-symbol buy/sell volume + price stats → `s3a://gold/daily_symbol_summary`

### Follow the data live

To *see* the lakehouse in action as the script runs:

```bash
# Easiest: open the RustFS console (http://localhost:9001) and keep it on the buckets view
# Optional, only if you have the AWS CLI installed on your host:
watch -n 1 "aws --endpoint-url http://localhost:9000 s3 ls --recursive s3://bronze/ && echo --- && aws --endpoint-url http://localhost:9000 s3 ls --recursive s3://silver/ && echo --- && aws --endpoint-url http://localhost:9000 s3 ls --recursive s3://gold/"
```

You should see the pipeline move through three stages:

1. `bronze/trades/event_date=.../*.parquet` appears **first** (raw rows).
2. `silver/trades/*.parquet` appears **second** — fewer files, deduplicated rows.
3. `gold/daily_symbol_summary/*.parquet` appears **last** — tiny aggregate table.

That ordering (bronze → silver → gold) *is* the medallion architecture working: each layer builds on the one before it, and the lake is the single source of truth at every step.

### Verify the output in RustFS

Open http://localhost:9001 → browse the buckets:

- `bronze/trades/` → partitioned Parquet files (event_date=...)
- `silver/trades/` → clean, deduplicated Parquet
- `gold/daily_symbol_summary/` → aggregate Parquet

---

## 📖 Optional: Use Jupyter instead of CLI

1. Open http://localhost:8888 in your browser (no password)
2. Create a new notebook
3. Run interactively cell-by-cell (copied from `bronze_silver_gold.py`) and inspect DataFrames, `explain()`, and Spark UI at http://localhost:4040

> **If Jupyter reports `Permission denied: Untitled.ipynb`**: the notebook can't save because the container's `jovyan` user lacks write access to the mounted `/home/week-1` host folder. The compose file now runs `chmod -R a+rwX /home/week-1 /home/data` at spark startup, so a fresh `podman-compose up -d` fixes it automatically. For the current session you can also fix it from the host: `chmod -R a+rwX week-1 data`.

---

## ✅ Day 1 Checklist

- [ ] `podman-compose up -d` starts all services
- [ ] RustFS console shows 5 buckets
- [ ] `bronze_silver_gold.py` runs end-to-end
- [ ] Parquet files appear in bronze / silver / gold buckets
- [ ] You can explain the separation of storage, compute, and metadata

## 💡 Concept Check

Why do we keep Bronze as **immutable append-only**, Silver **cleaned/deduped**, and Gold **business aggregates**?

- **Bronze** = source of truth, replayable, nothing discarded
- **Silver** = production-ready, validated, deduplicated
- **Gold** = curated for analytics / BI / ML consumers

## 🧹 Shutting Down / Restarting / Resetting

### Stop the environment (keep all data)

If the containers are already running and you want to stop them:

```bash
podman-compose down
```

This stops and removes the containers but **keeps the volumes** (your buckets + Parquet files survive).

### Restart the environment

```bash
podman-compose up -d
```

> It is safe to run this when containers are already up — it will only create what's missing. If a container is misbehaving, remove it first: `podman rm -f lakehouse-spark` (etc.) then run `up -d` again.

### Reset from scratch (purge all data)

```bash
podman-compose down -v
```

The `-v` flag also deletes the volumes (`rustfs-data`, `rustfs-logs`), wiping **all** buckets and data. After this, `podman-compose up -d` gives you a clean slate:

```bash
podman-compose up -d
podman-compose ps
```

You should see the stack come back up, buckets auto-created by `rustfs-init`, and empty bronze/silver/gold layers.

> **Note:** If ports are blocked by leftover containers (e.g. from an older MinIO-based setup), remove them first: `podman rm -f lakehouse-minio lakehouse-minio-init`.

### Understanding the one-shot setup containers

If you run `podman ps -a`, you'll see two containers sitting in `Exited (0)`:

| Container | What it does | Why it exits |
|-----------|--------------|--------------|
| `lakehouse-rustfs-perms` | Fixes volume ownership (`chown -R 10001:10001 /data /logs`) because RustFS runs as non-root UID `10001` | The `chown` finishes → shell command ends → exit `0`. Nothing left to do. |
| `lakehouse-rustfs-init` | Creates the buckets (`warehouse`, `bronze`, `silver`, `gold`, `raw`) via `aws s3 mb` | The bucket loop completes → exit `0`. Bucket definitions persist in the RustFS volume. |

**Why this is normal:**

- Exit code `0` means **success**, not a crash (a crash would show `Exited (1)` or higher).
- They are `restart: "no"` / one-shot, so podman never restarts them — they stay `Exited (0)`.
- They do their job in a guaranteed order via `depends_on`: `perms` fixes ownership → `rustfs` starts → `init` creates buckets → `spark`/`iceberg` come up last.
- The work they do survives them: bucket definitions live in the persistent RustFS volume, not in the container.

**Why they are re-created on every `up`:**

- `podman-compose down` removes **all** containers (volumes persist, containers don't). On the next `podman-compose up -d`, compose recreates them from the same definitions, they run their small job, and exit again.
- Re-running is safe because the work is **idempotent**: `chown` on already-correctly-owned dirs is a no-op, and `aws s3 mb` on an existing bucket is caught by `|| echo "bucket ... already exists"`.

So every `up` → they run for a few seconds → exit `0` → you see two `Exited (0)` containers. That's the intended lifecycle — it's a sign the setup worked, not a problem.