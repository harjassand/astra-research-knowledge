from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
root=Path(__file__).resolve().parent;p=root/'well_redistribution_survival_20261031';sys.path.insert(0,str(p))
import receive_survival as c
raw=json.loads((p/'small_raw_fixture.json').read_text());cert=json.loads((p/'small_certificate.json').read_text())
r=c.verify(raw,cert,times=[F(0),F(10**8),F(3*10**8),F(10**9)],ks_error=F(1,20),query_absolute_width=F(1,10),full_ratio=F(11,10))
newraw=c.core.fixture(512,F(20),F(1),False);oldraw=c.core.core.fixture(512,F(20),F(1),False)
assert c.base.same(newraw,oldraw)
h=hashlib.sha256(json.dumps(newraw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert h=='e693d5c1ccf5fe43336f3e845d78fdad3a308d0fe88094cc8c4688a5caca76ff'
def pick(folder):
 rows=json.loads((root/folder/'results.json').read_text())
 return next(x['certificate']for x in rows if x['fixture']['m']==512 and F(x['fixture']['mobility'])==1 and F(x['fixture']['coupling'])==20 and not x['fixture']['diagonal'])
old=pick('constant_spd_mfpt_20261031');new=pick('well_redistribution_mfpt_20261031')
fields=['acquisition','actual_full_generator','initialization','basin_mass','slab_resistance']
assert all(c.base.same(old[k],new[k])for k in fields)
assert all(old['task'][k]==new['task'][k]for k in ['beta','kappa'])
assert old['mean_hitting_time']['lower']==new['mean_hitting_time']['lower']
assert F(new['total_ratio_exact'])<F(old['total_ratio_exact'])
print(json.dumps({'small_original_external_task_receiver':r['status'],'unchanged_actual_model':{'status':'PASS','canonical_raw_sha256':h,'identical_fields':fields+['beta','kappa'],'old_ratio_display':float(F(old['total_ratio_exact'])),'new_ratio_display':float(F(new['total_ratio_exact']))},'scope':'changed witness, not physics; exact full Gibbs|A remains required'},sort_keys=True))
