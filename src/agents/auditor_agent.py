from pathlib import Path
from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType


def run_auditor(file_path: str) -> dict:
    """
    Auditor (Jour 7/8)
    - Attend un CHEMIN DE FICHIER
    - Décision : ACCEPTED / REQUIRES_FIX
    - Logs conformes
    """
    p = Path(file_path)

    if not p.exists() or not p.is_file():
        result = {
            "issues": [f"Invalid file path: {file_path}"],
            "decision": "REQUIRES_FIX"
        }
        log_experiment(
            agent_name="Auditor",
            model_used="N/A",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Analyze file (invalid path): {file_path}",
                "output_response": result
            },
            status="FAIL"
        )
        return result

    code = read_file(str(p))
    stripped = code.strip()

    # Règles fictives mais cohérentes pour les tests
    if stripped == "":
        issues = ["Empty file"]
        decision = "REQUIRES_FIX"
    elif "# FIXED" in code:
        issues = []
        decision = "ACCEPTED"
    elif "ERROR" in code:
        issues = ["Contains token ERROR"]
        decision = "REQUIRES_FIX"
    else:
        issues = []
        decision = "ACCEPTED"

    result = {"issues": issues, "decision": decision}

    log_experiment(
        agent_name="Auditor",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": f"Analyze the file: {str(p)}",
            "output_response": {
                "file_path": str(p),
                "result": result
            }
        },
        status="SUCCESS"
    )

    return result
