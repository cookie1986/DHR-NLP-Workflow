from pathlib import Path
import os
from dotenv import load_dotenv

def load_env():
    here = Path(__file__).resolve().parents[1]
    env_path = here / "config" / ".ENV"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)

# load on import
load_env()