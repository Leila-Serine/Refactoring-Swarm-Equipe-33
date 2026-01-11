import argparse
import os
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator")
    parser.add_argument("--target_dir", type=str, required=True)
    parser.add_argument("--max_iterations", type=int, default=2)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Cible introuvable : {args.target_dir}")
        return

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")
    print(f"🔁 Max iterations : {args.max_iterations}")

    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup",
            "output_response": f"Target: {args.target_dir}"
        },
        status="INFO"
    )

    # 🔹 Construction explicite de la liste de fichiers
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
            print("❌ Aucun fichier .py trouvé.")
            return
    else:
        print("❌ Chemin invalide.")
        return

    # 🔹 Orchestration fichier par fichier
    for file_path in files_to_process:
        print(f"\n📄 Traitement du fichier : {os.path.basename(file_path)}")
        current_target = file_path

        for iteration in range(1, args.max_iterations + 1):
            print(f"🔄 Itération {iteration}")

            analysis = run_auditor(current_target)

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": f"Iteration {iteration} – Auditor result",
                    "output_response": analysis
                },
                status="SUCCESS"
            )

            if analysis.get("decision") == "ACCEPTED":
                print("✅ Auditor a validé le code.")
                break

            print("⚠️ Correction requise → Fixer")
            current_target = run_fixer(current_target, analysis, iteration)

        else:
            print("🛑 Arrêt : max_iterations atteint")

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


if __name__ == "__main__":
    main()
