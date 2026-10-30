"""Exact algebraic receipt for the full QC extension theorem.

Rebuild a standalone scalar-Hessian heat certificate at gamma=8/7,
verify closedness and every density coefficient, and receive all constants
in the Hodge/QC extension including a globally QC, non-PC sextic control.
The universal variational argument is in QC_EXTENSION.txt.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('qc_extension_algebra',HERE/'receive.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
b=r.b;add,mul,scale,diff=b.add,b.mul,b.scale,b.diff
def constants(C,c,nu=R(1)):
 C,c,nu=R(C),R(c),R(nu);assert C>0 and c>0 and nu>0
 B2=2*C*C/c+3*C/2;B4=108*C**4/c**3+9*C*C/(4*c)+3*C/2;K4=R(32);Bz=B4*K4**4
 return {'B2':B2,'B4':B4,'Hodge_L4_bound':K4,'QC_mu_sufficient':max(256*B2*B2,1024*Bz*Bz)/nu}
def constructive_family(C,eta,nu=R(1)):
 """For any conic-ROC H, apply to H+eta|S|^4 with its coefficient bound C.

 The output polynomial is globally ROC. It is globally QC whenever H
 is Hessian-QC. The family over all eta characterizes that QC property.
 """
 C,eta,nu=R(C),R(eta),R(nu);assert eta>0
 out=constants(C,eta/4,nu);D=C+2*C*C/(4*eta);out['ROC_mu_sufficient']=C*D/(6*nu);out['mu']=max(out['QC_mu_sufficient'],out['ROC_mu_sufficient']);return out
def main():
 start=time.perf_counter();cert=json.loads((HERE/'dm_heat.json').read_text());powers=cert['quartic_powers'];coef=list(map(R,cert['quartic_coefficients']));H={tuple(pw):v for pw,v in zip(powers,coef) if v};A=[b.var(3,i) for i in range(3)];norm=add(mul(A[0],A[0]),scale(mul(A[1],A[1]),2),mul(A[2],A[2]));det=add(mul(A[0],A[2]),scale(mul(A[1],A[1]),-1));norm4=mul(norm,norm);assert H==add(norm4,scale(mul(norm,det),-R(16,7)))
 qa=cert['quadratic_value_powers'];assert len(qa)==6 and len({tuple(p) for p in qa})==6 and all(sum(p)==2 for p in qa)
 pairs=[tuple(p) for p in cert['two_form_pairs']];assert pairs==list(combinations(range(3),2));oc=list(map(R,cert['closed_two_form_coefficients']));assert len(oc)==18
 omega={pair:{tuple(pw):v for pw,v in zip(qa,oc[6*k:6*k+6]) if v} for k,pair in enumerate(pairs)}
 assert not add(diff(omega[1,2],0),scale(diff(omega[0,2],1),-1),diff(omega[0,1],2))
 W=[[{} for _ in range(3)] for _ in range(3)]
 for (i,j),P in omega.items():W[i][j]=P;W[j][i]=scale(P,-1)
 primitive=[scale(add(*(mul(A[i],W[i][j]) for i in range(3))),R(1,4)) for j in range(3)]
 assert all(add(diff(primitive[j],i),scale(diff(primitive[i],j),-1))==P for (i,j),P in omega.items())
 HH=[[diff(diff(H,i),j) for j in range(3)] for i in range(3)];S=[[{} for _ in range(4)] for _ in range(4)];p1=(0,1,2);p2=(1,2,3)
 for ids in (p1,p2):
  for i,j in product(range(3),repeat=2):S[ids[i]][ids[j]]=add(S[ids[i]][ids[j]],HH[i][j])
 for (i,j),P in omega.items():
  for a,c,sgn in ((p1[i],p2[j],1),(p2[j],p1[i],1),(p1[j],p2[i],-1),(p2[i],p1[j],-1)):S[a][c]=add(S[a][c],scale(P,R(sgn,2)))
 G=[list(map(R,row)) for row in cert['Gram']];margin=R(cert['shifted_PD_margin']);assert len(G)==12 and all(len(row)==12 for row in G) and G==list(map(list,zip(*G)))
 b.pd([[v-(margin if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(G)])
 for a,c in product(range(4),repeat=2):assert S[a][c]==add(*(scale(mul(A[i],A[j]),G[4*i+a][4*j+c]) for i,j in product(range(3),repeat=2)))
 # Exact constants used in the two quantitative norm inequalities.
 b.pd([[R(23,4),R(2)],[R(2),R(3,4)]])
 b.pd([[R(23,24),R(1,3)],[R(1,3),R(1,8)]])
 assert R(3,24**2)>R(1,256) and 25<32
 # H_(11/10) is a positive combination of the just-received QC quartic
 # and a quantitatively convex norm quartic.
 Hgamma=add(norm4,scale(mul(norm,det),-R(11,5)));assert Hgamma==add(scale(H,R(77,80)),scale(norm4,R(3,80)))
 c=R(3,320);C=R(1024);assert c==R(3,80)*R(1,4)
 assert all(pw[1]%2==0 for pw in Hgamma);Lorth=sum(abs(co)/2**(pw[1]//2) for pw,co in Hgamma.items());assert Lorth==R(189,10) and C>=36*Lorth
 got=constants(C,c);mu=R(2**192);assert mu>=got['QC_mu_sufficient']
 # The independent global-ROC constants also hold for this QC control.
 assert R(2**24)>=C+2*C*C/R(3,20) and 6*mu>=C*2**24
 t=R(1,2**110);point=b.evaluate(Hgamma,[t,R(0),t])+mu*(2*t*t)**3;assert point<0
 examples=[];seed=json.loads((HERE/'seeds.json').read_text());eta=R(1,1000)
 for rec in seed['records']:
  # Raw norm-quartic coefficient l1 norm is 16. This is a safe bound
  # for the orthonormal Hessian coordinates as well.
  Cseed=36*(sum(abs(R(v)) for v in rec['quartic_coefficients'])+16*eta);cc=constructive_family(Cseed,eta)
  examples.append({'source':rec['name'],'strictification_eta':str(eta),'polynomial':'[H+eta|S|^4](sym A)+(b-c)^2+mu|A|^6','mu':str(cc['mu']),'global_ROC':True,'global_QC_if_source_Hessian_QC':True,'source_Hessian_QC':'UNKNOWN'})
 result={'standalone_DM_8_7_Hessian_QC_certificate_reconstructed':True,'closed_quadratic_two_form_exact':True,'primitive_differentiated_exactly':True,'all_polynomial_heat_density_coefficients_match':True,'shifted_12_by_12_Gram_PD_margin':str(margin),'universal_Hodge_L4_bound':'32','strong_Hessian_QC_modulus_DM_11_10':'3/320','norm6_uniform_gap_coefficient':'1/256','global_QC_extension_mu_sufficient':str(got['QC_mu_sufficient']),'explicit_control':{'polynomial':'[|S|^4-(11/5)|S|^2 det S](sym A)+(b-c)^2+2^192|A|^6','global_QC':True,'global_ROC':True,'non_polyconvex':True,'negative_point_scalar':str(t),'negative_point_value':str(point),'QC_counterexample':False},'universal_constructive_family_examples':examples,'full_fixed_F_capacity':'NOT_RESOLVED','sharp_QC_boundary':'NOT_RESOLVED','genuine_ROC_QC_separation':'NOT_ACHIEVED','seconds':time.perf_counter()-start,'scope':'Universal quantitative transfer from strong scalar-Hessian QC to global 2x2 QC, and a faithful globally ROC extension family for the whole homogeneous Hessian-ROC quartic cone. The variational proof is in QC_EXTENSION.txt.'}
 (HERE/'qc_extension_replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('universal_constructive_family_examples',)},indent=2))
if __name__=='__main__':main()
