import sys
from pathlib import Path

# Add project root to sys path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

from execution.run_e2e import execute_e2e_flow

if __name__ == "__main__":
    prompt = "Aydınlık, ferah ve çok canlı renklere sahip, koyu tema KESİNLİKLE kullanmayan, animasyonları ilgi çekici modern bir fotoğraf stüdyosu"
    print(f"[RUNNER] Running E2E flow with prompt: {prompt}")
    execute_e2e_flow(prompt)
