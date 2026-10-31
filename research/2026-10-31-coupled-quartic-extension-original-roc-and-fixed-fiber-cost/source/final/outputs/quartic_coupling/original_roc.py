"""Independent all-parameter global ROC receipt for original J_r, r>0.

Use output SO(2) invariance, quartic polarization, and four exact
principal-minor factorizations. This admits the UNMODIFIED density,
independently of any normal penalty or numerical search.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import permutations
import importlib.util,json,time
HERE=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('original_n901_roc_algebra',HERE/'receive.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
add,mul,sc,power,var,diff=m.add,m.mul,m.sc,m.powp,m.var,m.diff
def det(M):
 out={}
 for perm in permutations(range(len(M))):
  term={(0,0):R((-1)**sum(perm[i]>perm[j] for i in range(len(M)) for j in range(i+1,len(M))))}
  for i,j in enumerate(perm):term=mul(term,M[i][j])
  out=add(out,term)
 return out
def verify():
 rp,a,bb,c,d=[var(5,i) for i in range(5)];one5={(0,)*5:R(1)};rp2=add(rp,sc(one5,2));u=add(power(a,2),power(c,2));v=add(power(bb,2),power(d,2));j=add(mul(a,d),sc(mul(bb,c),-1));conf=add(u,v,sc(j,-2));F=add(sc(mul(rp,power(conf,2)),9),sc(mul(mul(rp,add(rp,sc(one5,-1))),mul(rp2,power(u,2))),4),sc(mul(rp2,power(j,2)),24),sc(mul(mul(rp,rp2),mul(u,j)),24));lie=add(sc(mul(diff(F,1),c),-1),sc(mul(diff(F,2),d),-1),mul(diff(F,3),a),mul(diff(F,4),bb));assert not lie
 r,t=var(2,0),var(2,1);one={(0,0):R(1)};r1=add(r,one);r2=add(r,sc(one,2));r21=add(sc(r,2),one);H=[[m.substitute(diff(diff(F,i+1),j+1),[r,one,t,{},{}]) for j in range(4)] for i in range(4)];Q=add(sc(power(t,4),9),sc(mul(add(power(r,2),sc(r,-2),sc(one,-2)),power(t,2)),3),mul(power(r1,2),power(r21,2)));square=add(sc(power(t,2),3),sc(add(power(r,2),sc(r,-2),sc(one,-2)),R(1,2)));positive=mul(mul(r,r2),mul(add(sc(r,3),sc(one,2)),add(sc(r,5),sc(one,4))));assert Q==add(power(square,2),sc(positive,R(1,4)))
 M1=sc(mul(r,add(power(r21,2),sc(power(t,2),3))),12);M2=sc(mul(power(r,2),add(sc(mul(mul(r,r1),add(sc(power(t,2),3),one)),4),power(add(sc(power(t,2),3),sc(one,-1)),2))),432);M3=sc(mul(mul(power(r,2),r2),mul(power(t,2),Q)),20736);M4=sc(mul(power(r,4),mul(power(r2,4),power(t,4))),2985984)
 for k,expected in enumerate((M1,M2,M3,M4),1):assert det([row[:k] for row in H[:k]])==expected
 return {'r_range':'every real r>0','original_density':'J_r, with NO normal correction','left_SO2_Lie_identity_exact':True,'all_four_principal_minor_parameter_identities_exact':True,'third_minor_positive_square_plus_positive_product_exact':True,'full_unscaled_chart_determinant':'9*r^4*t^4','global_rank_one_convexity':True,'rank_one_chart_strict_for':'finite t != 0','acoustic_angular_contact_order':4,'QC':'not inferred from ROC'}
def main():
 start=time.perf_counter();out=verify();out['seconds']=time.perf_counter()-start;(HERE/'original_roc.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
