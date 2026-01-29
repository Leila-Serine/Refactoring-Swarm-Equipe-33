import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

load_dotenv()


def discover_files(target_path: str, file_ext: str) -> list[str]:
    """
    Découvre les fichiers à traiter.
    - fichier → [fichier]
    - dossier → fichiers avec extension donnée (non récursif)
    """
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
    # -------------------------------
    # 1️⃣ CLI
    # -------------------------------
    parser = argparse.ArgumentParser(
        description="Refactoring Swarm Orchestrator – Stable version (Jour 7/8)"
    )
    parser.add_argument("--target_dir", required=True)
    parser.add_argument("--max_iterations", type=int, required=True)
    parser.add_argument("--file_ext", type=str, required=True)
    parser.add_argument("--dry_run", type=str, required=True)

    args = parser.parse_args()

    target_dir = args.target_dir
    max_iter = args.max_iterations
    file_ext = args.file_ext.strip()
    dry_run = args.dry_run.lower() == "true"

    # -------------------------------
    # 2️⃣ Validation
    # -------------------------------
    if not os.path.exists(target_dir):
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Path validation",
                "output_response": f"Target path not found: {target_dir}"
            },
            status="FAIL"
        )
        print("❌ Chemin introuvable")
        return

    if max_iter <= 0:
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "CLI validation",
                "output_response": "max_iterations must be > 0"
            },
            status="FAIL"
        )
        print("❌ max_iterations invalide")
        return

    if not file_ext.startswith("."):
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "CLI validation",
                "output_response": f"Invalid file_ext: {file_ext}"
            },
            status="FAIL"
        )
        print("❌ file_ext invalide")
        return

    # -------------------------------
    # 3️⃣ Log STARTUP (plus précis)
    # -------------------------------
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup",
            "output_response": {
                "target_dir": target_dir,
                "max_iterations": max_iter,
                "file_ext": file_ext,
                "dry_run": dry_run
            }
        },
        status="INFO"
    )

    # -------------------------------
    # 4️⃣ Découverte fichiers
    # -------------------------------
    files = discover_files(target_dir, file_ext)

    if not files:
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "File discovery",
                "output_response": {
                    "target_dir": target_dir,
                    "file_ext": file_ext,
                    "result": "No matching files found"
                }
            },
            status="FAIL"
        )
        print("❌ Aucun fichier trouvé")
        return

    # -------------------------------
    # 5️⃣ Orchestration principale
    # -------------------------------
    for file_path in files:
        print(f"\n📄 Traitement : {os.path.basename(file_path)}")
        current_target = file_path

        for iteration in range(1, max_iter + 1):
            print(f"🔄 Itération {iteration}")

            # ---- Auditor ----
            analysis = run_auditor(current_target)

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Auditor decision received",
                    "output_response": {
                        "file": current_target,
                        "iteration": iteration,
                        "decision": analysis.get("decision")
                    }
                },
                status="SUCCESS"
            )

            if analysis.get("decision") == "ACCEPTED":
                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": "Stop condition",
                        "output_response": {
                            "file": current_target,
                            "iteration": iteration,
                            "reason": "ACCEPTED"
                        }
                    },
                    status="INFO"
                )
                break

            # ---- Fixer ----
            if dry_run:
                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": "Dry run – fix skipped",
                        "output_response": {
                            "file": current_target,
                            "iteration": iteration
                        }
                    },
                    status="INFO"
                )
                continue

            current_target = run_fixer(
                current_target,
                analysis,
                iteration
            )

        else:
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Stop condition",
                    "output_response": {
                        "file": file_path,
                        "reason": "MAX_ITERATIONS_REACHED",
                        "max_iterations": max_iter
                    }
                },
                status="FAIL"
            )

    # -------------------------------
    # 6️⃣ Shutdown
    # -------------------------------
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System shutdown",
            "output_response": "All files processed, clean termination"
        },
        status="INFO"
    )

    print("\n✅ FIN DU PROCESSUS – arrêt propre")


if __name__ == "__main__":
    main()
