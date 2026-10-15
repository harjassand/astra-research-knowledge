"""Export the symbolic discovery result as portable rational coefficient data."""
from pathlib import Path
import json, pickle, hashlib
import sympy as s
from reconstruct import D1,D2
root=Path(__file__).parent
with (root/'moving_family.pkl').open('rb') as f: data=pickle.load(f)
r=data['r']
CN=((r+1)*data['C']).applyfunc(s.cancel)
SN=(-(r+1)*data['S']).applyfunc(s.cancel)
WN=(-(r+1)*data['W']).applyfunc(s.cancel)
def encode_poly_matrix(M):
    deg=max(s.Poly(q,r).degree() for q in M if q!=0)
    return [[[str(s.Poly(M[i,j],r).nth(k)) for j in range(M.cols)] for i in range(M.rows)] for k in range(deg+1)]
obj={
 'schema':'astra-moving-acoustic-heat/v1',
 'date':'2026-10-15',
 'status':'EXACT_CERTIFICATE; external review and historical novelty unresolved',
 'parameter':'r', 'interval':['-21/8','-5/2'],
 'diffusion':['4897/5000','5103/5000'],
 'scalar_subtraction_epsilon':'1/2000',
 'rotationally_averaged_kappa':'3/16000',
 'integrand':'3*((a-d)^2+(b+c)^2)^2 + r*(r-1)/6*(a^2+c^2)^2 + (ad-bc)^2 + r*(a^2+c^2)*(ad-bc)',
 'matrix_entry_order':['a','b','c','d'],
 'jet_order':['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy'],
 'bilinear_order':'A_i z_j, A index outer, jet index inner',
 'omega_pair_order':[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 'omega_monomial_order':[[0,0],[0,1],[0,2],[0,3],[1,1],[1,2],[1,3],[2,2],[2,3],[3,3]],
 'encoding':'Arrays indexed [power_of_r][row][column], exact rational strings.',
 'reconstruction':{'C_r':'C_numerator(r)/(r+1)','S_r':'S_numerator(r)/(-(r+1))','omega_coefficients':'omega_numerator(r)/(-(r+1))'},
 'C_numerator':encode_poly_matrix(CN),
 'S_numerator':encode_poly_matrix(SN),
 'omega_numerator':encode_poly_matrix(WN),
 'provenance':{
  'source_repository':'https://github.com/harjassand/astra-research-knowledge',
  'repository_head_observed':'a6190a1083f688a7e4bf64adbc5244ef150ff2c4',
  'N850_certificate_path':'updates/FT-direction-transport-20261015/synthesis/nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json',
  'source_claimed_sha256':'4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000',
  'byte_verification':'Original coefficients were transcribed from retrieved source ranges, then the universal algebra was independently reconstructed. Original source byte hash was not reverified.',
  'new_construction':'Move the six-dimensional acoustic kernel; continue the rational certificate while fixing 48 free coefficients at the source values. Standalone verification does not rely on this construction procedure.'
 }
}
p=root/'MOVING_ACOUSTIC_CERTIFICATE.json'
p.write_text(json.dumps(obj,indent=2)+'\n')
print(p, p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
