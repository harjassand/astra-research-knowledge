"""Whole pointwise corrected-heat class: positive-r contact/involution face."""
from geometry import *
from pathlib import Path
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
import pickle
base=Path(__file__).parent
with open(base/'direct_symmetric.pkl','rb') as ff:data=pickle.load(ff)
vars_=data['vars'];w=vars_[:60];d1,d2=vars_[-2:]
subD={d1:(2*r+1)/(r+2),d2:3/(r+2)}
P=data['P'].subs(subD).expand();vv=data['vec'].subs(subD).applyfunc(s.cancel)
Pv=s.Poly(P,*(list(x)+list(z)),domain='EX')
P=sum((s.cancel(cc)*s.prod(xx**ee for xx,ee in zip(list(x)+list(z),mon)) for mon,cc in Pv.terms()),s.S.Zero)
free=sorted(P.free_symbols-set(x)-set(z)-{r},key=str)
print('remaining form parameters',free,flush=True)
h=(2*r+1)/3
AK=s.Matrix([b,h*a,d,h*c])
zz=s.Matrix([z[2],h*z[1],h*h*z[0],z[5],h*z[4],h*h*z[3]])
sub=dict(zip(list(x)+list(z),list(AK)+list(zz)))
diff=s.Poly(P.subs(sub,simultaneous=True)-h**3*P,*(list(x)+list(z)),domain='EX')
eq=[s.cancel(cc) for cc in diff.coeffs()]
sol=s.linsolve(eq,free);print('involution solution',sol,flush=True)
subsol=dict(zip(free,list(sol)[0]))
PP=P.subs(subsol).expand();vsol=vv.subs(subsol).applyfunc(s.cancel)
jet={a:0,b:0,c:1,d:0,z[0]:0,z[1]:1,z[2]:0,z[3]:0,z[4]:0,z[5]:0}
print('decisive jet value',s.factor(PP.subs(jet)),flush=True)
print('remaining symbols',PP.free_symbols-set(x)-set(z)-{r},flush=True)
with open(base/'positive_direct_face.pkl','wb') as ff:pickle.dump({'r':r,'P':PP,'vec':vsol,'vars':vars_,'sol':sol,'free':free,'jet_value':s.factor(PP.subs(jet))},ff)
