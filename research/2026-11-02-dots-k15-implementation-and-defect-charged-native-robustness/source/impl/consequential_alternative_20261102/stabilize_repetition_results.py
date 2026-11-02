import sys,json,numpy as np
sys.path.insert(0,'producer-workspace/consequential_alternative_20261102')
from flagged_repetition import rep_data,evaluate,counts,entropy_deficit_bias,entropy_from_llr
ROOT='producer-workspace/consequential_alternative_20261102'
path=ROOT+'highnoise_jointflags_results.json';a=json.load(open(path))
for rec in a:
 for row in rec['repetition']:row['Ic_XYZ']=[evaluate(rep_data(row['n'],np.array(rec['w']),np.array(rec['pauli']),o)) for o in [1,2,3]]
 rec['evaluation']='Stable entropy-deficit and log-likelihood-ratio formulas; exact count sum evaluated in float64'
json.dump(a,open(path,'w'),indent=2)

def comp(n,rec):
 w=np.array(rec['w']);p=np.array(rec['p']);c,lc=counts(n,len(w));ww=np.exp(lc+c@np.log(w));tt=np.exp(c@np.log(1-2*p));gain=ww@entropy_deficit_bias(tt)
 mass=np.column_stack([w*(1-p),w*p]).ravel();ll=np.column_stack([np.log((1-p)/p),np.log(p/(1-p))]).ravel();c,lc=counts(n,len(mass));ww=np.exp(lc+c@np.log(mass));bit=ww@entropy_from_llr(c@ll)
 return float(gain),float(bit)
path=ROOT+'rectangle_repetition_results.json';a=json.load(open(path))
for rec in a:
 for row in rec['records']:
  gs,bs=comp(row['n'],rec['small']);gl,bl=comp(row['n'],rec['large']);row['Ic_phase_low']=gs-bl;row['Ic_phase_high']=gl-bs
 rec['evaluation']='Stable entropy-deficit and log-likelihood-ratio formulas; exact count sum evaluated in float64'
json.dump(a,open(path,'w'),indent=2)
print('rectangle largest =',max(max(x['Ic_phase_low'],x['Ic_phase_high']) for rec in a for x in rec['records']))
