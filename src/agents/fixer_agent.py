from pathlib import Path
from src.utils.file_tools import read_file, write_file
from src.utils.logger import log_experiment, ActionType


def run_fixer(file_path: str, auditor_output: dict, iteration: int) -> str:
    """
    Fixer (Jour 7/8)
    - Attend un CHEMIN DE FICHIER
    - Écrit une correction fictive DÉTECTABLE
    - Génère un fichier de sortie unique par fichier/itération
    - Logs conformes
    """
    p = Path(file_path)

    if not p.exists() or not p.is_file():
        # On log en FAIL mais on ne crash pas
        log_experiment(
            agent_name="Fixer",
            model_used="N/A",
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
        # On retourne le même chemin pour laisser main.py gérer l’arrêt
        return file_path

    original_code = read_file(str(p))

    # Correction fictive : retirer ERROR + ajouter marqueur FIXED
    fixed_body = original_code.replace("ERROR", "").strip()
    fixed_code = (
        f"# FIXED – iteration {iteration}\n"
        "# Correction simulée par Fixer\n\n"
        f"{fixed_body}\n"
    )

    out_dir = Path("sandbox") / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    out_name = f"{p.stem}_fixed_iter_{iteration}{p.suffix}"
    fixed_path = out_dir / out_name

    write_file(str(fixed_path), fixed_code)

    log_experiment(
        agent_name="Fixer",
        model_used="N/A",
        action=ActionType.FIX,
        details={
            "input_prompt": {
                "iteration": iteration,
                "file_path": str(p),
                "auditor_output": auditor_output
            },
            "output_response": {
                "fixed_file": str(fixed_path),
                "note": "Correction fictive appliquée"
            }
        },
        status="SUCCESS"
    )

    return str(fixed_path)
