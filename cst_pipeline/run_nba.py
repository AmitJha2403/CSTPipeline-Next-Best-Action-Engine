# run_nba.py
import json
from engine.nba_pipeline import run_pipeline
import os
from tqdm import tqdm

if __name__ == "__main__":
    print("Running Next-Best-Action Engine...")

    results = run_pipeline(use_tqdm=True, limit=50, use_llm=False)

    output_path = os.path.join("cst_pipeline", "output", "nba_output.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved NBA output to: {output_path}")
    print(f"Total results: {len(results)}")
