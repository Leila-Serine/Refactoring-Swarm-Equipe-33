# src/agents/auditor_agent.py

from src.utils.file_tools import read_file


def run_auditor(file_path: str) -> dict:
    """
    Agent Auditor - version minimale (Étape 1)

    Rôle :
    - lire un fichier de code
    - produire une analyse simple (fictive)
    - NE PAS corriger
    """

    code = read_file(file_path)

    # Analyse fictive minimale (acceptée à cette étape)
    analysis = {
        "file": file_path,
        "issues_found": [
            "Analyse fictive : bugs potentiels non vérifiés",
            "Analyse fictive : style à améliorer",
        ],
        "summary": "Analyse minimale réalisée (pas d'IA réelle à cette étape)"
    }

    return analysis
