"""Export a separate universal negative-branch certificate; interval is frozen."""
import pickle,json,hashlib
import sympy as s
from pathlib import Path
base=Path(__file__).parent
with open(base/'representation_blocks.pkl','rb') as ff:blocks=pickle.load(ff)
data=blocks['data'];r=data['r'];y=data['y'];D=(r-1)*(r+2)
sub={y[1]:s.Rational(9,2)/D,y[3]:-9*(2*r+1)/D}
C=data['C'];S=data['S'].subs(sub).applyfunc(s.cancel)
vec=data['vec'].subs(sub).applyfunc(s.cancel);W=s.Matrix(6,10,list(vec[78:138]))
V=blocks['V'];B=(V.T*S*V).applyfunc(s.cancel)
sizes=[4,4,2,2];offset=0;ldls=[]
for size in sizes:
    BB=B[offset:offset+size,offset:offset+size]
    LL,DD=BB.LDLdecomposition(hermitian=False)
    LL=LL.applyfunc(s.cancel);pp=[s.factor(vv) for vv in DD.diagonal()]
    ldls.append({'L':LL,'pivots':pp})
    offset+=size
assert B==s.diag(*[B[sum(sizes[:i]):sum(sizes[:i+1]),sum(sizes[:i]):sum(sizes[:i+1])] for i in range(4)])
def pol(vv):
    pp=s.Poly(vv,r)
    return [str(pp.coeff_monomial(r**ii)) for ii in range(pp.degree()+1)] if vv!=0 else ['0']
def rational(vv):
    nn,dd=s.fraction(s.cancel(vv))
    return {'numerator':pol(nn),'denominator':pol(dd)}
def matrix(M):return [[rational(vv) for vv in row] for row in M.tolist()]
out={'schema':'astra.universal_sharp_negative_branch_heat_certificate.v1',
     'status':'exact_rational_certificate_external_review_unresolved',
     'domain':'r < -2',
     'formula':{'alpha':'3*r/(8*(r+2))','beta':'r*(r-1)/6','gamma':'1','delta':'r'},
     'coordinates':['a','b','c','d'],
     'jet_coordinates':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
     'matrix_vectorization':'row_major',
     'Z_order':'(a,b,c,d) kronecker (z0,z1,z2,z3,z4,z5)',
     'two_form_pair_order':[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
     'quadratic_monomial_order':[[0,0],[0,1],[0,2],[0,3],[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]],
     'C':matrix(C),'S':matrix(S),'W':matrix(W),'congruence_basis_V':matrix(V),
     'diffusion':[rational(vec[138]),rational(vec[139])],
     'block_sizes':sizes,'block_LDL':[{'L':matrix(ll['L']),'pivots':[rational(vv) for vv in ll['pivots']]} for ll in ldls],
     'proof_coordinate':'u=-r-2 > 0',
     'positivity_proof':'Every rational pivot has a numerator and denominator with nonnegative coefficients and at least one strictly positive coefficient after substituting r=-2-u and simultaneous sign normalization.',
     'free_parameter_choice':{'y1':'9/(2*(r-1)*(r+2))','y3':'-9*(2*r+1)/((r-1)*(r+2))'},
     'provenance':{'inherited_method':'Bruno and Pasqualotto arXiv:2608.06367v1','all_source_coefficients_free':True,
                   'old_interval_certificate_unchanged':True,'formal_proof_verification':False,'external_review':False,
                   'historical_priority':'UNKNOWN'}}
path=base/'UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(path.name,hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
print('det V',s.factor(V.det()),flush=True)
