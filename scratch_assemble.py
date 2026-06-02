import sys
from pathlib import Path

# Add project root and parent to sys path for static linter & runtime compliance
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR.parent))

from antigravitymain.execution.component_assembler import assemble_next_app
from antigravitymain.execution.deploy import deploy_app

def run_peachweb_assembly():
    blueprint_path = BASE_DIR / ".tmp" / "pipeline" / "peachweb_replica" / "experience_blueprint.json"
    session_id = "peachweb_replica_v3"
    
    print("\n==================================================")
    # 1. Assemble Peachweb replica Next.js application
    print(">>> 1. ASSEMBLING PEACHWEB HIGH-FIDELITY REPLICA APP")
    build_dir = assemble_next_app(blueprint_path, session_id)
    print(f"Assembly completed successfully at: {build_dir}")
    
    # 2. Run Next.js production compilation to verify build
    print("\n>>> 2. RUNNING PRODUCTION BUILD COMPILATION AUDIT")
    deploy_report = deploy_app(session_id)
    
    print("\n==================================================")
    print(">>> COMPILATION & VERIFICATION AUDIT COMPLETE")
    print(f"Compilation/Build: {'PASSED' if deploy_report.get('build_success', False) else 'FAILED'}")
    print(f"Live Local Deploy URL: {deploy_report.get('deploy_url')}")
    print("==================================================\n")

if __name__ == "__main__":
    run_peachweb_assembly()
