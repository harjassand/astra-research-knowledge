"""Replay a full saved coefficient witness with exact integer arithmetic.

No eigensystem, normal-form generation, root approximation, transcendental
library, or floating residual test is used for the error certificate.
"""
import argparse,json,gzip,time,hashlib
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import certify_finite_expression as c
BASE=Path(__file__).parent

def validate_original_input(row):
 eta=F(row['eta']);omega=F(row['omega']);B=row['B'];f=row['frequency_offset']
 assert eta==F(1,2**B) and omega*eta**3==F(2)**f
 D2=[[1,0,0],[0,0,0],[0,0,-1]];D1=[[0,0,0],[0,F(1,3),0],[0,0,-F(1,3)]];D0=[[-1,1,F(1,3)],[1,0,2],[F(1,3),2,1]]
 expected=[[[F(D2[i][j],4)-eta*D1[i][j]/2+eta**2*D0[i][j] for j in range(3)] for i in range(3)],[[ -D2[i][j]+eta*D1[i][j] for j in range(3)] for i in range(3)],D2]
 assert len(row['coefficients_ascending_t'])==3
 for r in range(3):
  for i in range(3):
   for j in range(3):assert F(row['coefficients_ascending_t'][r][i][j])==expected[r][i][j]
 assert row['interval']==['0','1'] and row['initial_matrix']=='I_3'
 assert F(row['operator_tolerance'])==F(1,2**row['precision_bits'])

def replay(rowid):
 start=time.perf_counter();result=json.loads((BASE/f'certified_expression_{rowid}.json').read_text());wp=BASE/result['coefficient_witness']
 assert hashlib.sha256(wp.read_bytes()).hexdigest()==result['coefficient_witness_sha256']
 with gzip.open(wp,'rt') as f:w=json.load(f)
 assert w['coefficient_fraction_bits']==c.P and w['phase_fraction_bits']==c.EP and w['global_error_fraction_bits']==c.CP
 row=w['row'];validate_original_input(row);end=F(2)**(row['B']-1);prev=-end
 U=(c.Q*np.eye(3,dtype=object),c.zero());error=0;panels=0
 for panel in w['panel_witnesses']:
  a,b,center,h=[F(panel[x]) for x in ('a','b','c','h')]
  assert a==prev and b>a and center-h==a and center+h==b;prev=b
  assert F(float(center))==center and F(float(h))==h
  C=[]
  for poly in panel['C_integer_pairs']:
   pp=[]
   for pair in poly:
    assert len(pair)==2
    mats=tuple(np.array([[int(x) for x in rr] for rr in mat],dtype=object) for mat in pair)
    assert all(m.shape==(3,3) for m in mats);pp.append(mats)
   assert pp;C.append(pp)
  ph=[[int(x) for x in p] for p in panel['phase_integer_coefficients']]
  assert len(ph)==len(C) and all(p and p[0]==0 for p in ph)
  V,local,_=c.certify_integer_panel(float(center),float(h),2.**row['frequency_offset'],C,ph);U,error=c.compose(V,U,error,local);panels+=1
 assert prev==end
 assert str(error)==result['global_operator_error_upper_integer']
 for i in range(3):
  for j in range(3):assert [str(U[0][i,j]),str(U[1][i,j])]==result['endpoint_exact_dyadic_integer_pairs'][i][j]
 assert error<=c.CQ//2**row['precision_bits']
 return {'row_id':rowid,'exact_witness_replay_passed':True,'input_coefficients_and_coverage_exactly_checked':True,'phase_constants_exactly_zero':True,'same_exact_output_and_error_bound':True,'panels':panels,'seconds':time.perf_counter()-start}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--rows',nargs='+',default=['B4_f0_s20','B6_f0_s20','B8_f0_s20','B3_f0_s36']);a=ap.parse_args();r=[replay(x) for x in a.rows];(BASE/'INTEGER_WITNESS_REPLAY.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
