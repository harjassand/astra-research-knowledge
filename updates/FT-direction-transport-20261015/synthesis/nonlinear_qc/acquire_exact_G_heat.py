"""Rational acquisition on a discovered G heat Gram face.

Rounded numerical entries choose only free variables in an exactly solved
linear system. Acceptance requires exact polynomial identity, closedness,
positive diffusion and exact positive LDL pivots on the reduced Gram.
"""
from pathlib import Path
import runpy,json,time
import numpy as np
import sympy as S

ROOT=Path(__file__).resolve().parent
tick=time.monotonic()
# Rebuild the exact algebra; the exploratory search is rerun only as a helper
# to expose its coefficient definitions, not as a theorem premise.
import sys
sys.argv=[str(ROOT/'search_complex_diffusion.py'),'0.0001','face_stage1.json']
ns=runpy.run_path(str(ROOT/'search_complex_diffusion.py'))
B=ns['Brat'];N=ns['N'];O=ns['O'];C=ns['C'];coeff=ns['coeff']
zred=B.T*ns['bmon']
n=B.cols
ij=[(i,j) for i in range(n) for j in range(i,n)]
P=S.Matrix.hstack(*[coeff(zred[i]*zred[j])*(1 if i==j else 2) for i,j in ij])
closed_map=O*N
H11,H12,H22=[coeff(t) for t in ns['heat']]
# Anisotropic real heat is enough for the numerical candidate. Impose zero
# rotating diffusion and zero off-diagonal real diffusion exactly.
T=P.row_join(-closed_map).row_join(-(H11-H22))
rhs=2*H22
rref,pivots=T.row_join(rhs).rref()
assert all(i<T.cols for i in pivots)
free=[j for j in range(T.cols) if j not in pivots]
print('exact affine rank',len(pivots),'free',len(free),'reduced rank',n,flush=True)
candidate=np.load(ROOT/'complex_diffusion_candidate_face_stage1_margin_0.0001.npz')
Bf=np.array(B,float)
left=np.linalg.solve(Bf.T@Bf,Bf.T)
Sf=left@candidate['gram']@left.T
eta=np.linalg.lstsq(np.array(N,float),candidate['closed_form_coeff'],rcond=1e-11)[0]
floating=np.r_[[Sf[i,j] for i,j in ij],eta,candidate['diffusion'][0,0]]

for denominator in (10000,100000,1000000,10000000):
    values=S.zeros(T.cols,1)
    for j in free:
        values[j]=S.Rational(round(float(floating[j])*denominator),denominator)
    for i,j in enumerate(pivots):
        values[j]=rref[i,-1]-sum(rref[i,k]*values[k] for k in free)
    assert T*values==rhs
    reduced=S.zeros(n)
    for k,(i,j) in enumerate(ij):
        reduced[i,j]=reduced[j,i]=values[k]
    d1=values[-1];d2=2-d1
    if d1<=0 or d2<=0:
        continue
    L,D=reduced.LDLdecomposition(hermitian=False)
    diag=list(D.diagonal())
    if not all(d>0 for d in diag):
        print('rounding',denominator,'positive pivots',sum(d>0 for d in diag),'of',len(diag),flush=True)
        continue
    assert L*D*L.T==reduced
    omega=N*values[len(ij):len(ij)+N.cols,0]
    gram=B*reduced*B.T
    assert O*omega==P*values[:len(ij),0]-d1*H11-d2*H22
    assert C*omega==S.zeros(16,1)
    cert={'schema':'astra-G-closed-anisotropic-heat/1',
       'status':'EXACT_ALGEBRA_PASS',
       'integrand':'G=3(u+v-2j)^2+(35/24)u^2+j^2-(5/2)ju',
       'matrix_entry_order':['a','b','c','d'],
       'jet_order':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
       'bilinear_order':'A_i jet_j, A index outer, jet index inner',
       'omega_pair_order':ns['formpairs'],'quadratic_coefficient_order':ns['xpairs'],
       'diffusion':[[str(d1),'0'],['0',str(d2)]],
       'identity':'Z^T (basis reduced_gram basis^T) Z = d1 D2G(A)[B1,B1] + d2 D2G(A)[B2,B2] + omega_A(B1,B2)',
       'basis':[[str(t) for t in row] for row in B.tolist()],
       'reduced_gram':[[str(t) for t in row] for row in reduced.tolist()],
       'gram':[[str(t) for t in row] for row in gram.tolist()],
       'omega_coefficients':[[str(t) for t in omega[10*i:10*i+10,0]] for i in range(6)],
       'ldl_diagonal':[str(t) for t in diag],
       'rounding_denominator_for_free_variables':denominator,
       'source_boundary':'numerical acquisition is dispensable; verify the complete rational certificate independently',
       'analytic_implication':'requires the separately written global anisotropic heat proof',
       'historical_novelty':'UNKNOWN','external_review':'UNKNOWN'}
    (ROOT/'G_EXACT_HEAT_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'status':'EXACT_PASS','diffusion':[str(d1),str(d2)],
       'reduced_gram_dimension':n,'positive_pivots':len(diag),'denominator':denominator,
       'seconds':time.monotonic()-tick},indent=2),flush=True)
    break
else:
    raise ArithmeticError('No rational positive certificate acquired from bounded exact reconstruction.')
