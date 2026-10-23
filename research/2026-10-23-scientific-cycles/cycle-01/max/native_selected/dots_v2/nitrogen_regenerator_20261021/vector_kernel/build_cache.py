"""Regenerate the pinned cache; no source-file modifications and no BVP calls."""
import os
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
import sys, time, json, hashlib, resource
from pathlib import Path
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent.parent / 'nitrogen_quench_recovery_20261021'
sys.path[:0] = [str(SOURCE / 'deps'), str(SOURCE)]
t0 = time.perf_counter()
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
import cantera as ct
from paper_model import gas_model

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if ct.__version__ != '3.2.0':
        raise RuntimeError('Rebuild is pinned to Cantera 3.2.0; revalidate another version.')
    g = gas_model()
    names = ['N2', 'O2', 'N', 'O', 'NO', 'NO2']
    assert g.species_names == names
    assert g.n_reactions == 7
    temps = np.linspace(200., 3500., 661)
    mu = np.empty((6, len(temps)))
    k = np.empty_like(mu)
    for i in range(6):
        for j, T in enumerate(temps):
            g.TPX = T, ct.one_atm, np.eye(6)[i]
            mu[i, j] = g.species_viscosities[i]
            k[i, j] = g.thermal_conductivity
    # Cubic interpolation in log(T), log(property); polynomial coefficients are
    # generated once with SciPy but runtime evaluation uses NumPy only.
    logT = np.log(temps)
    mu_coeff = CubicSpline(logT, np.log(mu), axis=1).c
    k_coeff = CubicSpline(logT, np.log(k), axis=1).c
    nasa = np.array([g.species(i).thermo.coeffs for i in range(6)])
    elements = np.array([[g.n_atoms(i, e) for i in range(6)] for e in ['N', 'O']])
    np.savez_compressed(ROOT / 'cache.npz', temperature=temps, log_temperature=logT,
                        pure_viscosity=mu, pure_conductivity=k,
                        mu_coeff=mu_coeff, conductivity_coeff=k_coeff,
                        nasa=nasa, molecular_weights=g.molecular_weights,
                        reactants=g.reactant_stoich_coeffs, products=g.product_stoich_coeffs,
                        element_atoms=elements)
    manifest = {
        'schema': 1, 'species': names, 'reaction_equations': g.reaction_equations(),
        'source_files': {str(p.relative_to(ROOT.parent.parent)): sha(p)
                         for p in [SOURCE / 'paper_model.py', SOURCE / 'sources/air.yaml']},
        'cache_sha256': sha(ROOT / 'cache.npz'),
        'constants': {'R_J_kmol_K': ct.gas_constant, 'avogadro_per_kmol': ct.avogadro,
                      'reference_pressure_Pa': ct.one_atm},
        'versions': {'cantera': ct.__version__, 'numpy': np.__version__, 'scipy_build_only': scipy.__version__},
        'transport': {'model': 'mixture-averaged', 'knots': len(temps), 'range_K': [200, 3500],
                      'spacing_K': 5, 'interpolation': 'not-a-knot cubic spline of log(property) in log(T)',
                      'viscosity_mixing': 'Wilke, tested independently against Cantera',
                      'conductivity_mixing': 'one half arithmetic plus one half harmonic mole-fraction mean, tested independently'},
        'thermo_declared_ranges_K': {s.name: [s.thermo.min_temp, s.thermo.max_temp] for s in g.species()},
        'scope': 'Exact supplied six-species seven-reaction thermal variant, not a new mechanism. N2 NASA below 300 K and R6 above 2200 K are source-model extrapolations. Transport fitted by Cantera over phase range then sampled over 200–3500 K; 200–300 K is transport extrapolation. No physical validity certificate.',
        'cache_build_wall_s_including_imports': time.perf_counter() - t0,
        'cache_build_max_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
