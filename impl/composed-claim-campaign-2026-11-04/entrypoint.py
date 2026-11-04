"""Only entry point copied with assessor modules to isolated staging."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import strict_load,encode,digest
from assessor import Assessor
supplied=strict_load(Path("supplied.json").read_bytes())
acquisition=json.loads(Path("acquisition.json").read_bytes())
def emit(e):
    sys.stdout.buffer.write(encode(e)+b"\n");sys.stdout.buffer.flush()
Assessor(supplied,acquisition,emit).run()
