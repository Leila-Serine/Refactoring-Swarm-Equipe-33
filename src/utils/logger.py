import json
import os
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict

# Chemin du fichier de logs
LOG_FILE = os.path.join("logs", "experiment_data.json")


class ActionType(str, Enum):
    """
    Énumération des types d'actions possibles pour standardiser l'analyse.
    """
    ANALYSIS = "CODE_ANALYSIS"
    GENERATION = "CODE_GEN"
    DEBUG = "DEBUG"
    FIX = "FIX"
    SYSTEM = "SYSTEM"


def log_experiment(
    agent_name: str = "System",
    model_used: str = "N/A",
    action: ActionType | str = ActionType.SYSTEM,
    details: Dict[str, Any] | str | None = None,
    status: str = "INFO"
):
    """
    Enregistre une interaction d'agent pour l'analyse scientifique.

    Cette version est volontairement TOLÉRANTE pour rester compatible
    avec main.py, auditor_agent.py et les futures évolutions.

    - agent_name, model_used, status ont des valeurs par défaut
    - details peut être une string ou un dict
    """

    # ── 1. Normalisation de l'action ─────────────────────────────
    if isinstance(action, ActionType):
        action_str = action.value
    else:
        action_str = str(action)

    # ── 2. Normalisation des détails ─────────────────────────────
    if details is None:
        details = {}

    if isinstance(details, str):
        # Cas du main.py : "Target: sandbox/test"
        details = {
            "input_prompt": details,
            "output_response": ""
        }

    if not isinstance(details, dict):
        raise ValueError("details must be a dict or a string")

    # ── 3. Validation minimale requise par le TP ──────────────────
    required_keys = ["input_prompt", "output_response"]
    for key in required_keys:
        if key not in details:
            details[key] = ""

    # ── 4. Création du dossier logs si nécessaire ─────────────────
    os.makedirs("logs", exist_ok=True)

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "model": model_used,
        "action": action_str,
        "details": details,
        "status": status
    }

    # ── 5. Lecture existante ─────────────────────────────────────
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            print(f"⚠️ Fichier de logs corrompu, recréation : {LOG_FILE}")
            data = []

    # ── 6. Écriture ──────────────────────────────────────────────
    data.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
