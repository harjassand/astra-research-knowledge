"""Actual continuous-kernel compression with an acquired infinite tail.

<vac,K_beta^r vac>=Z_open,r(beta). Three Krylov vectors therefore use the
six exact OPEN-chain trace functions. Known complete even moments TrK² and
TrK⁴ count every unrepresented spatial eigenvalue. A Temple bound is used
only after that count proves the trial mode is the unique largest modulus.
No zero-temperature gap, finite rank, MPS normalization or fitted tail.
"""
import pathlib,json,math,argparse
import mpmath as mp
ROOT=pathlib.Path(__file__).resolve().parent
mp.mp.dps=110;mp.iv.dps=110;iv=mp.iv
def lo(q):return math.nextafter(float(q.a),-math.inf)
def hi(q):return math.nextafter(float(q.b),math.inf)
def midpoint(q):return mp.mpf(q.mid._mpi_[0])

def open_trace(record,beta):
    n=record['n'];degree=record['degree'];mom=list(map(int,record['trace_2H_powers']))
    t=iv.mpf(beta)/2
    value=sum(iv.mpf(v)*(-t)**k/math.factorial(k)for k,v in enumerate(mom))
    x=6*(n-1)*iv.mpf(beta)
    tail=5**n*iv.exp(x)*x**(degree+1)/math.factorial(degree+1)
    return value+iv.mpf([-1,1])*tail

def pair_trace(beta):
    return sum(deg*iv.exp(-beta*e)for deg,e in [(1,-6),(3,-5),(5,-3),(7,0),(9,4)])

def periodic4_trace(beta):
    z=iv.mpf(0)
    # H4=(S0+S2).(S1+S3). Each sublattice pair has j=0,...,4 once.
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                energy=(j*(j+1)-a*(a+1)-b*(b+1))//2
                z+=(2*j+1)*iv.exp(-beta*energy)
    return z

def quadratic(c,m,offset):
    return sum(c[i]*c[j]*m[i+j+offset]for i in range(len(c))for j in range(len(c)))

def acquire(beta,records,krylov_rank=3,twisted=None):
    b=iv.mpf(beta);m=[iv.mpf(1)]+[open_trace(records[r],b)/(5**r)for r in range(1,7)]
    nominal=mp.matrix([midpoint(x)for x in m])
    G=mp.matrix([[nominal[i+j]for j in range(krylov_rank)]for i in range(krylov_rank)])
    H=mp.matrix([[nominal[i+j+1]for j in range(krylov_rank)]for i in range(krylov_rank)])
    ell=mp.cholesky(G);linv=ell**-1
    vals,vecs=mp.eigsy(linv*H*linv.T)
    candidate=linv.T*vecs[:,krylov_rank-1]
    candidate/=max(abs(x)for x in candidate)
    strings=[mp.nstr(x,85)for x in candidate];c=[iv.mpf(x)for x in strings]
    denominator=quadratic(c,m,0);assert lo(denominator)>0
    theta=quadratic(c,m,1)/denominator
    variance=quadratic(c,m,2)/denominator-theta**2
    assert hi(variance)>=0
    # All spectral moments below refer to J=K/5; the factor5 is retained.
    moments={2:pair_trace(2*b)/25,4:periodic4_trace(b)/625}
    counted=[]
    for power,total in moments.items():
        rem=total-theta.a**power
        if lo(rem)<0:continue
        other=rem**(iv.mpf(1)/power)
        counted.append((hi(other),power,other,total))
    sector_data=None
    if twisted is not None:
        values={}
        for name,rec in twisted.items():
            degree=rec['degree'];x=24*b
            value=sum(iv.mpf(int(v))*(-b/2)**k/math.factorial(k)for k,v in enumerate(rec['trace_2H_powers']))
            tail=625*iv.exp(x)*x**(degree+1)/math.factorial(degree+1)
            values[name]=(value+iv.mpf([-1,1])*tail)/625
        invariant=(moments[4]+3*values['P']+8*values['C'])/12
        complement=moments[4]-invariant
        rem=invariant-theta.a**4
        if lo(rem)>=0 and lo(complement)>=0:
            rinv=rem**iv.mpf('.25');rnon=(complement/3)**iv.mpf('.25')
            rout=rinv if rinv.b>=rnon.b else rnon
            sector_data={'A4_invariant_moment4_upper':hi(invariant),
                'A4_complement_moment4_upper':hi(complement),
                'other_invariant_modulus_upper':hi(rinv),
                'SO3_nontrivial_modulus_upper':hi(rnon)}
            counted.append((hi(rout),4,rout,moments[4]))
    assert counted
    _,power,other,total=min(counted,key=lambda row:row[0])
    separation=theta.a-other.b
    result={'beta':float(b.mid),'beta_exact':str(beta),'Krylov_rank':krylov_rank,
        'candidate_rational_decimal_coefficients':strings,
        'candidate_normalization_lower':lo(denominator),
        'Rayleigh_J_lower':lo(theta),'Rayleigh_J_upper':hi(theta),
        'variance_J_upper':hi(variance),
        'counting_even_moment':power,'all_other_moduli_J_upper':hi(other),
        'Perron_separation_lower':lo(separation),
        'unique_leading_mode_certified':lo(separation)>0,
        'status':'COUNTED_MODE_NOT_SEPARATED'}
    if sector_data is not None:result['sector_projection_data']=sector_data
    if lo(separation)<=0:return result,None
    top_lower=theta.a
    top_upper=theta.b+variance.b/separation
    result.update({'status':'ACTUAL_KERNEL_PERRON_AND_INFINITE_TAIL_CERTIFIED',
        'Perron_J_lower':lo(top_lower),'Perron_J_upper':hi(top_upper),
        'Perron_log_width_upper':hi(iv.log(top_upper/top_lower)),
        'rings':[]})
    # Keep the complete residual p-mass, not an assumed finite-rank model.
    remainder=total-top_lower**power
    bounds={}
    for n in [128,256,512]:
        assert n>=power and n%2==0
        log_lower=n*iv.log(top_lower)
        log_upper=iv.log(top_upper**n+remainder*other.b**(n-power))
        # Same-mode cancellation gives a much sharper spatial-purity bound.
        relative_tail=remainder*other.b**(n-power)/(top_lower**n)
        S_lower=1/(1+relative_tail)**2
        defect=(2*relative_tail+relative_tail**2)/(1+relative_tail)**2
        bounds[n]=(log_lower,log_upper)
        result['rings'].append({'n':n,'log_normalized_Z_lower':lo(log_lower),
            'log_normalized_Z_upper':hi(log_upper),
            'log_normalized_Z_width_upper':hi(log_upper-log_lower),
            'spatial_purity_lower':lo(S_lower),
            'spatial_defect_upper':hi(defect)})
    return result,bounds

