import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

# Charger les variables d'environnement
load_dotenv()


def main():
    # -------------------------------------------------
    # 1️⃣ Arguments CLI
    # -------------------------------------------------
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator")
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Dossier ou fichier cible"
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=1,
        help="Nombre maximum d’itérations Auditor/Fixer"
    )
    args = parser.parse_args()

    target_path = Path(args.target_dir)

    if not target_path.exists():
        print(f"❌ Cible introuvable : {args.target_dir}")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    print(f"🔁 Max iterations : {args.max_iterations}")

    # -------------------------------------------------
    # 2️⃣ Log SYSTEM – démarrage
    # -------------------------------------------------
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup – no LLM interaction",
            "output_response": f"Target: {args.target_dir}"
        },
        status="INFO"
    )

    # -------------------------------------------------
    # 3️⃣ Détermination des fichiers à traiter
    # -------------------------------------------------
    if target_path.is_dir():
        py_files = list(target_path.glob("*.py"))
        if not py_files:
            print("⚠️ Aucun fichier .py trouvé dans le dossier.")
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Directory scan",
                    "output_response": "No Python files found. Process stopped."
                },
                status="INFO"
            )
            return
    else:
        py_files = [target_path]

    # -------------------------------------------------
    # 4️⃣ Orchestration contrôlée (Jour 6)
    # -------------------------------------------------
    for file_path in py_files:
        print(f"\n📄 Traitement du fichier : {file_path.name}")
        current_file = str(file_path)

        for iteration in range(1, args.max_iterations + 1):
            print(f"🔄 Itération {iteration}")

            # ---------- AUDITOR ----------
            audit_result = run_auditor(current_file)

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.ANALYSIS,
                details={
                    "input_prompt": f"Iteration {iteration} – Auditor analysis",
                    "output_response": audit_result
                },
                status="SUCCESS"
            )

            # ---------- DÉCISION ----------
            if audit_result.get("decision") == "ACCEPTED":
                print("✅ Auditor a validé le code. Arrêt du processus.")

                log_experiment(
                    agent_name="System",
                    model_used="N/A",
                    action=ActionType.DEBUG,
                    details={
                        "input_prompt": f"Iteration {iteration} – Decision",
                        "output_response": "Auditor accepted the code. Process stopped."
                    },
                    status="SUCCESS"
                )
                break  # ⛔ arrêt explicite

            # ---------- FIXER ----------
            print(f"⚠️ Auditor a refusé. Lancer le Fixer pour l'itération {iteration}")

            fixed_file = run_fixer(current_file, audit_result, iteration)

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.FIX,
                details={
                    "input_prompt": f"Iteration {iteration} – Fixer correction",
                    "output_response": {
                        "fixed_file": fixed_file
                    }
                },
                status="SUCCESS"
            )

            current_file = fixed_file

        else:
            # Boucle terminée par max_iterations
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Max iterations reached",
                    "output_response": "Process stopped without acceptance."
                },
                status="FAIL"
            )

    # -------------------------------------------------
    # 5️⃣ Arrêt propre
    # -------------------------------------------------
    print("\n✅ FIN DU PROCESSUS")
    print("🛑 Arrêt contrôlé du système")

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


if __name__ == "__main__":
    main()
