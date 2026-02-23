from src.utils.logger import log_experiment, ActionType

def run_auditor(file_path: str) -> str:
    """
    Agent Auditor – version minimale (Jour 2)
    """
    input_prompt = f"Analyze the file: {file_path}"
    output_response = "Basic analysis: file received successfully."

    log_experiment(
        agent_name="Auditor",
        model_used="N/A",
        action=ActionType.ANALYSIS,
        details={
            "file_path": file_path,
            "input_prompt": input_prompt,
            "output_response": output_response
        },
        status="SUCCESS"
    )

    return output_response
