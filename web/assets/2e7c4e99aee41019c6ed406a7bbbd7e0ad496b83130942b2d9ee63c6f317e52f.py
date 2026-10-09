"""Replay the 81 preregistered finite controls; no universal certification."""
from pathlib import Path
import json
import numpy as np

OUT = Path(__file__).parent / "DESIGNED_CONTROLS.json"
P = [np.array([[0, 1], [1, 0]], dtype=complex),
     np.array([[0, -1j], [1j, 0]], dtype=complex),
     np.diag([1, -1]).astype(complex)]

def herm_function(x, fn):
    vals, vec = np.linalg.eigh(x)
    return (vec * fn(vals)) @ vec.conj().T

def quantities(rho, sigma, noise):
    s = np.sqrt(np.diag(sigma)).real
    bsb = noise @ np.diag(s) @ noise
    v = 2 * bsb / (s[:, None] + s[None, :])
    k = (np.sqrt(s)[:, None] * noise) / np.sqrt(s)[None, :]
    c = (np.sqrt(s)[:, None] * v) / np.sqrt(s)[None, :]
    n, vf, kf, cf = [np.kron(np.eye(2), q) for q in (noise, v, k, c)]
    q = herm_function(rho, np.sqrt)
    log_rho = herm_function(rho, np.log)
    log_sigma = np.kron(np.eye(2), np.diag(np.log(np.diag(sigma))))
    drho = (cf @ rho + rho @ cf.conj().T) / 2 - kf @ rho @ kf.conj().T
    j = np.trace(drho @ (log_rho - log_sigma)).real
    e = (np.trace(vf @ rho) - np.trace(n @ q @ n @ q)).real
    tau_log = np.kron(np.diag(np.log([1/3, 2/3])), np.eye(2))
    checks = {
        "trace_annihilation": abs(np.trace(drho)),
        "reference_log_cancellation": abs(np.trace(drho @ tau_log)),
        "stationarity": np.linalg.norm((c @ sigma + sigma @ c.conj().T)/2-k @ sigma @ k.conj().T),
        "Hs_zero": np.linalg.norm((v @ np.diag(s)+np.diag(s) @ v)/2-noise @ np.diag(s) @ noise),
    }
    return float(j), float(e), {key:float(value) for key,value in checks.items()}

rows=[]
for p_label,p in [("1/2",.5),("9/10",.9),("99/100",.99)]:
    sigma=np.diag([p,1-p])
    r=(p/(1-p))**.25
    vp=np.array([r,1])/np.sqrt(r*r+1)
    vm=np.array([r,-1])/np.sqrt(r*r+1)
    for h_label,h in [("0",0.),("3/5",.6),("1",1.)]:
        ap=np.kron([1.,0.],vp)
        am=np.kron([h,np.sqrt(1-h*h)],vm)
        for z_label,z in [("-1/4",-.25),("0",0.),("1/4",.25)]:
            w=(np.outer(ap,ap)+np.outer(am,am))/2+z*(np.outer(ap,am)+np.outer(am,ap))
            w=w/np.trace(w)
            for eps_label,eps in [("1/10",.1),("1/100",.01),("1/1000",.001)]:
                rho=((1-eps)*w+eps*np.eye(4)/4).astype(complex)
                jm=np.zeros((3,3));em=np.zeros((3,3));errors={}
                for i,pi in enumerate(P):
                    j,e,ch=quantities(rho,sigma,pi)
                    jm[i,i]=j;em[i,i]=e
                    for key,value in ch.items():errors[key]=max(errors.get(key,0.),value)
                for i in range(3):
                    for j in range(i+1,3):
                        js,es,ch=quantities(rho,sigma,P[i]+P[j])
                        jm[i,j]=jm[j,i]=(js-jm[i,i]-jm[j,j])/2
                        em[i,j]=em[j,i]=(es-em[i,i]-em[j,j])/2
                        for key,value in ch.items():errors[key]=max(errors.get(key,0.),value)
                fm=jm-np.pi*em
                vals,vec=np.linalg.eigh(fm)
                a=vec[:,0]
                noise=sum(a[i]*P[i] for i in range(3))
                jj,ee,ch=quantities(rho,sigma,noise)
                rows.append({
                    "exact_parameters":{"p":p_label,"h":h_label,"z":z_label,"epsilon":eps_label},
                    "rho_real_float":rho.real.tolist(),
                    "minimum_rho_eigenvalue":float(np.linalg.eigvalsh(rho)[0]),
                    "J_matrix":jm.tolist(),"E_matrix":em.tolist(),
                    "F_pi_eigenvalues":vals.tolist(),"minimum_noise_Pauli_coefficients":a.tolist(),
                    "J_at_minimum_noise":jj,"E_at_minimum_noise":ee,
                    "J_over_E_at_minimum_noise":jj/ee if ee>1e-14 else None,
                    "F_pi_direct_at_minimum_noise":jj-np.pi*ee,
                    "algebra_residuals":errors,
                    "negative_candidate":bool(vals[0]<-1e-8)
                })

assert len(rows)==81
report={
    "status":"finite floating-point diagnostics only; cannot prove universal inequality",
    "input_exact_specification":"DESIGNED_CONTROL_PREREG.txt, faithful algebraic state formula plus exact rational parameters in every row",
    "numpy_version":np.__version__,
    "number_of_states":len(rows),
    "negative_candidates":sum(row["negative_candidate"] for row in rows),
    "minimum_F_pi":min(row["F_pi_eigenvalues"][0] for row in rows),
    "worst_algebra_residual":max(value for row in rows for value in row["algebra_residuals"].values()),
    "rows":rows,
}
OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
print(json.dumps({key:report[key] for key in ["status","numpy_version","number_of_states","negative_candidates","minimum_F_pi","worst_algebra_residual"]},indent=2))
