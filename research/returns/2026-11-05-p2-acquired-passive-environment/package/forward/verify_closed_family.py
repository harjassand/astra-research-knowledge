"""Nontrivial bounded-potential example: compare race with direct rejection."""
import math,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad

A,B=1.,3.
RA,RB=2.,1.5
wa=lambda z:RA*(1+math.cos(z))/2
wb=lambda z:RB*(1+math.sin(1.3*z))/2
phi=lambda z:math.exp(-z*z/2)/math.sqrt(2*math.pi)
sa=quad(lambda z:phi(z)*math.exp(-wa(z)),-12,12,epsabs=1e-12)[0]
sb=quad(lambda z:phi(z)*math.exp(-wb(z)),-12,12,epsabs=1e-12)[0]
I=quad(lambda z:phi(z)*math.exp(-max(wa(z),wb(z))),-12,12,epsabs=1e-10,limit=500)[0]
sg=(A*sa+B*sb)/(A+B)
truth=B*sb/(A*sa+B*sb)
assert I<=sg+1e-12
K=20000
rng=np.random.default_rng(9932)
q=B/(A+B)
labels=[]
proposals=0
attempts=0
while len(labels)<K:
    source_a=rng.random()<q
    while True:
        z=float(rng.normal())
        proposals+=1
        W=wa(z) if source_a else wb(z)
        if math.log(rng.random()) < -W:
            break
    logacc=min(0.,wa(z)-wb(z)) if source_a else min(0.,wb(z)-wa(z))
    attempts+=1
    if math.log(rng.random())<logacc:
        labels.append(int(source_a))
result=dict(K=K,s_A=sa,s_B=sb,common_overlap=I,p_B=truth,
            race_expected_gaussian_proposals_per_label=1/I,
            race_observed_gaussian_proposals_per_label=proposals/K,
            race_observed_p_B=float(np.mean(labels)),race_attempts=attempts)
labels=[]
proposals=0
while len(labels)<K:
    is_b=rng.random()<B/(A+B)
    z=float(rng.normal());proposals+=1
    W=wb(z) if is_b else wa(z)
    if math.log(rng.random()) < -W:
        labels.append(int(is_b))
result.update(direct_expected_gaussian_proposals_per_full_configuration=1/sg,
              direct_observed_gaussian_proposals_per_full_configuration=proposals/K,
              direct_observed_p_B=float(np.mean(labels)))
p=Path(__file__).resolve().parent/'closed_family_results.json'
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
