"""Periodic linearized cat+buffer drift with imperfect physical CD detunings.

Unlike a generic noisy-X model, a detuning error is gauge-only. We quantify its
gauge excursion, including the delta*n frequency term, to expose the limits of
increasing modulation speed. This does not certify nonlinear bit-flip tails.
"""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

G,gamma,n,nu=1.,10.,8.,.2
alpha=np.sqrt(n)
h=nu*G*G/gamma
g3=h/alpha
F=g3*n
kc=2*G*G/gamma
K=np.ones((3,3))-np.eye(3)
I3=np.eye(3)
labels=list("ABABBABA")
directions={"A":np.array([1.,-1.,0.]),"B":np.array([1.,0.,-1.])}


def drift(deterr,S):
    # Order c(3), c†(3), b(3), b†(3).
    M=np.zeros((12,12),complex)
    M[0:3,0:3]=-1j*np.diag(deterr)
    M[3:6,3:6]=1j*np.diag(deterr)
    M[0:3,3:6]=-1j*h*S*K
    M[3:6,0:3]=1j*h*S*K
    M[0:3,6:9]=-1j*G*I3
    M[3:6,9:12]=1j*G*I3
    M[6:9,0:3]=-1j*G*I3
    M[9:12,3:6]=1j*G*I3
    M[6:9,6:9]=-gamma/2*I3
    M[9:12,9:12]=-gamma/2*I3
    source=np.zeros(12,complex)
    source[:3]=-1j*(F*S+alpha*deterr)
    source[3:6]=1j*(F*S+alpha*deterr)
    aug=np.zeros((13,13),complex)
    aug[:12,:12]=M
    aug[:12,12]=source
    return aug


def run(delta_ratio,eps,balanced,S):
    delta=delta_ratio*kc
    duration=np.pi/delta
    schedule=[(l,1) for l in labels]
    if balanced:
        schedule += [(l,-1) for l in labels[::-1]]
    propagators=[]
    substeps=[]
    V=np.eye(13,dtype=complex)
    for label,sign in schedule:
        M=drift(eps*delta*sign*directions[label],S)
        P=expm(M*duration)
        propagators.append(P)
        substeps.append(expm(M*duration/128))
        V=P@V
    z=np.zeros(13,complex);z[-1]=1
    z[:12]=np.linalg.solve(np.eye(12)-V[:12,:12],V[:12,12])
    radius=float(np.max(abs(np.linalg.eigvals(V[:12,:12]))))
    pops=[]
    beta_pops=[]
    for P in substeps:
        for _ in range(128):
            z=P@z
            pops.append(abs(z[:3])**2)
            beta_pops.append(abs(z[6:9])**2)
    pops=np.array(pops)
    return {"delta_over_confinement":delta_ratio,"fractional_CD_error":eps,
            "time_reversed_balancing":balanced,"parity":S,
            "cycle_duration":duration*len(schedule),"paired_rotations":len(schedule),
            "Floquet_spectral_radius":radius,
            "mean_total_gauge_population":float(np.mean(np.sum(pops,axis=1))),
            "max_single_mode_gauge_population":float(np.max(pops)),
            "max_displacement_fraction_of_cat_alpha":float(np.sqrt(np.max(pops)/n)),
            "mean_total_buffer_population":float(np.mean(np.sum(beta_pops,axis=1)))}


def main():
    out={"parameters":{"G":G,"gamma":gamma,"n":n,"nu":nu,"confinement":kc},
         "scope":"Periodic linearized deterministic mean dynamics; nonlinear tails and stochastic actuator noise are not included.",
         "cases":[]}
    for delta_ratio in (10.,50.,200.):
        for eps in (0.,.001,.01):
            for balanced in (False,True):
                rs=[run(delta_ratio,eps,balanced,S) for S in (-1,1)]
                out["cases"].append(max(rs,key=lambda r:r["max_single_mode_gauge_population"]))
    Path(__file__).with_name("cd_miscalibration_results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":main()
