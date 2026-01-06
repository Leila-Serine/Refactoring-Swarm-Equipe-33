# src/agents/fixer_agent.py

from src.utils.file_tools import read_file, write_file
from src.utils.logger import log_experiment, ActionType


def run_fixer(file_path: str, auditor_output: dict) -> str:
    """
    Fixer minimal – Jour 3
    - lit le fichier original
    - simule une correction simple
    - écrit le fichier corrigé dans sandbox/
    - log l'action FIX
    """

    # 1. Lire le code original
    original_code = read_file(file_path)

    # 2. Correction fictive (PAS D'IA)
    fixed_code = "# Correction fictive par Fixer (Jour 3)\n" + original_code

    # 3. Écriture dans sandbox
    fixed_path = "sandbox/fixed_code.py"
    write_file(fixed_path, fixed_code)

    # 4. Logging obligatoire
    log_experiment(
        agent_name="Fixer",
        model_used="N/A",
        action=ActionType.FIX,
        details={
            "input_prompt": {
                "file_path": file_path,
                "auditor_output": auditor_output
            },
            "output_response": {
                "fixed_file": fixed_path,
                "note": "Correction fictive appliquée"
            }
        },
        status="SUCCESS"
    )

    return fixed_path
