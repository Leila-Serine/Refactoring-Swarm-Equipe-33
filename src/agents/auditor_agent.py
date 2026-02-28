from pathlib import Path
from src.utils.file_tools import read_file
from src.utils.logger import log_experiment, ActionType
from src.utils.llm_client import analyze_code_with_llm

def run_auditor(file_path: str) -> dict:
    """
    Auditor avec Gemini API
    """
    p = Path(file_path)

    if not p.exists() or not p.is_file():
        result = {
            "issues": [f"Invalid file path: {file_path}"],
            "decision": "REQUIRES_FIX"
        }
        log_experiment(
            agent_name="Auditor",
            model_used="gemini-2.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Analyze file (invalid path): {file_path}",
                "output_response": result
            },
            status="FAIL"
        )
        return result

    code = read_file(str(p))
    
    # UTILISER GEMINI API
    result = analyze_code_with_llm(code, str(p))
    
    # FORCER REQUIRES_FIX si des issues sont trouvées
    if result.get("issues") and len(result["issues"]) > 0:
        if result["decision"] == "ACCEPTED":
            result["decision"] = "REQUIRES_FIX"

    log_experiment(
        agent_name="Auditor",
        model_used="gemini-2.5-flash",
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
