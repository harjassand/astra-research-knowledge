from pathlib import Path
from fractions import Fraction
import numpy as np,sympy as S,json
base=Path(__file__).parent
z=np.load(base/'full_parametric_simple.npz')
q=z['gram'];n0=int(z['n0']);n=len(q)
pairs=[(i,j) for i in range(n) for j in range(i,n) if (i<n0)==(j<n0)]
M=S.Matrix([[int(round(v)) for v in row] for row in z['mat']])
b=S.Matrix([S.Rational(float(v)).limit_denominator(100000) for v in z['rhs']])
print('affine system',M.shape,flush=True)
aug,piv=M.row_join(b).rref()
if M.cols in piv:raise RuntimeError('inconsistent affine equations')
print('rank',len(piv),'variables',len(pairs),flush=True)
free=[i for i in range(M.cols) if i not in piv]
blocks=[[0,3,4,5,6,9],[1,2,7,8],[n0+i for i in [0,1,4,6,7,8,9,12,13,14]],[n0+i for i in [2,3,5,10,11,15]]]
for den in [16,32,64,128,256,512,1024,2048,4096]:
 v=[S.Rational(round(float(q[i,j])*den),den) for i,j in pairs]
 for k,col in enumerate(piv):v[col]=aug[k,M.cols]-sum(aug[k,j]*v[j] for j in free)
 Q=S.zeros(n)
 for val,(i,j) in zip(v,pairs):Q[i,j]=Q[j,i]=val
 if M*S.Matrix(v)!=b:raise RuntimeError('affine exact residual')
 ev=np.linalg.eigvalsh(np.array(Q).astype(float))
 print('den',den,'min eigenvalue',ev[0],flush=True)
 if ev[0] <= .0001:continue
 pvs=[]
 for inds in blocks:
  B=Q.extract(inds,inds)
  # LDL, avoiding huge determinant calculations.
  L=S.eye(len(inds));D=[]
  for k in range(len(inds)):
   dv=S.factor(B[k,k]-sum(L[k,j]**2*D[j] for j in range(k)))
   if dv<=0:raise RuntimeError('exact LDL positivity failed')
   D.append(dv)
   for i in range(k+1,len(inds)):L[i,k]=S.factor((B[i,k]-sum(L[i,j]*L[k,j]*D[j] for j in range(k)))/dv)
  if L*S.diag(*D)*L.T!=B:raise RuntimeError('LDL identity failed')
  pvs.append([str(dv) for dv in D])
 cover=set(i for inds in blocks for i in inds)
 if cover!=set(range(n)):raise RuntimeError('block cover')
 for i in range(n):
  for j in range(n):
   if not any(i in inds and j in inds for inds in blocks) and Q[i,j]!=0:raise RuntimeError('not block diagonal')
 cert={'status':'exact rational certificate; verifier reconstructs identity and proves all four Gram blocks positive definite','variables':['r','a','b','c','d','s'],'stress':{'sigma1':'-(r+2)*s**2*b+7*r*b**3/(6*(r+2))','sigma2':'(r+2)*s**3+(5*r/2+2)*s**2*a+7*r*s*a**2/4+r*(4*r+3)*a**3/(12*(r+2))'},'subtracted_constant':'(r+2)*(r+3)*s**4/6','subtracted_first_row_tangent':'(r+2)*(2*r+3)*s**3*a/3','identity':'(r+2)*G = z0.T*Q0*z0 + r*z1.T*Q1*z1','z0':z['z0'].tolist(),'z1':z['z1'].tolist(),'block_split':n0,'gram':[[str(Q[i,j]) for j in range(n)] for i in range(n)],'positive_definite_blocks':blocks,'ldl_pivots':pvs,'rounding_denominator':den,'numerical_source_scope':'Only used to select rational coefficients; exact checks establish the certificate.'}
 (base/'ALL_R_STRESS_EXACT_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
 print('EXACT CERTIFICATE SAVED',flush=True)
 break
else:raise RuntimeError('No rational positive definite Gram found')
