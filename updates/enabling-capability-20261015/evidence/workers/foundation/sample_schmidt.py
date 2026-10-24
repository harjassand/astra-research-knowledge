"""Check a specific proposed grouping lemma on seeded Schmidt spectra.
This is neither a proof nor an estimate of a violation's probability.
"""
import json
from pathlib import Path
import numpy as np
from probe_grouping import cochoi_and_switched


def main():
    rng=np.random.default_rng(2026101502)
    rows=[]
    for d,count in [(2,80),(3,60),(4,30),(5,10)]:
        spectra=[]
        for r in range(1,d+1):
            a=np.zeros(d);a[:r]=1/r;spectra.append(("uniform_rank_"+str(r),a))
        for a in [.001,.01,.05,.1,.25,.5,1.,2.,10.]:
            for j in range(count//9):
                spectra.append(("dirichlet_"+str(a),rng.dirichlet(np.ones(d)*a)))
        for label,p in spectra:
            u=np.diag(np.sqrt(p)).reshape(-1)
            c,s,a=cochoi_and_switched(u,(d,d))
            val,vec=np.linalg.eigh(c)
            invroot=(vec/np.sqrt(val))@vec.conj().T
            ge=np.linalg.eigvalsh(invroot@s@invroot)
            rows.append({"d":d,"label":label,"schmidt_probabilities":p.tolist(),
                         "generalized_min":float(ge[0]),"generalized_max":float(ge[-1])})
        dr=[r for r in rows if r["d"]==d]
        print({"d":d,"count":len(dr),"least":min(r["generalized_min"] for r in dr),
               "greatest":max(r["generalized_max"] for r in dr)})
    out={"status":"FINITE_NUMERICAL_PROBE_ONLY","seed":2026101502,"rows":rows}
    Path(__file__).with_name("schmidt_probe.json").write_text(json.dumps(out,indent=2)+"\n")


if __name__=="__main__":main()
