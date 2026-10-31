"""Small counterexamples for unearned spectral certificates."""
import json
from pathlib import Path
import numpy as np

# A zero residual only certifies some eigenpair.
H=np.diag([-1.,0.])
v=np.array([0.,1.])
rayleigh=float(v@H@v)
residual=float(np.linalg.norm(H@v-rayleigh*v))

# Endpoint samples do not certify a whole lower envelope. Its cell vertex does.
u=np.array([-1.,0.,1.])
learned=-np.abs(u)
true=np.minimum(learned,-.5)

# A fixed hidden operator and norm-bounded, query-dependent errors cancel every
# signal in this deterministic random instance. The operator does not change.
rng=np.random.default_rng(21)
n,q,alpha,eta=1024,100,.05,.01
w=rng.normal(size=n); w/=np.linalg.norm(w)
queries=rng.normal(size=(q,n)); queries/=np.linalg.norm(queries,axis=1)[:,None]
signal_norms=alpha*np.abs(queries@w)
report={
    'wrong_eigenpair':{'rayleigh':rayleigh,'residual':residual,'true_minimum':-1.},
    'sampled_endpoints_miss_cell_vertex':{'controls':u.tolist(),'learned':learned.tolist(),
                                         'true':true.tolist(),'gap':(learned-true).tolist()},
    'rank_one_hiding':{'n':n,'queries':q,'hidden_minimum':-alpha,'noise_bound':eta,
                       'maximum_signal_norm':float(signal_norms.max()),
                       'all_answers_can_equal_zero':bool(np.all(signal_norms<=eta)),
                       'sphere_union_bound_on_revelation':float(2*q*np.exp(-(n-2)*eta**2/(2*alpha**2)))}
}
Path(__file__).with_name('useful_failures.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
