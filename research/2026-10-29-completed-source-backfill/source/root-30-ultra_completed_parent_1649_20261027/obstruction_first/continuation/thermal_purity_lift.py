"""Finite normalized-purity input compiler for the all-temperature bridge.

The temperature-coupling identity is source Eq.(5.10), not new here. Its
interval budget and actual high-temperature long-ring warm bound are made
explicit. Cold uniform-chain inputs remain unacquired. The replay on physical
spin-two dimers is only a known solvable control, never uniform-chain evidence.
"""
import pathlib,json,math
import mpmath as mp
mp.iv.dps=110;iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent
def lo(x):return math.nextafter(float(x.a),-math.inf)
def hi(x):return math.nextafter(float(x.b),math.inf)

def warm_error(L,beta):
    # Linked-cluster coefficients of normalized Z_2L and Z_L^2 agree through
    # degree L-1. Both operators have norm<=12L. Pay both entire-series tails.
    x=12*L*beta
    return 2*iv.exp(x)*x**L/math.factorial(L)

def dimer_log_z(beta):
    return iv.log(sum(d*iv.exp(-beta*e)for d,e in [(1,0),(3,1),(5,3),(7,6),(9,10)]))

def dimer_log_T(n,beta):
    return (n//2)*(dimer_log_z(2*beta)-2*dimer_log_z(beta))

def lift(log_s0,rows):
    s=log_s0
    for row in rows:s=2*s+row['logT_2L']-2*row['logT_L']
    return s

def run():
    (ROOT/'data').mkdir(exist_ok=True)
    L=128;beta_end=iv.mpf(64);K=13;beta0=beta_end/(2**K)
    warm=warm_error(L,beta0);assert hi(warm)<1
    budget=iv.mpf('0.001');tolerances=[];oracle=[];padded=[]
    for k in range(K):
        b=beta0*2**k;weight=2**(K-1-k)
        # Each pair contributes error <=weight*(epsilon+2epsilon).
        eps=budget/(3*K*weight)
        tolerances.append({'k':k,'beta':float(b.mid),'final_log_error_weight':weight,
            'required_each_log_purity_error_at_most':lo(eps),
            'rings':[L,2*L],'uniform_chain_inputs_acquired':False})
        p=dimer_log_T(L,b);q=dimer_log_T(2*L,b)
        oracle.append({'logT_L':p,'logT_2L':q})
        padded.append({'logT_L':p+iv.mpf([-1,1])*eps,
                       'logT_2L':q+iv.mpf([-1,1])*eps})
    # Dimer S is exactly1 at every even length; use its exact initial value.
    exact_control=lift(iv.mpf(0),oracle)
    padded_control=lift(iv.mpf(0),padded)
    assert lo(exact_control)<0<hi(exact_control)
    # This is the actual uniform-model initial condition, not a dimer input.
    worst_initial_contribution=2**K*iv.log(1-warm)
    residual_budget=budget-worst_initial_contribution
    # If future point inputs yield exp(logS)=.90, this is its certified lower.
    conditional_lower=iv.mpf('.90')*iv.exp(-residual_budget)
    result={'status':'ACTUAL_LONG_RING_WARM_INPUT_AND_CONDITIONAL_NORMALIZED_TEMPERATURE_COMPILER',
        'L':L,'double_ring':2*L,'cold_beta':64,'temperature_doublings':K,
        'uniform_initial_beta':'1/128',
        'uniform_initial_spatial_defect_upper':hi(warm),
        'uniform_initial_spatial_defect_log10_upper':hi(iv.log(warm)/iv.log(10)),
        'initial_log_error_after_all_doublings_upper':hi(-worst_initial_contribution),
        'initial_bound_uses_gap_or_variational_energy':False,
        'thermal_input_table':tolerances,
        'additional_final_input':'T(256,64), the double-ring temporal purity in Tasaki Theorem6.2; unacquired for uniform chain.',
        'total_normalized_purity_inputs':2*K+1,
        'final_logS_error_budget':'0.001',
        'if_future_point_S_is_0_90_certified_lower':lo(conditional_lower),
        'point_S_0_90_acquired':False,
        'dimer_control':{
            'n':L,'known_model':'H=sum of uncoupled spin-two dimers; shifted dimer energies0,1,3,6,10.',
            'exact_oracle_lift_logS_lower':lo(exact_control),
            'exact_oracle_lift_logS_upper':hi(exact_control),
            'padded_input_lift_logS_lower':lo(padded_control),
            'padded_input_lift_logS_upper':hi(padded_control),
            'padded_spatial_purity_lower':lo(iv.exp(padded_control)),
            'final_double_ring_temporal_purity_lower':lo(iv.exp(dimer_log_T(2*L,beta_end))),
            'transfer_to_uniform_chain':False},
        'missing_acquisition':'Certified relative thermal purities at the27 specified ring/temperature inputs. The interval/open-chain local-purity theorem does not supply periodic loop corrections or constants for free.'}
    # Stronger restart from the actual compressed-kernel acquisition. This
    # does not mark any uncomputed cold T as acquired.
    warm_path=ROOT/'data/vacuum_krylov_transfer_degree192_A4.json'
    if warm_path.exists():
        acquired=json.loads(warm_path.read_text())
        warm_row=next(r for r in acquired['rows']if r['beta_exact']=='0.75')
        warm_ring=next(r for r in warm_row['rings']if r['n']==256)
        delta=iv.mpf(warm_ring['spatial_defect_upper']);kk=7;bb=iv.mpf(3)/4
        initial_debt=2**kk*delta/(1-delta)
        remaining_budget=budget-initial_debt
        table=[]
        for k in range(kk):
            weight=2**(kk-1-k);eps=remaining_budget/(3*kk*weight)
            table.append({'beta':float((bb*2**k).mid),'rings':[256,512],
                'required_each_log_purity_error_at_most':lo(eps),
                'thermal_inputs_acquired':False})
        result['acquired_A4_warm_restart']={'L':256,'warm_beta':'3/4',
            'spatial_defect_upper':warm_ring['spatial_defect_upper'],
            'warm_spatial_input_acquired':True,'cold_beta':96,'doublings':kk,
            'propagated_initial_log_error_upper':hi(initial_debt),
            'final_logS_error_budget_including_initial_debt':'0.001',
            'thermal_input_table':table,'additional_final_input':'T(512,96), unacquired',
            'total_normalized_thermal_inputs':15,'cold_seed_acquired':False}
    (ROOT/'data/thermal_purity_lift.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result

if __name__=='__main__':run()
