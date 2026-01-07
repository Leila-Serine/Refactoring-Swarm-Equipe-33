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
    
    log_experiment(
    agent_name="Fixer",
    model_used="N/A",
    action=ActionType.FIX,
    details={
        "file_path": file_path,
        "input_prompt": "Fix the code based on auditor analysis",
        "output_response": f"Correction fictive appliquée → {fixed_path}"
    },
    status="SUCCESS"
)


    return fixed_path
