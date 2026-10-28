"""Connected free-energy readout with exact source moments and full loops.

The scalar Perron normalization cancels from S_n. I/O/N source sectors are
counted separately, including a new complete sixth N moment. A finite open
Krylov message only supplies a genuine Rayleigh lower bound; no accurate
pressure and no operator multiplicative residual are required.
"""
import pathlib,json,math,hashlib,functools,argparse,time
from fractions import Fraction as F
import mpmath as mp
ROOT=pathlib.Path(__file__).resolve().parents[1]
PRIOR=ROOT.parents[1]/'sol8_opportunity_selection_20261027/obstruction_first/continuation'
mp.mp.dps=230;mp.iv.dps=230;iv=mp.iv

def lower(x):return math.nextafter(float(x.a),-math.inf)
def upper(x):return math.nextafter(float(x.b),math.inf)
def midpoint(x):return mp.mpf(x.mid._mpi_[0])
def exact(x):
    if isinstance(x,F):return iv.mpf(x.numerator)/x.denominator
    return iv.mpf(x)

@functools.lru_cache(None)
def chebyshev_moments(moments,bonds):
    """P_k(B)=R^k T_k((B+c)/R), with integer R=10b,c=2b.

    Every local bond has spectrum[-6,4], so all physical states of
    Y=(2H+2b)/(10b) lie in[-1,1]. All cancellations below are integer exact.
    """
    R=10*bonds;c=2*bonds;degree=len(moments)-1
    old=[1];current=[c,1];out=[F(moments[0])]
    if degree==0:return tuple(out)
    denominator=R
    for k in range(1,degree+1):
        numerator=sum(a*moments[i]for i,a in enumerate(current))
        assert abs(numerator)<=moments[0]*denominator
        out.append(F(numerator,denominator))
        if k==degree:break
        new=[0]*(len(current)+1)
        for j,a in enumerate(current):new[j]+=2*c*a;new[j+1]+=2*a
        for j,a in enumerate(old):new[j]-=R*R*a
        old,current=current,new;denominator*=R
    return tuple(out)

@functools.lru_cache(None)
def bessel_coefficients(a_string,degree):
    a=exact(F(a_string));aa=a*a/4;out=[]
    for k in range(degree+1):
        term=(a/2)**k/math.factorial(k);total=term;m=0
        while True:
            nxt=term*aa/((m+1)*(m+k+1))
            ratio=aa/((m+2)*(m+k+2))
            if upper(ratio)<.5 and upper(nxt/total)<1e-140:
                total+=iv.mpf([0,1])*nxt/(1-ratio)
                break
            total+=nxt;term=nxt;m+=1
            assert m<3000
        out.append(total)
    return tuple(out)

def thermal_trace(rec,beta,bonds=None):
    """Full all-state trace; exact integer moments plus analytic Cheby tail.

    exp(-beta H)=exp(beta b)[I0(a)+2 sum(-1)^k Ik(a) T_k(Y)],
    a=5 beta b. A Laurent/Cauchy bound encloses every omitted coefficient.
    """
    n=rec['n'];bonds=n-1 if bonds is None else bonds
    if bonds==0:return iv.mpf(5)
    mom=tuple(map(int,rec['trace_2H_powers']));degree=len(mom)-1
    tm=chebyshev_moments(mom,bonds);a=F(beta)*5*bonds
    coeff=bessel_coefficients(str(a),degree)
    value=coeff[0]*exact(tm[0])+sum(2*(-1)**k*coeff[k]*exact(tm[k])for k in range(1,degree+1))
    tails=[]
    for rr in [F(11,10),F(6,5),F(3,2),F(2),F(3),F(4),F(5),F(8),F(10),F(16),F(32)]:
        r=exact(rr)
        tails.append(2*iv.exp(exact(a)*(r+1/r)/2)/(r**(degree+1)*(1-1/r)))
    tail=min(tails,key=upper)*5**n
    return iv.exp(exact(F(beta)*bonds))*(value+iv.mpf([-1,1])*tail)

def periodic4(beta):
    beta=exact(F(beta));out=iv.mpf(0)
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                energy=(j*(j+1)-a*(a+1)-b*(b+1))//2
                out+=(2*j+1)*iv.exp(-beta*energy)
    return out/625

def q(c,m,offset):return sum(c[i]*c[j]*m[i+j+offset]for i in range(len(c))for j in range(len(c)))

def scalar_rayleigh(beta,records):
    m=[iv.mpf(1)]+[thermal_trace(records[r],beta)/5**r for r in range(1,7)]
    if any(lower(x)<=0 for x in m):return None
    mid=[midpoint(x)for x in m]
    g=mp.matrix([[mid[i+j]for j in range(3)]for i in range(3)])
    h=mp.matrix([[mid[i+j+1]for j in range(3)]for i in range(3)])
    try:
        ell=mp.cholesky(g);linv=ell**-1
        es,us=mp.eigsy(linv*h*linv.T);candidate=linv.T*us[:,2]
    except Exception:return None
    candidate/=max(abs(x)for x in candidate)
    strings=[mp.nstr(x,160)for x in candidate];c=[iv.mpf(s)for s in strings]
    denominator=q(c,m,0)
    if lower(denominator)<=0:return None
    theta=q(c,m,1)/denominator
    variance=q(c,m,2)/denominator-theta**2
    return theta,variance,strings

