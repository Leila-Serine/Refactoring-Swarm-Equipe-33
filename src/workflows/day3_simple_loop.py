# src/workflows/day3_simple_loop.py

from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer


def run_day3_once(file_path: str) -> str:
    """
    Boucle simple Jour 3 :
    Auditor -> Fixer (1 seule fois)
    """

    auditor_output = run_auditor(file_path)
    fixed_file = run_fixer(file_path, auditor_output)

    return fixed_file
