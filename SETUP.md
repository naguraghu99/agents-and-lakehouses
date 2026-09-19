# Setup

This course has **two independent tracks** — get each one running before its phases start.

| Track | Where | What you need | Optional |
|---|---|---|---|
| Agentic AI course | `agentic-ai-40-days/` | Python 3.10+ · a free Groq API key | Ollama (local models) |
| Lakehouse course | `lakehouse/` | Podman (or Docker) + `podman-compose` | AWS CLI (host, for `s3 ls`) |

Both together need roughly **4 GB of free RAM** and ~2 GB of disk for the lakehouse containers.

There is no GPU requirement — every LLM call in this repo goes to Groq's free tier, and the lakehouse runs locally in user-space containers.

---

## Track A — Agentic AI course (Python + one free API key)

### 1. Python version

The pinned dependency set (`agentic-ai-40-days/requirements.txt`) requires **Python 3.10+**. Python 3.11 / 3.12 is what it is tested with.

Check your version:

```bash
python3 --version   # needs to report 3.10 or higher
```

### 2. Create a virtual environment

```bash
cd agentic-ai-40-days
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows (PowerShell)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The requirements include Groq, LangChain, LangGraph, ChromaDB (for RAG), FastAPI/uvicorn (for the async module) and ruff. `pip` will resolve the whole locked set.

### 3. API keys — what is required vs optional

| Variable | Required? | Used by | Where to get it |
|---|---|---|---|
| `GROQ_API_KEY` | **Yes** for LLM modules (4, 5, 7, 8) | the Groq client + LangChain Groq | Free at https://console.groq.com/keys |
| `GEMINI_API_KEY` | No — nothing in the course calls it yet | reserved | https://aistudio.google.com/apikey |
| `META_*` / Llama keys | No — reserved for future modules | reserved | — |

The reader also supports **Ollama** (`langchain-ollama` is in the pinned deps) if you want fully local, key-free models — but all course examples target Groq.

### 4. Configure a module

Each LLM module ships an `.env.example`. Copy it and fill in your key:

```bash
# from agentic-ai-40-days/4.prompt_engineering/
cp .env.example .env
# edit .env →  GROQ_API_KEY="gsk_..."
```

The example modules (e.g. `groq_client.py`, `tool_calling.py`) read the key via `python-dotenv` (`load_dotenv()`), so run them **from that module's directory**.

```bash
cd 4.prompt_engineering && python groq_client.py
cd 5.tool_calling        && python tool_calling.py
cd 7.simple_rag          && python simple_rag.py
```

**Never commit a `.env` or the raw key files.** See [Secrets, data, and credentials](#secrets-data-and-credentials).

---

## Track B — Lakehouse course (containers on your laptop)

### 1. Install Podman (or Docker)

Podman is the tested path (rootless, daemon-free):

```bash
sudo apt update && sudo apt install -y podman podman-compose   # Debian/Ubuntu
# podman + podman-compose on Fedora, or Docker Desktop + docker compose elsewhere
```

Docker works too — the compose file is Docker-compatible; replace `podman-compose` with `docker compose` in every command below.

> **Rootless note:** if `podman-compose up` complains about binding ports, run with `sudo` or configure rootless podman networking.

### 2. Start the stack

```bash
cd lakehouse
podman-compose up -d          # first run downloads images + hadoop-aws jars — allow a few minutes
podman-compose ps             # wait until spark shows healthy/up
```

| Service | Purpose | URL |
|---|---|---|
| RustFS | S3-compatible object storage ("the lake") | http://localhost:9001 (console) |
| Spark + Jupyter | PySpark compute | http://localhost:8888 · Spark UI http://localhost:4040 |
| Iceberg REST | table metadata catalog (JSON API, no UI) | http://localhost:8181/v1/config |
| RustFS S3 API | endpoint your scripts use | http://localhost:9000 (admin / password) |

`rustfs-init` auto-creates five buckets on startup: `raw`, `bronze`, `silver`, `gold`, `warehouse`.

### 3. Run Week 1

```bash
podman-compose exec spark python /home/week-1/bronze_silver_gold.py
```

Then watch bronze → silver → gold Parquet appear in the RustFS console, or from the host:

```bash
aws --endpoint-url http://localhost:9000 s3 ls --recursive s3://bronze/  # per-command; see week-1/README.md for the full watch loop
```

The detailed week-1 walkthrough (how the containers talk to each other, driver–executor, reset options) is in `lakehouse/week-1/README.md`.

### 4. Stop / clean up

```bash
podman-compose down      # stop, keep data (volumes survive)
podman-compose down -v   # stop AND wipe all buckets / Parquet — full reset
```

Two one-shot containers (`rustfs-perms`, `rustfs-init`) exit `0` on startup — that is normal, not a crash (details in `lakehouse/week-1/README.md`).

---

## Secrets, data, and credentials

**Never commit these** (the `.gitignore` already excludes them — keep it that way):

- `api_gemini`, `api_key_groq`, `api_meta` — raw key files at the repo root
- `.env` files (templates `.env.example` are committed and safe)
- `*.key`, `*.pem`
- Notebook checkpoints (`.ipynb_checkpoints/`)

A CI check in `.github/workflows/validate.yml` guards the repo against accidentally tracking keys or the raw key files.

**The Hiver dataset** (`phases 1–5`) is **not** in this repo and must be downloaded manually:

- Source: Kaggle — `thoughtvector/customer-support-on-twitter` (`twcs.csv`, ~3M rows, Twitter support conversations).
- Download it yourself, keep it **outside** the repo, and work from a 1% subsample only (Phase 1).
- It is historical (~2017) and cannot be redistributed from this repo, so a fresh clone will not contain it.

**The 15-minute rule:** this course is built so a clean clone plus the steps above reproduces every headline number in under 15 minutes. If a step here takes longer, that is a bug — log it in `hiver/journey/learning-log.md`.