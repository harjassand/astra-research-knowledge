"""Check complete energy-transition effect identities with degenerate spectra.

The conditional source Hamiltonians have different eigenbases. These tests
would detect the incorrect replacement of the full frame by one transition,
or the loss of degenerate-eigenspace cross terms.
"""
import json
from pathlib import Path
import numpy as np


def unitary(rng, n):
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    q,r=np.linalg.qr(a)
    return q @ np.diag(np.diag(r)/np.abs(np.diag(r))).conj()


def projectors(energies,u):
    return {int(e):u[:,energies==e]@u[:,energies==e].conj().T
            for e in np.unique(energies)}


def main():
    rng=np.random.default_rng(816031)
    cases=[]
    for n in [3,4,6,8]:
        for repetition in range(12):
            es=rng.integers(-3,4,size=n)
            ed=rng.integers(-3,4,size=n)
            us,ud=unitary(rng,n),unitary(rng,n)
            hs=us@np.diag(es)@us.conj().T
            hd=ud@np.diag(ed)@ud.conj().T
            ps,pd=projectors(es,us),projectors(ed,ud)
            ug=unitary(rng,n)
            vals=rng.uniform(.4,1.6,size=n)
            g=ug@np.diag(vals)@ug.conj().T
            frame={}
            for e1,p1 in pd.items():
                for e0,p0 in ps.items():
                    om=e1-e0
                    frame[om]=frame.get(om,np.zeros_like(g))+p1@g@p0
            x=g.copy(); errors=[]; tails=[]
            for k in range(4):
                lhs=sum(float(om**(2*k))*gg.conj().T@gg for om,gg in frame.items())
                rhs=sum(p@x.conj().T@x@p for p in ps.values())
                relative=float(np.linalg.norm(lhs-rhs,2)/max(1.,np.linalg.norm(rhs,2)))
                assert relative<1e-11
                errors.append(relative)
                if k:
                    threshold=2.5
                    tail=sum((gg.conj().T@gg for om,gg in frame.items() if abs(om)>threshold),np.zeros_like(g))
                    upper=float(np.linalg.norm(x,2)**2/threshold**(2*k))
                    actual=float(np.linalg.eigvalsh(tail).max())
                    assert actual<=upper+1e-10
                    tails.append(dict(moment=k,actual_tail_effect_norm=actual,upper_bound=upper))
                x=hd@x-x@hs
            complete=sum(gg.conj().T@gg for gg in frame.values())
            floor=float(np.linalg.eigvalsh(complete).min())
            assert floor>=float(vals.min()**2)-1e-11
            cases.append(dict(dimension=n,conditional_hamiltonian_commutator=float(np.linalg.norm(hs@hd-hd@hs,2)),
                              source_energies_S=es.tolist(),source_energies_D=ed.tolist(),
                              moment_relative_errors=errors,total_rate_floor=floor,
                              minimum_gain_squared=float(vals.min()**2),tails=tails))
    out=dict(scope="Exact finite energy-frame algebra only; no reservoir Markov or secular approximation is certified.",
             cases=cases,max_moment_relative_error=max(max(c['moment_relative_errors']) for c in cases))
    (Path(__file__).resolve().parent/'local_spectral_frame_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(cases=len(cases),max_moment_relative_error=out['max_moment_relative_error']),indent=2))


if __name__=='__main__':main()
