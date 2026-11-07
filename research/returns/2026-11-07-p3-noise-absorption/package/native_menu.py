"""Finite supplied-generator menu audit, without full-system enumeration.

Local matrices and affine rate caps are INPUT promises. These routines do not
acquire or implement actuators. scipy.linprog returns binary64 candidates;
the exact finite-bit LP theorem is in the report, and exact small fixtures
are independently checked by rational_certificates.py.
"""
import itertools
import numpy as np
from scipy.optimize import linprog
from noise_absorption import PAULI, kron_all, product_state, reset_super


def local_ptm(superop, s):
    basis = np.stack([kron_all([PAULI[x] for x in word]).reshape(-1,order="F")
                      for word in itertools.product("IXYZ", repeat=s)], axis=1)
    ans = basis.conj().T @ superop @ basis / (2**s)
    if np.max(np.abs(ans.imag)) > 1e-9:
        raise ValueError("Hermiticity preservation failed")
    return ans.real


def sparse_generator(superop, support, tol=1e-12):
    """Tensor basis: identity superoperator plus E_ab except E_00.

    No tensor of dimension 2**n is constructed. An O(16**s) expansion is paid.
    Keys omit identity-superoperator factors, so overlap cancellation is exact
    in the underlying mathematical representation.
    """
    s=len(support)
    ptm=local_ptm(superop,s)
    digits=list(itertools.product(range(4),repeat=s))
    ans={}
    for i,rd in enumerate(digits):
        for j,cd in enumerate(digits):
            value=ptm[i,j]
            if abs(value)<tol: continue
            choices=[]
            for a,b in zip(rd,cd):
                choices.append([(0,1),(5,-1),(10,-1),(15,-1)] if (a,b)==(0,0)
                               else [(4*a+b,1)])
            for prod in itertools.product(*choices):
                key=tuple((site,label) for site,(label,_) in zip(support,prod) if label!=0)
                coeff=value
                for _,sign in prod: coeff*=sign
                ans[key]=ans.get(key,0)+coeff
    return {k:v for k,v in ans.items() if abs(v)>tol}


def sparse_stationarity(superop, support, probabilities, tol=1e-12):
    probs=[probabilities[i] for i in support]
    rho=product_state(probs)
    bases=[[np.diag([1-p,p]), PAULI["X"],PAULI["Y"],PAULI["Z"]] for p in probs]
    labels=list(itertools.product(range(4),repeat=len(support)))
    b=np.stack([kron_all([basis[a] for basis,a in zip(bases,l)]).reshape(-1,order="F")
                for l in labels],axis=1)
    coeff=np.linalg.solve(b,superop @ rho.reshape(-1,order="F"))
    if np.max(abs(coeff.imag))>1e-9: raise ValueError("Non-Hermitian state defect")
    return {tuple((site,a) for site,a in zip(support,l) if a):float(c.real)
            for l,c in zip(labels,coeff) if abs(c)>tol}


def add_sparse(items):
    out={}
    for d in items:
        for k,v in d.items(): out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if abs(v)>1e-12}


def solve_menu(n, probabilities, noise_terms, controls, reset_blocks=None,
               coverage_rate=1., mode="reset"):
    """noise_terms/controls contain support, super; controls also cap,cost,name."""
    conv=(lambda term:sparse_generator(term["super"],term["support"])) if mode=="reset" else (
        lambda term:sparse_stationarity(term["super"],term["support"],probabilities))
    noise=add_sparse([conv(x) for x in noise_terms])
    cols=[conv(x) for x in controls]
    blocks=[]
    if mode=="reset":
        blocks=reset_blocks if reset_blocks is not None else [[i] for i in range(n)]
        for b in blocks:
            om=product_state([probabilities[i] for i in b])
            term={"support":b,"super":reset_super(om)-np.eye(4**len(b))}
            cols.append({k:-v for k,v in conv(term).items()})
    keys=sorted(set(noise).union(*(set(x) for x in cols)))
    aeq=np.array([[col.get(k,0.) for col in cols] for k in keys],float)
    beq=-np.array([noise.get(k,0.) for k in keys])
    if not keys:
        aeq=None;beq=None
    bounds=[(0,x.get("cap",None)) for x in controls]+[(0,None)]*len(blocks)
    obj=[x.get("cost",1.) for x in controls]+[0.]*len(blocks)
    aub=[];bub=[]
    for i in range(n):
        if mode=="reset":
            aub.append([0.]*len(controls)+[-float(i in b) for b in blocks])
            bub.append(-coverage_rate)
    result=linprog(obj,A_ub=np.array(aub) if aub else None,b_ub=np.array(bub) if bub else None,
                   A_eq=aeq,b_eq=beq,bounds=bounds,method="highs")
    record={"mode":mode,"success":bool(result.success),"status":int(result.status),
            "message":result.message,"equation_count":len(keys),"variable_count":len(cols),
            "largest_local_qubits":max([len(x["support"]) for x in noise_terms+controls]+[len(b) for b in blocks]+[0])}
    if result.success:
        record.update(control_rates={x.get("name",str(i)):float(result.x[i]) for i,x in enumerate(controls)},
                      reset_rates=result.x[len(controls):].tolist(),cost=float(result.fun),
                      equality_residual=float(np.max(abs(aeq@result.x-beq))) if keys else 0.)
    return record