def run(degree=96,sector_aware=False):
    moment_path=ROOT/f'data/open_moments_exact_degree{degree}.json'
    if degree==24 and not moment_path.exists():moment_path=ROOT/'data/open_moments_exact.json'
    data=json.loads(moment_path.read_text())
    records={r['n']:r for r in data['chains']};assert len(records)==6
    betas=['0.0078125','0.015625','0.03125','0.0625','0.125','0.25','0.375','0.5','0.625','0.75','1']
    twisted=None
    if sector_aware:
        t=json.loads((ROOT/'data/twisted4_moments_exact_degree192.json').read_text())
        twisted={r['twist']:r for r in t['records']}
        betas+=['1.25','1.5','2','2.5']
    rows=[];bounds={}
    for beta in betas:
        row,box=acquire(beta,records,twisted=twisted);rows.append(row)
        if box is not None:bounds[beta]=box
    purities=[]
    for beta,double in [('0.0078125','0.015625'),('0.015625','0.03125'),('0.03125','0.0625'),('0.0625','0.125'),('0.125','0.25'),('0.25','0.5'),('0.375','0.75'),('0.5','1')]:
        if beta not in bounds or double not in bounds:continue
        for n in [128,256]:
            a0,a1=bounds[beta][n];b0,b1=bounds[double][n]
            lower=b0-2*a1-n*iv.log(5);upper=b1-2*a0-n*iv.log(5)
            purities.append({'n':n,'beta':float(beta),'logT_lower':lo(lower),
                'logT_upper':hi(upper),'logT_width_upper':hi(upper-lower),
                'scope':'Actual uniform spin-two periodic ring, all physical and spatial eigenvalues included by the source-kernel identities and counted even-moment tail.'})
    result={'status':'ACTUAL_COMPRESSED_HIGH_TEMPERATURE_TRANSFER_INPUTS',
        'open_chain_trace_moment_degree':degree,
        'local_source_kernel':'Continuous-time merged-history kernel, vacuum atom of mass1.',
        'kernel_moment_identity':'<vac,K_beta^r vac>=Z_open,r(beta)',
        'complete_even_moments':'TrK²=Tr exp(-2beta h_pair); TrK⁴=Z_periodic4(beta).',
        'source_dimensions':'Three Krylov coefficients plus six certified open-chain trace functions; no history cutoff or finite-rank assumption.',
        'rows':rows,'acquired_long_ring_thermal_purities':purities,
        'cold_bootstrap_seed_acquired':False}
    tag='_A4'if sector_aware else ''
    path=ROOT/f'data/vacuum_krylov_transfer_degree{degree}{tag}.json';path.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2));return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=96);p.add_argument('--sector-aware',action='store_true');a=p.parse_args();run(a.degree,a.sector_aware)
