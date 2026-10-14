from fractions import Fraction as F
import json,time
from acquisition import run_acquired
from collective_sector import CollectiveRing
from preparation import run as prep

def exp_bounds(x,tol=F(1,10**35)):
    """Rational Taylor enclosure for nonnegative x; explicit tail bound."""
    if x<0:raise ValueError('requires x>=0')
    term=F(1);total=term;j=0
    while True:
        j+=1;term=term*x/j;total+=term
        ratio=x/(j+1)
        if ratio<1:
            tail=term*ratio/(1-ratio)
            if tail<=tol:return total,total+tail

def uncertainty(lo,hi,n,logt_error,field_error,clock_error):
    # Oscillation of dimensionless energy discrepancy on a uniform n-cycle.
    omega=n*(logt_error+field_error);_,expup=exp_bounds(2*omega)
    a=1-clock_error;b=1+clock_error
    low=lo/(b*expup);high=hi*expup/a
    return {'n':n,'logt_error':str(logt_error),'field_error':str(field_error),'clock_error':str(clock_error),
            'lo':float(low),'hi':float(high),'ratio':float(high/low),'lo_exact':str(low),'hi_exact':str(high)}

def main():
    start=time.perf_counter();root='/mnt/data/astra_source_escape';out={'rarity':[],'dimension':[],'clock':[],'uncertainty':[],'decisions':{}}
    for t in [10,100,1000,10000]:
        a=run_acquired(16,F(t));json.dump(a,open(f'{root}/acquired_n16_t{t}.json','w'));out['rarity'].append(a)
        print('rarity',t,a['tau_lo'],a['tau_hi'],a['ratio'],a['end_to_end_seconds'],flush=True)
    for n in [8,16,24,32]:
        a=run_acquired(n,F(1000));json.dump(a,open(f'{root}/acquired_n{n}_t1000.json','w'));out['dimension'].append(a)
        print('dimension',n,a['ratio'],a['end_to_end_seconds'],flush=True)
    for nu,kap in [(F(1,10),F(1)),(F(10),F(1)),(F(1),F(1,10)),(F(1),F(10))]:
        a=run_acquired(16,F(1000),nu=nu,kappa=kap);out['clock'].append(a)
        print('clock',nu,kap,a['tau_lo'],a['tau_hi'],a['ratio'],flush=True)
    A=out['dimension'][2];B=run_acquired(24,F(1200));json.dump(B,open(f'{root}/acquired_n24_t1200.json','w'))
    L=F(A['lower_exact']);U=F(A['upper_exact'])
    for h in [F(0),F(1,100000),F(1,10000),F(1,1000),F(1,100)]:
        out['uncertainty'].append(uncertainty(L,U,24,F(0),h,F(0)))
    for eta in [F(0),F(1,500),F(1,100),F(1,20)]:
        out['uncertainty'].append(uncertainty(L,U,24,F(0),F(0),eta))
    # Each energy query has error delta=1e-5. Four-term contrasts yield
    # |delta log t|<=2delta and |delta field|<=6delta in this class.
    Arob=uncertainty(L,U,24,F(2,100000),F(6,100000),F(1,500))
    Brob=uncertainty(F(B['lower_exact']),F(B['upper_exact']),24,F(2,100000),F(6,100000),F(1,500))
    out['decisions']={'A':{k:v for k,v in A.items() if k not in ['witness','query_transcript']},
                     'B':{k:v for k,v in B.items() if k not in ['witness','query_transcript']},
                     'A_robust':Arob,'B_robust':Brob,
                     'B_over_A_certified':float(F(Brob['lo_exact'])/F(Arob['hi_exact']))}
    prepout=prep(24,F(1000));json.dump(prepout,open(f'{root}/prepared_n24_t1000.json','w'))
    out['preparation']=prepout;out['total_experiment_seconds']=time.perf_counter()-start
    # Smaller summary retains paths to witness files for principal cases.
    for key in ['rarity','dimension','clock']:
        out[key]=[{k:v for k,v in a.items() if k not in ['witness','query_transcript']} for a in out[key]]
    out['preparation']={k:v for k,v in prepout.items() if k not in ['witnesses','Gamma','G0']}
    json.dump(out,open(f'{root}/experiments.json','w'));print('decision',out['decisions']['B_over_A_certified'],flush=True)
if __name__=='__main__':main()
