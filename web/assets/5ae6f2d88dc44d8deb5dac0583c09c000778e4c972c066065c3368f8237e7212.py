#!/usr/bin/env python3
"""Rational-delta finite certificates using the frozen owned outward arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,math,time
from axial_finite_psd_certificate import Arithmetic,cdiv
OWN=Path(__file__).parent
class RationalDeltaArithmetic(Arithmetic):
    def __init__(self,p,delta):super().__init__(p);self.delta=delta
    def populations(self,N):
        q=[];meta=[]
        for k in range(N+1):
            x=self.delta*F((2*k-N)**2,4*N)
            ex,m=self.exp_minus(x);C=math.comb(N,k)
            q.append((ex[0]//C,cdiv(ex[1],C)));meta.append(m)
        return q,meta
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--delta',default='5/4');ap.add_argument('--max-N',type=int,default=63)
    ap.add_argument('--precision',type=int,default=384);ap.add_argument('--wall-limit',type=float,default=30.)
    args=ap.parse_args();delta=F(args.delta)
    assert 0<delta<F(13863,10000) and 2<=args.max_N<=128 and args.precision>=128 and 0<args.wall_limit<=60
    start=time.perf_counter();a=RationalDeltaArithmetic(args.precision,delta);cases=[]
    out={'scope':'Exact finite rational-delta PSD certificates only; analytic infinite-tail theorem required separately.',
         'delta':str(delta),'precision_bits':args.precision,'denominator':str(a.D),'max_N_requested':args.max_N,'cases':cases,
         'algorithm':'frozen owned outward dyadic arithmetic and rational exp; rational delta wrapper','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        for N in range(2,args.max_N+1):
            if time.perf_counter()-start>args.wall_limit:raise TimeoutError('declared bounded wall limit reached')
            q,meta=a.populations(N)
            cases.append({'N':N,'q_intervals':[[str(x),str(y)] for x,y in q],'exp_enclosure_metadata':meta,'matrices':[a.ldl(N,s,q) for s in [0,1]]})
        out['status']='PASS all requested finite cases strictly positive'
    except Exception as e:out['status']='INCOMPLETE';out['failure']=repr(e)
    out['wall_seconds']=time.perf_counter()-start;out['completed_max_N']=cases[-1]['N'] if cases else None
    out['wrapper_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out['arithmetic_source_sha256']=hashlib.sha256((OWN/'axial_finite_psd_certificate.py').read_bytes()).hexdigest()
    slug=f'{delta.numerator}over{delta.denominator}'
    path=OWN/'evidence'/f'axial_delta{slug}_finite_N{args.max_N}_P{args.precision}.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'delta':str(delta),'completed_max_N':out['completed_max_N'],'wall_seconds':out['wall_seconds'],'path':str(path)}))
    if out['status']=='INCOMPLETE':raise SystemExit(1)
if __name__=='__main__':main()
