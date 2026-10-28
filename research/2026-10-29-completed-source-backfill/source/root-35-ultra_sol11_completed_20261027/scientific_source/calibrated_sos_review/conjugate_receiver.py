"""Exact conjugate receiver; stdlib only, no optimization/differentiation fit."""
from pathlib import Path
from fractions import Fraction as Q
import json,runpy,math,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
src=runpy.run_path(str(OUT.parent/'support_gram_compiler/verify_grams_independently.py'),run_name='given_input')
rec=json.loads((OUT/'RECEIVER.json').read_text());kap=Q(rec['kappa']);ee=Q(rec['e']);sigma=Q(rec['sigma']);B=list(map(Q,rec['B']))
add,scale,mul=src['psum'],src['sc'],src['mul']
H=add(src['F'],scale(-kap,mul(src['q'],src['q'])));E=add(H,scale(ee,src['T']))
pH=add(src['p'],scale(-2*kap,mul(src['q'],mul(src['T'],src['T']))))
def value(poly):return sum((c*math.prod(x**n for x,n in zip(B,e)) for e,c in poly.items()),Q(0))
def dv(poly,i):
    out=Q(0)
    for e,c in poly.items():
        if e[i]:
            ex=list(e);ex[i]-=1;out+=c*e[i]*math.prod(x**n for x,n in zip(B,ex))
    return out
cof=[B[3],-B[2],-B[1],B[0]];k=value(pH)/(value(src['T'])+sigma)**2
j=[dv(E,i)-k*cof[i] for i in range(4)]+[k]
z=list(map(Q,rec['selected_z']));z0=list(map(Q,rec['z0']));n=list(map(Q,rec['normal']))
assert sum(x*y for x,y in zip(j,n))==Q(rec['slope'])
t=Q(rec['selected_t']);g=Q(rec['selected_G_value'])
assert t==Q(rec['base_t'])+sum(x*(y-z) for x,y,z in zip(j,z,z0))
w=[x+2*kap*y for x,y in zip(j,z)];conj=sum(x*y for x,y in zip(w,z))-g
assert conj==kap*sum(x*x for x in z)-Q(rec['base_t'])+sum(x*y for x,y in zip(j,z0))
gap=g+conj-sum(x*y for x,y in zip(w,z));assert gap==0
out={'status':'EXACT_GLOBAL_FENCHEL_PAIR_ACQUIRED','jet_gradient':list(map(str,j)),'z':list(map(str,z)),
 'w':list(map(str,w)),'G_value':str(g),'G_conjugate_value':str(conj),'display_w':list(map(float,w)),
 'display_G_conjugate_value':float(conj),'Fenchel_gap_exact':str(gap),'inverse_gradient_Gstar_at_w':list(map(str,z)),
 'strong_convexity_constant':str(2*kap),'global_gradient_Gstar_Lipschitz_bound':str(1/(2*kap)),
 'seconds':time.monotonic()-START,'scope':'Exact69-SOS/Dirac contact proves affine ell_B supports V globally. '
 'Adding kappa norm^2 gives w in partialG(z); strong convexity gives unique conjugate maximizer z. No conjugate optimization.'}
(OUT/'CONJUGATE_RECEIVER.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','display_w','display_G_conjugate_value','Fenchel_gap_exact','seconds']},indent=2))
