"""
Root Launcher for Credit Scoring Pipeline.
Delegates to Credit_scoring_project-main/run_pipeline.py
"""
import sys
import os

# Ensure UTF-8 output encoding on Windows consoles
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

root_dir = Path(__file__).resolve().parent
project_dir = root_dir / "Credit_scoring_project-main"

if not project_dir.exists():
    raise FileNotFoundError(f"Project directory not found at: {project_dir}")

# Change working directory and sys.path
sys.path.insert(0, str(project_dir))

from run_pipeline import main

if __name__ == "__main__":
    main()
