from pathlib import Path
from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType


def run_auditor(file_path: str) -> dict:
    """
    Agent Auditor – version minimale conforme TP (Jour 3)
    """

    path = Path(file_path)

    if path.is_dir():
        py_files = list(path.glob("*.py"))
        if not py_files:
            raise FileNotFoundError("No .py file found in target directory.")
        target_file = py_files[0]
    else:
        target_file = path

    code = read_file(str(target_file))

    analysis_result = {
        "issues": [
            "Fictitious bug detected",
            "Fictitious style issue"
        ]
    }

    log_experiment(
        agent_name="Auditor",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "file_path": str(target_file),
            "input_prompt": f"Analyze the file: {target_file}",
            "output_response": "Basic analysis completed (fictitious)"
        },
        status="SUCCESS"
    )

    return analysis_result
