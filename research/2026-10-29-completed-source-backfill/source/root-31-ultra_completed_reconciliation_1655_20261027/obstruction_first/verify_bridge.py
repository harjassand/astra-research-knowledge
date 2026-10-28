"""Independent small arithmetic verifier; no optimizers or producer imports.

Replays rational moment inclusion and all-length positivity of the repaired
transfer spectrum, and the exact algebraic variational inequality. Full matrix
tail and MPS contractions have separate explicit recomputation commands.
"""
import pathlib,sys,json,math
from fractions import Fraction as F
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'sol6_openings_20261027/positive_current_operation/vendor'))
import mpmath as mp
mp.iv.dps=90;iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent

def frac_iv(q):return iv.mpf(q.numerator)/q.denominator
def lo(q):return math.nextafter(float(q.a),-math.inf)
def hi(q):return math.nextafter(float(q.b),math.inf)


def main():
    w=json.loads((ROOT/'data/moment_counting_witness_positive.json').read_text())
    assert w['status']=='EXACT_RATIONAL_MOMENTS_AND_ALL_LENGTH_POSITIVITY'
    J=[(int(r['multiplicity']),F(r['eigenvalue']))for r in w['J_spectrum']]
    N=[(int(r['multiplicity']),F(r['eigenvalue']))for r in w['N_spectrum_one_copy']]
    assert all(c>0 for c,x in J+N) and J[0]==(2,F(11,10))
    cap=F(1069,1000);v=F(11,10)
    assert all(abs(x)<cap for c,x in J[1:]+N)
    moments={};margins=[];upper_margins=[]
    for n in range(4,9):
        jm=sum(c*x**n for c,x in J);nm=sum(c*x**n for c,x in N)
        for p,z in [(0,jm+3*nm),(1,jm-nm)]:
            cert=json.loads((ROOT/f'data/trace_n{n}_p{p}_b12.json').read_text())
            assert cert['status']=='DIRECTED_SCALAR_ENCLOSURE_UNDER_DECLARED_IEEE_MATRIX_MODEL'
            lower,upper=F(cert['trace_lower']),F(cert['trace_upper']);assert lower<z<upper
            margins.extend([z-lower,upper-z]);upper_margins.append(upper-z);moments[n,p]=z
            assert all(b['positive_lift_margin_lower']>0 for b in cert['blocks'])
            assert sum(b['dimension']*b['multiplicity']for b in cert['blocks'])==5**n
    count=sum(c for c,x in J+N);stop=741
    tail=2-3*count*(frac_iv(cap/v))**stop;assert lo(tail)>0
    powersJ=[iv.mpf(1)for x in J];powersN=[iv.mpf(1)for x in N]
    ratiosJ=[frac_iv(x/v)for c,x in J];ratiosN=[frac_iv(x/v)for c,x in N]
    minimum=float('inf');at=None
    for n in range(1,stop):
        powersJ=[p*x for p,x in zip(powersJ,ratiosJ)];powersN=[p*x for p,x in zip(powersN,ratiosN)]
        if n<4:continue
        j=sum(c*p for (c,x),p in zip(J,powersJ));nn=sum(c*p for (c,x),p in zip(N,powersN))
        for label,z in [('I',j+3*nn),('P',j-nn)]:
            assert lo(z)>0,(n,label,lo(z))
            if lo(z)<minimum:minimum,at=lo(z),[n,label]
    # A proper rotation has chi_1=1+2cos(theta) in [-1,3]. Every twisted
    # trace J+chi_1*N is between the two positive endpoint traces.
    # Two equal largest moduli imply p_max<=1/2 and spatial purity<=1/2.
    # Qualitative simplicity does not repair the quantitative finite input:
    # split the leading pair into v and v+epsilon, 0<epsilon<=1e-8.
    # Each acquired trace increases by at most this exact rational quantity.
    eps0=F(1,10**8);stability=8*eps0*(v+eps0)**7
    assert stability<min(upper_margins)

    trial=json.loads((ROOT/'data/mps_periodic_exact_n64.json').read_text())
    V,U0,U1=(int(trial[k])for k in ['V','U0','U1']);assert V>0 and trial['n']==64
    qlo=F(2449489742783178,10**15);qhi=F(2449489742783179,10**15)
    assert qlo*qlo<6<qhi*qhi
    qe=qhi if U1>=0 else qlo
    bound=F(U0)+qe*U1
    assert bound<F(-2*4761*V,1000)
    a=F(4761,1000);ar=F('4.76124816');beta=F(12)
    scaled=[]
    for n in range(4,9):
        factor=iv.exp(frac_iv(beta*n*(ar-a)))
        for p in [0,1]:
            cert=json.loads((ROOT/f'data/trace_n{n}_p{p}_b12.json').read_text())
            interval=iv.mpf([cert['trace_lower'],cert['trace_upper']])*factor
            model=frac_iv(moments[n,p])*factor
            assert lo(model)>=lo(interval) and hi(model)<=hi(interval)
            scaled.append({'n':n,'twist':p,'lower':max(0.,lo(interval)),'upper':hi(interval)})
    # The scaled countermodel X'=exp[12*(ar-a)]X still has two equal
    # leading modes and positive twisted traces. The actual MPS certifies
    # Z64(b)>1 for every b>0 at a=4.761; the model satisfies it too.
    result={'status':'PASS','scope':__doc__,'exact_moment_comparisons':10,'smallest_exact_moment_margin':str(min(margins)),'all_length_positivity':{'finite_lengths':[4,740],'tail_from':741,'minimum_normalized_lower':minimum,'at':at,'tail_lower':lo(tail)},'spatial_purity_upper_all_even_lengths':'1/2','simple_leading_family':{'epsilon_range':'0<epsilon<=1/100000000','largest_eigenvalues':'11/10+epsilon,11/10','exact_moment_perturbation_upper':str(stability),'uniform_length_threshold_from_these_inputs':'No: for any finite N choose epsilon < min(eps0,(1.1/N)*log(5)) to keep purity<5/6 at every even n<=N.'},'model_dimension':sum(c for c,x in J)+3*sum(c for c,x in N),'exact_variational_shift':'4761/1000','variational_energy_upper':hi(frac_iv(bound/F(2*V))),'normalized_trace_boxes_at_acquired_shift':scaled,'limitations':['The matrix tail bounds rely on the declared IEEE product model and are replayed separately.','The source-local kernel and all-temperature physical Hamiltonian interface are not constructed by the transfer countermodel.','No spin-two uniform gap or computational advantage is proved.']}
    (ROOT/'data/bridge_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items()if k not in ['smallest_exact_moment_margin','normalized_trace_boxes_at_acquired_shift','scope']},indent=2))

if __name__=='__main__':main()
