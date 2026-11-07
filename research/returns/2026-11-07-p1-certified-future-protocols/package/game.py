"""Exact finite-game compiler for an unbounded repeated-service protocol.

All data are acquired port matrices. No native dynamics are imported.
The full report proves the general parity-game reduction; this execution
solves the indicated safety automaton by a greatest fixed point.
"""
from fractions import Fraction as Q
from itertools import product
import numpy as np

COMMANDS=((0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
REQUESTS=((0,1),(0,-1),(1,1),(1,-1),(2,1),(2,-1))
SCALE=1<<40
THETA=Q(1,2)
# A nearest-even 40-bit ADC reports a threshold code +/-1/2 beginning
# half an ADC unit earlier. Both threshold codes are even, hence the two
# outer cells include the tie. The middle analogue cell is open.
ANALOG_THRESHOLD=THETA-Q(1,2*SCALE)
DEADLINE=4

def labels(value,radius):
    lo=value-radius;hi=value+radius
    out=[]
    if lo<=-ANALOG_THRESHOLD:out.append(-1)
    if hi>-ANALOG_THRESHOLD and lo<ANALOG_THRESHOLD:out.append(0)
    if hi>=ANALOG_THRESHOLD:out.append(1)
    return tuple(out)

def observe(raw):
    half=SCALE//2
    return tuple(-1 if x<=-half else 1 if x>=half else 0 for x in raw)

class ProtocolGame:
    def __init__(self,G,m=4):
        self.m=m
        self.G=[[[int(Q(v)*SCALE) for v in row] for row in mat] for mat in G]
        self.words=[w for w in product(range(7),repeat=m) if all(a==0 or b==0 for a,b in zip(w,w[1:]))]
        self.index={w:i for i,w in enumerate(self.words)}
        self.M=len(self.words)
        self.pred=[]
        self.build_mults=0;self.build_adds=0
        for w in self.words:
            y=[]
            for row in range(3):
                z=0
                for lag,a in enumerate(reversed(w)):
                    for col in range(3):
                        z+=self.G[lag][row][col]*COMMANDS[a][col]
                        self.build_mults+=1;self.build_adds+=1
                y.append(z)
            self.pred.append(tuple(y))
        self.pred_Q=[tuple(Q(z,SCALE) for z in y) for y in self.pred]
        self.next=np.full((self.M,7),-1,dtype=np.int32)
        for i,w in enumerate(self.words):
            for a in (range(7) if w[-1]==0 else (0,)):
                self.next[i,a]=self.index[w[1:]+(a,)]
        self.initial=self.index[(0,)*m]
        self.solve_calls=0;self.total_rounds=0;self.boolean_checks=0

    def allowed(self,radius):
        return [tuple(labels(v,radius) for v in y) for y in self.pred_Q]

    def solve(self,radius,certificate=False):
        self.solve_calls+=1
        allowed=self.allowed(Q(radius))
        bad=np.zeros(self.M,dtype=bool)
        hit=np.zeros((self.M,6),dtype=bool)
        miss=np.zeros((self.M,6),dtype=bool)
        for i,cols in enumerate(allowed):
            bad[i]=sum(any(v!=0 for v in cs) for cs in cols)>=2
            for t,(axis,sign) in enumerate(REQUESTS):
                hit[i,t]=sign in cols[axis]
                miss[i,t]=any(v!=sign for v in cols[axis])
        W=np.ones((self.M,6,DEADLINE),dtype=bool)
        rank=np.zeros(W.shape,dtype=np.int32)
        rounds=0
        while True:
            rounds+=1
            good=np.zeros((self.M,6,DEADLINE,7),dtype=bool)
            future_requests=W[:,:,-1].all(axis=1)
            for a in range(7):
                valid=self.next[:,a]>=0
                src=np.flatnonzero(valid)
                dest=self.next[src,a]
                base=(~bad[dest])[:,None] & ((~hit[dest]) | future_requests[dest,None])
                for k in range(DEADLINE):
                    cont=np.zeros((len(src),6),dtype=bool) if k==0 else W[dest,:,k-1]
                    good[src,:,k,a]=base & ((~miss[dest]) | cont)
                    self.boolean_checks+=len(src)*6*5
            nw=good.any(axis=3)
            removed=W & ~nw
            rank[removed]=rounds
            if np.array_equal(nw,W):break
            assert not (nw & ~W).any()
            W=nw
        self.total_rounds+=rounds
        pol=np.full(W.shape,-1,dtype=np.int8)
        # Prefer zero command when a winning strategy can meet all deadlines.
        for a in reversed(range(7)):
            pol[good[:,:,:,a]&W]=a
        out={'radius':Q(radius),'initial_winning':bool(W[self.initial,:,-1].all()),
             'winning_states':int(W.sum()),'total_states':int(W.size),'iterations':rounds}
        if certificate:out.update(W=W,rank=rank,policy=pol,allowed=allowed,good=good)
        return out

    def critical(self):
        vals={Q(0),Q(1)}
        for y in self.pred_Q:
            for v in y:
                for d in (abs(v-ANALOG_THRESHOLD),abs(v+ANALOG_THRESHOLD)):
                    if 0<d<1:vals.add(d)
        vals=sorted(vals)
        # Search open intervals; their graphs are exactly constant.
        lo=-1;hi=len(vals)-1
        while hi-lo>1:
            k=(lo+hi)//2
            ans=self.solve((vals[k]+vals[k+1])/2)
            if ans['initial_winning']:lo=k
            else:hi=k
        crit=vals[lo+1]
        at=self.solve(crit)
        return {'critical_radius':crit,'at_boundary_winning':at['initial_winning'],
                'distinct_breakpoints':len(vals),'last_winning_open_interval':
                None if lo<0 else [vals[lo],vals[lo+1]],
                'first_losing_open_interval':None if hi>=len(vals)-1 else [vals[hi],vals[hi+1]]}

    def verify(self,sol):
        W=sol['W'];rank=sol['rank'];pol=sol['policy'];allowed=sol['allowed']
        checked=0;loss_checks=0;examples=[]
        for s in range(self.M):
            for t,(axis,sign) in enumerate(REQUESTS):
                for k in range(DEADLINE):
                    if W[s,t,k]:
                        acts=[int(pol[s,t,k])]
                    else:
                        acts=[a for a in range(7) if self.next[s,a]>=0]
                    for a in acts:
                        sp=int(self.next[s,a]);assert sp>=0
                        found_bad=None
                        for o in product(*allowed[sp]):
                            unsafe=sum(v!=0 for v in o)>1
                            served=o[axis]==sign
                            if unsafe:
                                losing=True;target=None
                            elif served:
                                target=next((j for j in range(6) if not W[sp,j,-1] and rank[sp,j,-1]<rank[s,t,k]),None)
                                losing=target is not None
                            elif k==0:
                                losing=True;target=None
                            else:
                                target=t
                                losing=not W[sp,t,k-1] and rank[sp,t,k-1]<rank[s,t,k]
                            if W[s,t,k]:
                                assert not unsafe
                                if served:assert W[sp,:,-1].all()
                                else:assert k>0 and W[sp,t,k-1]
                                checked+=1
                            elif losing:
                                found_bad={'state':[s,t,k],'action':a,'observation':o,'next_request':target}
                                break
                        if not W[s,t,k]:
                            assert found_bad is not None
                            loss_checks+=1
                            if len(examples)<8:examples.append(found_bad)
        return {'status':'PASS','winning_policy_observation_branches':checked,
                'losing_state_action_refutations':loss_checks,'losing_examples':examples,
                'rank_max':int(rank.max()),'scope':'complete fixed-point and decreasing-rank certificates, all game states and allowed observations'}
