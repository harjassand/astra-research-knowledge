from pathlib import Path
from fractions import Fraction as F
import sys,json,time
A=Path(__file__).resolve().parent;S=A/'replay/matched_energy_clock_constructor_20261101';sys.path.insert(0,str(S));import receive_matched_clock as r
small=json.loads((S/'small_certificate.json').read_text());st=r.external_from_record(small);checks=0;items=[]
def ok(a,s):
 global checks
 assert a,s
 checks+=1;items.append(s)
raw=r.p.old.fixture(64,F(1),F(1,3));st.update(beta=F(9),physical_spacing=9*st['physical_spacing']);z=r.certify(raw,**st)
for k in ['global_moment_error_upper','record_TV_error_upper','reference_dimensionless_step','sharp_trial_vector_error_upper','sign_vector_error_upper','comparison_flip_probability','event']:
 ok(r.base.same(z[k],small[k]),'exact beta/mobility covariance '+k)
ok(F(z['reference_flip_rate'])*9==F(small['reference_flip_rate']) and F(z['actual_physical_spacing'])==9*F(small['actual_physical_spacing']),'actual physical scaling not abstract renaming')
ok(F(z['raw_derivative_acquisition']['Hessian_trace_coefficient_norm_squared'])*9==F(small['raw_derivative_acquisition']['Hessian_trace_coefficient_norm_squared']),'actual raw H scales with mobility squared')
ok(r.verify(raw,z,**st)['status']=='PASS','full scaled raw model actually received')
nr=r.p.old.fixture(68,F(1));nr['energy_terms'][67]['coefficient']='1/2';nt=r.external_from_record(small);nt.update(beta=F(2,3),physical_spacing=F(10**9),path_error=F(99,100),full_ratio=F(10),Nt=128,Ny=64,max_grid=16384)
nz=r.certify(nr,**nt);ok(nz['raw_derivative_acquisition']['alpha']==17 and nz['raw_derivative_acquisition']['pure_coefficient_min']=='1/2','odd integer Gamma shape and nonfirst pure minimum actually acquired');ok(r.verify(nr,nz,**nt)['status']=='PASS','odd-alpha nonunit-beta complete original query received')
(A/'received_scaling_case.json').write_text(json.dumps({'raw':raw,'certificate':z},indent=2)+'\n');(A/'received_odd_shape_case.json').write_text(json.dumps({'raw':nr,'certificate':nz},indent=2)+'\n');report={'status':'PASS','checks':checks,'details':items,'odd_case_TV':float(F(nz['record_TV_error_upper']))};(A/'scaling_odd_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
