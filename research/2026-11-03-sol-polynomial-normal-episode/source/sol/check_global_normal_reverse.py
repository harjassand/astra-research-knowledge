#!/usr/bin/env python3
"""Exact reverse policy identities and eligible-pair activation checks."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_corner_bridge import channels,ff,Y
from check_global_normal_reference import normal,residual,weight,displacement

P=Path(__file__).resolve().parent

def probe(x,alpha,beta,core):
    base=residual(x);mu=weight(x,base,alpha,beta,core);actual={}
    labels=[('block',p,j) for p in (0,1) for j in range(4)]+[('core',0),('core',1)]
    for label in labels:
        v=displacement(label);pre=tuple(x[j]-v[j] for j in range(6))
        if min(pre)<0 or not normal(pre,label):continue
        rate=next((r for _,r,l in channels(pre,alpha,beta,core) if l==label),F(0))
        if rate:actual[label]=weight(pre,base,alpha,beta,core)*rate/mu
    expected={}
    for p,rates in enumerate((alpha,beta)):
        a=x[3*p];j=a%3;own=x[3*p:3*p+3]
        if j==0:
            expected[('block',p,3)]=F(rates[0])
            term=F(rates[3])*ff(own,Y[3])
            if term:expected[('block',p,2)]=term
        elif j==1:
            rate=F(rates[1])*ff(own,Y[1])
            if rate:expected[('block',p,0)]=rate
        else:
            rate=F(rates[2])*ff(own,Y[2])
            if rate:expected[('block',p,1)]=rate
    for out,rate,label in channels(x,alpha,beta,core):
        if label[0]=='core':expected[('core',1-label[1])]=rate
    assert actual==expected,(x,actual,expected)
    assert sum(actual.values())==sum(r for _,r,l in channels(x,alpha,beta,core) if normal(x,l))
    if x[0]%3==x[3]%3==0:
        t0=24*min(alpha[3],beta[3])
        for p in (0,1):
            out=list(x);out[3*p]+=3;out[3*p+1]+=2;out[3*p+2]+=2
            eligible=lambda z:any(z[3*i]>=3 and min(z[3*i+1],z[3*i+2])>=2 for i in (0,1))
            assert eligible(out)
            term=sum(r for _,r,l in channels(tuple(out),alpha,beta,core) if l[0]=='block' and l[2]==3)
            assert term>=t0
            for y,r,l in channels(tuple(out),alpha,beta,core):
                if l[0]=='core':assert eligible(y)

def main():
    count=0
    for a in (0,1,2,3,4,5,6,9,12):
        for d in (0,1,2,3,4,5,6,9,12):
            for b,c,e,f in ((0,0,0,0),(1,0,0,1),(2,2,0,0),(5,3,4,8),(0,100,2,300)):
                for alpha,beta,core in (((1,1,1,1),(1,1,1,1),(2,1)),((1,5,3,7),(2,2,4,11),(3,7))):
                    probe((a,b,c,d,e,f),alpha,beta,core);count+=1
    result={'scope':'Exact actual adjoint rates, all phases, zero hazards, and reverse-packet eligible-donor preservation.','cases':count}
    (P/'results/global_normal_reverse_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
