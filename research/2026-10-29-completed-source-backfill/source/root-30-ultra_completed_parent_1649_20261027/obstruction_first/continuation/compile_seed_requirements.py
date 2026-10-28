"""Directed relative-error budget for the actual positive Gibbs gate.

This compiles a finite local-model representation and needed scalar tolerance.
It does not contract the enormous time-history operator or claim a seed.
"""
import pathlib,json,math
import mpmath as mp
mp.iv.dps=80;iv=mp.iv
ROOT=pathlib.Path(__file__).resolve().parent
def lo(q):return math.nextafter(float(q.a),-math.inf)
def hi(q):return math.nextafter(float(q.b),math.inf)


def log_error(n,beta,steps):
    b=iv.mpf(beta);d=b/steps
    # Exact quadratic local gate relative error, including its physical
    # minimum eigenvalue; n*steps gate insertions are paid.
    eta=36*d**3*iv.exp(12*d)
    if hi(eta)>=1:return None
    gate=-n*steps*iv.log(1-eta)
    # Center every h at h+I, norm5. Matching even/odd layers have total
    # norm<=5n, and both nested commutator norms are<=1000n.
    # The exact Strang integral gives C=1000n/24+1000n/12=125n.
    # Conjugation norms contribute e^(3*d*5n), and log Lipschitz adds
    # e^(d*5n). Thus the log-partition error is the following expression.
    strang=125*n*b*d*d*iv.exp(20*n*d)
    return gate+strang


def sufficient_steps(n,beta,tolerance):
    budget=iv.mpf(tolerance);left=0;right=max(1,int(beta))
    while True:
        err=log_error(n,beta,right)
        if err is not None and hi(err)<lo(budget):break
        left=right;right*=2
    while right-left>1:
        middle=(left+right)//2;err=log_error(n,beta,middle)
        if err is not None and hi(err)<lo(budget):right=middle
        else:left=middle
    return {'n':n,'beta':beta,'log_partition_error_budget':tolerance,'sufficient_time_slices':right,'delta_upper':hi(iv.mpf(beta)/right),'log_partition_error_upper':hi(log_error(n,beta,right)),'finite_history_dimension':'9^'+str(right),'K_MPO_virtual_dimension':5,'Q_MPO_virtual_dimension':25,'meaning':'Finite uniform local tensor plus explicitly bounded Trotter/Taylor error, not a finite-rank compression or a tractable contraction.'}


def purity_from_norms(a_half,a_double_half,relative_hs_error):
    # A_half approximates exp(-beta*H_n/2), A_double_half the appropriate
    # numerator purification. This scalar interface applies to S or T.
    eta=iv.mpf(relative_hs_error);an=iv.mpf(a_half);anum=iv.mpf(a_double_half)
    zn=(an/(1+eta))**2,(an/(1-eta))**2
    znum=(anum/(1+eta))**2,(anum/(1-eta))**2
    return znum[0]/zn[1]**2,znum[1]/zn[0]**2


def run():
    (ROOT/'data').mkdir(exist_ok=True)
    rows=[sufficient_steps(n,b,'0.001')for n,b in [(128,64),(256,96),(512,128)]]
    eta=iv.mpf('0.001')
    # If computed candidate norms give a point purity0.90, this is the
    # dimension-free rigorous lower conversion. It is a tolerance example,
    # not an acquired uniform-chain purity.
    lower_factor=(1-eta)**4/(1+eta)**2
    upper_factor=(1+eta)**4/(1-eta)**2
    result={'status':'CONSTRUCTIVE_REPRESENTATION_BUDGET_NO_BOOTSTRAP_SEED','rows':rows,'candidate_relative_HS_error':'0.001','purity_multiplicative_lower_factor':lo(lower_factor),'purity_multiplicative_upper_factor':hi(upper_factor),'point_purity_0_90_certified_lower_if_inputs_acquired':lo(iv.mpf('.9')*lower_factor),'point_purity_0_90_is_acquired':False,'normalization':'Purities use norm ratios and require no supplied thermodynamic energy shift. Stage1 exact64 energy remains only a64-site result.'}
    (ROOT/'data/seed_requirements.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));return result


if __name__=='__main__':run()
