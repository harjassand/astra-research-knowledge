"""Sharp HS-lift obstruction and an acquired all-p>=2 repair.

All large-chain evaluations use closed-form local spin-two dimer spectra and
directed scalar arithmetic. No exponential Hilbert space is instantiated.
"""
import pathlib,json,math
import mpmath as mp
mp.iv.dps=90;iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent
def lo(q):return math.nextafter(float(q.a),-math.inf)
def hi(q):return math.nextafter(float(q.b),math.inf)
def log10hi(q):return hi(iv.log(q)/iv.log(10))


def dimer_partition(beta,n):
    assert n%2==0
    # Shift each dimer by6: exact eigenvalues0,1,3,6,10, degeneracies1,3,5,7,9.
    z=sum(d*iv.exp(-beta*e)for d,e in [(1,0),(3,1),(5,3),(7,6),(9,10)])
    return z**(n//2)


def run():
    (ROOT/'data').mkdir(exist_ok=True)
    n=400;eps=iv.mpf('0.000001');beta=iv.mpf(1)/96
    s=iv.sqrt(dimer_partition(2*beta,n));t=iv.sqrt(dimer_partition(4*beta,n));amplitude=eps*s
    # M=Y+amplitude*P_ground is positive, commuting, and an explicit small MPO.
    # Its HS error relative toY is exactlyeps, while its squared error is exact:
    squared_error=(2*amplitude+amplitude**2)/t
    uniform_lower=eps**2*iv.exp(n*(iv.log(5)/2-12*beta))
    # For the UNIFORM spin-two chain, TrH=0 gives Z(2beta)>=5^n, while
    # Emin>=-6n gives sqrtZ(4beta)<=5^(n/2)*exp(12beta*n).
    # Adding known positive amplitude eps*5^(n/2) times a product projector
    # has HS relative error<=eps and squared-error ratio at leastuniform_lower.
    cold_beta=iv.mpf(20);cold_s=iv.sqrt(dimer_partition(2*cold_beta,n));discard=iv.sqrt(dimer_partition(2*cold_beta,n)-1)
    rayleigh=iv.mpf(1);L=rayleigh-discard;assert lo(L)>0
    eta=discard/L;q=8;lift=3*eta*q*iv.exp(3*eta*q)
    # Here M=P_ground and the tail is exactly known from the local spectrum.
    # The norm bridge uses||error||p<=||error||2 forp>=2 and||Y||p>=L.
    result={'status':'DIRECTED_LONG_CHAIN_NORM_OBSTRUCTION_AND_LATE_TEMPERATURE_CLOSURE','n':n,'local_spin':2,'high_temperature_beta':'1/96','high_temperature_relative_HS_error':'1e-6','dimer_squared_relative_HS_error_log10_lower':lo(iv.log(squared_error)/iv.log(10)),'uniform_chain_squared_error_log10_lower':lo(iv.log(uniform_lower)/iv.log(10)),'uniform_chain_scope':'A positive rank-one product-projector perturbation of the actual Gibbs operator; no zero-temperature gap or ground-vector oracle is assumed in the bound. This is an obstruction to an HS-only guarantee, not an impossibility result for structured algorithms.','cold_dimer_beta':20,'cold_HS_discard_upper':hi(discard),'cold_checked_Rayleigh_lower':lo(L),'simultaneous_relative_error_all_p_ge_2_upper':hi(eta),'positive_lift_q':q,'positive_lift_relative_error_all_p_ge_2_upper':hi(lift),'low_temperature_premise':'Tail and ground projector acquired exactly from the physical spin-two dimer spectrum, not transferred to the uniform chain.','limitation':'The actual uniform-chain long-ring Gibbs MPO and its certified HS tail have not been acquired.'}
    (ROOT/'data/norm_bridge.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    return result


if __name__=='__main__':run()
