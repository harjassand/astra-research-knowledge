"""Independent exact thermal-series gate; conditional Lifshitz model only.
No candidate code, floating quadrature or measured response inputs imported.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def atan_interval(x,n=40):
    s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
    other=s+(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,other),max(s,other)

def pi_interval():
    a,b=atan_interval(F(1,5)),atan_interval(F(1,239))
    return 16*a[0]-4*b[1],16*a[1]-4*b[0]

def exp_neg_upper(x,n=48):
    term=F(1);s=F(1)
    for k in range(1,n+1):term*=x/F(k);s+=term
    return 1/s

def envelope(L,T):
    ml,mh=pi_interval()
    pi_lo,pi_hi=F(3141592653589793,10**15),F(3141592653589794,10**15)
    assert pi_lo<=ml<mh<=pi_hi
    kb=F('1.380649e-23');h=F('6.62607015e-34');c=F(299792458)
    raw_tau=8*pi_lo*pi_lo*L*kb*T/(h*c)
    tau=F(raw_tau.numerator*10**8//raw_tau.denominator,10**8)
    raw_xi=4*pi_lo*pi_lo*kb*T/h
    xi1=F(raw_xi.numerator//raw_xi.denominator)
    if tau<=0 or xi1<=0:raise ValueError('chosen compact grid is too coarse for these parameters')
    raw_q=exp_neg_upper(tau)
    q=F(-((-raw_q.numerator*10**15)//raw_q.denominator),10**15)
    assert 0<q<1 and tau>0 and pi_hi>pi_lo>3
    # A(t)=3/2*(t+1)*exp(-t)+integral_t^infty x²/(exp(x)-1)dx.
    # For t>=tau, integral<=exp(-t)*(t²+2t+2)/(1-q).
    # A decreases with t. Substitute tau_lo and sum exact geometric moments.
    s0=q/(1-q);s1=q/(1-q)**2;s2=q*(1+q)/(1-q)**3
    all_j=F(3,2)*(tau*s1+s0)+(tau*tau*s2+2*tau*s1+2*s0)/(1-q)
    # For sum A(j*tau)/j² use sum q^j/j and /j² <=sum q^j.
    weighted=s0*(F(3,2)*(tau+1)+(tau*tau+2*tau+2)/(1-q))
    c_upper=all_j/(8*pi_lo)
    s_upper=weighted/(8*pi_lo*L**3*xi1**2)
    return {'tau_lower':tau,'q_upper':q,
            'C_coefficient_upper':c_upper,'S_total_coefficient_upper':s_upper,
            'pi_lower':pi_lo,'pi_upper':pi_hi}

def record(x):return {'exact_rational':str(x),'display':float(x)}

def main():
    L=F(1,200000);T=F(300);b=envelope(L,T)
    t=F(9,11)
    ln10_lower=2*sum((t**(2*k+1)/F(2*k+1) for k in range(100)),F(0))
    contrast_required=ln10_lower*L**3/b['C_coefficient_upper']
    sum_required=ln10_lower/b['S_total_coefficient_upper']
    assert b['C_coefficient_upper']<F(1062,10**6)
    assert contrast_required>F('2.71e-13')
    assert b['C_coefficient_upper']<F('0.001060685106292')
    assert b['S_total_coefficient_upper']<F('1.392489440339e-16')
    assert contrast_required>F('2.71355876420e-13')
    assert sum_required>F('1.65357454519e16')
    # Declared VERY loose physical-constant enclosures, consistent with live
    # NIST2022CODATA pages; these empirical premises are not exact SI definitions.
    me_lower,eps_lower,e=F('9.1e-31'),F('8.85e-12'),F('1.602176634e-19')
    assert e*e/(me_lower*eps_lower)<3200
    per_Z=b['S_total_coefficient_upper']*3200
    assert per_Z*1000<F('4.5e-10')
    assert per_Z*1000<F('4.456e-10')
    result={'scope':'conditional fixed-Drude interplate chemical-potential contrast; no local barrier/rate claim',
      'L_m':str(L),'T_K':str(T),
      'bounds':{k:record(v) for k,v in b.items()},
      'necessary_C_over_n_for_tenfold_equilibrium_quotient_m3_lower':record(contrast_required),
      'necessary_S_total_for_tenfold_equilibrium_quotient_m3_per_s2_lower':record(sum_required),
      'conservative_bound_per_Z_AB':record(per_Z),
      'bound_for_Z_AB_at_most_1000':record(per_Z*1000),
      'coarse_physical_constant_premises':{'electron_mass_lower_kg':str(me_lower),'vacuum_permittivity_lower_F_per_m':str(eps_lower)},
      'constant_sources':['https://physics.nist.gov/cgi-bin/cuu/Value?me','https://physics.nist.gov/cgi-bin/cuu/Value?ep0'],
      'SI_defining_constants_h_kB_c_e_exact':True,'physical_response_or_source_model_acquired':False,
      'decisions_use_only_exact_rationals':True}
    Path(__file__).with_name('EXACT_GATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'C_coefficient_upper':float(b['C_coefficient_upper']),
      'S_total_coefficient_upper':float(b['S_total_coefficient_upper']),
      'necessary_C_over_n_lower':float(contrast_required),'necessary_S_total_lower':float(sum_required)}))

if __name__=='__main__':main()
