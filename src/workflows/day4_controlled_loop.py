from pathlib import Path

from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer


def run_controlled_loop(target_dir: str, max_iterations: int = 2) -> dict:
    """
    JOUR 4 — Boucle contrôlée Auditor ↔ Fixer
    - arrêt si Auditor OK
    - arrêt si max_iterations atteint
    """

    target_path = Path(target_dir)

    if not target_path.exists():
        raise FileNotFoundError(f"Dossier introuvable : {target_dir}")

    # 1️⃣ Trouver un fichier .py
    py_files = list(target_path.glob("*.py"))
    if not py_files:
        raise FileNotFoundError("Aucun fichier .py trouvé dans le dossier cible.")

    current_file = str(py_files[0])
    iteration = 1

    while iteration <= max_iterations:

        # 2️⃣ AUDITOR
        audit_result = run_auditor(current_file)

        issues = audit_result.get("issues", [])

        # 3️⃣ Condition d’arrêt : OK
        if not issues:
            return {
                "status": "SUCCESS",
                "iterations": iteration,
                "final_file": current_file
            }

        # 4️⃣ FIXER
        current_file = run_fixer(
            file_path=current_file,
            auditor_output=audit_result,
            iteration=iteration
        )

        iteration += 1

    # 5️⃣ Arrêt forcé (max itérations)
    return {
        "status": "FAIL",
        "iterations": max_iterations,
        "final_file": current_file
    }
