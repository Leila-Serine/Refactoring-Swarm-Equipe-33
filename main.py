import argparse
import sys
import os
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

# Charger les variables d'environnement (.env)
load_dotenv()


def main():
    # -------------------------------
    # 1️⃣ Arguments CLI (Jour 4)
    # -------------------------------
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator")
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Dossier ou fichier cible à analyser (sandbox uniquement)"
    )
    parser.add_argument(
        "--max_iterations",
        type=int,
        default=1,
        help="Nombre maximum d’itérations Auditor/Fixer"
    )
    args = parser.parse_args()

    # -------------------------------
    # 2️⃣ Vérifications de base
    # -------------------------------
    if not os.path.exists(args.target_dir):
        print(f"❌ Cible introuvable : {args.target_dir}")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    print(f"🔁 Max iterations : {args.max_iterations}")

    # -------------------------------
    # 3️⃣ Log SYSTEM (démarrage)
    # -------------------------------
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

    # -------------------------------
    # 4️⃣ Orchestration contrôlée
    # -------------------------------
    current_target = args.target_dir

    for iteration in range(1, args.max_iterations + 1):
        print(f"\n🔄 Itération {iteration}")

        # ---- Auditor ----
        analysis_result = run_auditor(current_target)

        # Log itération (ANALYSIS)
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Iteration {iteration} – Auditor analysis",
                "output_response": analysis_result
            },
            status="SUCCESS"
        )

        # Vérifier la décision de l'Auditor avant d'appeler le Fixer
        if analysis_result.get("decision") == "ACCEPTED":
            print(f"✅ Auditor a accepté le code dans l'itération {iteration}. Arrêt du processus.")
            break  # Arrêter si l'Auditor a accepté le code

        # ⚠️ Si la décision est "REQUIRES_FIX", on applique le Fixer
        print(f"⚠️ Auditor a refusé. Lancer le Fixer pour l'itération {iteration}")

        # ---- Fixer ----
        fixed_file = run_fixer(current_target, analysis_result, iteration)

        # Log itération (FIX)
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

        # Le fichier corrigé devient la nouvelle cible
        current_target = fixed_file

    # -------------------------------
    # 5️⃣ Arrêt propre
    # -------------------------------
    print("\n✅ FIN DU PROCESSUS")
    print("🛑 Arrêt après itérations contrôlées")

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
