import argparse
import os
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

# Charger les variables d'environnement
load_dotenv()


def main():
    # -------------------------------
    # 1️⃣ Arguments CLI
    # -------------------------------
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator")
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Fichier ou dossier cible (sandbox uniquement)"
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=2,
        help="Nombre maximum d’itérations Auditor/Fixer"
    )
    args = parser.parse_args()

    # -------------------------------
    # 2️⃣ Vérification du chemin
    # -------------------------------
    if not os.path.exists(args.target_dir):
        print(f"❌ Cible introuvable : {args.target_dir}")
        return

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    print(f"🔁 Max iterations : {args.max_iterations}")

    # -------------------------------
    # 3️⃣ Log SYSTEM – démarrage
    # -------------------------------
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup – no LLM interaction",
            "output_response": f"Target directory: {args.target_dir}"
        },
        status="INFO"
    )

    # -------------------------------
    # 4️⃣ Découverte des fichiers à traiter
    # -------------------------------
    if os.path.isfile(args.target_dir):
        files_to_process = [args.target_dir]

    elif os.path.isdir(args.target_dir):
        files_to_process = [
            os.path.join(args.target_dir, f)
            for f in os.listdir(args.target_dir)
            if f.endswith(".py")
        ]

        if not files_to_process:
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "File discovery",
                    "output_response": "No Python files found"
                },
                status="FAIL"
            )
            print("❌ Aucun fichier .py trouvé dans le dossier.")
            return
    else:
        print("❌ Chemin invalide.")
        return

    # -------------------------------
    # 5️⃣ Orchestration contrôlée
    # -------------------------------
    for file_path in files_to_process:
        print(f"\n📄 Traitement du fichier : {os.path.basename(file_path)}")

        current_target = file_path

        for iteration in range(1, args.max_iterations + 1):
            print(f"🔄 Itération {iteration}")

            # ---- Auditor ----
            analysis_result = run_auditor(current_target)

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": f"Iteration {iteration} – Auditor result",
                    "output_response": analysis_result
                },
                status="SUCCESS"
            )

            # ---- Décision d'arrêt ----
            if analysis_result.get("decision") == "ACCEPTED":
                print("✅ Auditor a validé le code. Arrêt du processus.")
                break

            # ---- Fixer ----
            print(f"⚠️ Auditor a refusé. Lancer le Fixer pour l'itération {iteration}")
            current_target = run_fixer(
                current_target,
                analysis_result,
                iteration
            )

        else:
            print("🛑 Arrêt : nombre maximum d’itérations atteint")

    # -------------------------------
    # 6️⃣ Arrêt propre
    # -------------------------------
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
    print("🛑 Arrêt après itérations contrôlées")


if __name__ == "__main__":
    main()
