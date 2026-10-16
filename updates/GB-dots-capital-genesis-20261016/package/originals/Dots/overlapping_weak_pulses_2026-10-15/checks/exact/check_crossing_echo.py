"""Exact crossing-pulse conditional-character obstruction; installed SymPy only."""
import sympy as sp
I=sp.eye(2); X=sp.Matrix([[0,1],[1,0]]); Z=sp.diag(1,-1)
kron=sp.kronecker_product
H1=kron(X,I,X);H2=kron(I,X,Z);ZA=kron(Z,I,I);ZC=kron(I,Z,I);In=sp.eye(8)
c=sp.Rational(99,101);s=sp.Rational(20,101)
assert H1*H1==In and H2*H2==In and H1*H2==-H2*H1
R1=c*In-sp.I*s*H1;R2=c*In-sp.I*s*H2
Us={}
for r in [1,-1]:
 for t in [1,-1]:
  R1r=c*In-sp.I*r*s*H1;R2t=c*In-sp.I*t*s*H2
  U=R2t.H*R1r.H*R2t*R1r
  fa=In if r==1 else ZA;fc=In if t==1 else ZC
  # Time order: A frame, +H1, C frame, +H2, -H1, A undo, -H2, C undo.
  physical=fc*R2.H*fa*R1.H*R2*fc*R1*fa
  assert U==physical and U.H*U==In
  Us[r,t]=U
Ks={}
for a in [0,1]:
 for b in [0,1]:
  Ks[a,b]=sum((r**a*t**b*Us[r,t] for r in [1,-1] for t in [1,-1]),sp.zeros(8))/4
cos2=c*c-s*s;sin2=2*c*s
expected={(0,0):(c*c+s*s*cos2)*In,
 (0,1):sp.I*c*s*(1-cos2)*H2,
 (1,0):-sp.I*s*s*sin2*H1,
 (1,1):c*s*sin2*H1*H2}
probs={}
for ab in Ks:
 assert Ks[ab]==expected[ab]
 E=Ks[ab].H*Ks[ab];p=E[0,0]
 assert E==p*In
 probs[ab]=p
assert sum(probs.values())==1
pA=probs[1,0]+probs[1,1];pC=probs[0,1]+probs[1,1]
assert probs[1,1]/pA==c*c and probs[1,1]/pC==c*c
# A real Z_A measurement at A completion, and Z_C at C completion,
# give the same joint labels on encoded |00>_AC, for every bath input.
V=sp.zeros(8,2);V[0,0]=1;V[1,1]=1
for a in [0,1]:
 for b in [0,1]:
  PA=(In+(-1)**a*ZA)/2;PC=(In+(-1)**b*ZC)/2
  E=sp.zeros(2)
  for r in [1,-1]:
   for t in [1,-1]:
    Q1=c*In-sp.I*r*s*H1;Q2=c*In-sp.I*t*s*H2
    K=PC*Q2.H*PA*Q1.H*Q2*Q1*V
    E+=K.H*K/4
  assert E==probs[a,b]*sp.eye(2)
# Each pulse's two lobes have total action 2theta. theta<=tan(theta)=s/c.
action_upper=2*s/c;p_upper=action_upper**2
assert c*c>p_upper
print('PASS: physical frames equal signed Hamiltonian evolution; exact Fourier Kraus/completeness; genuine completion-syndrome probabilities.')
for ab,p in probs.items(): print('P',ab,'=',p)
print('P(C_bad | A_bad)=P(A_bad | C_bad)=',c*c)
print('Each integrated nonbath norm is 2theta <=',action_upper,'; its square <=',p_upper)
print('Conditional gap =',sp.factor(c*c-p_upper))
print('Pair probability <= product of the two action-square upper bounds:',probs[1,1]<=p_upper*p_upper)
