from pathlib import Path
from src.utils.file_tools import read_file, write_file
from src.utils.logger import log_experiment, ActionType
from src.utils.llm_client import fix_code_with_llm


def run_fixer(file_path: str, auditor_output: dict, iteration: int) -> str:
    """
    Fixer – Version finale corrigée
    - Respecte strictement le dossier target_dir (sandbox uniquement)
    - Génère un fichier corrigé dans le même dossier que le fichier original
    - Logs conformes
    """

    p = Path(file_path)

    # ---------------- Validation ----------------
    if not p.exists() or not p.is_file():
        log_experiment(
            agent_name="Fixer",
            model_used="gemini-2.5-flash",
            action=ActionType.FIX,
            details={
                "input_prompt": {
                    "iteration": iteration,
                    "file_path": file_path,
                    "auditor_output": auditor_output
                },
                "output_response": {
                    "error": "Invalid file path, cannot fix"
                }
            },
            status="FAIL"
        )
        return file_path

    try:
        original_code = read_file(str(p))
    except Exception as e:
        log_experiment(
            agent_name="Fixer",
            model_used="gemini-2.5-flash",
            action=ActionType.FIX,
            details={
                "input_prompt": str(p),
                "output_response": {"error": str(e)}
            },
            status="FAIL"
        )
        return file_path

    # ---------------- VRAIE Correction avec Gemini ----------------
    issues = auditor_output.get("issues", [])
    if issues:
        fixed_body = fix_code_with_llm(original_code, str(p), issues)
    else:
        fixed_body = original_code

    fixed_code = (
        f"# FIXED – iteration {iteration}\n"
        f"# Corrected by Gemini API\n\n"
        f"{fixed_body}\n"
    )

    # ---------------- Respect strict du target_dir ----------------
    # On écrit dans le même dossier que le fichier original
    out_dir = p.parent

    out_name = f"{p.stem}_fixed_iter_{iteration}{p.suffix}"
    fixed_path = out_dir / out_name

    try:
        write_file(str(fixed_path), fixed_code)
    except Exception as e:
        log_experiment(
            agent_name="Fixer",
            model_used="gemini-2.5-flash",
            action=ActionType.FIX,
            details={
                "input_prompt": str(fixed_path),
                "output_response": {"error": str(e)}
            },
            status="FAIL"
        )
        return file_path

    # ---------------- Log SUCCESS ----------------
    log_experiment(
        agent_name="Fixer",
        model_used="gemini-2.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": {
                "iteration": iteration,
                "file_path": str(p),
                "auditor_output": auditor_output
            },
            "output_response": {
                "fixed_file": str(fixed_path),
                "note": "Correction appliquée via Gemini"
            }
        },
        status="SUCCESS"
    )

    return str(fixed_path)
