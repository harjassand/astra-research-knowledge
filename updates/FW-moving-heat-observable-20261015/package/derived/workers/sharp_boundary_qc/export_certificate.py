"""Export the exact certificate; discovery pickle files are not verifier inputs."""
from pathlib import Path
import pickle,json,hashlib
import sympy as s
base=Path(__file__).parent
with open(base/'symmetric_face.pkl','rb') as ff:face=pickle.load(ff)
with open(base/'interval_choice.pkl','rb') as ff:choice=pickle.load(ff)
r=choice['r'];sub=choice['sub'];C=face['C']
S=choice['S'];vec=face['vec'].subs(sub).applyfunc(s.cancel)
W=s.Matrix(6,10,list(vec[78:138]))
DC=9*(r+1)*(2*r+1);DS=-(r+2)
CN=(DC*C).applyfunc(s.cancel);SN=(DS*S).applyfunc(s.cancel);WN=(DS*W).applyfunc(s.cancel)
def pol(vv):
    pp=s.Poly(vv,r)
    return [str(pp.coeff_monomial(r**ii)) for ii in range(pp.degree()+1)] if vv!=0 else ['0']
def matrix(M):return [[pol(vv) for vv in row] for row in M.tolist()]
out={
 'schema':'astra.sharp_acoustic_heat_certificate.v1',
 'status':'exact_rational_certificate_external_review_unresolved',
 'interval':['-21/8','-5/2'],
 'formula':{'alpha':'3*r/(8*(r+2))','beta':'r*(r-1)/6','gamma':'1','delta':'r'},
 'coordinates':['a','b','c','d'],
 'jet_coordinates':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
 'matrix_vectorization':'row_major',
 'Z_order':'(a,b,c,d) kronecker (z0,z1,z2,z3,z4,z5)',
 'two_form_pair_order':[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 'quadratic_monomial_order':[[0,0],[0,1],[0,2],[0,3],[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]],
 'C_denominator':pol(DC),'S_denominator':pol(DS),'W_denominator':pol(DS),
 'C_numerator':matrix(CN),'S_numerator':matrix(SN),'W_numerator':matrix(WN),
 'diffusion':[pol(vec[138]),pol(vec[139])],
 'bernstein':{'coordinate':'t=8*(r+21/8)','degree':int(choice['degree']),
               'matrices':[[[str(vv) for vv in row] for row in BB.tolist()] for BB in choice['BB']]},
 'free_parameter_choice':{str(yy):str(vv) for yy,vv in sub.items()},
 'provenance':{
   'method':'all free Gram and closed two-form coefficients on the twelve-dimensional forced acoustic-kernel complement; target rotation and paired reflection averaging',
   'full_linear_face_rank':134,'full_linear_face_columns':140,
   'fixed_source_coefficients':0,
   'inherited_heat_method':'Bruno and Pasqualotto, arXiv:2608.06367v1',
   'closest_local_source':'../../sources/astra_compatible_heat_result/RESEARCH_REPORT.md',
   'not_claimed':['general planar Morrey implication','historical novelty','external review','formal proof verification']}}
path=base/'SHARP_ACOUSTIC_HEAT_CERTIFICATE.json'
path.write_text(json.dumps(out,indent=2)+'\n')
print(path.name,hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
