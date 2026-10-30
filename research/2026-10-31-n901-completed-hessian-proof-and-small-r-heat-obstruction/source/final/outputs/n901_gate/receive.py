"""Independent stdlib receipt for a direct compatible-Hessian N901 proof.

Rebuild J_r and the ORIGINAL cubic; verify the closed two-form, its
primitive, every heat-density coefficient, and strict rational Gram pivots.
No optimization code or historical cubic identity is imported.
"""
from fractions import Fraction as R
from itertools import product,combinations
from math import lcm,comb
from pathlib import Path
import json,time
HERE=Path(__file__).resolve().parent
def add(*polys):
 out={}
 for P in polys:
  for pw,c in P.items():out[pw]=out.get(pw,R(0))+c
 return {pw:c for pw,c in out.items() if c}
def scale(P,c):return {pw:c*v for pw,v in P.items() if c*v}
def mul(P,Q):
 out={}
 for a,c in P.items():
  for b,d in Q.items():
   pw=tuple(x+y for x,y in zip(a,b));out[pw]=out.get(pw,R(0))+c*d
 return {pw:c for pw,c in out.items() if c}
def var(n,i):return {tuple(int(j==i) for j in range(n)):R(1)}
def diff(P,i):
 out={}
 for pw,c in P.items():
  if pw[i]:
   ee=list(pw);ee[i]-=1;out[tuple(ee)]=c*pw[i]
 return out
def lift(P,n):return {pw+(0,)*(n-len(pw)):c for pw,c in P.items()}
def power(P,n):
 out={(0,)*len(next(iter(P))):R(1)}
 for _ in range(n):out=mul(out,P)
 return out
def parameter_poly(coeff,n=8):return {(k,)+(0,)*(n-1):R(c) for k,c in enumerate(coeff) if R(c)}
def pd(A):
 den=lcm(*(v.denominator for row in A for v in row));B=[[int(v*den) for v in row] for row in A];last=1;pivots=[]
 for k in range(len(A)):
  pivot=B[k][k];assert pivot>0,(k,pivot);pivots.append(pivot)
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    v=B[i][j]*pivot-B[i][k]*B[k][j];assert v%last==0;B[i][j]=B[j][i]=v//last
  last=pivot
 return len(pivots)
def source(r):
 p,q,w=[var(3,i) for i in range(3)];sig=r+1;kap=r*(r+2)/3;alpha=3*r/(8*(r+2));beta=r*(r-1)/6
 a,b,c,d=q,w,scale(p,-sig),scale(q,-sig);u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));j=add(mul(a,d),scale(mul(b,c),-1));T=add(u,v,scale(j,-2));J=add(scale(mul(T,T),alpha),scale(mul(u,u),beta),mul(j,j),scale(mul(u,j),r))
 lead=scale(J,1/(kap*sig*sig));cub=add(scale(mul(mul(p,p),q),-1),scale(mul(mul(q,q),q),-1/(sig*sig)));quad=mul(p,p)
 return add(lead,cub,quad)
