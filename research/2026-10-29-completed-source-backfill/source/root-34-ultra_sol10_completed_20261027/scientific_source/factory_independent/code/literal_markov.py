"""Exact independent absorbing-chain outputs, rewards and joint time PGF."""
from fractions import Fraction as F
import pathlib,json,time,argparse,sys
from model import Chain,SOURCE,EFF,raw_reward
from exact_solve import ExactFactor,verify_system
sys.set_int_max_str_digits(0)
ROOT=pathlib.Path(__file__).resolve().parents[1]

def run(n,lam,exponent=2):
    begin=time.monotonic();chain=Chain(lam);states,initial,Q,R=chain.matrices(n);S=len(states)
    A=[[F(i==j)-Q[i][j]for j in range(S)]for i in range(S)]
    print('CHAIN',n,'states',S,'built',time.monotonic()-begin,flush=True)
    fact=ExactFactor(A);print('FACTORED',n,time.monotonic()-begin,flush=True)
    U=fact.solve(R);verify_system(A,U,R)
    assert all(sum(row)==1 and min(row)>=0 for row in U)
    V=fact.solve(U);verify_system(A,V,U)
    reward=[raw_reward(n,s)for s in states]
    rhs=[[reward[i]*x for x in U[i]]for i in range(S)]
    C=fact.solve(rhs);verify_system(A,C,rhs)
    law=U[initial];time_joint=V[initial];source_joint=C[initial]
    mean=sum(k*p for k,p in enumerate(law));wall=sum(time_joint);source=sum(source_joint)
    covariance=sum(k*p for k,p in enumerate(time_joint))-mean*wall
    fusion=fact.solve([[(1-reward[i])*sum(U[i])]for i in range(S)])[initial][0]
    assert source+fusion==wall
    print('REWARDS',n,time.monotonic()-begin,flush=True)
    z=F(lam)**exponent
    Az=[[F(i==j)-z*Q[i][j]for j in range(S)]for i in range(S)]
    Bz=[[z*x for x in row]for row in R]
    Z=ExactFactor(Az).solve(Bz);verify_system(Az,Z,Bz)
    result={'status':'EXACT_LITERAL_ABSORBING_CHAIN_FULL_STATE_TIME_REWARDS',
      'n':n,'lambda':str(F(lam)),'source':list(map(str,SOURCE)),'efficiency':str(EFF),
      'transient_states':S,'reachable_transient_states':S,'time_cutoff':None,
      'exact_output_probabilities':list(map(str,law)),
      'exact_joint_photon_wall_first_moments':list(map(str,time_joint)),
      'exact_joint_photon_source_first_moments':list(map(str,source_joint)),
      'exact_mean':str(mean),'exact_expected_clocks':str(wall),'exact_expected_sources':str(source),
      'exact_expected_fusions':str(fusion),'exact_photon_time_covariance':str(covariance),
      'joint_pgf_z':str(z),'joint_pgf_lambda_exponent':exponent,
      'exact_joint_pgf_probabilities':list(map(str,Z[initial])),
      'display':{'mean':float(mean),'clocks':float(wall),'sources':float(source),
                 'fusions':float(fusion),'Cov_photon_time':float(covariance)},
      'all_linear_systems_checked_exactly':True,
      'maximum_result_numerator_bits':max(x.numerator.bit_length()for row in U+V+C+Z for x in row),
      'maximum_result_denominator_bits':max(x.denominator.bit_length()for row in U+V+C+Z for x in row),
      'elapsed_seconds':time.monotonic()-begin,
      'scope':'Supplied number-diagonal model only; no useful distilled quantum resource or physical acquisition.'}
    stem=f'n{n}_lambda{F(lam).numerator}_{F(lam).denominator}'
    (ROOT/f'results/literal_{stem}.json').write_text(json.dumps(result,indent=2)+'\n')
    data={'n':n,'lambda':str(F(lam)),'initial_index':initial,'states':states,'source_reward':reward,
          'Q_sparse':[[(j,str(p))for j,p in enumerate(row)if p]for row in Q],
          'R_sparse':[[(k,str(p))for k,p in enumerate(row)if p]for row in R]}
    (ROOT/f'results/chain_{stem}.json').write_text(json.dumps(data,indent=2)+'\n')
    print('COMPLETED',n,result['display'],'seconds',result['elapsed_seconds'],flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=4);p.add_argument('--lambda',dest='lam',default='999/1000');a=p.parse_args()
    assert a.n>0 and a.n&(a.n-1)==0
    run(a.n,F(a.lam))
