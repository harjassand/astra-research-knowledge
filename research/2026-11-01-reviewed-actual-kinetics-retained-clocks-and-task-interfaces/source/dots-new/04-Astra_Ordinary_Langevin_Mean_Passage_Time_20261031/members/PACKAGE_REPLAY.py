from pathlib import Path
from fractions import Fraction as F
import sys,json
p=Path(__file__).resolve().parent/'constant_spd_mfpt_20261031'
sys.path.insert(0,str(p))
import receive_mfpt as c
raw=json.loads((p/'small_raw_fixture.json').read_text())
cert=json.loads((p/'small_certificate.json').read_text())
print(json.dumps(c.verify(raw,cert,beta=F(1),kappa=F(1),quad_relative=F(1,1000),full_ratio=F(11,10)),sort_keys=True))
