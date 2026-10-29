"""Outward source/offspring/envelope/positive-cell receiver, no simulation."""
from fractions import Fraction as F
from pathlib import Path
import json,time
from flint import arb,fmpq,ctx

ctx.prec=192
def b(x):
    x=F(x);return arb(fmpq(x.numerator,x.denominator))

def main():
    started=time.perf_counter();root=Path(__file__).parent
    rows=json.loads((root/'RADIAL_ROW_CERTIFICATE.json').read_text())
    assert rows['status']=='PASS_continuum_row_certificate'
    ordered=sorted(rows['head_admission'],key=lambda r:F(*r['v_interval'][0]))
    last=F(0)
    for row in ordered:
        lo,hi=(F(*x) for x in row['v_interval']);assert lo==last and hi>lo
        assert F(*row['row_bound_upper'])<F(99,100);last=hi
    assert last==8
    aa=max(abs(F(*r['controls'][0])) for r in ordered)
    cc=max(abs(F(*r['controls'][1])) for r in ordered)
    beta=b(F(3,4));D=b(F(1,3200))
    zbeta=(2*arb.pi())**F(3,8)*beta**F(-3,2)
    cbeta=zbeta/beta.sqrt();assert cbeta.upper()<4
    assert zbeta.upper()<b(F(16,5))
    nu0=2*(2/arb.pi()).sqrt()
    E_bound=16+b(F(8,3))+4+beta**F(-3,2)/nu0*(b(aa)+4*b(cc))
    assert E_bound.upper()<48
    # Explicit local positive-Picard time/head/tail qualifier.
    v=b(32)
    tail=4/(beta*(1-beta)*v*v)+beta**F(-3,2)*(-(1-beta)*v*v/2).exp()*(1+2*(2/(arb.pi()*beta)).sqrt()/v)
    assert tail.upper()<b(F(1,40))
    assert F(48)*34/F(200000)<F(1,100)
    assert F(1,40)+F(40,3200)<F(1,16)
    assert F(5,16384)<F(1,3200)
    def cdf(s,bb):
        s=b(s);return (s*(bb/2).sqrt()).erf()-s*(2*bb/arb.pi()).sqrt()*(-bb*s*s/2).exp()
    masses=[cdf(1,arb(1)),cdf(2,arb(1))-cdf(1,arb(1)),1-cdf(2,arb(1))]
    bm=[zbeta*cdf(1,beta),zbeta*(cdf(2,beta)-cdf(1,beta)),zbeta*(1-cdf(2,beta))]
    margins=[a-D*bb for a,bb in zip(masses,bm)]
    assert all(x.lower()>b(F(1,10)) for x in margins)
    assert (1+D*zbeta).upper()<b(F(1001,1000))
    offspring=b(F(99,100))+4*D*cbeta
    assert offspring.upper()<b(F(199,200))
    # Factory multiplier <=2+48/(1-1/400)<51; margin >=3/400.
    assert 2+F(48)/(1-F(1,400))<51
    factory_bound=F(19,2)*51/F(3,400)
    assert factory_bound==64600
    cube_inside_ratio=(2*arb.pi())**F(-3,8)*(-arb(6)).exp()
    assert cube_inside_ratio.lower()>D
    cube_a=1-(b(4)/arb(2).sqrt()).erf()**3
    cube_b=zbeta*(1-(b(4)*(beta/2).sqrt()).erf()**3)
    assert (cube_a-D*cube_b).lower()>0
    result={'status':'PASS_outward_completion_constants','certified_head_intervals':len(ordered),
        'max_control_a':str(aa),'max_control_c':str(cc),'beta':'3/4','D':'1/3200','delta':'1/16384',
        'Z_beta':str(zbeta),'C_beta':str(cbeta),'envelope_over_nu_bound':str(E_bound),
        'envelope_uniform_upper':48,'offspring_bound':str(offspring),'mean_nodes_upper':200,
        'factory_base_coins_per_branch_upper':int(factory_bound),
        'positive_picard_tail_at32':str(tail),'positive_picard_time':'1/200000',
        'cell_M_masses':list(map(str,masses)),'cell_M_beta_masses':list(map(str,bm)),
        'cell_positive_margins':list(map(str,margins)),'expected_cell_proposals':str(1+D*zbeta),
        'TV_equilibrium_prefactor':str(D*zbeta/2),'TV_decay_rate':str(nu0/200),
        'arbitrary_finite_cartesian_grid_cube':'[-4,4]^3 plus one overflow cell',
        'cube_inside_M_over_M_beta_lower':str(cube_inside_ratio),
        'cube_overflow_M_mass':str(cube_a),'cube_overflow_M_beta_mass':str(cube_b),
        'cube_overflow_positive_margin':str(cube_a-D*cube_b),
        'continuous_velocity_sampler_acquired':False,'elapsed_seconds':time.perf_counter()-started}
    (root/'COMPLETION_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
