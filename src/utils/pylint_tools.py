# src/utils/pylint_tools.py

import subprocess
import sys
import re
from pathlib import Path


def run_pylint(target_path: str) -> dict:
    """
    Lance pylint sur un fichier Python dans sandbox/
    et retourne un résumé exploitable.
    """

    # 1️⃣ Validation basique
    if not isinstance(target_path, str):
        raise ValueError("target_path must be a string")

    path = Path(target_path)

    # 2️⃣ Sécurité sandbox
    if path.is_absolute():
        raise PermissionError("Chemins absolus interdits.")

    if ".." in path.parts:
        raise PermissionError("Remontée de dossier interdite ('..').")

    full_path = path.resolve()

    if not full_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {target_path}")

    if not str(full_path).startswith(str(Path("sandbox").resolve())):
        raise PermissionError("Pylint autorisé uniquement dans sandbox.")

    # 3️⃣ Commande pylint (via python -m pylint)
    cmd = [sys.executable, "-m", "pylint", str(full_path)]

    process = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    output = (process.stdout or "") + (process.stderr or "")

    # 4️⃣ Extraction du score pylint (si présent)
    score = None
    match = re.search(r"rated at ([\-0-9\.]+)/10", output)
    if match:
        score = float(match.group(1))

    # 5️⃣ Résultat structuré
    return {
        "target": str(full_path),
        "score": score,
        "returncode": process.returncode,
        "raw_output": output
    }
