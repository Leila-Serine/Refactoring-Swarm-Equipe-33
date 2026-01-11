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
    Retourne la liste des fichiers à traiter.
    - Si target_path est un fichier => retourne [target_path]
    - Si target_path est un dossier => retourne tous les fichiers *file_ext* du dossier (non récursif)
    """
    p = Path(target_path)

    if p.is_file():
        return [str(p)]

    if p.is_dir():
        return [str(x) for x in p.iterdir() if x.is_file() and x.suffix == file_ext]

    return []


def main():
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator (Jour 7/8)")

    # Conformément au doc Jour 6 : arguments explicités
    parser.add_argument("--target_dir", type=str, required=True, help="Fichier ou dossier cible (sandbox)")
    parser.add_argument("--max_iterations", type=int, required=True, help="Max cycles Auditor→Fixer par fichier")
    parser.add_argument("--file_ext", type=str, required=True, help="Extension à traiter, ex: .py")
    parser.add_argument("--dry_run", type=str, required=True, help="true/false (simulation uniquement)")

    args = parser.parse_args()

    target = args.target_dir
    max_iter = args.max_iterations
    file_ext = args.file_ext.strip()

    dry_run_raw = args.dry_run.strip().lower()
    if dry_run_raw not in ("true", "false"):
        print("❌ --dry_run doit être 'true' ou 'false'")
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "CLI validation",
                "output_response": "Invalid --dry_run value (expected true/false)"
            },
            status="FAIL"
        )
        return
    dry_run = (dry_run_raw == "true")

    if not os.path.exists(target):
        print(f"❌ Cible introuvable : {target}")
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Path validation",
                "output_response": f"Target not found: {target}"
            },
            status="FAIL"
        )
        return

    if max_iter <= 0:
        print("❌ --max_iterations doit être > 0")
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "CLI validation",
                "output_response": "Invalid max_iterations (<= 0)"
            },
            status="FAIL"
        )
        return

    if not file_ext.startswith("."):
        print("❌ --file_ext doit commencer par un point (ex: .py)")
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
        return

    print(f"🚀 DEMARRAGE SUR : {target}")
    print(f"🔁 Max iterations : {max_iter}")
    print(f"🧾 file_ext : {file_ext}")
    print(f"🧪 dry_run : {dry_run}")

    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup – no LLM interaction",
            "output_response": {
                "target_dir": target,
                "max_iterations": max_iter,
                "file_ext": file_ext,
                "dry_run": dry_run
            }
        },
        status="INFO"
    )

    files_to_process = discover_files(target, file_ext)

    if not files_to_process:
        msg = f"No files found matching {file_ext}"
        print(f"❌ {msg}")
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "File discovery",
                "output_response": {
                    "target_dir": target,
                    "file_ext": file_ext,
                    "result": msg
                }
            },
            status="FAIL"
        )
        return

    # Boucle multi-fichiers (corrige la remarque du chef)
    for file_path in files_to_process:
        filename = os.path.basename(file_path)
        print(f"\n📄 Traitement du fichier : {filename}")

        current_target = file_path

        for iteration in range(1, max_iter + 1):
            print(f"🔄 Itération {iteration}")

            # 1) Auditor (toujours sur un FICHIER)
            analysis_result = run_auditor(current_target)

            if analysis_result.get("decision") == "ACCEPTED":
                print("✅ Auditor a validé. Passage au fichier suivant.")
                break

            # 2) Fixer si refus
            print(f"⚠️ Auditor a refusé. Lancer Fixer (itération {iteration})")

            if dry_run:
                # Simulation : on n’écrit pas de fichier corrigé
                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": "Dry run – skip fix",
                        "output_response": {
                            "file": current_target,
                            "iteration": iteration,
                            "decision": "SKIPPED_FIX_DRY_RUN"
                        }
                    },
                    status="INFO"
                )
                # En dry_run, on ne peut pas “améliorer” le code, donc on continue jusqu'à max_iter
                continue

            current_target = run_fixer(current_target, analysis_result, iteration)

        else:
            # boucle terminée sans break => max itérations atteintes
            print("🛑 Arrêt : max_iterations atteint pour ce fichier.")
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

    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System shutdown",
            "output_response": "Process finished cleanly"
        },
        status="INFO"
    )

    print("\n✅ FIN DU PROCESSUS")
    print("🛑 Arrêt propre")


if __name__ == "__main__":
    main()
