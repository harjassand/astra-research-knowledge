"""Exact consumer of the strengthened whole-curve radius; reuses root inputs."""
from compile import Q,OUT,zeros,mm,kron,trace,ldl
import json,time
def main():
 start=time.perf_counter();raw=json.loads((OUT/'FIXTURE.json').read_text())
 h,u,v=([list(map(Q,row)) for row in raw[k]] for k in ['H','U','V'])
 r=1;m=Q(1);ell=Q(8,9);eps=m*ell**2/(2**22*r**3);a0=m*ell**2/(2**18*r**3)
 assert eps==a0/16 and eps==Q(1,5308416)
 assert eps+9*r*a0<=m*ell**2/(2**14*r*r)
 fraction=Q(140,9*2**22)+Q(35,192*r);assert fraction<Q(1,2)
 po=zeros(9);eye=zeros(9)
 for i in range(9):eye[i][i]=1
 for i in range(3):
  for j in range(3):po[3*i+i][3*j+j]=1
 assert trace(h)==1 and 1-trace(mm(po,h))/3==ell;ldl(h,Q(1,13))
 x=[[po[i][j]+eps*h[i][j] for j in range(9)] for i in range(9)]
 xu,iv=kron(x,u),kron(eye,v);z=[[xu[i][j]+iv[i][j] for j in range(18)] for i in range(18)]
 pivot=ldl(z);whole=trace(z);assert whole==12+eps
 red=[[sum((z[(3*i+b)*2+t][(3*j+b)*2+t] for b in range(3) for t in range(2)),Q(0)) for j in range(3)] for i in range(3)]
 assert red==[[whole/3 if i==j else Q(0) for j in range(3)] for i in range(3)]
 assert [[z[2*i+1][2*j+1] for j in range(9)] for i in range(9)]==[[t/2 for t in row] for row in x]
 off=[[z[b][6+c] for c in range(6)] for b in range(6)];assert any(t for row in mm(off,off) for t in row)
 # Exact exclusions from ordinary condition24 and low-Schmidt families.
 condition_lower=27/eps+1;assert condition_lower>24
 fidelity=(3+eps/9)/(3+eps);assert fidelity>Q(2,3)
 rawmargin=eps*ell/4+Q(1,3150);cmi=rawmargin/whole
 out={'status':'EXACT_KAPPA_FREE_ENTIRE_CURVE_AND_BATH_ADMITTED','epsilon':str(eps),'a0':str(a0),'large_noise_charge_fraction_bound':str(fraction),'source_trace':str(whole),'raw_Delta_lower':str(rawmargin),'CMI_excess_lower':str(cmi),'CMI_display':float(cmi),'Z_LDL_pivot':str(pivot),'ordinary_condition_number_lower':str(condition_lower),'singlet_fidelity_of_filtered_source':str(fidelity),'low_Schmidt_family_excluded':True,'old_reset_square_zero_excluded':True,'reduction_region_excluded':True,'input_upper_C_bound_required':False,'seconds':time.perf_counter()-start,'scope':'Whole-curve theorem plus inherited common-bath identity. Exact synthetic matrices, not a physical instrument or global classification of every positive source family.'}
 (OUT/'KAPPA_FREE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
 (OUT/'KAPPA_FREE_FIXTURE.json').write_text(json.dumps({'epsilon':str(eps),'Z':[[str(t) for t in row] for row in z]},indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','epsilon','CMI_excess_lower','CMI_display','seconds']},indent=2))
if __name__=='__main__':main()
