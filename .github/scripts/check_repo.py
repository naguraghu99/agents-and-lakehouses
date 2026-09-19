#!/usr/bin/env python3
"""Lightweight repository-structure + hygiene checks for CI (stdlib only).

Run from the repo root:  python .github/scripts/check_repo.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors = []


def fail(what: str, detail: str = "") -> None:
    errors.append(f"{what}: {detail}" if detail else what)


def main() -> int:
    # 1. Required top-level files/dirs.
    required = ["README.md", "COURSE.md", "SETUP.md", "PROGRESS.md",
                "concepts/README.md", "lakehouse/README.md",
                "hiver/ROADMAP.md", ".gitignore"]
    for path in required:
        if not (ROOT / path).exists():
            fail(f"missing required file/dir", path)

    # 2. No known-bad folder names (rigorousness over cleverness).
    bad_segments = ["aysnc", "lakehouse-learning", "AgenticAI-Hiver"]
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir():
            for bad in bad_segments:
                if bad in p.name:
                    fail("bad folder name", f"{p.name} ({bad}) -> rename")

    # The async module must exist under its corrected name.
    if not (ROOT / "agentic-ai-40-days/8.async_coding").is_dir():
        fail("async module not found inside agentic-ai-40-days/8.async_coding")

    # 3. Local markdown links (relative "../x/y.md") must resolve.
    md_files = list(ROOT.rglob("*.md"))
    link_re = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")
    for md in md_files:
        if ".venv" in md.parts or ".opencode" in md.parts:
            continue
        for m in link_re.finditer(md.read_text(encoding="utf-8", errors="replace")):
            target = m.group(1).strip()
            if not target or target.startswith(("http:", "https:", "mailto:", "www.")):
                continue
            # Resolve relative to the markdown file's directory.
            resolved = (md.parent / target)
            # Allow file paths with URL-encoded spaces etc. to pass only if found.
            if not resolved.exists() and not resolved.with_suffix(".md").exists():
                fail("broken md link", f"{md.relative_to(ROOT)} -> {target}")

    # 4. Secret hygiene on TRACKED files only (git tracked, not working-tree junk).
    secret_files = {"api_gemini", "api_key_groq", "api_meta"}
    secret_patterns = [r"gsk_[A-Za-z0-9]{20,}", r"AIza[0-9A-Za-z_-]{30,}",
                       r"LLM_[0-9A-Za-z_-]{20,}"]
    git_cmd = f"git -C {ROOT} ls-files"
    import subprocess
    tracked = subprocess.run(git_cmd, shell=True, capture_output=True,
                             text=True).stdout.splitlines()
    for path in tracked:
        name = Path(path).name
        if name in secret_files or name.endswith((".key", ".pem")):
            fail("tracked secret file", path)
        if name == ".env":
            fail("tracked .env", path)
        # Skip binary outputs; only scan text-ish files.
        if re.search(r"\.(png|jpg|pdf|bin|lock)$", path):
            continue
        try:
            text = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pat in secret_patterns:
            if re.search(pat, text):
                fail("possible secret pattern in tracked file", f"{path} ({pat})")

    # 5. Lightweight YAML sanity: workflows must have name/on/runs-on; compose must have services.
    for wf in sorted((ROOT / ".github/workflows").glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        for key in ("name:", "on:", "runs-on"):
            if key not in text:
                fail("workflow missing key", f"{wf.name}: {key}")
    compose = ROOT / "lakehouse/docker-compose.yml"
    if compose.exists() and "services:" not in compose.read_text(encoding="utf-8"):
        fail("compose missing services", str(compose))

    if errors:
        print(f"check_repo: {len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("check_repo: structure + hygiene OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())