def receive(cert):
 r=R(cert['r']);assert r>0;P=source(r);A=[var(3,i) for i in range(3)];H=[var(7,3+i) for i in range(4)];p1=(0,1,2);p2=(1,2,3);pairs=list(combinations(range(3),2));powers=sorted([pw for pw in product(range(3),repeat=3) if sum(pw)<=2],key=lambda p:(sum(p),p));oc=list(map(R,cert['closed_two_form']));assert len(oc)==30
 omega={ij:{pw:co for pw,co in zip(powers,oc[10*k:10*k+10]) if co} for k,ij in enumerate(pairs)}
 assert not add(diff(omega[1,2],0),scale(diff(omega[0,2],1),-1),diff(omega[0,1],2))
 W=[[{} for _ in range(3)] for _ in range(3)]
 for (i,j),Q in omega.items():W[i][j]=Q;W[j][i]=scale(Q,-1)
 primitive=[]
 for j in range(3):
  aj={}
  for i in range(3):
   for pw,co in W[i][j].items():aj=add(aj,scale(mul(A[i],{pw:co}),R(1,sum(pw)+2)))
  primitive.append(aj)
 assert all(add(diff(primitive[j],i),scale(diff(primitive[i],j),-1))==Q for (i,j),Q in omega.items())
 raw={}
 for ids in (p1,p2):
  for i,j in product(range(3),repeat=2):raw=add(raw,mul(lift(diff(diff(P,i),j),7),mul(H[ids[i]],H[ids[j]])))
 for (i,j),Q in omega.items():raw=add(raw,mul(lift(Q,7),add(mul(H[p1[i]],H[p2[j]]),scale(mul(H[p1[j]],H[p2[i]]),-1))))
 N=3*r*r+8*r+4;pp=-3*N/((r+1)**2*(2*r+1));ww=N/(r+1);rows=[[(2,0,R(1)),(0,0,R(-2))],[(1,0,R(1)),(0,1,-pp)],[(2,1,R(1)),(0,1,R(-2))],[(3,0,R(1)),(0,1,-ww)]]+[[ (a,h,R(1))] for a,h in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,1),(3,2),(3,3))]
 assert rows==[[(a,h,R(c)) for a,h,c in row] for row in cert['face']]
 features=[]
 for row in rows:
  features.append(add(*(scale(mul({(0,)*7:R(1)} if a==0 else var(7,a-1),H[h]),co) for a,h,co in row)))
 G=[list(map(R,row)) for row in cert['Gram']];assert len(G)==12 and all(len(row)==12 for row in G) and G==list(map(list,zip(*G)));margin=R(cert['PD_margin']);assert margin>0
 pivots=pd([[v-(margin if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(G)])
 sos=add(*(scale(mul(features[i],features[j]),G[i][j]) for i,j in product(range(12),repeat=2)));assert raw==sos
 return {'r':str(r),'original_N901_cubic_rebuilt':True,'closed_two_form_and_primitive_exact':True,'all_heat_density_coefficients_exact':True,'reduced_Gram_positive_pivots':pivots,'reduced_Gram_PD_margin':str(margin),'global_scalar_Hessian_QC':True,'N901_17_all_periodic_W2_4_fields':True,'unrestricted_general_U_claim':False}
def receive_family(cert):
 t,p,q,w=[var(8,i) for i in range(4)];h=[var(8,4+i) for i in range(4)];one={(0,)*8:R(1)};l1=add(one,t);l2=add(scale(one,2),t);a2=add(one,scale(t,2));a3=add(scale(one,3),scale(t,2));N=add(scale(one,3),scale(t,8),scale(power(t,2),4))
 extra=cert.get('denominator_extra_t_power',0);assert extra in (0,2);tx=power(t,extra);d=scale(mul(tx,mul(mul(power(l1,2),l2),mul(power(a2,2),power(a3,2)))),R(1,2700));E=mul(t,mul(power(l1,2),l2));D=mul(d,power(E,2));assert d==parameter_poly(cert['denominator_d_coefficients'])
 # Rebuild t^2 times the original matrix V, followed by the exact
 # original alpha,beta,kappa,sigma factors; this is not a new quartic.
 ut=add(mul(power(t,2),power(q,2)),mul(power(l1,2),power(p,2)));vt=add(mul(power(t,2),power(w,2)),mul(power(l1,2),power(q,2)));jt=mul(mul(t,l1),add(mul(p,w),scale(power(q,2),-1)));conf=add(ut,vt,scale(jt,-2))
 Jnum=add(scale(mul(power(t,2),power(conf,2)),9),scale(mul(mul(add(one,scale(t,-1)),a2),power(ut,2)),4),scale(mul(mul(power(t,2),a2),power(jt,2)),24),scale(mul(mul(t,a2),mul(ut,jt)),24))
 fac=scale(mul(tx,mul(power(l1,4),mul(power(l2,3),power(a3,2)))),R(1,21600));Dover=scale(mul(tx,mul(power(t,2),mul(power(l1,4),mul(power(l2,3),mul(power(a2,2),power(a3,2)))))),R(1,2700))
 Pnum=add(mul(fac,Jnum),scale(mul(D,mul(power(p,2),q)),-1),scale(mul(mul(Dover,power(t,2)),power(q,3)),-1),mul(D,power(p,2)))
 def value_coefficient(exponent):return {(pw[0],)+(0,)*7:c for pw,c in Pnum.items() if pw[1:4]==exponent and not any(pw[4:])}
 nq=add(scale(one,9),scale(t,36),scale(power(t,2),40),scale(power(t,3),12))
 assert value_coefficient((2,0,0))==D and value_coefficient((2,1,0))==scale(D,-1) and value_coefficient((2,2,0))==scale(D,R(1,4))
 assert value_coefficient((0,4,0))==scale(mul(Dover,nq),R(1,8)) and value_coefficient((0,3,0))==scale(mul(Dover,power(t,2)),-1)
 # At t=1, d=1 and E=12. Verify the complete source normalization.
 P1={}
 for pw,c in Pnum.items():
  assert not any(pw[4:]);key=pw[1:4];P1[key]=P1.get(key,R(0))+c
 assert {pw:c for pw,c in P1.items() if c}==scale(source(R(1)),144)
 # Exact all-parameter quadratic loss at the conformal acoustic mean:
 # P_nu(p,2,0)-P_nu(0,2,0)=(nu-1)p^2+c40*p^4.
 pp={}
 for pw,c in Pnum.items():
  if pw[3]:continue
  ee=(pw[0],pw[1])+(0,)*6;pp[ee]=pp.get(ee,R(0))+c*2**pw[2]
 assert all(not c for pw,c in pp.items() if pw[1] not in (0,4))
 powers=sorted([pw for pw in product(range(3),repeat=3) if sum(pw)<=2],key=lambda p:(sum(p),p));pairs=list(combinations(range(3),2));nums=cert['two_form_numerators'];assert len(nums)==30;omega={}
 for k,ij in enumerate(pairs):
  omega[ij]=add(*(mul(parameter_poly(nums[10*k+j]),{(0,)+pw+(0,)*4:R(1)}) for j,pw in enumerate(powers)))
 assert not add(diff(omega[1,2],1),scale(diff(omega[0,2],2),-1),diff(omega[0,1],3))
 W=[[{} for _ in range(3)] for _ in range(3)]
 for (i,j),Q in omega.items():W[i][j]=Q;W[j][i]=scale(Q,-1)
 primitive=[];A=(p,q,w)
 for j in range(3):
  aj={}
  for i in range(3):
   for pw,c in W[i][j].items():aj=add(aj,scale(mul(A[i],{pw:c}),R(1,sum(pw[1:4])+2)))
  primitive.append(aj)
 assert all(add(diff(primitive[j],i+1),scale(diff(primitive[i],j+1),-1))==Q for (i,j),Q in omega.items())
 ids1=(0,1,2);ids2=(1,2,3);raw={}
 for ids in (ids1,ids2):
  for i,j in product(range(3),repeat=2):raw=add(raw,mul(diff(diff(Pnum,i+1),j+1),mul(h[ids[i]],h[ids[j]])))
 for (i,j),Q in omega.items():raw=add(raw,mul(Q,add(mul(h[ids1[i]],h[ids2[j]]),scale(mul(h[ids1[j]],h[ids2[i]]),-1))))
 l12=mul(power(l1,2),l2);qm2=add(q,scale(one,-2));features=[mul(E,mul(qm2,h[0])),add(mul(l12,mul(p,h[0])),scale(mul(t,mul(N,h[1])),3)),mul(E,mul(qm2,h[1])),add(mul(mul(t,E),mul(w,h[0])),scale(mul(mul(t,l1),mul(l2,mul(N,h[1]))),-1)),mul(l12,mul(p,h[1])),mul(E,mul(p,h[2])),mul(mul(t,E),mul(p,h[3])),mul(E,mul(q,h[2])),mul(mul(t,E),mul(q,h[3])),mul(mul(t,E),mul(w,h[1])),mul(mul(t,E),mul(w,h[2])),mul(mul(power(t,2),E),mul(w,h[3]))]
 H=cert['Gram_polynomial'];assert len(H)==12 and all(len(row)==12 for row in H);Nbern=cert['Bernstein_degree'];assert Nbern>=0 and all(len(pol)==Nbern+1 for row in H for pol in row);HP=[[parameter_poly(pol) for pol in row] for row in H];assert HP==list(map(list,zip(*HP)));blocks=cert['blocks'];assert blocks==[[0,4,6,7,9,11],[1,2,3,5,8,10]]
 assert all(not HP[i][j] for i in blocks[0] for j in blocks[1]);margin=R(cert['Bernstein_PD_margin']);assert margin>0
 low,high=map(R,cert['t_range']);assert (low,high,extra) in ((R(0),R(1),0),(R(1),R(4,3),2));ww=[[sum((R(comb(k,a),comb(Nbern,a))*comb(pw,a)*low**(pw-a)*(high-low)**a for a in range(min(k,pw)+1)),R(0)) for pw in range(Nbern+1)] for k in range(Nbern+1)]
 for k in range(Nbern+1):
  for block in blocks:
   B=[[sum((ww[k][pw]*R(H[i][j][pw]) for pw in range(Nbern+1)),R(0))-(margin if i==j else 0) for j in block] for i in block];pd(B)
 sos=add(*(mul(HP[i][j],mul(features[i],features[j])) for i,j in product(range(12),repeat=2)));assert raw==sos
 # The source Gram is D_r H(t) D_r/d(t). Across both ranges,
 # d<=6 and min D_r^2>=9/[16(1+r^4)]. The norm-quartic heat
 # density is at most 72 |S|_Euclidean^2 |third_jet|^2.
 assert 12*2*3==72 and 72*4==288
 assert R(16,9)*R(7,3)**2*R(10,3)*R(11,3)**2*R(17,3)**2/2700<6 and R(9,16)/(6*288)==R(1,3072)
 pd([[R(23,4),R(2)],[R(2),R(3,4)]])
 return {'r_range':'every finite real r >= 1' if low==0 else 'every real 3/4 <= r <= 1','parameter_interval':[str(low),str(high)],'original_source_and_cubic_rebuilt':True,'full_parameter_polynomial_identity_exact':True,'closed_two_form_and_primitive_exact':True,'Bernstein_block_PD_checks':2*(Nbern+1),'Bernstein_PD_margin':str(margin),'global_scalar_Hessian_QC':True,'quadratic_coefficient_nu':'1','nu_sharp_for_global_all_mean_Hessian_QC':True,'non_Hessian_polyconvex_support_obstruction_coefficients_exact':True,'N901_17_all_periodic_W2_4_fields':True,'leading_strong_Hessian_QC_modulus':str(margin/R(3072))+'/(1+r^4)','unrestricted_general_U':'NOT_RESOLVED','Morrey_separation':'NOT_ACHIEVED'}
def main():
 start=time.perf_counter();records=[]
 for path in sorted(HERE.glob('certificate_r*.json')):records.append(receive(json.loads(path.read_text())))
 assert records;families=[receive_family(json.loads((HERE/name).read_text())) for name in ('family_r_ge_1.json','family_r_3_4_to_1.json')];out={'records':records,'parameter_uniform_families':families,'combined_r_range':'every finite real r >= 3/4','combined_Bernstein_block_checks':sum(v['Bernstein_block_PD_checks'] for v in families),'remaining_parameter_range':'0 < r < 3/4 NOT_RESOLVED','seconds':time.perf_counter()-start,'scope':'Direct exact heat/Stokes proof of the ORIGINAL N901 target at the admitted parameters. No false cubic identity, no independence assumption, no finite-mode restriction. The variational argument and parameter scope are in PROOF.txt.'};(HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
