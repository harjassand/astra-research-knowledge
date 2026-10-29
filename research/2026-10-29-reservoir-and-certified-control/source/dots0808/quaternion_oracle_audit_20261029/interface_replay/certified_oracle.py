"""Total mathematical oracle when max_grid_points=None; no success on a resource cap."""
from quartic_sos_oracle import *
from exact_grid_fallback import grid_fallback
from numbers import Integral

def certified_global_minimum(coeff,tolerance,fast=True,max_grid_points=None):
 coeff={tuple(e):Q(c) for e,c in coeff.items()};tol=Q(tolerance)
 if tol<=0 or any(len(e)!=4 or any(not isinstance(v,Integral) or isinstance(v,bool) or v<0 for v in e) or sum(e)!=4 for e in coeff):raise ValueError('homogeneous quartic and positive tolerance required')
 coeff={e:coeff.get(e,Q(0)) for e in exps}
 if not any(coeff.values()):return dict(status='certified',method='zero_polynomial',lower='0',upper='0',gap='0',quaternion=['1','0','0','0'])
 failure=None
 if fast:
  try:
   mm=max(abs(v) for v in coeff.values());scale=2**max(0,mm.numerator.bit_length()-mm.denominator.bit_length()+1);f={e:c/scale for e,c in coeff.items()}
   g0,gq,ns=gram_param(f);qr,up=find_candidate(f,starts=24)
   target=float(tol/scale);digits=min(12,max(1,math.ceil(-math.log10(max(target,1e-300)))+2))
   xx,trace=barrier_search(g0,gq,ns,mu_final=10.**(-digits));lo,ys,G,piv,tries=rational_certificate(g0,gq,ns,xx,bits=50,repair_start_bits=48);verify_identity(f,lo,G)
   upper=up*scale;lower=lo*scale;gap=upper-lower
   if gap<=tol:
    return dict(status='certified',method='rational_SOS',lower=str(lower),upper=str(upper),gap=str(gap),quaternion=[str(x) for x in qr],gram_scale=scale,gram=[[str(x) for x in row] for row in G],normalized_lower=str(lo))
   failure=dict(reason='valid_SOS_gap_exceeds_target',gap=str(gap),lower=str(lower),upper=str(upper))
  except Exception as exc:failure=dict(reason='numerical_certificate_finder_failed',exception_type=type(exc).__name__)
 result=grid_fallback(coeff,tol,max_points=max_grid_points)
 if result['status']=='complete_exact_grid_certificate':result['status']='certified';result['method']='complete_exact_grid'
 if failure is not None:result['fast_path_failure']=failure
 return result

if __name__=='__main__':
 root=Path(__file__).parent;bank=json.load(open(root/'bank_one_axis.json'));raw=bank_polynomial(bank,0);f={e:Q(c,4*bank['probe_calls']) for e,c in raw.items()}
 actual=certified_global_minimum(f,Q(1,10**7),max_grid_points=10000);assert actual['status']=='certified' and actual['method']=='rational_SOS'
 zero=certified_global_minimum({},Q(1,10**9));assert zero['status']=='certified'
 forced_grid=certified_global_minimum({(4,0,0,0):Q(1)},Q(1),fast=False,max_grid_points=10000);assert forced_grid['status']=='certified'
 nonsos={e:Q(0) for e in exps}
 for e in [(2,2,0,0),(0,2,2,0),(2,0,2,0),(0,0,0,4)]:nonsos[e]=Q(1)
 nonsos[(1,1,1,1)]=Q(-4)
 blocked=certified_global_minimum(nonsos,Q(1,10**6),max_grid_points=10000);assert blocked['status']=='budget_exceeded_no_oracle_success'
 result=dict(actual_bank=actual,zero=zero,forced_grid=forced_grid,nonsos_resource_cap=blocked,scope='Executed complete-interface branches. Uncapped fallback is a finite algorithm, not an assertion of practical fine-tolerance cost.')
 (root/'certified_oracle_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:{j:v for j,v in x.items() if j not in ['gram']} if isinstance(x,dict) else x for k,x in result.items()},indent=2))
