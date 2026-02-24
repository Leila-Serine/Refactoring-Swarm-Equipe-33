import subprocess
from src.utils.logger import log_experiment, ActionType


def run_judge(target_dir: str, iteration: int) -> dict:
    """
    Judge robuste compatible Windows
    """

    try:
        result = subprocess.run(
            ["python", "-m", "pytest", target_dir],
            capture_output=True,
            text=True
        )

        success = result.returncode == 0

        log_experiment(
            agent_name="Judge",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": {
                    "iteration": iteration,
                    "target_dir": target_dir
                },
                "output_response": {
                    "returncode": result.returncode,
                    "stdout": result.stdout[-500:],
                    "stderr": result.stderr[-500:]
                }
            },
            status="SUCCESS" if success else "FAIL"
        )

        return {"decision": "ACCEPTED" if success else "REJECTED"}

    except Exception as e:
        log_experiment(
            agent_name="Judge",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": {
                    "iteration": iteration,
                    "target_dir": target_dir
                },
                "output_response": {
                    "error": str(e)
                }
            },
            status="FAIL"
        )

        return {"decision": "REJECTED"}