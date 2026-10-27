"""Reciprocal finite-energy broadcast programming construction.

Continuous coordinates x_i in [-1,1], with hard stops and concave quadratic barriers:
E=sum c_i(1-x_i^2)/2-H sum g_i x_i-sum_(i<j) J_ij x_i x_j-sum b_i x_i.
Every J is symmetric. Endpoint relay events are exact in this energy model.
No arbitrary directed transition graph, local input, or per-stage clock is used.

All computations use exact rational arithmetic. Physical fabrication and finite
temperature reliability are separate unanswered interfaces.
"""
from fractions import Fraction as F
from dataclasses import dataclass


@dataclass
class Network:
    N:int
    names:list
    c:list
    g:list
    b:list
    J:list
    q:list
    z:list
    m:list

    def local(self,state,H):
        return [self.g[i]*H+self.b[i]+sum(w*state[j] for j,w in self.J[i].items())
                for i in range(len(self.names))]

    def margins(self,state,H):
        f=self.local(state,H)
        return [self.c[i]+state[i]*f[i] for i in range(len(state))]

    def energy(self,state,H):
        return -sum((self.g[i]*H+self.b[i])*state[i] for i in range(len(state)))-sum(
            w*state[i]*state[j] for i in range(len(state)) for j,w in self.J[i].items() if j>i)

    def moment(self,state):
        return sum(gg*ss for gg,ss in zip(self.g,state))


def build(N):
    L=2*N+1
    names=[f'q{i+1}' for i in range(L)]+[f'z{i+1}' for i in range(L)]+[f'm{i+1}' for i in range(N)]
    q=list(range(L));z=list(range(L,2*L));m=list(range(2*L,2*L+N))
    c=[F(10)]*L+[F(40)]*L+[F(13)]*N
    g=[F(1)]*L+[F(2)]*L+[F(1)]*N
    b=[F(0)]*len(names)
    b[q[0]]=-10 # fixed left track endpoint +1, reciprocal AF coupling -10.
    b[q[-1]]=10 # fixed right track endpoint -1.
    J=[{} for _ in names]
    def edge(i,j,w):
        J[i][j]=F(w);J[j][i]=F(w)
    for i in range(L-1):edge(q[i],q[i+1],-10)
    for i in range(L):edge(q[i],z[i],-4 if i%2==0 else 4)
    for i in range(N):
        edge(m[i],q[2*i+1],1)
        edge(m[i],q[2*i+2],1)
    return Network(N,names,c,g,b,J,q,z,m)


def settle(net,state,H,record=None,order='lowest'):
    """Relax at fixed H. Endpoint energy strictly decreases for every flip."""
    state=list(state)
    for _ in range(100*len(state)+1):
        margins=net.margins(state,H)
        bad=[i for i,x in enumerate(margins) if x<0]
        if not bad:return state
        i=bad[-1] if order=='highest' else min(bad,key=lambda j:margins[j]) if order=='steepest' else bad[0]
        before=net.energy(state,H);old=state[i];state[i]=-old
        drop=before-net.energy(state,H)
        if drop<=0:raise AssertionError('energy failed to decrease')
        if record is not None:record.append(dict(kind='flip',name=net.names[i],index=i,H=H,old=old,new=state[i],dissipation=drop))
    raise RuntimeError('excess events')


def ramp(net,state,H0,H1,record=None,order='lowest'):
    """Quasistatic monotone ramp with exact switching fields.

    A tiny rational overshoot resolves marginal events, far below all margins.
    It is retained in the work receipt. No pulse timing sets the state.
    """
    state=list(state);H0=F(H0);H1=F(H1)
    direction=1 if H1>H0 else -1
    h=H0;epsilon=F(1,10**9)
    for _ in range(100*len(state)+1):
        unstable=[i for i,x in enumerate(net.margins(state,h)) if x<0]
        if unstable:state=settle(net,state,h,record,order)
        fi=net.local(state,F(0))
        candidates=[]
        for i,si in enumerate(state):
            if si==-direction:
                threshold=(direction*net.c[i]-fi[i])/net.g[i]
                if direction*(threshold-h)>=0 and direction*(H1-threshold)>0:
                    candidates.append(threshold)
        if not candidates:
            if record is not None:record.append(dict(kind='field',H0=h,H1=H1,work=-net.moment(state)*(H1-h)))
            return settle(net,state,H1,record,order)
        critical=min(candidates) if direction>0 else max(candidates)
        hnew=critical+direction*epsilon
        if direction*(H1-hnew)<0:hnew=H1
        if record is not None:record.append(dict(kind='field',H0=h,H1=hnew,work=-net.moment(state)*(hnew-h)))
        h=hnew
        state=settle(net,state,h,record,order)
    raise RuntimeError('excess ramp events')


def protocol(bits):
    # Extra fixed levels expose preparation rather than hide it in a large ramp.
    seq=[('reset',-64),('prepare',-10),('align',8),('temporary_set',15),('arm',24),('nucleate',-10),('erase',-16)]
    for i,bit in enumerate(bits):
        seq.append((f'position_{i+1}',10))
        if bit:seq.append((f'write_{i+1}',12))
        seq.append((f'advance_{i+1}',-10))
    seq.append(('hold',0))
    return seq


def run(bits,initial=None,order='lowest'):
    net=build(len(bits));state=list(initial) if initial is not None else [-1]*len(net.names)
    H=F(0);events=[];phases=[]
    initial_energy=net.energy(state,H)
    for phase,value in protocol(bits):
        start=len(events)
        state=ramp(net,state,H,F(value),events,order)
        H=F(value)
        phases.append(dict(name=phase,H=H,state=list(state),minimum_endpoint_margin=min(net.margins(state,H)),
                           flipped=[e['name'] for e in events[start:] if e['kind']=='flip']))
    output=[(state[i]+1)//2 for i in net.m]
    work=sum(e['work'] for e in events if e['kind']=='field')
    diss=sum(e['dissipation'] for e in events if e['kind']=='flip')
    final_energy=net.energy(state,H)
    assert work==diss+final_energy-initial_energy
    return dict(net=net,output=output,state=state,phases=phases,events=events,
                work=work,dissipation=diss,gross_positive_work=sum(max(F(0),e['work']) for e in events if e['kind']=='field'),
                energy_change=final_energy-initial_energy,correct=output==list(bits))


def serializable(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serializable(v) for k,v in value.items() if k!='net'}
    if isinstance(value,list):return [serializable(v) for v in value]
    return value


if __name__=='__main__':
    import json
    for bits in [[0],[1],[0,1,0],[1,0,1,1],[0,0,0,0]]:
        r=run(bits)
        print(json.dumps(dict(bits=bits,output=r['output'],correct=r['correct'],min_margin=str(min(x['minimum_endpoint_margin'] for x in r['phases'])),
                              flips=sum(e['kind']=='flip' for e in r['events']),dissipation=float(r['dissipation']),work=float(r['work']),gross=float(r['gross_positive_work']))))
