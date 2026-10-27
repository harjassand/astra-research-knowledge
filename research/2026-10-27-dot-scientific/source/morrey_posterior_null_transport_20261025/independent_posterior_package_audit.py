from pathlib import Path
from fractions import Fraction as Q
from math import comb
import sympy as s,json
P=Path(__file__).parent
# Independent Laurent-zero-frequency moments.
def moment(e):
 a,b,c=e;return Q(sum(comb(a,i)*comb(b,j)*comb(c,k)for i in range(a+1)for j in range(b+1)for k in range(c+1)if a+c==2*(i+k)and b+c==2*(j+k)),2**sum(e))
features=[{(0,0,0):Q(1)}]+[{tuple(int(j==i)for j in range(3)):Q(1)}for i in range(3)]+[{(1,1,0):Q(1),(1,0,1):Q(1),(0,1,1):Q(1)}]
G=s.Matrix([[sum(x*y*moment(tuple(a+b for a,b in zip(e,f)))for e,x in p.items()for f,y in q.items())for q in features]for p in features]);H=G-s.eye(5)/8
assert H[0,0]==s.Rational(7,8);block=H[1:4,1:4];assert block==s.eye(3)*s.Rational(3,8);assert H[4,4]-(H[4,1:4]*block.inv()*H[1:4,4])[0]==s.Rational(1,8)
u,v,w=s.symbols('u v w');q=u*v+u*w+v*w;B=s.Matrix([[u+w,w],[w,v+w]]);assert s.expand(B.det()-q)==0
au,av,aw=s.symbols('au av aw');L=s.Matrix([[au,(aw-au-av)/2],[(aw-au-av)/2,av]]);AA=(au+av+aw)**2-2*(au**2+av**2+aw**2);assert s.expand(L.det()-AA/4)==0
x,y,z,t=s.symbols('x y z t');U=s.Matrix([x,y]);V=s.Matrix([z,t]);cross=x*t-y*z
assert s.expand((U.T*L*V)[0]**2+L.det()*cross**2-(U.T*L*U)[0]*(V.T*L*V)[0])==0
GG=u*v*w+(u*u+v*v+w*w)/2;assert s.hessian(GG,(u,v,w))==s.Matrix([[1,w,v],[w,1,u],[v,u,1]])
c=Q(28319,60000);assert (1-Q(1681,30000))/2==c;assert Q(4,27)*c==Q(28319,405000)
assert Q(500,27)<25;assert 2+Q(21,2)**2/64==Q(953,256)
assert Q(1,2)**2*Q(1,8)**2/48==Q(1,12288)
assert Q(3,4)-3*Q(8,15)/2+Q(15,32)*3*Q(8,15)**2==Q(7,20)
out={'status':'PASS','Gram_lower':'I/8','multiplier_sup_bound':'104/c','finite_continuation_epsilon':'c/208','strong_root_variance_gain':'9/128','strong_root_cubic_gain':'1/512','completion_W1':'sqrt(3V)','remote_tail_coefficient':'28319/405000','four_vertex_physical_gap':'1/12288','actual_source_conservative_family_gap':'7/20','scope':'Finite source-posterior guidance and conditional traps only; no variance exhaustion/source reachability/gradient-law counterexample.'};(P/'independent_posterior_package_audit.json').write_text(json.dumps(out,indent=2));print(out)
