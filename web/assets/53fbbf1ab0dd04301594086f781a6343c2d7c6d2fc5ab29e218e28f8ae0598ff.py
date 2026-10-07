#!/usr/bin/env python3
"""Bounded high-precision moment diagnostics, never a separability proof."""
import json,time,math
from pathlib import Path
import mpmath as mp
mp.mp.dps=140
def qseq(N,delta):
    return [mp.exp(-delta*(mp.mpf(k)-mp.mpf(N)/2)**2/N)/math.comb(N,k) for k in range(N+1)]
def pivots(N,delta):
    q=qseq(N,delta); results=[]
    for shift in [0,1]:
        n=(N-shift)//2+1
        H=mp.matrix([[q[i+j+shift]/mp.sqrt(q[2*i+shift]*q[2*j+shift]) for j in range(n)] for i in range(n)])
        L=mp.matrix(n); mins=mp.inf
        for i in range(n):
            value=H[i,i]-sum(L[i,k]**2 for k in range(i)); mins=min(mins,value)
            if value<=0: results.append({'shift':shift,'positive':False,'pivot':str(value),'index':i}); break
            L[i,i]=mp.sqrt(value)
            for j in range(i+1,n):
                L[j,i]=(H[j,i]-sum(L[j,k]*L[i,k] for k in range(i)))/L[i,i]
        else: results.append({'shift':shift,'positive':True,'min_pivot':str(mins)})
    return all(r['positive'] for r in results),results
def main():
    start=time.perf_counter(); target=2*mp.log(2); cases=[]
    for N in range(2,65):
        ok,data=pivots(N,target); cases.append({'N':N,'at_2log2':ok,'tests':data})
        if not ok and N>2: break
    thresholds=[]
    for N in [3,4,5,6,8,10,12,16,24,32]:
        lo,hi=mp.mpf('0'),mp.mpf('2.1')
        for _ in range(35):
            mid=(lo+hi)/2
            ok,_=pivots(N,mid)
            if ok: lo=mid
            else: hi=mid
        thresholds.append({'N':N,'diagnostic_threshold_bracket':[str(lo),str(hi)]})
    out={'scope':'mpmath Cholesky diagnostics of truncated logit-Stieltjes moment matrices; positivity tests necessary and interior sufficiency via classical finite moment criteria still requires proof/interface audit','dps':mp.mp.dps,'at_target':cases,'thresholds':thresholds,'wall_seconds':time.perf_counter()-start}
    path=Path(__file__).with_name('evidence')/'axial_moment_probe.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'target':str(target),'tested_max_N':cases[-1]['N'],'failures':[x['N'] for x in cases if not x['at_2log2']],'thresholds':thresholds,'seconds':out['wall_seconds']}))
if __name__=='__main__': main()
