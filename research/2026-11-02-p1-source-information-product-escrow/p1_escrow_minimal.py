#!/usr/bin/env python3
"""P1 physical product-escrow theorem, minimal executable adversarial test.
Standard library. All numbers illustrative, NOT measured optical/reactor data.
This mathematical code does NOT acquire spectral, pressure, photon, or leak bounds.
"""
from math import expm1, log, sqrt
F = 96485.33212
R = 8.314462618

def bounds(y, wmax, km_hi, ki_hi, other_hi, e,
           wmin=0.0, km_lo=0.0, tau_max=None):
    """Distribution-free CH4 mole interval for a whole-aperture observation.

    The spectral species class must cover ALL absorbers; otherwise invalid.
    w has units m^-2, k has units m^2/mol, observed 0<=y<=1.
    """
    assert 0 <= y <= 1 and 0 <= e <= 1
    assert km_hi > 0 and wmax > 0 and ki_hi >= 0 and other_hi >= 0
    lower = max(0., ((y-e)/wmax - ki_hi*other_hi)/km_hi)
    upper = None
    if tau_max is not None and wmin > 0 and km_lo > 0:
        assert tau_max >= 0
        alpha = -expm1(-tau_max)/tau_max if tau_max else 1.
        upper = (y+e)/(alpha*wmin*km_lo)
    return lower, upper

def ray_absorption(target_moles, interferent_moles, area, k_target, k_int):
    """Nonlinear Beer-Lambert full-aperture measured absorptance."""
    assert len(target_moles) == len(interferent_moles) and target_moles
    n = len(target_moles)
    assert min(target_moles+interferent_moles) >= 0
    per_ray_area = area/n
    return sum(-expm1(-(k_target*t+k_int*i)/per_ray_area)
               for t,i in zip(target_moles,interferent_moles))/n

def photon_hoeffding(n, delta):
    assert n > 0 and 0 < delta < 1
    return sqrt(log(2/delta)/(2*n))

def carbon_source_lower(batch_methane_lower, blank_ch4_upper,
                        other_carbon_upper):
    assert min([blank_ch4_upper,other_carbon_upper]+batch_methane_lower) >= 0
    return max(0.,sum(batch_methane_lower)-blank_ch4_upper-other_carbon_upper)

def main():
    # Hypothetical 2cm2 at 0.2 A/cm2 for 300 s with 60% CH4 FE.
    charge = .4*300
    methane = .6*charge/(8*F)
    volume = 1.e-4    # 0.1 L, hypothetical
    area = .02        # 200cm2 illuminated, hypothetical
    optical_path = .005
    total = 101325*volume/(R*298.15)
    km, ki, e = 1., .001, .0001  # hypothetical spectral envelope
    n = 1000
    per_ray = total/n
    assert methane < total
    assert methane < 100*per_ray
    uniform = [methane/n]*n
    clump = [0.]*n
    left = methane
    for j in range(n):
        x = min(per_ray,left)
        clump[j] = x
        left -= x
        if left <= 0:
            break
    patch = [methane/100 if j<100 else 0. for j in range(n)]
    layouts = {"uniform":uniform, "max_clump":clump,
               "ten_pct_patch":patch, "permuted":list(reversed(clump))}
    tau_max = km*(total/volume)*optical_path
    results = {}
    for name, tar in layouts.items():
        assert all(0 <= a <= per_ray for a in tar)
        other = [per_ray-x for x in tar]
        y = ray_absorption(tar,other,area,km,ki)
        low,hi = bounds(y,1/area,km,ki,total,e,
                        wmin=1/area,km_lo=km,tau_max=tau_max)
        assert low <= methane+1e-15, (name,low,methane)
        assert hi is not None and methane <= hi+1e-15
        results[name]=(y,low,hi)
    # Crucial impossibility for one-ray/aliquot optical measurement:
    # in clumped sample, a ray outside the CH4 patch has zero methane.
    assert clump[-1] == 0 and clump[0] > 0
    assert abs(results["max_clump"][0]-results["permuted"][0]) < 1e-13
    # Carbon-source provenance cannot be established from CH4 absorption
    # unless other feed carbon is inventoried or isotopically excluded.
    pyridine_carbon = (.0036/63.546)*.5 * 20 * 5
    print("P1 full-aperture synthetic adversarial certificate")
    for name,(y,lo,hi) in results.items():
        print(f"{name:15} y={y:.8f} N_CH4_LB={lo:.9f} "
              f"true_N={methane:.9f} N_CH4_UB={hi:.9f}")
    print(f"blind ray has CH4=0; shot noise M=1e11,d=1e-6: "
          f"{photon_hoeffding(10**11,1e-6):.8f}")
    print(f"5-min hypothetical methane={methane:.8f}mol; nominal "
          f"pyridine-carbon in source initial 500mL={pyridine_carbon:.7f}mol")
    assert carbon_source_lower([methane],0,pyridine_carbon)==0
    print("PASS: physical mixture cap, upper/lower, permutation, spot failure, provenance caveat")

if __name__ == "__main__":
    main()
