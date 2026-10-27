from pathlib import Path
from fractions import Fraction as Q
import sympy as S,json
P=Path(__file__).parent
A=(S.sqrt(6)+S.sqrt(2))/4;B=(S.sqrt(6)-S.sqrt(2))/4;t=1/S.sqrt(2)
pts=[S.Matrix([S.Rational(1,2),A,B]),S.Matrix([S.Rational(1,2),-A,-B]),S.Matrix([-1,t,-t]),S.Matrix([-1,-t,t])];ww=[S.Rational(1,3)]*2+[S.Rational(1,6)]*2;J=(S.ones(3)-S.eye(3))/2
for z in pts:
 u,v,w=z;q=(z.T*J*z)[0]
 assert S.simplify(1+2*u*v*w-u*u-v*v-w*w)==0
 assert S.simplify(q-sum(z)/2)==0
 assert S.simplify(-2*u+2*v*w)!=0
 Bz=S.Matrix([[u+w,w],[w,v+w]]);assert S.simplify(sum(x*x for x in Bz))>S.Rational(1,256)
mean=S.simplify(sum((w*z for w,z in zip(ww,pts)),S.zeros(3,1)));assert mean==S.zeros(3,1)
C=S.simplify(sum((w*z*z.T for w,z in zip(ww,pts)),S.zeros(3)));assert C==S.diag(S.Rational(1,2),(3+S.sqrt(3))/6,(3-S.sqrt(3))/6)
assert S.simplify(S.Matrix.hstack(*(S.Matrix([1,*z]) for z in pts)).det())!=0
G=S.zeros(5);G[0,0]=1
for i in range(1,4):G[i,i]=S.Rational(1,2);G[i,4]=G[4,i]=S.Rational(1,4)
G[4,4]=S.Rational(3,4);inv=G.inv();assert inv[4,4]==S.Rational(8,3)
N=1<<28;eta=Q(1,786432);bump=Q(1,196608);correction=Q(156,N)
assert correction<eta/2
residual_bound=Q(243,2*N)+Q(9,16)*eta
assert residual_bound<=bump/4
floor=eta-correction;assert floor>0
gap=bump-residual_bound;assert gap>=Q(1,262144)
p=Q(1,2*(N*N+1));assert p*(N*N+1)==Q(1,2)
out={'status':'EXACT_REGULAR_TIMELIKE_TRAP_AND_EXPLICIT_AC_BAD_LABEL','atoms':[list(map(str,z)) for z in pts],'weights':list(map(str,ww)),'phase_atoms_pi_units':[['1/3','1/12'],['1/3','13/12'],['1','1/4'],['1','5/4']],'correct_affine_support_relation':'q=(u+v+w)/2; NOT q=u','covariance':[[str(C[i,j]) for j in range(3)] for i in range(3)],'regression_a':['1/2']*3,'delta':'0','mean':['0']*3,'q_moment':'0','source_gram_inverse':[[str(inv[i,j]) for j in range(5)] for i in range(5)],'Fejer_order':N,'mu_mixture_eta':str(eta),'moment_correction_sup_upper':str(correction),'density_floor_lower':str(floor),'density_upper_bound':N*N+1,'residual_square_upper':str(residual_bound),'global_bump_height':str(bump),'nonlaminate_gap_lower':str(gap),'declared_gap_lower':'1/262144','positive_bad_branch_probability':str(p),'scope':'Explicit bounded strictly positive mu-AC D0 nonlaminate posterior and an admissible bad source label. Original mu is NOT declared nonlaminate; a good policy may avoid this branch.'}
(P/'regular_timelike_trap_and_ac_bad_label_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['atoms','weights','phase_atoms_pi_units','source_gram_inverse','covariance']},indent=2))
