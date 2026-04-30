# Ml Experiment Tracker

SQLite-backed experiment tracker for local ML runs, metrics and reproducibility notes.

## Stack

- Language: Python
- Difficulty: very high
- Scope: small, self-contained service/tool with clear extension points

## Project layout

The repository keeps implementation code under `src/` where that is idiomatic, plus a short runnable entry point and a small sample payload when useful.

## Run

```bash
python src/tracker.py log --project churn --model forest --metric auc=0.91
```

## Engineering notes

The implementation keeps parsing, domain logic and output formatting separate enough to grow without turning into a script dump. Generated artifacts and dependency folders are intentionally ignored.
