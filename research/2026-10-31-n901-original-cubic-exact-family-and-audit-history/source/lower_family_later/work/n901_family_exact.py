"""Receive and export an exact, parameter-uniform original N901 certificate.

The independent receiver uses only the exported polynomials and rebuilds
the original functional. No numerical margin is an analytic premise.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
from math import comb
import sys,pickle,json,time
import sympy as s
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/n901_gate'));import receive as b
T=pickle.loads((root/'work/n901_parameter_template.pickle').read_bytes());K=pickle.loads((root/'work/n901_family_kernel.pickle').read_bytes());r=T['r'];t=K['t'];lo=K['minpower'];gp=T['Gram_pairs'];data=K['data'];active=K['active'];compact='--compact' in sys.argv;rec=json.loads((root/('work/n901_compact_fit.json' if compact else 'work/n901_family_fit_d5_e16.json')).read_text());deg=rec['degree'];count=len(active)*(deg+1);extra=rec.get('extra_t_power',0);low=R(rec.get('t_lower','0'));high=R(rec.get('t_upper','1'))
def rat(x):return R(int(x.p),int(x.q)) if hasattr(x,'p') else R(x)
def sq(x):return s.Rational(x.numerator,x.denominator)
def main():
 start=time.perf_counter();eq=[];rhs=[]
 for power in range(lo,-extra):
  for k in range(len(gp)):
   row=[]
   for a in range(len(active)):
    for l in range(deg+1):row.append(data[k][a+1].nth(power-lo-l) if power-lo-l>=0 else 0)
   if any(row) or data[k][0].nth(power-lo):eq.append(row);rhs.append(-data[k][0].nth(power-lo))
 A=s.Matrix(eq) if eq else s.zeros(0,count);bb=s.Matrix(rhs) if rhs else s.zeros(0,1);rr,piv=A.row_join(bb).rref();assert count not in piv;free=[i for i in range(count) if i not in piv];u=[R(0)]*count;flat=[v for row in rec['u_coefficients'] for v in row]
 for i in free:u[i]=R(round(flat[i]*2**32),2**32)
 for k,i in enumerate(piv):u[i]=rat(rr[k,-1])-sum((rat(rr[k,j])*u[j] for j in free),R(0))
 assert A*s.Matrix([sq(x) for x in u])==bb;u=[u[a*(deg+1):(a+1)*(deg+1)] for a in range(len(active))];N=rec['Bernstein_degree'];HP=[]
 for k in range(len(gp)):
  coeff={}
  for (power,),v in data[k][0].terms():coeff[power+lo+extra]=rat(v)
  for a in range(len(active)):
   for (power,),v in data[k][a+1].terms():
    for l,uv in enumerate(u[a]):coeff[power+lo+extra+l]=coeff.get(power+lo+extra+l,R(0))+rat(v)*uv
  assert all(not v for power,v in coeff.items() if power<0);HP.append([coeff.get(power,R(0)) for power in range(N+1)])
 H=[[[R(0)]*(N+1) for j in range(12)] for i in range(12)]
 for (i,j),pol in zip(gp,HP):H[i][j]=H[j][i]=pol
 margin=R(1,65536);checks=0
 ww=[[sum((R(comb(k,a),comb(N,a))*comb(p,a)*low**(p-a)*(high-low)**a for a in range(min(k,p)+1)),R(0)) for p in range(N+1)] for k in range(N+1)]
 for k in range(N+1):
  B=[[sum((ww[k][p]*H[i][j][p] for p in range(N+1)),R(0)) for j in range(12)] for i in range(12)]
  for block in K['blocks']:b.pd([[B[i][j]-(margin if i==j else 0) for j in block] for i in block]);checks+=1
 den=K['den']*t**extra;E=t*(1+t)**2*(t+2);D=s.expand(den*E**2);freeval=[s.Integer(0)]*len(T['free'])
 for a,j in enumerate(active):freeval[j]=(1/t)**K['fexp'][a]*sum(sq(v)*t**l for l,v in enumerate(u[a]))
 omega=[]
 for row in T['solution'][78:]:
  val=row[0].subs(r,1/t)+sum(row[j+1].subs(r,1/t)*freeval[j] for j in range(len(freeval)) if row[j+1] and freeval[j]);v=s.Poly(s.cancel(D*val),t);omega.append([str(v.nth(k)) for k in range(v.degree()+1)] if v else ['0'])
 Hout=[[[str(v) for v in pol] for pol in row] for row in H]
 out={'parameter':'t=1/r','t_range':[str(low),str(high)],'actual_r_range':'3/4 <= r <= 1' if compact else '1 <= r < infinity','denominator_extra_t_power':extra,'denominator_d_coefficients':[str(s.Poly(den,t).nth(k)) for k in range(s.degree(den,t)+1)],'denominator_d_factorization':'t^extra*(1+t)^2*(2+t)*(1+2t)^2*(3+2t)^2/2700','feature_multiplier_E':'t*(1+t)^2*(2+t)','Gram_polynomial':Hout,'two_form_numerators':omega,'common_two_form_denominator':'d(t)*E(t)^2','Bernstein_degree':N,'Bernstein_PD_margin':str(margin),'blocks':K['blocks'],'exact_Bernstein_block_checks':checks,'free_polynomial_coefficients':[[str(v) for v in row] for row in u],'free_positions':active,'free_scaling_exponents':K['fexp'],'Gram_scaling_exponents':K['gexp'],'Laurent_cancellation_rank':len(piv)}
 dest=root/('outputs/n901_gate/family_r_3_4_to_1.json' if compact else 'outputs/n901_gate/family_r_ge_1.json');dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'file':str(dest),'r_range':out['actual_r_range'],'exact_Bernstein_checks':checks,'margin':str(margin),'Laurent_cancellation_rank':len(piv),'seconds':time.perf_counter()-start}),flush=True)
if __name__=='__main__':main()
