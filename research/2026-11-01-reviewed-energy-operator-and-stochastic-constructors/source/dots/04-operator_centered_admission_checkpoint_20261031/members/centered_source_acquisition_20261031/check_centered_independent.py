import copy,json
import sympy as S
import acquire_centered_certificate as cc
import receive_centered_schedule as recv
import test_centered_acquisition as t
raw=cc.raw; checks=[]
def ck(n,b):assert b,n;checks.append(n)
s=t.lossy();cert=cc.acquire(s);sch=t.scheduled(s,cert);out=recv.acquire(sch)
def leaves(x,p=()):
    if type(x) is dict:
        for k,v in x.items():yield from leaves(v,p+(k,))
    elif type(x) is list:
        for k,v in enumerate(x):yield from leaves(v,p+(k,))
    elif type(x) is int:yield p,x
for path,v in leaves(out):
    for rep in (bool(v),float(v)):
        z=copy.deepcopy(out);d=z
        for k in path[:-1]:d=d[k]
        d[path[-1]]=rep
        ck('receiver alias '+str(path)+str(type(rep)),not recv.verify_certificate(sch,z))
# Mixed rank-two source charge, full-rank creating coupling: not pure-reference.
m=t.base([4]);lam=10**12;m['requested_gap']=t.q(lam);m['activation_cap']=t.q(0)
L0=S.zeros(4);L0[0,2]=1;L1=S.zeros(4);L1[1,3]=1
X=S.zeros(4);X[0,2]=X[2,0]=X[1,3]=X[3,1]=1
m['couplings']=[t.coupling('full rank creation',0,X)]
m['generator_terms']=[t.term('both losses',[0],S.zeros(4),[(lam,L0),(lam,L1)])]
ms=t.centered(m);mc=cc.acquire(ms)
ck('mixed rank two actual source',mc['status']=='CERTIFIED' and mc['projectors'][0]['transparent_rank']==2 and cc.verify_certificate(ms,mc))
mo=recv.acquire(t.scheduled(ms,mc))
ck('mixed source full schedule',mo['status']=='PASS' and mo['guarded_alternative']['conditional_status']=='NOT_APPLICABLE')
# Paid catalog and external task semantics cannot be replaced by certificate data.
z=copy.deepcopy(ms);z['candidate_budget']['max_subsets_per_cell']=3
bad=copy.deepcopy(mc);bad['external_input_sha256']=raw.digest(z)
ck('no hidden favorable subset',not cc.verify_certificate(z,bad))
z=copy.deepcopy(sch);z['schedule']['task']['amplitude_budget']=[1,10**20]
ck('easier task not substituted',not recv.verify_admitted(z,out))
# Empty-coefficient source is ordinary control-only, despite nontrivial source dynamics.
z=copy.deepcopy(s);z['operator_model']['couplings']=[];zc=cc.acquire(z);zo=recv.acquire(t.scheduled(z,zc))
ck('zero coupling no division',zo['status']=='PASS' and zo['certificate']['eta_upper']==[0,1])
# PBP=0 checked termwise: total PP cancellation is not assumed by acquisition.
z=copy.deepcopy(s);P=S.diag(1,0);z['operator_model']['couplings'][0]['source_matrix']=t.mat(P)
y=copy.deepcopy(z['operator_model']['couplings'][0]);y['id']='opposite';y['source_matrix']=t.mat(-P);z['operator_model']['couplings'].append(y)
ck('termwise centering conservative',cc.acquire(z)['status']=='UNKNOWN')
# Guarded mode is only advertised for an actual annihilating coefficient.
z=copy.deepcopy(s);z['operator_model']['couplings'][0]['source_matrix']=t.mat(S.diag(0,1)+S.Rational(1,10**9)*S.Matrix([[0,1],[1,0]]))
zc=cc.acquire(z);zo=recv.acquire(t.scheduled(z,zc));ck('tiny creation still not guarded',zo['guarded_alternative']['conditional_status']=='NOT_APPLICABLE')
# Exact radius and exponential inequalities in the actual output.
p=out['parameters'];C=raw.rat(p['c']);kap=raw.rat(p['kappa']);tau=raw.rat(p['tau']);g=p['g'];eps=raw.rat(p['epsilon_ctl']);R=raw.rat(out['certificate']['radius'])
allow=lambda r:16*C*r<=kap and 72*r*r*C*C*g*tau<=kap and (eps==0 or 2*r*eps<=1)
ck('actual max dyadic radius',allow(R) and not allow(2*R) and int(R)&(int(R)-1)==0)
x=raw.rat(out['certificate']['exponent']);e=out['certificate']['exponential_power'];E=raw.rat(out['certificate']['exponential_upper'])
ck('exact exponential integer',e==S.ceiling(8*x) and E==S.Rational(8,7)**e)
ck('actual amplitude formula',raw.rat(out['certificate']['eta_upper'])==E/(R-1))
print(json.dumps({'count':len(checks),'checks':checks,'scope':'exact supplied-model tests; no author artifact writes'},indent=2))
