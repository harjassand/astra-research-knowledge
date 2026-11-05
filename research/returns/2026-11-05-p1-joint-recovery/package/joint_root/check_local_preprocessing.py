"""Dense checks of the exact local-Petz-visibility recurrence, not an asymptotic test."""
from pathlib import Path
import json
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "root_analysis"))
from spectrum import swap_matrix

PAULI = [np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex),
         np.diag([1, -1]).astype(complex)]

def depolarize_site(a, site, n, visibility):
    dims = [2] * n
    x = a.reshape(dims + dims)
    traced = np.trace(x, axis1=site, axis2=n + site)
    order = [i for i in range(n) if i != site] + [site]
    # Appending a fresh maximally mixed site then undoing this permutation.
    y = np.kron(traced.reshape(2**(n-1), 2**(n-1)), np.eye(2)/2)
    inv = np.argsort(order).tolist()
    y = y.reshape(dims+dims).transpose(inv + [i+n for i in inv]).reshape(a.shape)
    return visibility * a + (1-visibility) * y

def check(n, theta, lambdas):
    d = 2**n
    u = np.eye(2*d, dtype=complex)
    for j in range(1, n+1):
        p = swap_matrix(n+1, 0, j)
        u = np.cos(theta)*u + 1j*np.sin(theta)*(p@u)
    bath = []
    for pauli in PAULI:
        w = u @ np.kron(pauli, np.eye(d)) @ u.conj().T
        bath.append(np.trace(w.reshape(2,d,2,d), axis1=0, axis2=2)/2)
    noisy = []
    for b in bath:
        for j, v in enumerate(lambdas):
            b = depolarize_site(b, j, n, v)
        noisy.append(b)
    gram = np.array([[np.trace(x.conj().T@y)/d for y in noisy] for x in bath])
    c,s = np.cos(theta), np.sin(theta)
    a,q = 0.,1.
    for v in lambdas:
        a,q = a + v*s**4*q, (c**4 + 2*v*c*c*s*s)*q
    return {"n":n,"theta":theta,"lambdas":lambdas,"predicted_a":float(a),
            "max_gram_error":float(np.max(np.abs(gram-a*np.eye(3))))}

def main():
    out=[]
    for n in range(1,6):
        for theta in [.04,.1,.4,.9,1.4]:
            for lam in [0.,.2,.7,.99,1.]:
                out.append(check(n,theta,[lam]*n))
            out.append(check(n,theta,np.linspace(.13,.91,n).tolist()))
    result={"scope":"finite dense Gram checks, n<=5; no arbitrary shared-memory claim",
            "case_count":len(out),"max_error":max(x["max_gram_error"] for x in out),
            "cases":out}
    Path(__file__).with_name("local_preprocessing_checks.json").write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!="cases"}))

if __name__ == "__main__": main()
