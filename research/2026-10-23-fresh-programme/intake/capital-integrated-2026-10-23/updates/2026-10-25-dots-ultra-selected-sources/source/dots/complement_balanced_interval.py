"""Finite rational balanced-message simplex witness; exact resource parameters.
Natural logs, interval eigenvalues. No derivative or zero-eigenvalue limit.
"""
from fractions import Fraction as Q
import mpmath as m,json
from pathlib import Path
m.iv.dps=70;iv=m.iv
N=4;eps=Q(7,400);t=Q(21,1000);lam=Q(-1,3);c=lam+(1-lam)/3
a=1-eps+eps/N;b=eps/N;ap=(1-eps)*c+eps/N;k2=3*t*t
assert a*b>k2 and ap*b>lam*lam*k2

def I(x):return iv.mpf(x.numerator)/x.denominator
def chi(a,b,k2):
 a,b,k2=I(a),I(b),I(k2);z=iv.sqrt((a-b)**2+4*k2);lp=(a+b+z)/2;lm=(a+b-z)/2
 return lp*iv.ln(lp)+lm*iv.ln(lm)-a*iv.ln(a)-b*iv.ln(b),lm
ci,ei=chi(a,b,k2);co,eo=chi(ap,b,lam*lam*k2);gap=co-ci/3
eta=iv.sqrt(I(k2/(a*b)));kappa=(1+eta)/(1-eta)
out={'N':N,'epsilon':str(eps),'t':str(t),'lambda':str(lam),'a':str(a),'b':str(b),'a_output':str(ap),'offdiag_squared_input':str(k2),'message_prior':'1/2','exact_reference_marginals_equal':True,'classical_label_uniform_each_message':True,'CMI_input_interval':str(ci),'CMI_output_interval':str(co),'ratio_interval':str(co/ci),'gap_above_classical_and_quantum_MI_one_third':str(gap),'each_hypothesis_min_eigenvalue_lower_interval':str(ei/N),'joint_hypothesis_likelihood_bound_interval':str(kappa),'strict_advantage':bool(gap.a>0),'scope':'finite balanced CMI witness for qubit universal-NOT / four-symbol complement channel; reference dimension8 after Bell encoding; no experimental preparation or capacity claim'}
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
