"""Exact same-information global-versus-local pricing ablation, no source calls."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
p=Path(__file__).resolve().parent
current=json.loads((p/'results.json').read_text())[1]['certificate']
oldpath=p.parent/'well_redistribution_mfpt_20261031'/'results.json'
frozen=json.loads((oldpath.parent/'FROZEN_SHA256.json').read_text())['files']['results.json']
b=oldpath.read_bytes();assert len(b)==frozen['bytes']and hashlib.sha256(b).hexdigest()==frozen['sha256']
old=next(q['certificate']for q in json.loads(b)if q['fixture']['m']==512 and q['fixture']['coupling']=='20')
H=F(current['constants']['density_price_factor_upper']);BA=H*F(old['source_A_inverse_per_mass_upper'])*F(old['basin_mass']['upper'])
mh=F(current['nominal_basin_mass']['upper']);bl=F(current['lower_density_basin_mass']['lower']);rl=F(current['nominal_resistance']['lower']);rh=F(current['nominal_resistance']['upper']);eta=F(current['constants']['eta_v_upper']);cs=F(current['constants']['source_S_nominal_factor_upper'])
ratio=((1+eta/2)*BA+(eta/2)*H*mh*mh*rh*cs)/(bl*bl*rl)
eps=(1+eta)*(BA+eta*H*mh*mh*rh*cs)/(rl*bl*bl)-1
ks=eps+F(current['initial_law_error_upper'])+F(current['finite_rate_error_upper'])
r=json.loads((p/'comparison_ablation.json').read_text())
assert F(r['global_price_H'])==H
assert F(r['coarse_mean_ratio'])==ratio
assert F(r['coarse_KS_bound'])==ks
assert F(r['localized_mean_ratio'])==F(current['total_mean_ratio'])
assert F(r['localized_KS_bound'])==F(current['uniform_KS_error_upper'])
assert ratio>F(11,10) and F(current['total_mean_ratio'])<F(101,100)
assert ks>F(1,10) and F(current['uniform_KS_error_upper'])<F(1,100)
out={'status':'PASS','exact_checks':8,'source_normalizer_or_angular_calls':0,'scope':'deliberately coarse same-current pricing ablation, not physical or algorithmic lower bound'}
(p/'comparison_ablation_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
