"""Pilot fit and count-only held-out contrast certificate, exact rationals.

Use fresh acquisition only: this algorithm and its finite confidence pool
were fixed before residual_counts.json was generated. Coefficients depend
only on the independent pilot. No plant module is imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import numpy as np
def mat(a): return [[F(v) for v in row] for row in a]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def inv(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]
def ab(a): return [[abs(x) for x in row] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def eye(): return mat([[1,0],[0,1]])
def maxrowsum(a): return max(sum(abs(x) for x in row) for row in a)
def minimum(a): return min(x for row in a for x in row)
def serialize(v):
    if isinstance(v,F):return {'rational':str(v),'decimal':float(v)}
    if isinstance(v,dict):return {str(k):serialize(x) for k,x in v.items()}
    if isinstance(v,list):return [serialize(x) for x in v]
    return v

ROOT=Path(__file__).resolve().parent
BETA=F(11); GRID=[F(0),F(1,8),F(1,4),F(3,8),F(1,2),F(3,4),F(1)]
K=2+len(GRID)*16
N_PILOT=100000

def ceil_sqrt(q,denominator=10**12):
    q=F(q); target=q*denominator**2
    ceil_target=(target.numerator+target.denominator-1)//target.denominator
    n=math.isqrt(ceil_target)
    if n*n<ceil_target:n+=1
    result=F(n,denominator);assert result*result>=q
    return result

class Oracle:
    def __init__(self,tables): self.tables={tuple(t['actions']):t for t in tables}
    def event(self,actions,requirements):
        t=self.tables[tuple(actions)]
        return F(sum(c for bits,c in t['counts'].items()
                     if all(int(bits[i])==o for i,o in requirements.items())),t['shots'])
    def H(self):
        return mat([[1,1],[self.event((1,),{0:1}),self.event((0,1),{1:1})]])
    def Hz(self,a,o):
        return mat([[self.event((a,),{0:o}),self.event((0,a),{1:o})],
                    [self.event((a,1),{0:o,1:1}),self.event((0,a,1),{1:o,2:1})]])

def residual_stat(oracle,S,W,a,o,row,col):
    terms={};constant=F(0)
    def add_event(actions,req,coeff):
        key=tuple(actions);table=oracle.tables[key]
        weights=terms.setdefault(key,{bits:F(0) for bits in table['counts']})
        for bits in weights:
            if all(int(bits[i])==z for i,z in req.items()):weights[bits]+=coeff
    SW=mul(S,W)
    for k,prep in enumerate([(),(0,)]):
        coeff=SW[k][col]
        if row==0:constant+=coeff
        else:add_event(prep+(1,),{len(prep):1},coeff)
        req={len(prep):o}
        actions=prep+(a,)
        if row==1:actions+=(1,);req[len(prep)+1]=1
        add_event(actions,req,-S[k][col])
    estimate=constant;variance=F(0)
    for actions,weights in terms.items():
        table=oracle.tables[actions];n=table['shots']
        estimate+=sum(weights[b]*c for b,c in table['counts'].items())/n
        span=max(weights.values())-min(weights.values())
        variance+=span*span/n
    radius=ceil_sqrt((BETA/2)*variance)
    return estimate,radius

def tvbox(p,E):
    l=[max(F(0),x-e) for x,e in zip(p,E)];u=[min(F(1),x+e) for x,e in zip(p,E)]
    assert sum(l)<=1<=sum(u)
    return max(min(sum(x for x,k in zip(u,m) if k),1-sum(x for x,k in zip(l,m) if not k))
               -sum(x for x,k in zip(p,m) if k) for m in product([0,1],repeat=4))

def main():
    data=json.loads((ROOT/'residual_counts.json').read_text())
    rng=np.random.default_rng(320011)
    pilot=[];validation=[]
    for table in data['tables']:
        keys=list(table['counts']);vals=np.array([table['counts'][b] for b in keys])
        first=rng.multivariate_hypergeometric(vals,N_PILOT)
        pilot.append({'actions':table['actions'],'shots':N_PILOT,
                      'counts':{b:int(c) for b,c in zip(keys,first)}})
        validation.append({'actions':table['actions'],'shots':table['shots']-N_PILOT,
                           'counts':{b:int(c) for b,c in zip(keys,vals-first)}})
    (ROOT/'residual_split_counts.json').write_text(json.dumps({'pilot':pilot,'validation':validation},indent=2)+'\n')
    p=Oracle(pilot);v=Oracle(validation);Hp=p.H();Hv=v.H();nval=min(t['shots'] for t in validation)
    dH=mat([[0,0],[ceil_sqrt(BETA/(2*nval))]*2]);results=[]
    for s in GRID:
        S=mat([[1+s,-s],[-s,1+s]])
        What={(a,o):mul(mul(inv(mul(Hp,S)),p.Hz(a,o)),S) for a,o in product(range(2),repeat=2)}
        Vhat=mul(Hv,S);U=inv(Vhat);dV=mul(dH,ab(S));A=mul(ab(U),dV)
        nu=maxrowsum(A)
        if nu>=1:results.append({'s':s,'status':'UNKNOWN_INVERSE'});continue
        M=mul(inv(sub(eye(),A)),ab(U));E={};max_residual=F(0)
        for a,o in What:
            residual=mat([[0,0],[0,0]]);radius=mat([[0,0],[0,0]])
            direct=sub(mul(Vhat,What[a,o]),mul(v.Hz(a,o),S))
            for i,j in product(range(2),repeat=2):
                residual[i][j],radius[i][j]=residual_stat(v,S,What[a,o],a,o,i,j)
                assert residual[i][j]==direct[i][j]
                max_residual=max(max_residual,abs(residual[i][j]))
            E[a,o]=mul(M,add(ab(residual),radius))
        margin=min(minimum(sub(What[z],E[z])) for z in What)
        initial=mul(inv(S),mat([[1],[0]]))
        status='PASS' if margin>=0 and minimum(initial)>=0 else 'UNKNOWN_POSITIVITY'
        record={'s':s,'status':status,'margin':margin,'nu':nu,'max_validation_residual':max_residual}
        if status=='PASS':
            t=F(0)
            for a,j in product(range(2),repeat=2):
                pp=[What[a,o][i][j] for o in range(2) for i in range(2)]
                ee=[E[a,o][i][j] for o in range(2) for i in range(2)]
                assert sum(pp)==1 and min(pp)>=0
                t=max(t,tvbox(pp,ee))
            record.update(local_tv=t,one_macro_tv=3*t/(2+3*t),
                          W={str(z):x for z,x in What.items()},entry_errors={str(z):x for z,x in E.items()})
        results.append(record)
    passing=[r for r in results if r['status']=='PASS']
    best=min(passing,key=lambda r:(r['local_tv'],-r['margin'])) if passing else None
    out={'independent_fresh_dataset':True,'resets':data['resets'],
         'native_interventions':data['native_interventions'],'pilot_per_setting':N_PILOT,
         'validation_per_setting':nval,'event_pool':K,'failure_expression':f'{2*K} exp(-11)',
         'failure_decimal':2*K*math.exp(-11),'candidates':results,'selected':best}
    (ROOT/'residual_certificate.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
    summary={k:out[k] for k in ['resets','native_interventions','event_pool','failure_decimal']}
    summary['selected']=None if best is None else {k:best[k] for k in ['s','margin','local_tv','one_macro_tv']}
    print(json.dumps(serialize(summary),indent=2))
if __name__=='__main__':main()
