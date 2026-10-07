"""Independent high-precision diagnostic; floating point signs are not proofs."""
import json, math, time
from pathlib import Path
import mpmath as mp
OUT=Path(__file__).parent

def normalized_hankel(N, shift, delta):
    m=(N-shift)//2
    logs=[mp.log(math.comb(N,k)) for k in range(N+1)]
    return [[mp.exp((logs[2*i+shift]+logs[2*j+shift])/2-logs[i+j+shift]+delta*(i-j)**2/N) for j in range(m+1)] for i in range(m+1)]

def ldlt(A):
    n=len(A); L=[[mp.mpf(0)]*n for _ in range(n)]; d=[]
    for i in range(n):
        for j in range(i):
            L[i][j]=(A[i][j]-mp.fsum(L[i][k]*L[j][k]*d[k] for k in range(j)))/d[j]
        di=A[i][i]-mp.fsum(L[i][k]**2*d[k] for k in range(i))
        d.append(di); L[i][i]=1
        if di<=0:
            return {'positive':False,'first_nonpositive_index':i,'pivot':str(di),'min_previous':str(min(d[:-1],default=mp.mpf(1)))}
    return {'positive':True,'minimum_pivot':str(min(d)),'final_pivot':str(d[-1]),'dimension':n}

def run(N):
    mp.mp.dps=2*N+80
    ans={'N':N,'dps':mp.mp.dps,'delta':'2*log(2)','diagnostic_only':True,'blocks':[]}
    t=time.monotonic()
    for shift in [0,1]:
        z=ldlt(normalized_hankel(N,shift,2*mp.log(2)))
        ans['blocks'].append({'shift':shift,**z})
        print(json.dumps({'N':N,'shift':shift,'positive':z['positive'],'elapsed':time.monotonic()-t}),flush=True)
    ans['seconds']=time.monotonic()-t
    (OUT/f'diagnostic_N{N}.json').write_text(json.dumps(ans,indent=2))
    return ans

if __name__=='__main__':
    import sys
    for N in map(int,sys.argv[1:]): run(N)
