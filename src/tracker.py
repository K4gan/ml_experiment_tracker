from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from time import time


DB_PATH = Path("experiments.sqlite")


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, project TEXT, model TEXT, metrics TEXT, params TEXT, created_at REAL)"
    )
    return conn


def log_run(project: str, model: str, metrics: dict[str, float], params: dict[str, str]) -> int:
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO runs(project, model, metrics, params, created_at) VALUES (?, ?, ?, ?, ?)",
            (project, model, json.dumps(metrics, sort_keys=True), json.dumps(params, sort_keys=True), time()),
        )
        return int(cursor.lastrowid)


def list_runs(project: str) -> list[tuple[int, str, str]]:
    with connect() as conn:
        return list(conn.execute("SELECT id, model, metrics FROM runs WHERE project = ? ORDER BY id DESC", (project,)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny sqlite-backed experiment tracker.")
    sub = parser.add_subparsers(dest="command", required=True)
    log = sub.add_parser("log")
    log.add_argument("--project", required=True)
    log.add_argument("--model", required=True)
    log.add_argument("--metric", action="append", default=[])
    show = sub.add_parser("list")
    show.add_argument("--project", required=True)
    args = parser.parse_args()

    if args.command == "log":
        metrics = dict(item.split("=", 1) for item in args.metric)
        run_id = log_run(args.project, args.model, {k: float(v) for k, v in metrics.items()}, {})
        print(f"run_id={run_id}")
    else:
        for run_id, model, metrics in list_runs(args.project):
            print(f"{run_id} {model} {metrics}")


if __name__ == "__main__":
    main()
