import sys
from pathlib import Path

# Add project root and parent to sys path for static linter & runtime compliance
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR.parent))

from execution.component_assembler import assemble_next_app
from execution.deploy import deploy_app

def run_aiona_assembly():
    blueprint_path = BASE_DIR / ".tmp" / "pipeline" / "aiona" / "experience_blueprint.json"
    session_id = "aiona_v1"
    
    print("\n==================================================")
    print(">>> 1. ASSEMBLING AIONA HIGH-FIDELITY LUXURY SITE")
    build_dir = assemble_next_app(blueprint_path, session_id)
    print(f"Assembly completed successfully at: {build_dir}")
    
    print("\n>>> 2. RUNNING PRODUCTION BUILD COMPILATION AUDIT")
    deploy_report = deploy_app(session_id)
    
    print("\n==================================================")
    print(">>> COMPILATION & VERIFICATION AUDIT COMPLETE")
    print(f"Compilation/Build: {'PASSED' if deploy_report.get('build_success', False) else 'FAILED'}")
    print(f"Warnings/Errors: {deploy_report.get('warnings')}")
    print("==================================================\n")

if __name__ == "__main__":
    run_aiona_assembly()
