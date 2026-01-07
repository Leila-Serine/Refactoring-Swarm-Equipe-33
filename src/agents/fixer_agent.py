from pathlib import Path
from src.utils.file_tools import read_file, write_file
from src.utils.logger import log_experiment, ActionType


def run_fixer(file_path: str, auditor_output: dict, iteration: int) -> str:
    """
    Fixer – Jour 4
    Correction fictive détectable par l'Auditor
    """

    path = Path(file_path)

    # 🟢 Cas où on reçoit un dossier
    if path.is_dir():
        py_files = list(path.glob("*.py"))
        if not py_files:
            raise FileNotFoundError(
                "Aucun fichier .py trouvé pour correction."
            )
        target_file = py_files[0]
    else:
        target_file = path

    # 1️⃣ Lire le code original
    original_code = read_file(str(target_file))

    # 2️⃣ Correction fictive DÉTECTABLE
    # - suppression de ERROR
    # - ajout d’un marqueur FIXED
    fixed_code = original_code.replace("ERROR", "").strip()
    fixed_code = (
    f"# FIXED – itération {iteration}\n"
    "# Correction simulée par Fixer\n"
    + original_code.replace("ERROR", "").strip()
)


    # 3️⃣ Écriture dans sandbox
    fixed_path = "sandbox/fixed_code.py"
    write_file(fixed_path, fixed_code)

    # 4️⃣ Logging conforme TP
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
