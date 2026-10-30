"""Exact receipt of conic-ROC quartics and their GLOBAL ROC extensions.

No numeric solver or work/ helper. The complete global extension argument
is analytic in PROOF.txt. Strict Gram margins and every polynomial Gram
identity are reconstructed over Q; an explicit non-PC control is checked.
"""
from pathlib import Path
from fractions import Fraction as R
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('hessian_extension_algebra',HERE.parent/'graded_stabilization/receive.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
b=g.core;add,mul,scale,diff=b.add,b.mul,b.scale,b.diff
def main():
 start=time.perf_counter();cert=json.loads((HERE/'seeds.json').read_text());powers=cert['powers'];assert len(powers)==15 and len({tuple(pw) for pw in powers})==15 and all(sum(pw)==4 for pw in powers)
 x,y=b.var(2,0),b.var(2,1);ray=[mul(x,x),mul(x,y),mul(y,y)];extensions=[]
 for rec in cert['records']:
  coef=list(map(R,rec['quartic_coefficients']));P={tuple(pw):co for pw,co in zip(powers,coef) if co};HH=[[g.substitute(diff(diff(P,i),j),ray) for j in range(3)] for i in range(3)];G=[list(map(R,row)) for row in rec['Gram']];eta=R(rec['strict_Gram_margin']);assert len(G)==9 and all(len(row)==9 for row in G) and G==list(map(list,zip(*G))) and eta>0
  b.pd([[v-(eta if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(G)])
  for k in range(5):
   for i in range(3):
    for j in range(3):assert sum(G[3*a+i][3*c+j] for a in range(3) for c in range(3) if a+c==k)==HH[i][j].get((4-k,k),R(0))
  c=eta/4;assert c==R(rec['strict_conic_ROC_modulus_Frobenius']);C=36*sum(map(abs,coef));D=C+2*C*C/c;nu=R(1);mu=C*D/(6*nu)
  assert mu>0 and 6*mu*nu>=C*D
  extensions.append({'name':rec['name'],'strict_conic_ROC_modulus':str(c),'Hessian_operator_coefficient_bound':str(C),'local_ROC_radius_squared':str(nu/D),'normal_quadratic_coefficient':str(nu),'sixth_degree_coefficient':str(mu),'global_polynomial':'H(sym A)+nu*(b-c)^2+mu*|A|^6','global_ROC':'PROVED_BY_UNIVERSAL_EXTENSION_BOUND','QC':'UNKNOWN'})
 # A fully explicit non-PC positive control for the global extension.
 A=[b.var(3,i) for i in range(3)];norm=add(mul(A[0],A[0]),scale(mul(A[1],A[1]),2),mul(A[2],A[2]));det=add(mul(A[0],A[2]),scale(mul(A[1],A[1]),-1));norm4=mul(norm,norm);H0=add(norm4,scale(mul(norm,det),-R(16,7)));H=add(norm4,scale(mul(norm,det),-R(11,5)))
 assert H==add(scale(H0,R(77,80)),scale(norm4,R(3,80)))
 Hroot=[[b.evaluate(diff(diff(H0,i),j),[R(1),R(0),R(0)]) for j in range(3)] for i in range(3)];b.pd(Hroot)
 rotation=[scale(A[1],2),add(A[2],scale(A[0],-1)),scale(A[1],-2)];assert not add(*(mul(diff(H0,i),rotation[i]) for i in range(3)))
 # Orthonormal coordinates are (a,sqrt(2)b,c); only even powers of b occur.
 assert all(pw[1]%2==0 for pw in H);orthonorm=sum(abs(co)/2**(pw[1]//2) for pw,co in H.items());assert orthonorm==R(189,10)
 C=R(2**10);c=R(3,20);D=R(2**24);mu=R(2**32);nu=R(1);assert C>=36*orthonorm and D>=C+2*C*C/c and 6*mu*nu>=C*D
 t=R(1,2**20);value=b.evaluate(H,[t,R(0),t])+mu*(2*t*t)**3;assert value==-R(59,160)*t**4<0
 control={'quartic_H':'|S|^4-(11/5)*|S|^2*det S','polynomial':'H(sym A)+(b-c)^2+2^32*|A|^6','strict_conic_ROC_modulus':'3/20','Hessian_operator_bound':'1024','local_ROC_radius_squared':str(R(1,2**24)),'global_ROC':True,'non_polyconvex':True,'negative_point':['1/1048576','0','0','1/1048576'],'negative_point_value':str(value),'QC':'NOT_RESOLVED_HERE','is_a_QC_counterexample':False}
 result={'all_three_quartic_Gram_identities_exact':True,'all_three_shifted_9_by_9_Grams_PD':True,'extensions':extensions,'explicit_non_PC_control':control,'actual_ROC_QC_separation':'NOT_ACHIEVED','seconds':time.perf_counter()-start,'scope':'Universal constructive extension from strict scalar-Hessian quartic ROC to global 2x2 ROC degree-six polynomials, with exact admitted examples. No actual negative field has been received.'}
 (HERE/'replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
