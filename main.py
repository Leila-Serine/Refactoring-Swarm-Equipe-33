import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer
from src.agents.judge_agent import run_judge

load_dotenv()


def discover_files(target_path: str, file_ext: str) -> list[str]:
    p = Path(target_path)

    if p.is_file():
        return [str(p)]

    if p.is_dir():
        return [
            str(x) for x in p.iterdir()
            if x.is_file() and x.suffix == file_ext
        ]

    return []


def main():
    # ---------------- CLI sécurisé ----------------
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm – Final Stable Version"
    )

    parser.add_argument("--target_dir", required=True)
    parser.add_argument("--max_iterations", type=int, default=5)
    parser.add_argument("--file_ext", type=str, default=".py")
    parser.add_argument("--dry_run", type=str, default="false")

    args = parser.parse_args()

    target_dir = args.target_dir
    max_iter = min(args.max_iterations, 10)  # Sécurité max 10
    file_ext = args.file_ext.strip()
    dry_run = args.dry_run.lower() == "true"

    if not os.path.exists(target_dir):
        print("❌ Target path not found")
        return

    files = discover_files(target_dir, file_ext)

    if not files:
        print("❌ No matching files found")
        return

    # ---------------- Orchestration ----------------
    for file_path in files:
        print(f"\n📄 Processing: {file_path}")
        current_target = file_path

        for iteration in range(1, max_iter + 1):
            print(f"🔄 Iteration {iteration}")

            # 1️⃣ Auditor
            analysis = run_auditor(current_target)

            if analysis.get("decision") == "ACCEPTED":
                print("✅ Auditor accepted")
                break

            # 2️⃣ Fixer
            if not dry_run:
                current_target = run_fixer(
                    current_target,
                    analysis,
                    iteration
                )

            # 3️⃣ Judge
            judge_result = run_judge(target_dir, iteration)

            if judge_result.get("decision") == "ACCEPTED":
                print("✅ Judge accepted")
                break

        else:
            print("⚠ Max iterations reached")

    print("\n✅ PROCESS FINISHED")


if __name__ == "__main__":
    main()