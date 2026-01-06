# src/agents/auditor_agent.py

from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType


def run_auditor(file_path: str) -> dict:
    code = read_file(file_path)

    input_prompt = f"Analyse du fichier {file_path}"
    output_response = {
        "issues": [
            "Analyse fictive : bugs potentiels",
            "Analyse fictive : style à améliorer"
        ]
    }

    log_experiment(
        action=ActionType.ANALYSIS,
        input_prompt=input_prompt,
        output_response=output_response,
        status="success"
    )

    return output_response