def read_inputs():
    paths={'open':PRIOR/'data/open_moments_exact_degree192.json',
           'twist4':PRIOR/'data/twisted4_moments_exact_degree192.json',
           'cycle6':ROOT/'results/cycle6_moments_exact_degree192.json'}
    objects={k:json.loads(p.read_text())for k,p in paths.items()}
    records={r['n']:r for r in objects['open']['chains']}
    twists={r['twist']:dict(r,n=4)for r in objects['twist4']['records']}
    six={r['twist']:r for r in objects['cycle6']['records']}
    assert set(six)=={'I','P'}
    receipts={k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for k,p in paths.items()}
    return records,twists,six,receipts

def acquire(beta,records,twists,six,n=256):
    trial=scalar_rayleigh(beta,records)
    if trial is None:return {'beta_exact':beta,'status':'RAYLEIGH_INPUT_NOT_ACQUIRED'},None
    theta,var,strings=trial
    z4=periodic4(beta)
    p4=thermal_trace(twists['P'],beta,bonds=4)/625
    c4=thermal_trace(twists['C'],beta,bonds=4)/625
    i4=(z4+3*p4+8*c4)/12;o4=(z4+3*p4-4*c4)/12;n4=(z4-p4)/4
    n6=(thermal_trace(six['I'],beta,bonds=6)-thermal_trace(six['P'],beta,bonds=6))/(4*5**6)
    rem=i4-theta.a**4
    row={'beta_exact':beta,'theta_J_lower':lower(theta),'theta_J_upper':upper(theta),
         'variance_J_upper':upper(var),'candidate_rational_decimal_coefficients':strings,
         'I4': [lower(i4),upper(i4)],'O4':[lower(o4),upper(o4)],
         'N4':[lower(n4),upper(n4)],'N6':[lower(n6),upper(n6)]}
    if lower(theta)<=0 or min(lower(rem),lower(o4),lower(n6))<0:
        row['status']='COUNTED_INPUT_NOT_POSITIVE';return row,None
    ri=rem**iv.mpf('.25');ro=o4**iv.mpf('.25');rn4=n4**iv.mpf('.25');rn6=n6**(iv.mpf(1)/6)
    # Each upper is valid. Select the smaller *bound*, with its full p-mass.
    if upper(rn6)<upper(rn4):pn=6;rn=rn6;nm=n6
    else:pn=4;rn=rn4;nm=n4
    theta_lower=theta.a
    tau=rem.b*ri.b**(n-4)/theta_lower**n+2*o4.b*ro.b**(n-4)/theta_lower**n+3*nm.b*rn.b**(n-pn)/theta_lower**n
    logs=-2*iv.log(1+tau)
    row.update({'status':'ACTUAL_ALL_MODE_CONNECTED_LOOP_BOUND',
                'N_tail_moment':pn,'I_other_moduli_upper':upper(ri),'O_moduli_upper':upper(ro),
                'N_moduli_upper':upper(rn),'all_other_moduli_ratio_upper':upper(max([ri.b,ro.b,rn.b],key=upper)/theta_lower),
                'ring':n,'relative_complete_loop_tail_upper':upper(tau),
                'logS_lower':lower(logs),'logS_upper':0.,'one_minus_S_upper':upper(1-iv.exp(logs)),
                'scalar_Temple_log_pressure_width_upper':upper(iv.log(1+var.b/(theta_lower*(theta_lower-ri.b))))if lower(theta_lower-ri.b)>0 else None})
    return row,(logs.a,iv.mpf(0))

def main():
    p=argparse.ArgumentParser();p.add_argument('--betas',nargs='+',default=['3/4','3/2','3','6']);args=p.parse_args()
    start=time.monotonic();records,twists,six,receipts=read_inputs();rows=[];bounds={}
    for beta in args.betas:
        row,interval=acquire(beta,records,twists,six);rows.append(row)
        if interval is not None:bounds[F(beta)]=interval
        print({k:row[k]for k in ['beta_exact','status','theta_J_lower','N_moduli_upper','relative_complete_loop_tail_upper','logS_lower']if k in row},flush=True)
    increments=[]
    for b,(l0,u0)in bounds.items():
        if 2*b not in bounds:continue
        l1,u1=bounds[2*b];low=l1-2*u0;high=u1-2*l0
        increments.append({'beta_exact':str(b),'quantity':'log T512(beta) - 2 log T256(beta)',
                           'lower':lower(low),'upper':upper(high),'width_upper':upper(high-low),
                           'first_pair_7.44047619e-7_precision_pass':upper(high-low)<7.44047619e-7})
    result={'status':'ACTUAL_CONNECTED_FREE_ENERGY_CERTIFICATES_AT_REPORTED_BETAS',
            'input_receipts':receipts,'rows':rows,'connected_thermal_increments':increments,
            'seconds':time.monotonic()-start,'individual_cold_log_purities_acquired':False,
            'uniform_spin_two_gap_proved':False,
            'arithmetic_scope':'Exact CRT power moments and integer Chebyshev conversion; explicit analytic coefficient/remainder bounds; outward mpmath interval consumer.'}
    (ROOT/'results/scalar_loop_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(increments,indent=2));print('seconds',result['seconds'],flush=True)

if __name__=='__main__':main()
