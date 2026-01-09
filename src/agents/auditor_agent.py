# src/agents/auditor_agent.py

from pathlib import Path
from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType


def run_auditor(file_path: str) -> dict:
    """
    Auditor – Jour 4 & 5
    - Accepte un fichier OU un dossier
    - Décision explicite ACCEPTED / REQUIRES_FIX
    """

    path = Path(file_path)

    # 🟢 Si un dossier est fourni
    if path.is_dir():
        py_files = list(path.glob("*.py"))
        if not py_files:
            raise FileNotFoundError(
                f"Aucun fichier .py trouvé dans le dossier {file_path}"
            )
        target_file = py_files[0]
    else:
        target_file = path

    code = read_file(str(target_file))

    # 🔍 Analyse fictive contrôlée
    if "# FIXED" in code:
        issues = []
        decision = "ACCEPTED"
    else:
        issues = [
            "Analyse fictive : bugs potentiels",
            "Analyse fictive : style à améliorer"
        ]
        decision = "REQUIRES_FIX"

    result = {
        "issues": issues,
        "decision": decision
    }

    # 📝 Log conforme TP
    log_experiment(
        agent_name="Auditor",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "file_path": str(target_file),
            "input_prompt": f"Analyze the file: {target_file}",
            "output_response": result
        },
        status="SUCCESS"
    )

    return result
