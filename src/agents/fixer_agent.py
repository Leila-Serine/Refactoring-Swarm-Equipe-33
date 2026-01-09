# src/agents/fixer_agent.py

from pathlib import Path
from src.utils.file_tools import read_file, write_file
from src.utils.logger import log_experiment, ActionType


def run_fixer(file_path: str, auditor_output: dict, iteration: int) -> str:
    """
    Fixer – Jour 4 & 5
    - Correction fictive DÉTECTABLE
    - Compatible fichier OU dossier
    """

    path = Path(file_path)

    # 🟢 Si un dossier est fourni
    if path.is_dir():
        py_files = list(path.glob("*.py"))
        if not py_files:
            raise FileNotFoundError(
                "Aucun fichier .py trouvé pour correction."
            )
        target_file = py_files[0]
    else:
        target_file = path

    # 1️⃣ Lecture du code original
    original_code = read_file(str(target_file))

    # 2️⃣ Correction fictive VISIBLE et DÉTECTABLE
    fixed_code = (
        f"# FIXED – iteration {iteration}\n"
        "# Correction simulée par Fixer\n\n"
        + original_code.replace("ERROR", "# ERROR FIXED")
    )

    # 3️⃣ Écriture du fichier corrigé
    fixed_path = "sandbox/fixed_code.py"
    write_file(fixed_path, fixed_code)

    # 4️⃣ Log conforme TP
    log_experiment(
        agent_name="Fixer",
        model_used="N/A",
        action=ActionType.FIX,
        details={
            "input_prompt": {
                "iteration": iteration,
                "file_path": str(target_file),
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
