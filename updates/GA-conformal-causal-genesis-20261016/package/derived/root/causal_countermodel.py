"""Finite diagnostics of the analytic switched-state countermodel; no material fit."""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
PRIOR_REL = Path('updates/FZ-positive-memory-genesis-20261016/package/derived/workers/fz_catalysis_evidence_acquisition/authored/analysis_results.json')
PRIOR = next((parent/PRIOR_REL for parent in ROOT.parents if (parent/PRIOR_REL).is_file()),
             Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')/PRIOR_REL)


def find_ratio(obj):
    if isinstance(obj, dict):
        if 'dynamic_to_static_ethane_ratio' in obj:
            return obj['dynamic_to_static_ethane_ratio']
        for value in obj.values():
            result = find_ratio(value)
            if result is not None:
                return result
    if isinstance(obj, list):
        for value in obj:
            result = find_ratio(value)
            if result is not None:
                return result
    return None


def main():
    blob = PRIOR.read_bytes()
    rho = find_ratio(json.loads(blob))
    if rho is None:
        raise RuntimeError('pinned source ratio absent')
    h, d, beta = 10.0, 0.1, 0.0
    deficit = h+d*beta-(h+d)*rho
    rows = []
    for mu in [1e-6, 1e-4, 1e-3, 1e-2, 3e-2, 5e-2]:
        integral = -math.expm1(-mu*h)/mu
        v = math.exp(-mu*h)
        z = deficit/integral
        if not 0 < z < 1:
            raise RuntimeError('inadmissible selected parameter')
        u = (1-z)/(1-z*v)
        lam = -math.log(u)/d
        mean = (h-z*integral+d*beta)/(h+d)
        if abs(mean-rho) >= 1e-13 or abs(z-(1-u+u*v*z)) >= 1e-13:
            raise RuntimeError('periodic identity diagnostic failed')
        rows.append({'mu_per_s':mu, 'lambda_per_s':lam,
                     'cycle_mean_ratio':mean, 'periodic_start_state':z,
                     'isolated_10s_suppression_area_s':(1-u)*integral,
                     'conditioned_omit_next_pulse_suppression_area_s':z*(-math.expm1(-mu*(h+d)))*integral,
                     'cycle_contraction':u*v, 'cycles_for_1_over_e_deviation':-1/math.log(u*v)})
    result = {'status':'finite floating diagnostics of exact analytic construction; not measured catalyst parameters',
              'source_revision':'f80a8f15137575133ad2c9af975513b32e8fa93e',
              'source_path':str(PRIOR), 'source_sha256':hashlib.sha256(blob).hexdigest(),
              'h_s':h, 'negative_s':d, 'rho_from_prior_FZ_final_figure2':rho,
              'beta_illustration_not_measured':beta, 'suppression_area_s':deficit,
              'models':rows}
    (ROOT/'CAUSAL_NONIDENTIFIABILITY_DIAGNOSTIC.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'models':len(rows), 'max_mean_error':max(abs(r['cycle_mean_ratio']-rho) for r in rows),
                      'small_mu_isolated_deficit_s':rows[0]['isolated_10s_suppression_area_s'],
                      'large_mu_isolated_deficit_s':rows[-1]['isolated_10s_suppression_area_s']}))


if __name__ == '__main__':
    main()
