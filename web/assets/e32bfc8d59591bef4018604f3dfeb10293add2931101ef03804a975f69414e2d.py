#!/usr/bin/env python3
"""Bounded exact rational-delta prefix certificates with proved congruences."""
from pathlib import Path
from fractions import Fraction as F
import argparse,datetime,hashlib,json,math,time
from axial_finite_psd_certificate import Arithmetic,cdiv
OWN=Path(__file__).parent
DELTA=F(138629437,100000000)

class BoundedArithmetic(Arithmetic):
    def __init__(self,p,deadline):
        super().__init__(p);self.deadline=deadline;self.stage='initialization'
    def check(self,stage):
        self.stage=stage
        if time.perf_counter()>self.deadline:
            raise TimeoutError('declared wall limit reached at '+stage)
    def scale(self,a,n):
        assert n>=0
        return n*a[0],n*a[1]
    def populations(self,N):
        q=[None]*(N+1);meta=[None]*(N+1)
        for k in range(N//2+1):
            self.check(f'N={N}, input k={k}')
            x=DELTA*F((2*k-N)**2,4*N)
            ex,m=self.exp_minus(x);C=math.comb(N,k)
            q[k]=(ex[0]//C,cdiv(ex[1],C));meta[k]=m
            q[N-k]=q[k];meta[N-k]=m
        return q,meta
    def ldl_matrix(self,N,shift,kind,H,original_dimension):
        n=len(H);L=[[(0,0) for _ in range(n)] for _ in range(n)];ds=[]
        for i in range(n):
            self.check(f'N={N}, shift={shift}, block={kind}, pivot={i}')
            v=H[i][i]
            for k in range(i):v=self.sub(v,self.mul(self.square(L[i][k]),ds[k]))
            if v[0]<=0:
                raise ArithmeticError(f'uncertified pivot N={N},shift={shift},block={kind},i={i},bounds={v}')
            ds.append(v);L[i][i]=(self.D,self.D)
            for j in range(i+1,n):
                self.check(f'N={N}, shift={shift}, block={kind}, row={j}, column={i}')
                v=H[j][i]
                for k in range(i):v=self.sub(v,self.mul(self.mul(L[j][k],L[i][k]),ds[k]))
                L[j][i]=self.div(v,ds[i])
        return {'shift':shift,'block_kind':kind,'original_dimension':original_dimension,'dimension':n,
                'diagonal_intervals':[[str(x),str(y)] for x,y in ds],
                'L_strict_lower_intervals':[[[str(x),str(y)] for x,y in row[:i]] for i,row in enumerate(L)],
                'minimum_lower_pivot_integer':str(min(d[0] for d in ds)) if ds else None}
    def required_matrices(self,N,q):
        if N%2:
            m=N//2+1;H=[[q[i+j] for j in range(m)] for i in range(m)]
            return [self.ldl_matrix(N,0,'full_odd',H,m)]
        result=[]
        for shift in [0,1]:
            m=(N-shift)//2+1;h=m//2
            H=[[q[i+j+shift] for j in range(m)] for i in range(m)]
            P=[[self.scale(self.add(H[i][j],H[i][m-1-j]),2) for j in range(h)] for i in range(h)]
            A=[[self.scale(self.sub(H[i][j],H[i][m-1-j]),2) for j in range(h)] for i in range(h)]
            if m%2:
                for i in range(h):P[i].append(self.scale(H[i][h],2))
                P.append([self.scale(H[h][i],2) for i in range(h)]+[H[h][h]])
            result.append(self.ldl_matrix(N,shift,'plus',P,m))
            result.append(self.ldl_matrix(N,shift,'minus',A,m))
        return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--min-N',type=int,required=True);ap.add_argument('--max-N',type=int,required=True)
    ap.add_argument('--precision',type=int,required=True);ap.add_argument('--wall-limit',type=float,required=True)
    args=ap.parse_args()
    assert 3<=args.min_N<=args.max_N<=199 and 128<=args.precision<=4096 and 0<args.wall_limit<=60
    path=OWN/'evidence'/f'axial_optimal_rational_prefix_N{args.min_N}_{args.max_N}_P{args.precision}.json'
    if path.exists():raise SystemExit('preserving existing evidence; choose a new range or precision')
    start=time.perf_counter();a=BoundedArithmetic(args.precision,start+args.wall_limit);cases=[]
    out={'scope':'Exact finite strict PSD at rational delta_bar only; requires separate analytic N>=200 endpoint proof, N2 explicit mixture, and compact Bernstein moment lemma.',
         'delta':str(DELTA),'precision_bits':args.precision,'denominator':str(a.D),'requested_N_range':[args.min_N,args.max_N],
         'declared_acquisition_wall_limit_seconds':args.wall_limit,'cases':cases,
         'algorithm':'owned outward dyadic arithmetic, alternating rational exp with range squaring; exact palindrome, odd reversal and even plus/minus congruences; enclosed unit-L LDL',
         'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        for N in range(args.min_N,args.max_N+1):
            a.check(f'N={N}, case start');q,meta=a.populations(N);matrices=a.required_matrices(N,q)
            cases.append({'N':N,'q_intervals':[[str(x),str(y)] for x,y in q],
                          'exp_enclosure_metadata':meta,'matrices':matrices,
                          'omitted_matrix_identity':'H1=J H0 J' if N%2 else None})
        out['status']='PASS all requested finite cases strictly positive'
    except Exception as e:
        out['status']='INCOMPLETE';out['failure']=repr(e);out['failure_stage']=a.stage
    out['acquisition_wall_seconds']=time.perf_counter()-start
    out['completed_N_range']=[cases[0]['N'],cases[-1]['N']] if cases else None
    out['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out['arithmetic_source_sha256']=hashlib.sha256((OWN/'axial_finite_psd_certificate.py').read_bytes()).hexdigest()
    out['congruence_proof_sha256']=hashlib.sha256((OWN/'PREFIX_SYMMETRY_AND_BUDGET.txt').read_bytes()).hexdigest()
    serialize_start=time.perf_counter();payload=json.dumps(out,indent=2)+'\n';path.write_text(payload)
    receipt={'status':out['status'],'delta':str(DELTA),'completed_N_range':out['completed_N_range'],
             'acquisition_wall_seconds':out['acquisition_wall_seconds'],'serialization_wall_seconds':time.perf_counter()-serialize_start,
             'path':str(path),'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    path.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
    if out['status']=='INCOMPLETE':raise SystemExit(1)
if __name__=='__main__':main()
