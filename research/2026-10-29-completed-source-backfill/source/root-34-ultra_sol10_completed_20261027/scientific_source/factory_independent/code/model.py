"""Independent literal controller, input-side death, and Fock detector kernel.

No producer imports. A clock performs one primitive raw preparation or fusion.
New source photons appear at its end; every previously held mode loses first.
"""
from fractions import Fraction as F
from math import comb,factorial
from functools import lru_cache
SOURCE=(F(99,500),F(4,5),F(1,500));EFF=F(19,20)

@lru_cache(None)
def state_space(n):
    if n==1:return (('raw',),)
    child=state_space(n//2)
    return tuple([('L',s)for s in child]+[('R',a,s)for a in range(n+1)for s in child]+[('F',a,b)for a in range(n+1)for b in range(n+1)])

def start(n):return ('raw',)if n==1 else('L',start(n//2))

def raw_reward(n,s):
    if n==1:return 1
    if s[0]=='F':return 0
    return raw_reward(n//2,s[1]if s[0]=='L'else s[2])

@lru_cache(None)
def beamsplitter(i,j):
    N=i+j;out=[]
    for k in range(N+1):
        c=sum(comb(i,a)*comb(j,k-a)*(-1)**(j-k+a)for a in range(max(0,k-j),min(i,k)+1))
        out.append(F(c*c*factorial(k)*factorial(N-k),2**N*factorial(i)*factorial(j)))
    assert sum(out)==1
    return tuple(out)

class Chain:
    def __init__(self,lam):self.lam=F(lam);self.cache={};self.loss_cache={}
    def loss(self,a):
        if a not in self.loss_cache:self.loss_cache[a]=tuple(F(comb(a,k))*self.lam**k*(1-self.lam)**(a-k)for k in range(a+1))
        return self.loss_cache[a]
    def transition(self,n,s):
        key=(n,s)
        if key in self.cache:return self.cache[key]
        out={}
        def add(t,p):
            if p:out[t]=out.get(t,F(0))+p
        if n==1:
            for k,p in enumerate(SOURCE):add(('out',k),p)
        elif s[0]=='L':
            for t,p in self.transition(n//2,s[1]).items():
                add(('R',t[1],start(n//2))if t[0]=='out'else('L',t),p)
        elif s[0]=='R':
            for a,lp in enumerate(self.loss(s[1])):
                if not lp:continue
                for t,p in self.transition(n//2,s[2]).items():
                    add(('F',a,t[1])if t[0]=='out'else('R',a,t),lp*p)
        else:
            _,a,b=s;success=F(0)
            for i,pa in enumerate(self.loss(a)):
                for j,pb in enumerate(self.loss(b)):
                    if not(pa and pb):continue
                    for k,bs in enumerate(beamsplitter(i,j)):
                        p=pa*pb*bs*(1-EFF)**(i+j-k)
                        add(('out',k),p);success+=p
            add(start(n),1-success)
        assert sum(out.values())==1 and min(out.values())>=0
        self.cache[key]=out;return out
    def matrices(self,n):
        states=state_space(n);index={s:i for i,s in enumerate(states)};S=len(states)
        Q=[[F(0)]*S for _ in states];R=[[F(0)]*(2*n+1)for _ in states]
        for i,s in enumerate(states):
            for t,p in self.transition(n,s).items():
                if t[0]=='out':R[i][t[1]]+=p
                else:Q[i][index[t]]+=p
        reachable={index[start(n)]};todo=list(reachable)
        while todo:
            i=todo.pop()
            for j,p in enumerate(Q[i]):
                if p and j not in reachable:reachable.add(j);todo.append(j)
        assert len(reachable)==S
        return states,index[start(n)],Q,R
