from pathlib import Path
from fractions import Fraction as F
import sys,json
p=Path(__file__).resolve().parent/'radial_kinetic_service_20261031'
sys.path.insert(0,str(p))
import receive_kinetic as c
raw=json.loads((p/'small_raw_fixture.json').read_text())
cert=json.loads((p/'small_certificate.json').read_text())
# External original task reconstructed literally, not accepted from the certificate.
task=dict(initial_state=[F(1)]+[F(0)]*7,protocol=[{'y':F(-1),'duration':F(1,3)},{'y':F(0),'duration':F(1,2)},{'y':F(1,2),'duration':F(2,3)}],threshold=F(1),cdf_absolute_error=F(1,10**10))
print(json.dumps(c.verify(raw,cert,**task),sort_keys=True))
