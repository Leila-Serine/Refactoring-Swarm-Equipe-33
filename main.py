import argparse
import sys
import os
from dotenv import load_dotenv
from src.utils.logger import log_experiment, ActionType

# Charger les variables d'environnement
load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Dossier {args.target_dir} introuvable.")
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {args.target_dir}")

    # Log conforme au protocole strict du TP
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "target_dir": args.target_dir,
            "input_prompt": "System startup – no LLM interaction",
            "output_response": "System initialized successfully"
        },
        status="SUCCESS"
    )

    print("✅ MISSION_COMPLETE")

if __name__ == "__main__":
    main()
