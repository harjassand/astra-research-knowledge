"""Finite diagnostic of the new flagged-dilution identities, not of N675."""
import json
import numpy as np


def blockdiag(*blocks):
    out = np.zeros((sum(x.shape[0] for x in blocks),) * 2, complex)
    off = 0
    for x in blocks:
        out[off:off+x.shape[0], off:off+x.shape[0]] = x
        off += x.shape[0]
    return out


def spectral(a, f):
    e, u = np.linalg.eigh(a)
    assert e.min() > 0
    return (u * f(e)) @ u.conj().T


def ptrace_ref(a, n, d):
    return np.trace(a.reshape(n, d, n, d), axis1=1, axis2=3)


def measure(a, effects, d):
    n = effects[0].shape[0]
    t = a.reshape(n, d, n, d)
    return blockdiag(*(np.einsum('ba,aibj->ij', p, t) for p in effects))


def fisher(a, h):
    e, u = np.linalg.eigh(a)
    assert e.min() > 0
    k = u.conj().T @ h @ u
    return float(np.sum(2 * np.abs(k)**2 / (e[:, None] + e[None, :])).real)


def relent(a, b):
    return float(np.trace(a @ (spectral(a, np.log) - spectral(b, np.log))).real)


def norm1(a):
    return float(np.abs(np.linalg.eigvalsh(a)).sum())


def normop(a):
    return float(np.abs(np.linalg.eigvalsh(a)).max())


def relative_norm(a, product):
    t = spectral(product, lambda x: 1 / np.sqrt(x))
    return normop(t @ (a-product) @ t)


def memory_kraus(rho, n, d):
    root = spectral(rho, np.sqrt)
    return [np.sqrt(d) * root[a*d:(a+1)*d, f*d:(f+1)*d]
            for a in range(n) for f in range(n)]


def memory_apply(kraus, x):
    return sum(k @ x @ k.conj().T for k in kraus)


def check_close(a, b, label):
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    assert error < 2e-11, (label, error)
    return error


def main():
    eye = np.eye(2)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1, -1])
    d = n = 2
    pi = eye/d
    rho = (np.eye(4) + .2*np.kron(x,x) + .1*np.kron(z,z))/4
    tangent = np.kron(x,z)/4
    filler = np.eye(4)/4
    product = np.kron(ptrace_ref(rho,n,d), pi)
    effects_e = [(eye+.6*z)/2, (eye-.6*z)/2]
    effects_f = [(eye+.7*x)/2, (eye-.7*x)/2]
    ar = measure(rho,effects_e,d)
    br = measure(rho,effects_f,d)
    ah = measure(tangent,effects_e,d)
    bh = measure(tangent,effects_f,d)
    gap = fisher(br,bh)-fisher(ar,ah)
    assert gap > 0
    alpha = rho+.1*tangent
    beta = rho
    entropy_gap = relent(measure(alpha,effects_f,d), br)-relent(measure(alpha,effects_e,d), ar)
    assert entropy_gap > 0
    base_k = memory_kraus(rho,n,d)
    filler_k = memory_kraus(filler,n,d)
    test = x+.3*y+.7*z
    check_close(memory_apply(filler_k,test),test,'product means identity')
    records = []
    for s in [.5, .125, 1/1024]:
        rhos = blockdiag(s*rho,(1-s)*filler)
        hs = blockdiag(s*tangent,np.zeros_like(tangent))
        products = np.kron(ptrace_ref(rhos,2*n,d),pi)
        pe = [blockdiag(p,np.zeros((n,n))) for p in effects_e]
        pf = [blockdiag(p,np.zeros((n,n))) for p in effects_f]
        common = blockdiag(np.zeros((n,n)),eye)
        pe.append(common)
        pf.append(common)
        gs = (fisher(measure(rhos,pf,d),measure(hs,pf,d))
              -fisher(measure(rhos,pe,d),measure(hs,pe,d)))
        alphas = blockdiag(s*alpha,(1-s)*filler)
        betas = blockdiag(s*beta,(1-s)*filler)
        es = (relent(measure(alphas,pf,d),measure(betas,pf,d))
              -relent(measure(alphas,pe,d),measure(betas,pe,d)))
        ks = memory_kraus(rhos,2*n,d)
        errors = {
            'fisher_scaling': check_close(gs,s*gap,'Fisher'),
            'entropy_scaling': check_close(es,s*entropy_gap,'entropy'),
            'scaled_operator_norm': check_close(d*normop(rhos-products),s*d*normop(rho-product),'operator'),
            'trace_norm': check_close(norm1(rhos-products),s*norm1(rho-product),'trace'),
            'relative_norm_unchanged': check_close(relative_norm(rhos,products),relative_norm(rho,product),'relative'),
            'lazy_memory': check_close(memory_apply(ks,test),(1-s)*test+s*memory_apply(base_k,test),'memory'),
            'kraus_tp': check_close(sum(k.conj().T@k for k in ks),eye,'TP'),
            'kraus_unital': check_close(sum(k@k.conj().T for k in ks),eye,'unital'),
        }
        records.append({'s':s, 'min_eigenvalue':float(np.linalg.eigvalsh(rhos).min()),
                        'fisher_gap':gs, 'entropy_gap':es, 'max_error':max(errors.values())})
    print(json.dumps({'scope':'finite diagnostic of flagged dilation only',
                      'base_fisher_gap':gap,'base_entropy_gap_nats':entropy_gap,
                      'records':records},indent=2))


if __name__ == '__main__':
    main()
