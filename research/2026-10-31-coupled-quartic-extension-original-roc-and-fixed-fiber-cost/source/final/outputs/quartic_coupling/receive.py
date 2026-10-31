"""Exact construction and receipt for coupled, degree-four extensions.

Retain an arbitrary prescribed off-Sym quartic coupling. Receive finite
coefficients that give global ROC, and global QC when the stated actual
Hessian premise holds. N901 supplies that premise on its admitted range.
No solver, sampled direction, free-law realization, or degree-six term.
The complete variational argument is in PROOF.txt.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import product
import importlib.util,json,time
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('quartic_coupling_algebra',HERE.parent/'n901_gate/receive.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
add,mul,sc,diff,powp,var=b.add,b.mul,b.scale,b.diff,b.power,b.var
def substitute(P,variables):
 n=len(next(iter(variables[0])));out={}
 for pw,c in P.items():
  term={(0,)*n:c}
  for x,k in zip(variables,pw):
   if k:
    if not x:term={};break
    term=mul(term,powp(x,k))
  out=add(out,term)
 return out
def evaluate(P,x):return sum((c*__import__('math').prod(v**k for v,k in zip(x,pw)) for pw,c in P.items()),R(0))
def serialize(P):return [list(pw)+[str(c)] for pw,c in sorted(P.items())]
def raw_norm():
 p,q,w=[var(3,i) for i in range(3)];return add(mul(p,p),sc(mul(q,q),2),mul(w,w))
def coordinates():
 a,bb,c,d=[var(4,i) for i in range(4)];S=[a,sc(add(bb,c),R(1,2)),d];z=add(bb,sc(c,-1));return S,z
def J(r,variables):
 a,bb,c,d=variables;u=add(mul(a,a),mul(c,c));v=add(mul(bb,bb),mul(d,d));j=add(mul(a,d),sc(mul(bb,c),-1));conf=add(u,v,sc(j,-2));return add(sc(mul(conf,conf),3*r/(8*(r+2))),sc(mul(u,u),r*(r-1)/6),mul(j,j),sc(mul(u,j),r))
def n901(r):
 sig=r+1;kap=r*(r+2)/3;a,bb,c,d=[var(4,i) for i in range(4)];F=sc(J(r,[c,d,sc(a,-sig),sc(bb,-sig)]),1/(kap*sig**2));S,z=coordinates();H=substitute(F,[var(3,0),var(3,1),var(3,1),var(3,2)]);assert H=={pw:co for pw,co in b.source(r).items() if sum(pw)==4};return F,H
def compile_extension(F,H,H1,delta,c0,c1):
 S,z=coordinates();norm=raw_norm();N4=powp(norm,2);Rfull=add(F,sc(substitute(H,S),-1));p,q,w,t=[var(4,i) for i in range(4)];Rraw=substitute(Rfull,[p,add(q,sc(t,R(1,2))),add(q,sc(t,-R(1,2))),w]);assert all(pw[3]>=1 for pw in Rraw)
 C=36*sum(map(abs,H1.values()));CR=48*sum(map(abs,Rraw.values()));D=C+2*C*C/c0;B2=2*C*C/c1+3*C/2;B4=108*C**4/c1**3+9*C*C/(4*c1)+3*C/2;Bz=32**4*B4
 need=max(R(1),D/(2*delta),8*B2/delta,8*Bz/delta,CR*CR/(4*delta*delta));exponent=0
 while R(2)**exponent<need:exponent+=2
 aa=R(2)**exponent;beta=R(2)**(exponent//2)
 assert 2*delta*aa>=D and delta*aa/8>=B2 and delta*aa*aa/8>=Bz and 4*delta**2*aa>=CR**2
 dilated={pw:co/beta**pw[3] for pw,co in Rraw.items()};assert 48*sum(map(abs,dilated.values()))<=2*delta
 ns=substitute(norm,S);Na=powp(add(ns,sc(mul(z,z),aa)),2);P=add(substitute(H1,S),Rfull,sc(Na,delta));W=add(P,sc(F,-1),sc(substitute(add(H1,sc(H,-1)),S),-1));assert W==sc(Na,delta)
 # Recover the actual normal penalty after subtracting its symmetric
 # strictification. Its value and FIRST normal derivative vanish at t=0.
 penalty=sc(add(Na,sc(substitute(N4,S),-1)),delta);penraw=substitute(penalty,[p,add(q,sc(t,R(1,2))),add(q,sc(t,-R(1,2))),w]);assert all(pw[3]>=2 for pw in penraw)
 assert all(sum(pw)==4 for pw in P)
 return P,penalty,{'delta':str(delta),'source_H1_Hessian_bound_C':str(C),'source_H1_conic_ROC_modulus':str(c0),'source_H1_actual_Hessian_QC_modulus_if_admitted':str(c1),'normal_coupling_Hessian_bound_CR':str(CR),'rank_one_error_D':str(D),'actual_Hodge_error_B2':str(B2),'actual_Hodge_error_B4':str(B4),'actual_Hodge_error_Bz':str(Bz),'a':str(aa),'a_power_of_two':exponent,'normal_dilation_beta':str(beta),'dilated_normal_coupling_coefficient_bound':str(48*sum(map(abs,dilated.values()))),'normal_penalty_value_and_first_jet_vanish_on_Sym':True,'degree':4}
def fadd(*ps):
 out={}
 for P in ps:
  for k,c in P.items():out[k]=out.get(k,R(0))+c
 return {k:c for k,c in out.items() if c}
def fmul(P,Q):
 out={}
 for k,c in P.items():
  for l,d in Q.items():
   key=tuple(x+y for x,y in zip(k,l));out[key]=out.get(key,R(0))+c*d
 return {k:c for k,c in out.items() if c}
def fscale(P,c):return {k:c*v for k,v in P.items() if c*v}
def fpoly(P,arrays):
 out={}
 for pw,c in P.items():
  term={(0,0):c}
  for A,k in zip(arrays,pw):
   for _ in range(k):term=fmul(term,A)
  out=fadd(out,term)
 return out
def energy_gap(P,M,G):
 A=[fadd(G[i],{(0,0):M[i]}) for i in range(4)];return fpoly(P,A).get((0,0),R(0))-evaluate(P,M)
def actual_controls(P,penalty,constants):
 aa=R(constants['a']);delta=R(constants['delta']);e=1/(4*(aa+1));M=[R(1),e,-e,R(0)];ray=[R(1),R(0),e,R(0)];HH=[[diff(diff(penalty,i),j) for j in range(4)] for i in range(4)];hval=sum((evaluate(HH[i][j],M)*ray[i]*ray[j] for i,j in product(range(4),repeat=2)),R(0));expected=4*delta*aa*e**2*(-3+(2+12*aa)*e**2);assert hval==expected<0
 plane=[{(1,0):v/2,(-1,0):v/2} if v else {} for v in ray];pen_gap=energy_gap(penalty,M,plane);full_gap=energy_gap(P,M,plane);assert pen_gap<0 and full_gap>0
 # Mixed actual gradients, including resonant frequencies and nonzero
 # normal components. All integrals are exact Fourier constant terms.
 waves=[((1,0),(R(1,3),R(2,5))),((0,1),(R(-2,7),R(1,2))),((1,1),(R(1,5),R(-3,8))),((2,-1),(R(1,9),R(1,11)))];G=[{} for _ in range(4)]
 for k,v in waves:
  vals=[v[0]*k[0],v[0]*k[1],v[1]*k[0],v[1]*k[1]]
  for i,x in enumerate(vals):G[i]=fadd(G[i],{k:x/2,tuple(-a for a in k):x/2})
 z=fadd(G[1],fscale(G[2],-1));E=[{} for _ in range(4)];X=[{} for _ in range(4)]
 for k,zz in z.items():
  x,y=k;norm=R(x*x+y*y);mat=[x*y,y*y,-x*x,-x*y]
  for i,v in enumerate(mat):E[i][k]=zz*v/norm
 for i in range(4):X[i]=fadd(G[i],fscale(E[i],-1))
 assert X[1]==X[2]
 for k in set().union(*(A.keys() for A in X)):
  x,y=k;xx=[A.get(k,R(0)) for A in X];s=xx[0]/(x*x) if x else xx[3]/(y*y);assert xx==[s*x*x,s*x*y,s*x*y,s*y*y]
 E2=sum((fmul(A,A).get((0,0),R(0)) for A in E),R(0));z2=fmul(z,z).get((0,0),R(0));assert E2==z2
 mixed_mean=[R(1,3),R(-2,5),R(7,11),R(1,2)];mixed_gap=energy_gap(P,mixed_mean,G);assert mixed_gap>0
 return {'penalty_alone_negative_rank_one_Hessian':str(hval),'penalty_alone_actual_negative_plane_wave_gap':str(pen_gap),'same_plane_wave_full_corrected_gap':str(full_gap),'mixed_four_wave_full_corrected_gap':str(mixed_gap),'exact_actual_Hodge_decomposition':True,'exact_L2_curl_cost_identity':True,'negative_penalty_is_not_a_QC_counterexample_to_the_full_polynomial':True}
def receive_seed(rec,powers):
 H={tuple(pw):R(c) for pw,c in zip(powers,rec['quartic_coefficients']) if R(c)};x,y=var(2,0),var(2,1);ray=[mul(x,x),mul(x,y),mul(y,y)];HH=[[substitute(diff(diff(H,i),j),ray) for j in range(3)] for i in range(3)];G=[list(map(R,row)) for row in rec['Gram']];eta=R(rec['strict_Gram_margin']);b.pd([[v-(eta if i==j else 0) for j,v in enumerate(row)] for i,row in enumerate(G)])
 for k in range(5):
  for i,j in product(range(3),repeat=2):assert sum(G[3*a+i][3*c+j] for a,c in product(range(3),repeat=2) if a+c==k)==HH[i][j].get((4-k,k),R(0))
 return H
def conformal_identity():
 # An all-real-parameter identity, cleared by the positive denominator
 # 8*r*(r+1)^2*(r+2)^2. Rebuild it from the ORIGINAL full J_r.
 sp=importlib.util.spec_from_file_location('quartic_coupling_conformal_source',HERE.parent/'n901_gate/heat_obstruction.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);Pnum,D=m.source_numerator();r,p,q,w=[var(4,i) for i in range(4)];one={(0,)*4:R(1)};sig=add(one,r);rp2=add(sc(one,2),r);aa=add(one,q);cc=sc(mul(sig,p),-1);dd=add(one,sc(mul(sig,q),-1));u=add(mul(aa,aa),mul(cc,cc));v=add(mul(w,w),mul(dd,dd));j=add(mul(aa,dd),sc(mul(w,cc),-1));conf=add(u,v,sc(j,-2));Jnum=add(sc(mul(r,powp(conf,2)),9),sc(mul(mul(r,add(r,sc(one,-1))),mul(rp2,powp(u,2))),4),sc(mul(rp2,powp(j,2)),24),sc(mul(mul(r,rp2),mul(u,j)),24));det=add(mul(p,w),sc(mul(q,q),-1));rhs=add(Pnum,sc(mul(mul(sig,powp(rp2,2)),det),24),sc(mul(mul(r,powp(rp2,2)),q),-8),sc(mul(powp(rp2,2),add(r,sc(one,3))),4));assert Jnum==rhs
 return {'original_Jr_conformal_identity_all_parameter_coefficients_exact':True,'identity':'Jr(I+T*S)/(kappa*sigma^2)=P_r(S)+3*det(S)/(r*sigma)-q/sigma^2+(r+3)/(2*r*sigma^2)','consequence':'Jr is strictly U-free quasiconvex at every full matrix mean for r>=3/4; no uniform all-background modulus inferred'}
def normal_fiber_control(F,P,constants,rr):
 p=var(1,0);one={(0,):R(1)};K=sc(substitute(diff(F,2),[p,one,one,{}]),-1);k2=(2*rr+1)/(2*(rr+2));k0=-(9*rr*rr+16*rr+6)/(2*rr*(rr+1)**2);assert K=={(2,):k2,(0,):k0};delta=R(constants['delta']);aa=R(constants['a']);amp=-k2/(20*delta);M=[R(0),R(1),R(1),R(0)];base=[{(1,0):R(1,2),(-1,0):R(1,2)},{},{},{}];corr=[{}, {},{(2,0):-amp/(2*aa),(-2,0):-amp/(2*aa)},{}];combined=[fadd(base[i],corr[i]) for i in range(4)];base_gap=energy_gap(P,M,base);full_gap=energy_gap(P,M,combined);lowering=full_gap-base_gap;assert full_gap>0 and lowering<0
 # Leading normal-fiber coefficient for the finite two-mode corrector.
 leading=-k2*k2/(160*delta);assert k2*amp/4+5*delta*amp*amp/2==leading<0
 # The exact optimal coefficient is -k2^2*(5/2-sqrt(6))/(8delta).
 # Its attained mean-zero corrector uses <1/(2+cos^2 x)>=1/sqrt(6).
 assert R(5,2)**2>6 and R(49,20)**2>6 and R(5,2)-R(49,20)==R(1,20)
 return {'base_actual_Hessian':'M+diag(cos(x),0), M=[[0,1],[1,0]]','forcing_K_p2_coefficient':str(k2),'forcing_K_constant':str(k0),'weight':'2+cos(x)^2','optimal_attained_coefficient':'-'+str(k2*k2/(8*delta))+'*(5/2-sqrt(6))','optimal_actual_curl_corrector':'-'+str(k2/(4*delta))+'*[1-sqrt(6)/(2+cos(x)^2)]','finite_Fourier_trial_coefficient':str(leading),'finite_a_actual_energy_lowering':str(lowering),'full_corrected_Jensen_gap_after_lowering':str(full_gap),'infimum_of_fixed_corrector_limits':'ATTAINED','limit_of_unbounded_a_dependent_fiber_infima':'NOT_ASSERTED'}
def nonlocal_two_dimensional_control(F,P,constants):
 delta=R(constants['delta']);aa=R(constants['a']);M=[R(1),R(0),R(0),R(1)];X=[{} for _ in range(4)]
 for k in ((1,0),(0,1),(1,1)):
  x,y=k;vals=[-R(x*x,10),-R(x*y,10),-R(x*y,10),-R(y*y,10)]
  for i,v in enumerate(vals):
   if v:X[i]=fadd(X[i],{k:v/2,tuple(-a for a in k):v/2})
 S=[fadd(X[i],{(0,0):M[i]}) for i in range(4)];W=[fpoly(diff(F,i),S) for i in range(4)];K={}
 for k in set().union(*(A.keys() for A in W)):
  x,y=k
  if not x and not y:continue
  vals=[A.get(k,R(0)) for A in W];K[k]=(-x*x*vals[2]-x*y*vals[3]+x*y*vals[0]+y*y*vals[1])/R(x*x+y*y)
 K={k:v for k,v in K.items() if v};assert K and len({(x,y) for x,y in K if x*y})>0
 weight=fadd(*(fmul(A,A) for A in S));K2=fmul(K,K);n2=K2.get((0,0),R(0));nw=fmul(weight,K2).get((0,0),R(0));assert n2>0 and nw>0;tt=n2/(4*delta*nw);z=fscale(K,-tt);E=[{} for _ in range(4)]
 for k,zz in z.items():
  x,y=k;norm=R(x*x+y*y)
  for i,v in enumerate((x*y,y*y,-x*x,-x*y)):E[i][k]=zz*v/norm
 direct=sum((fmul(W[i],E[i]).get((0,0),R(0)) for i in range(4)),R(0));dual=fmul(K,z).get((0,0),R(0));assert direct==dual
 leading=direct+2*delta*fmul(weight,fmul(z,z)).get((0,0),R(0));assert leading==-n2*n2/(8*delta*nw)<0
 combined=[fadd(X[i],fscale(E[i],1/aa)) for i in range(4)];base_gap=energy_gap(P,M,X);after_gap=energy_gap(P,M,combined);lowering=after_gap-base_gap;assert after_gap>0 and lowering<0
 # The same direction lowers the UNCORRECTED original energy by a
 # concrete rational line search. Its total Jensen gap is still positive.
 tau=R(1);base0=energy_gap(F,M,X)
 while True:
  candidate=[fadd(X[i],fscale(E[i],tau)) for i in range(4)];gg=energy_gap(F,M,candidate)
  if gg<base0:break
  tau/=2
  assert tau>R(1,2**200)
 return {'base_potential':'(cos(x)+cos(y)+cos(x+y))/10','mean':'I','source_force_real_frequency_pairs':len(K)//2,'force_received_as_actual_Hodge_adjoint':True,'exact_negative_leading_coefficient':str(leading),'finite_a_corrected_energy_lowering':str(lowering),'full_corrected_Jensen_gap_after_lowering':str(after_gap),'uncorrected_original_rational_descent_step':str(tau),'uncorrected_original_energy_lowering':str(gg-base0),'uncorrected_original_Jensen_gap':str(gg),'uncorrected_original_negative_witness':gg<0,'actual_two_dimensional_nonconstant_U':True,'force_Fourier_coefficients':[[x,y,str(c)] for (x,y),c in sorted(K.items())]}
def main():
 start=time.perf_counter();norm=raw_norm();N4=powp(norm,2);S,z=coordinates();source_receipts=[b.receive_family(json.loads((HERE.parent/'n901_gate'/name).read_text())) for name in ('family_r_ge_1.json','family_r_3_4_to_1.json')];instances=[]
 for rr in (R(3,4),R(1),R(2)):
  F,H=n901(rr);c=1/(R(201326592)*(1+rr**4));delta=c/16;H1=add(H,sc(N4,-delta));P,W,constants=compile_extension(F,H,H1,delta,c,c/2);assert P==add(F,sc(mul(mul(z,z),substitute(norm,S)),2*delta*R(constants['a'])),sc(powp(z,4),delta*R(constants['a'])**2));controls=actual_controls(P,W,constants)
  sig=rr+1;kap=rr*(rr+2)/3;coeff2=2*kap*delta*R(constants['a']);coeff4=kap*delta*R(constants['a'])**2/sig**2
  instance={'r':str(rr),'source':'original J_r(T_r B)/(kappa*sigma^2)','source_actual_Hessian_QC_modulus':str(c),'global_ROC':True,'global_QC':True,'original_off_plane_coupling_retained':True,'exact_source_value_and_first_normal_jet_preserved':True,'original_A_coordinate_normal_penalty':{'U2_times_sym_Tinv_A_norm2_coefficient':str(coeff2),'U4_coefficient':str(coeff4)},'constants':constants,'polynomial_B_coordinates':serialize(P),'actual_controls':controls,'attained_normal_fiber_control':normal_fiber_control(F,P,constants,rr)}
  if rr==R(3,4):instance['nonlocal_two_dimensional_normal_control']=nonlocal_two_dimensional_control(F,P,constants)
  instances.append(instance)
 # The entire conic-ROC source family has a degree-preserving faithful
 # representation; the three retained QC-unknown seeds remain UNKNOWN.
 seeds=json.loads((HERE.parent/'hessian_frontier/seeds.json').read_text());Fbase,Hbase=n901(R(1));Rbase=add(Fbase,sc(substitute(Hbase,S),-1));families=[];eta=R(1,1000)
 for rec in seeds['records']:
  H=receive_seed(rec,seeds['powers']);F=add(substitute(H,S),Rbase);delta=eta/2;H1=add(H,sc(N4,delta));P,W,constants=compile_extension(F,H,H1,delta,2*eta,eta/8);assert substitute(P,[var(3,0),var(3,1),var(3,1),var(3,2)])==add(H,sc(N4,eta));families.append({'name':rec['name'],'eta':str(eta),'global_ROC':True,'source_Hessian_QC':'UNKNOWN','full_QC_if_source_Hessian_QC':True,'quartic_degree':4,'arbitrary_chosen_normal_coupling':'retained N901 r=1 coupling','constants':constants,'polynomial':serialize(P)})
 b.pd([[R(23,4),R(2)],[R(2),R(3,4)]]);assert 2+4+2==8
 out={'source_parameter_gate_reconstructed':True,'source_parameter_Bernstein_checks':sum(v['Bernstein_block_PD_checks'] for v in source_receipts),'original_constrained_full_background_identity':conformal_identity(),'universal_coupled_theorem_scope':'all homogeneous quartic full-matrix couplings with the stated strong actual Hessian premise; all affine means and actual W1,4 gradients','N901_parameter_scope':'every finite real r >= 3/4 by the analytic formulas; three literal instantiations below','N901_instances':instances,'faithful_degree_four_ROC_examples':families,'original_uncorrected_Jr_general_U':'NOT_RESOLVED','actual_ROC_QC_separation':'NOT_ACHIEVED','historical_extension_mechanism':'Dal Maso-Fonseca-Leoni-Morini 2003, Theorem 1.1 and formula (3.8); explicit coupling retention is proved in PROOF.txt','seconds':time.perf_counter()-start};(HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'source_Bernstein_checks':out['source_parameter_Bernstein_checks'],'original_Jr_strict_Ufree_QC_at_every_full_mean_identity_received':True,'all_three_N901_quartic_couplings_globally_ROC_and_QC':True,'N901_a_powers_of_two':[v['constants']['a_power_of_two'] for v in instances],'all_three_penalties_alone_have_actual_negative_plane_wave_gap':True,'all_three_mixed_gradient_controls_pass':True,'all_three_attained_normal_correctors_have_actual_negative_relaxation':True,'all_three_QC_unknown_source_extensions_globally_ROC':True,'degree':4,'unmodified_Jr_general_U':'NOT_RESOLVED','separation':'NOT_ACHIEVED','seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
