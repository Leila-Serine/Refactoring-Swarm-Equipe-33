# main.py

import argparse
import sys
import os
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

load_dotenv()


def main():
    # -------------------------------
    # 1️⃣ Arguments CLI
    # -------------------------------
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator")
    parser.add_argument("--target_dir", type=str, required=True)
    parser.add_argument("--max_iterations", type=int, default=1)
    args = parser.parse_args()

    # -------------------------------
    # 2️⃣ Vérifications
    # -------------------------------
    if not os.path.exists(args.target_dir):
        print(f"❌ Cible introuvable : {args.target_dir}")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    print(f"🔁 Max iterations : {args.max_iterations}")

    # -------------------------------
    # 3️⃣ Log démarrage SYSTEM
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

        try:
            analysis_result = run_auditor(current_target)
        except Exception as e:
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": f"Iteration {iteration} – Auditor failed",
                    "output_response": str(e)
                },
                status="FAIL"
            )
            break

        # Si le code est accepté → arrêt
        if analysis_result.get("decision") == "ACCEPTED":
            print("✅ Auditor a validé le code. Arrêt du processus.")
            break

        print(f"⚠️ Auditor a refusé. Lancer le Fixer pour l'itération {iteration}")

        fixed_file = run_fixer(current_target, analysis_result, iteration)
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
