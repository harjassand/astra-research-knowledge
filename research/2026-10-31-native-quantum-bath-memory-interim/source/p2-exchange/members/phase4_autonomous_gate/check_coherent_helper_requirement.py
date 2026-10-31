"""Essential-resource check: helper singlet/triplet coherence between queries.

Full six-spin unitary and all dephasing/final-readout Kraus histories.
No reset occurs in any case. Final acceptance uses helper singlet only.
"""
from functools import reduce
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh, expm

I2=np.eye(2)
ps=[np.array([[0,1],[1,0]])/2,
    np.array([[0,-1j],[1j,0]])/2,np.diag([1,-1])/2]
kron=lambda xs:reduce(np.kron,xs)
def spin(n):
    return [[kron([p if k==j else I2 for k in range(n)]) for p in ps]
            for j in range(n)]
s,sd=spin(6),spin(4)
Jd=[sum(sd[j][a] for j in range(4)) for a in range(3)]
JD2=sum(x@x for x in Jd)
w,q=eigh(JD2)
bases=[q[:,abs(w-j*(j+1))<1e-8] for j in range(3)]
P0,P1,P2=[x@x.conj().T for x in bases]
R=[sum(sd[j][a] for j in [1,2,3]) for a in range(3)]
R2=sum(x@x for x in R)
D=P1@(R2-.75*np.eye(16))/3
singlet=np.array([0,1,-1,0])/np.sqrt(2)
outputs=[singlet,np.array([1,0,0,0]),np.array([0,1,1,0])/np.sqrt(2),np.array([0,0,0,1])]
V=np.kron(np.eye(16),singlet[:,None])
P=V@V.conj().T;Q=np.eye(64)-P;Z=2*P-np.eye(64)
H=sum(sum(s[j][a]@s[4][a] for a in range(3)) for j in [1,2,3])+sum(s[0][a]@s[5][a] for a in range(3))
U=expm(-1j*np.pi*H)
phi=np.arccos(1/3)
phase=lambda theta:np.eye(64)+(np.exp(1j*theta)-1)*P
Rp,Rm=phase(phi),phase(-phi)

def instrument(d1,d2,alpha=phi,beta=-phi):
    """d1,d2 are complete Kraus lists, inserted after first/second query."""
    clean=np.zeros((16,16),complex)
    total=np.zeros((16,16),complex)
    code_triplet=0.
    count=0
    for a in d1:
        for b in d2:
            evolution=U@phase(alpha)@b@U.conj().T@phase(beta)@a@U
            for h,state in enumerate(outputs):
                Vh=np.kron(np.eye(16),state[:,None])
                K=Vh.conj().T@evolution@V
                effect=K.conj().T@K
                total+=effect
                if h==0:clean+=effect
                else:code_triplet+=float(np.linalg.norm(K@bases[0],2)**2)
                count+=1
    wrong=float(eigh((P1+P2)@clean@(P1+P2),eigvals_only=True).max())
    return clean,dict(worst_false_accept=wrong,
                      code_false_erasure=float(1-eigh(bases[0].conj().T@clean@bases[0],eigvals_only=True).min()),
                      completeness_error=float(np.linalg.norm(total-np.eye(16),2)),
                      fine_histories=count,
                      code_triplet_amplitude_squared_bound=code_triplet)

identity=[np.eye(64)]
pinch=[P,Q]
results={"complete_pinching":[],"partial_dephasing":[],"phase_errors":[]}
for name,d1,d2,expected in [
        ("none",identity,identity,0),
        ("after_first_query",pinch,identity,3/8),
        ("after_second_query",identity,pinch,3/8),
        ("after_both_queries",pinch,pinch,7/16)]:
    E,data=instrument(d1,d2)
    data.update(name=name,analytic_false_accept=expected,
                effect_formula_error=float(np.linalg.norm(E-P0-expected*(D+P2),2)))
    assert data["effect_formula_error"]<2e-13
    assert abs(data["worst_false_accept"]-expected)<2e-13
    assert data["completeness_error"]<2e-13
    results["complete_pinching"].append(data)

def dephasing(eta):
    # Multiplies P rho Q and Q rho P by eta; leaves both diagonal blocks intact.
    return [np.sqrt((1+eta)/2)*np.eye(64),np.sqrt((1-eta)/2)*Z]
for eta1,eta2 in [(1.,1.),(0.,1.),(1.,0.),(0.,0.),(.25,.5),(.9,.9),(.99,.99),(.9,1.)]:
    expected=(7-eta1-eta2-5*eta1*eta2)/16
    E,data=instrument(dephasing(eta1),dephasing(eta2))
    data.update(eta1=eta1,eta2=eta2,analytic_false_accept=expected,
                effect_formula_error=float(np.linalg.norm(E-P0-expected*(D+P2),2)))
    assert data["effect_formula_error"]<2e-13
    assert data["completeness_error"]<2e-13
    results["partial_dephasing"].append(data)

for ep,em in [(0.,0.),(.001,0.),(.01,0.),(.1,0.),(.01,.01),(.01,-.01),(.1,-.1)]:
    alpha,beta=phi+ep,-phi+em
    F=3*np.exp(1j*alpha)+3*np.exp(1j*beta)+np.exp(1j*(alpha+beta))-3
    expected=float(abs(F)**2/64)
    quadratic=(ep+em)**2/16+(ep-em)**2/8
    E,data=instrument(identity,identity,alpha,beta)
    data.update(positive_phase_error=ep,negative_phase_error=em,
                analytic_false_accept=expected,leading_quadratic=quadratic,
                effect_formula_error=float(np.linalg.norm(E-P0-expected*(D+P2),2)))
    assert data["effect_formula_error"]<2e-13
    assert data["completeness_error"]<2e-13
    results["phase_errors"].append(data)

out=Path(__file__).with_name("coherent_helper_requirement_results.json")
out.write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps({"file":str(out),"complete_pinching":results["complete_pinching"],
                  "max_effect_error":max(x["effect_formula_error"] for group in results.values() for x in group),
                  "max_instrument_error":max(x["completeness_error"] for group in results.values() for x in group)},indent=2))
