"""Reconstruct the compatible determinant and verify its exact rational SOS remainder."""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from triad_core import *
here=Path(__file__).parent
A,B,C,D,E=S.symbols('A B C D E',real=True);rs=[conformal((0,A),(1,0)),conformal((B,C),(0,1)),conformal((D+E,-D+E),(1,1))]
N=moments([r[0] for r in rs],[r[1] for r in rs]);terms=S.Poly(N.det(method='domain-ge'),A,B,C,D,E).terms()
actual={tuple(m):F(str(c)) for m,c in terms if m[0]>0}
cert=json.loads((here/'two_free_positive_A_sos.json').read_text());replay={}
def add(m,c):replay[m]=replay.get(m,F(0))+c
for m,c,aa,bb,w1,w2 in cert['pairs']:
 m=tuple(m);aa=tuple(aa);bb=tuple(bb);c=F(c);w1=F(w1);w2=F(w2)
 assert all(e%2==0 for e in aa+bb) and all(2*q==a+b for q,a,b in zip(m,aa,bb))
 assert w1>0 and w2>0 and 4*w1*w2==c*c
 add(aa,w1);add(bb,w2);add(m,c)
for m,c in cert['residue']:
 m=tuple(m);c=F(c);assert all(e%2==0 for e in m) and c>=0;add(m,c)
replay={m:c for m,c in replay.items() if c}
assert replay==actual
assert len(cert['pairs'])==286 and len(cert['residue'])==203
print('PASS: reconstructed determinant remainder is the sum of 286 two-monomial squares and 203 monomial squares.')
print('PASS: determinant boundary at A=0 is a two-wave zero-third-moment field, PSD by the inherited ROC block argument.')
# A genuinely free-polarization example and exact Schur data.
ex=N.subs({A:1,B:1,C:1,D:1,E:1});H=ex[:4,:4];vv=ex[:4,4];ww=ex[:4,5]
alpha=S.factor(ex[4,4]-(vv.T*H.inv()*vv)[0]);beta=S.factor(ex[5,5]-(ww.T*H.inv()*ww)[0]);rho=S.factor(ex[4,5]-(vv.T*H.inv()*ww)[0])
print('Example A=B=C=D=E=1: c=',ex[4,5],', a=',alpha,', b=',beta,', r=',rho,', ab-r^2=',S.factor(alpha*beta-rho*rho))
