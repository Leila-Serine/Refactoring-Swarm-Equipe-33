import json
import os
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict

# Chemin du fichier de logs
LOG_FILE = os.path.join("logs", "experiment_data.json")


class ActionType(str, Enum):
    ANALYSIS = "CODE_ANALYSIS"
    GENERATION = "CODE_GEN"
    DEBUG = "DEBUG"
    FIX = "FIX"


def log_experiment(agent_name: str,
                   model_used: str,
                   action,
                   details=None,
                   status: str = "INFO"):
    """
    Logger conforme aux documents du TP IGL
    - action ∈ ActionType UNIQUEMENT
    - logs System forcés en DEBUG
    - compatible avec main.py (legacy)
    """

    # 🟢 CAS 1 — Appel SYSTEM depuis main.py (legacy)
    # log_experiment("System", "STARTUP", "Target: sandbox/test", "INFO")
    if agent_name == "System" and isinstance(action, str) and isinstance(details, str):
        status = details  # "INFO"
        details = {
    "input_prompt": "Analyse du fichier sandbox/test/sample.py",
    "output_response": {
        "issues": [
            "Analyse fictive : bugs potentiels",
            "Analyse fictive : style à améliorer"
        ]
    },
    "target_file": "sandbox/test/sample.py",
    "agent_role": "Auditor",
    "iteration": 1,
    "comment": "Analyse simulée – Jour 3 (sans IA réelle)"
}

        action_enum = ActionType.DEBUG

    # 🟢 CAS 2 — Appel normal conforme
    elif isinstance(action, ActionType):
        action_enum = action

    # 🔴 AUTRES CAS → INTERDIT
    else:
        raise ValueError(
            f"Action invalide '{action}'. "
            "Utilisez ActionType ou un appel System autorisé."
        )

    # 🔒 Validation obligatoire de details
    if not isinstance(details, dict):
        raise ValueError("details doit être un dictionnaire")

    for key in ("input_prompt", "output_response"):
        if key not in details:
            raise ValueError(f"Champ obligatoire manquant dans details: {key}")

    # 📌 Construction du log
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "model": model_used,
        "action": action_enum.value,
        "details": details,
        "status": status
    }

    # 📖 Lecture existante
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            data = []

    data.append(entry)

    # 💾 Écriture finale
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
