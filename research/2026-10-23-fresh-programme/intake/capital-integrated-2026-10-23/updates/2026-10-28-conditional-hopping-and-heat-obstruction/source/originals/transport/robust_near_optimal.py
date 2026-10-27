"""Correlated thermodynamic decision under unknown conditional hopping.
Uses explicit published central witnesses; exact algebra, no solver or source imports.
"""
from robust_decision import *
from math import factorial
import hashlib

def pnorm(fields,weights,den,kind='inverse'):
 return sum((w*sup_sqrt(norm2(field,den,kind)) for field,w in zip(fields,weights)),F())

def pop(field):return {w:v for w,v in field.items() if w[0]==0 and v}

def weight_sum(vals,k,h):return sum((h**(j-k)/factorial(j-k)*vals[j] for j in range(k,len(vals))),F())

if __name__=='__main__':
 tick=time.monotonic();path=SRC/'results/fresh/witness.npz';z=np.load(path);rec=json.loads(path.with_suffix('.json').read_text());den=int(z['den'][0]);M=len(z['FN'])-1;h=F(27,512)
 ff=[expand(z['fw'],row) for row in z['FN']];gg=[expand(z['gw'],row) for row in z['GN']]
 # Physical Hc coefficients are hnum/2048; act's output denominator is 1024*inputden.
 HC=[(3,0,-1024),(3,3,-1024),(0,3,2048),(0,5,1109)];H1=[(0,5,2)]
 EF=[];GG=[];C0=[];C1=[];CA=[];Ccross=[];CG=[];maxspan=int(rec['full_output_span'])
 for j in range(M+1):
  f=ff[j];g=gg[j];E=[Efield(f,s) for s in range(4)];edge=defaultdict(int)
  for field in E:
   for w,v in field.items():edge[w]+=v
  EF.append(sup_sqrt(norm2(clean(edge),8*den,'S')));GG.append(sup_sqrt(norm2(g,den,'S')))
  c0=F();c1=F();ca=F();cross=F();cg=F();pops10=[];pops01=[];pops11=[]
  for sigma in range(4):
   field=act(E[sigma],HC);c0+=sup_sqrt(norm2(field,8192*den,'inverse'));pops10.append(pop(field));maxspan=max(maxspan,max((x|s).bit_length() for x,s in field))
   field=act(E[sigma],H1);assert not pop(field);c1+=sup_sqrt(norm2(field,32*den,'inverse'));maxspan=max(maxspan,max((x|s).bit_length() for x,s in field))
   field=act(f,hpattern(sigma));ca+=sup_sqrt(norm2(field,4*den,'inverse'));pops01.append(pop(field));maxspan=max(maxspan,max((x|s).bit_length() for x,s in field))
   field=act(g,hpattern(sigma));assert not pop(field);cg+=sup_sqrt(norm2(field,4*den,'inverse'));maxspan=max(maxspan,max((x|s).bit_length() for x,s in field))
   row=[]
   for eta in range(4):
    field=act(E[eta],hpattern(sigma));cross+=sup_sqrt(norm2(field,32*den,'inverse'));row.append(pop(field));maxspan=max(maxspan,max((x|s).bit_length() for x,s in field))
   pops11.append(row)
  total=defaultdict(int)
  for sigma in range(4):
   assert pops10[sigma]=={w:2048*v for w,v in pops01[sigma].items()}
   for w,v in pops10[sigma].items():total[w]+=v
   for eta in range(4):
    assert {w:256*v for w,v in pops11[sigma][eta].items()}==(pops10[eta] if sigma==eta else {})
  assert not clean(total)
  C0.append(c0);C1.append(c1);CA.append(ca);Ccross.append(cross);CG.append(cg)
  print('exact jet constants',j,'seconds',time.monotonic()-tick,flush=True)
 # Save reusable exact norm summaries before the selected interval evaluation.
 Af=act(ff[0],HC);assert not pop(Af);A2=norm2(Af,1024*den,'inverse');S2=norm2(ff[0],den,'S');pair=F(-ff[0].get((3,1),0)+ff[0].get((3,2),0),2*den)
 assert 4*(2*pair-S2-A2)==F(rec['D_interval_exact'][0])
 raw={'EF':list(map(str,EF)),'GS':list(map(str,GG)),'C0':list(map(str,C0)),'C1':list(map(str,C1)),'CA':list(map(str,CA)),'Ccross':list(map(str,Ccross)),'CG':list(map(str,CG)),'full_output_span':maxspan,'A0_f_inverse_norm':str(sup_sqrt(A2)),'nominal_D_lower':rec['D_interval_exact'][0],'source_witness_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 (OUT/'CENTRAL_HOPPING_NORM_BOUNDS.json').write_text(json.dumps(raw,indent=2)+'\n')
 # Uniform field/perturbation norms throughout s in [0,h].
 ef=[weight_sum(EF,k,h) for k in [0,1]];gn=[weight_sum(GG,k,h) for k in [0,1]]
 c10=[weight_sum(C0,k,h)+h*weight_sum(C1,k,h)+(k*weight_sum(C1,k-1,h) if k else 0) for k in [0,1]]
 c01=[weight_sum(CA,k,h) for k in [0,1]];c11=[weight_sum(Ccross,k,h) for k in [0,1]];ag=[weight_sum(CG,k,h) for k in [0,1]]
 Q=[F(s) for s in rec['residual_norm_upper_exact']];qnom=[weight_sum(Q,k,h) for k in [0,1]]
 poly=[F(s) for s in rec['corrected_D_polynomial_exact']];gain=poly[0]-sum((v*h**j for j,v in enumerate(poly)),F())
 rows=[]
 for eps in [F(1,100),F(1,1000),F(1,10000),F(1,100000)]:
  rho=eps/(1-eps);m2=1/(1-eps)**2-1;bA=[rho*c10[k]+eps*c01[k]+eps*rho*c11[k] for k in [0,1]]
  bo=[rho*ef[k]+eps*ag[k]+(eps/2 if not k else 0) for k in [0,1]]
  qq=[qnom[k]+sup_sqrt(bo[k]**2+bA[k]**2) for k in [0,1]]
  delta_hat=8*m2*ef[0]*ef[1]+8*(bA[1]*gn[0]+bA[0]*gn[1])
  error=4*(2*qq[0]*qq[1]+qq[0]**2)
  improvement=gain-h*(delta_hat+error)
  row={'epsilon':str(eps),'improvement_lower_exact':str(improvement),'improvement_lower_float_diagnostic':float(improvement),'delta_corrected_derivative_upper':str(delta_hat),'derivative_error_upper':str(error)};rows.append(row)
  print(json.dumps({'epsilon':str(eps),'improvement_lower_float_diagnostic':float(improvement)}),flush=True)
 data={'decision':'V=1109/512 versus71/32, U=4,d=2; four positive conditional hopping amplitudes in[1-epsilon,1+epsilon]','half_interval':str(h),'uniform_edge_S_norms':list(map(str,ef)),'uniform_g_S_norms':list(map(str,gn)),'c10':list(map(str,c10)),'c01':list(map(str,c01)),'c11':list(map(str,c11)),'cAg':list(map(str,ag)),'uniform_nominal_residual_norms':list(map(str,qnom)),'nominal_corrected_gain_exact':str(gain),'bounds':rows,'complete_output_span':maxspan,'min_ring_size':2*maxspan+1,'population_identities_exact':(4*21),'source_witness_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'seconds':time.monotonic()-tick,'scope':'Actual thermodynamic second-moment D via inherited source transfer and audited conditional-hop extension; no global optimum or acquisition claim'}
 (OUT/'ROBUST_NEAR_OPTIMAL_DECISION.json').write_text(json.dumps(data,indent=2)+'\n')
