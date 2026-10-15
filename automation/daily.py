"""Bounded, one-task coding agent. Standard library only."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ("backend/app/", "backend/tests/", "frontend/app/", "docs/")
MAX_FILES = 2
MAX_CHARS_PER_FILE = 12000
MAX_OUTPUT_TOKENS = 3500
INPUT_USD_PER_M = 0.75
OUTPUT_USD_PER_M = 4.50


def run(*args, timeout=90):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def tasks():
    lines = (ROOT / "ROADMAP.md").read_text(encoding="utf-8").splitlines()
    found = [(int(m.group(1)), m.group(2)) for line in lines if (m := re.match(r"^(\d{2})\. (.+)$", line))]
    if len(found) != 90 or [n for n, _ in found] != list(range(1, 91)):
        raise ValueError("ROADMAP.md must have exactly 90 ordered tasks")
    return found


def select_task(progress):
    done = {item["id"] for item in progress["completed"]}
    return next(((n, description) for n, description in tasks() if n not in done), None)


def allowed_path(name):
    path = Path(name)
    return (not path.is_absolute() and ".." not in path.parts and
            name.replace("\\", "/") == name and
            any(name.startswith(prefix) for prefix in ALLOWED) and
            not name.endswith((".env", ".pem", ".key")))


def apply_edits(files):
    if not isinstance(files, dict) or not 1 <= len(files) <= MAX_FILES:
        raise ValueError("Proposal must change one or two files")
    for name, content in files.items():
        if not allowed_path(name) or not isinstance(content, str) or len(content) > MAX_CHARS_PER_FILE:
            raise ValueError(f"Unsafe or oversized edit: {name}")
    for name, content in files.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def check(files):
    names = list(files)
    if any(name.startswith("backend/") for name in names):
        result = run(sys.executable, "-m", "pytest", "-q", "backend/tests", timeout=90)
        if result.returncode:
            return False, (result.stdout + result.stderr)[-4000:]
    if any(name.startswith("frontend/") for name in names):
        result = run("npm", "run", "lint", "--prefix", "frontend", timeout=90)
        if result.returncode:
            return False, (result.stdout + result.stderr)[-4000:]
    if any(name.startswith("docs/") for name in names):
        if any(not (ROOT / name).read_text(encoding="utf-8").strip() for name in names):
            return False, "Documentation file is empty"
    return True, "Targeted checks passed"


def ask_agent(task, feedback, budget):
    context = {
        "task": task,
        "roadmap": (ROOT / "ROADMAP.md").read_text(encoding="utf-8")[:2500],
        "backend": (ROOT / "backend/app/main.py").read_text(encoding="utf-8")[:5500],
        "frontend": (ROOT / "frontend/app/page.tsx").read_text(encoding="utf-8")[:4500],
        "feedback": feedback,
    }
    prompt = json.dumps(context)
    # One UTF-8 character per input token is a deliberately conservative ceiling.
    worst = ((len(prompt) + 1000) * INPUT_USD_PER_M + MAX_OUTPUT_TOKENS * OUTPUT_USD_PER_M) / 1_000_000
    if worst > budget:
        raise RuntimeError("Daily API budget exhausted before model request")
    payload = {"model": os.getenv("OPENAI_MODEL", "gpt-5.4-mini"), "input": [
        {"role": "system", "content": "You are a constrained coding agent. Implement exactly the given task. Return only JSON: {\"files\": {\"relative/path\": \"complete file content\"}}. Change at most two files under backend/app/, backend/tests/, frontend/app/, or docs/. No secrets, workflow edits, dependency edits, or unrelated work."},
        {"role": "user", "content": prompt}], "max_output_tokens": MAX_OUTPUT_TOKENS,
        "reasoning": {"effort": "low"}, "store": False}
    request = urllib.request.Request("https://api.openai.com/v1/responses", data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=100) as response:
        data = json.load(response)
    usage = data.get("usage", {})
    actual = (usage.get("input_tokens", len(prompt) + 1000) * INPUT_USD_PER_M +
              usage.get("output_tokens", MAX_OUTPUT_TOKENS) * OUTPUT_USD_PER_M) / 1_000_000
    text = "".join(part.get("text", "") for item in data.get("output", [])
                   for part in item.get("content", []) if part.get("type") == "output_text")
    return json.loads(text)["files"], budget - max(actual, 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--controlled-test", action="store_true", help="Exercise first task without API or commit")
    args = parser.parse_args()
    progress = json.loads((ROOT / "progress.json").read_text(encoding="utf-8"))
    chosen = select_task(progress)
    if chosen is None:
        print("Roadmap complete")
        return
    day = dt.datetime.now(dt.timezone(dt.timedelta(hours=1))).date().isoformat()
    if any(item["date"] == day for item in progress["completed"]):
        print("One task already completed today")
        return
    number, description = chosen
    branch = f"codex/day-{number:02d}"
    if not args.controlled_test and run("gh", "api", f"repos/{os.environ['GITHUB_REPOSITORY']}/git/ref/heads/{branch}").returncode == 0:
        print(f"Existing branch {branch}; waiting for PR integration")
        return
    if args.controlled_test:
        files = {"docs/architecture.md": "# AgentForge architecture\n\nThe Next.js dashboard calls a FastAPI service. LangGraph runs planning steps. PostgreSQL stores project state. GitHub Actions runs one bounded coding task daily.\n"}
        apply_edits(files)
        ok, detail = check(files)
        print(f"Controlled task {number}: {detail}")
        if not ok:
            raise RuntimeError(detail)
        return
    budget = float(os.getenv("DAILY_BUDGET_USD", "0.06"))
    feedback = ""
    for attempt in range(1, 3):
        files, budget = ask_agent(description, feedback, budget)
        apply_edits(files)
        ok, feedback = check(files)
        if ok:
            progress["completed"].append({"id": number, "date": day, "task": description, "author": "AgentForge Automation", "checks": feedback})
            # Contribution eligibility is verified separately; workflow success is not proof.
            progress["contributions"].append({"date": day, "status": "unverified"})
            (ROOT / "progress.json").write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8")
            print(f"Completed task {number} on attempt {attempt}")
            return
        print(f"Attempt {attempt} failed: {feedback}", file=sys.stderr)
    (ROOT / "failed-attempt.txt").write_text(f"Task {number}: {description}\n{feedback}\n", encoding="utf-8")
    raise RuntimeError("Two attempts failed; incomplete files retained as workflow artifact")


if __name__ == "__main__":
    main()
