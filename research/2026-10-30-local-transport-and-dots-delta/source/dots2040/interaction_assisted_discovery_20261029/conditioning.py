import numpy as np, sympy as s,json,math
from scipy.linalg import expm, expm_frechet
from finite_boundary_tests import rowgen,exclusion
rates=s.symbols('a b c d e f');edges={(0,1):1,(1,0):1,**dict(zip([(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)],rates))};Q=rowgen(4,edges);point=dict(zip(rates,[1,2,1,3,2,3]));times=[.1,.2,.5,1,2,4];out=[]
for cap in [1,2]:
 st,L=exclusion(Q,cap=cap,alpha=1);l=np.array(L.subs(point),float);dl=[np.array(L.diff(p),float) for p in rates];a=np.zeros(len(st));a[0]=1;b=np.array([int(0 in z) for z in st]);J=[];means=[]
 for t in times:
  means.append(float(a@expm(l*t)@b));J.append([float(a@expm_frechet(l*t,d*t,compute_expm=False)@b) for d in dl])
 sv=np.linalg.svd(J,compute_uv=False)
 out.append({'cap':cap,'times':times,'probabilities':means,'jacobian_singular_values':sv.tolist(),'condition_number':float(sv[0]/sv[-1])})
r=json.load(open(__file__.replace('conditioning.py','finite_boundary_results.json')))['finite_boundary_occupancy'][-1];gap=abs(r['r_01']-r['equilibrium']);out.append({'saved_pair_fixed_t':r['t'],'gap':gap,'hoeffding_95_percent_sufficient_trials_one_unknown_against_two_known_hypotheses':math.ceil(2*math.log(40)/(gap*gap)),'reset_and_trial_time_not_included':True})
print(json.dumps(out,indent=2))
