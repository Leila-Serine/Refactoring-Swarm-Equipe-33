import argparse
import os
import sys
from dotenv import load_dotenv

from src.utils.logger import log_experiment, ActionType
from src.agents.auditor_agent import run_auditor
from src.agents.fixer_agent import run_fixer

load_dotenv()


def main():
    # -------------------------------
    # 1) CLI arguments (Jour 6)
    # -------------------------------
    parser = argparse.ArgumentParser(description="Refactoring Swarm Orchestrator (Day 6)")
    parser.add_argument("--target_dir", type=str, required=True, help="Target file or directory (sandbox)")
    parser.add_argument("--max_iterations", type=int, default=2, help="Maximum iterations allowed")
    args = parser.parse_args()

    target = args.target_dir
    max_iterations = args.max_iterations

    # -------------------------------
    # 2) Basic checks
    # -------------------------------
    if not os.path.exists(target):
        print(f"❌ Target not found: {target}")
        # log clean failure
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Startup check",
                "output_response": f"Target not found: {target}",
            },
            status="FAIL",
        )
        sys.exit(1)

    if max_iterations < 1:
        print("❌ --max_iterations must be >= 1")
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Startup check",
                "output_response": f"Invalid max_iterations: {max_iterations}",
            },
            status="FAIL",
        )
        sys.exit(1)

    print(f"🚀 DEMARRAGE SUR : {target}")
    print(f"🔁 Max iterations : {max_iterations}")

    # -------------------------------
    # 3) System startup log
    # -------------------------------
    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System startup – no LLM interaction",
            "output_response": f"Target: {target}",
        },
        status="INFO",
    )

    # -------------------------------
    # 4) Controlled orchestration loop
    # -------------------------------
    current_target = target
    last_audit = None
    stopped_reason = None
    final_status = "FAIL"  # default unless accepted

    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 Itération {iteration}")

        # ---- Auditor step ----
        try:
            audit = run_auditor(current_target)
            last_audit = audit
        except Exception as e:
            # log and stop cleanly
            print(f"❌ Auditor error: {e}")
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.ANALYSIS,
                details={
                    "input_prompt": f"Iteration {iteration} – Auditor crashed",
                    "output_response": {"error": str(e), "target": current_target, "iteration": iteration},
                },
                status="FAIL",
            )
            stopped_reason = f"Auditor crashed at iteration {iteration}"
            break

        # log Auditor result (system-level trace)
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": f"Iteration {iteration} – Auditor analysis",
                "output_response": {
                    "iteration": iteration,
                    "target": current_target,
                    "auditor_result": audit,
                },
            },
            status="SUCCESS",
        )

        # decision
        decision = None
        if isinstance(audit, dict):
            decision = audit.get("decision")

        if decision == "ACCEPTED":
            print("✅ Auditor a validé le code. Arrêt du processus.")
            stopped_reason = f"Accepted at iteration {iteration}"
            final_status = "SUCCESS"
            break

        # If not accepted, decide if we are allowed to fix or must stop
        if iteration >= max_iterations:
            print("🛑 Max iterations atteint. Arrêt en échec contrôlé.")
            stopped_reason = f"Max iterations reached ({max_iterations})"
            final_status = "FAIL"

            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Stop condition reached",
                    "output_response": {
                        "reason": stopped_reason,
                        "iteration": iteration,
                        "last_audit": last_audit,
                    },
                },
                status="FAIL",
            )
            break

        # ---- Fixer step ----
        print(f"⚠️ Auditor a refusé. Lancer le Fixer pour l'itération {iteration}")
        try:
            fixed_file = run_fixer(current_target, audit, iteration)
        except Exception as e:
            print(f"❌ Fixer error: {e}")
            log_experiment(
                agent_name="System",
                model_used="N/A",
                action=ActionType.FIX,
                details={
                    "input_prompt": f"Iteration {iteration} – Fixer crashed",
                    "output_response": {"error": str(e), "target": current_target, "iteration": iteration},
                },
                status="FAIL",
            )
            stopped_reason = f"Fixer crashed at iteration {iteration}"
            final_status = "FAIL"
            break

        # log Fixer result (system-level trace)
        log_experiment(
            agent_name="System",
            model_used="N/A",
            action=ActionType.FIX,
            details={
                "input_prompt": f"Iteration {iteration} – Fixer correction",
                "output_response": {
                    "iteration": iteration,
                    "from_target": current_target,
                    "fixed_file": fixed_file,
                },
            },
            status="SUCCESS",
        )

        # next iteration target
        current_target = fixed_file

    # -------------------------------
    # 5) Clean shutdown log
    # -------------------------------
    print("\n✅ FIN DU PROCESSUS")
    print(f"🛑 Raison: {stopped_reason or 'Unknown'}")

    log_experiment(
        agent_name="System",
        model_used="N/A",
        action=ActionType.DEBUG,
        details={
            "input_prompt": "System shutdown",
            "output_response": {
                "final_status": final_status,
                "reason": stopped_reason,
                "last_audit": last_audit,
            },
        },
        status="INFO" if final_status == "SUCCESS" else "FAIL",
    )


if __name__ == "__main__":
    main()
