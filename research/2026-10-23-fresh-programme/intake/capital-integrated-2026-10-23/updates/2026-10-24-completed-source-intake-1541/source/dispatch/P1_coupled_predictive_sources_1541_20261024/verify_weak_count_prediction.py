"""Exact finite weak-readout predictions and their classical nonlinear limit.

The Gaussian family here is R=I-theta*A, A=[[2,-1],[-1,2]]. It is explicitly
different from the balanced preparation in KERR_CORE_CERTIFICATE.json.
The prescribed angle is 2 atan(theta/2), and no-photon-loss factor is1-theta.
These approach scaled interaction time1 and scaled detection exposure1.
"""
from fractions import Fraction as F
from pathlib import Path
import json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'agents'/'coupled_physical_witness_20261024'))
from verify_coupled_record_witness import first_port_balance_interval


def tv_at_balance(p0, balance, classical):
    p=(p0,(1-p0+balance)/2,(1-p0-balance)/2)
    return sum(abs(x-y) for x,y in zip(p,classical))/2


def pack(v):
    if isinstance(v,F): return {'exact':str(v),'decimal':float(v)}
    if isinstance(v,dict): return {k:pack(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [pack(x) for x in v]
    return v


def main():
    # Classical p(z)=3/pi² exp[-z† A z], nonlinear Kerr flow for scaled time1,
    # mixer then first-port counts over scaled total exposure1.
    p0=F(3,8);balance=F(19,108)
    classical=(p0,(1-p0+balance)/2,(1-p0-balance)/2)
    out=[]
    for theta in (F(1,16),F(1,64),F(1,256),F(1,1024)):
        r,s,q=1-2*theta,theta,1-theta
        cosine=(4-theta**2)/(4+theta**2)
        sine=4*theta/(4+theta**2)
        assert cosine**2+sine**2==1
        b0=first_port_balance_interval(r,s,F(1),q,cells=16384)
        b1=first_port_balance_interval(r,s,cosine,q,cells=16384)
        none=((1-r)**2-s*s)/(1-2*r*q+(r*r-s*s)*q*q)
        gap=((b0[0]-b1[1])/2,(b0[1]-b1[0])/2)
        # Absolute values are piecewise linear; include every kink for exact min.
        candidates=[b1[0],b1[1]]
        for x in (2*classical[1]-(1-none),(1-none)-2*classical[2]):
            if b1[0]<=x<=b1[1]:candidates.append(x)
        ds=[tv_at_balance(none,x,classical) for x in candidates]
        approximation=(min(ds),max(tv_at_balance(none,x,classical) for x in b1))
        row={'theta':theta,'physical_R_diagonal':r,'physical_R_off_diagonal':s,
             'per_photon_survival':q,'cos_angle':cosine,'sin_angle':sine,
             'no_count_exact':none,'kerr_balance_interval':b1,
             'whole_record_TV_from_classical_limit_interval':approximation,
             'whole_record_TV_kerr_vs_no_kerr_interval':gap}
        out.append(row)
        print(json.dumps({'theta':str(theta),'classical_limit_error_interval':[float(x) for x in approximation],
                          'nonlinear_record_gap_interval':[float(x) for x in gap]}),flush=True)
    data={'status':'exact rational monotone integral enclosures,80-bit outward dyadic arithmetic',
          'scope':__doc__,'classical_limit_record':classical,
          'limiting_nonlinear_record_gap':'151/432 - (3/4) log(3/2)',
          'cells_per_integral':16384,'examples':out}
    Path(__file__).with_name('WEAK_COUNT_PREDICTION_EXACT.json').write_text(json.dumps(pack(data),indent=2)+'\n')


if __name__=='__main__':main()
