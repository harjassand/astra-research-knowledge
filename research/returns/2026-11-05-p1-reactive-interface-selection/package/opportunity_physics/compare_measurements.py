"""Reproduce table-based electrolyte comparison. Standard library only.
Input is a manual transcription of Tables 1-2, Bergstrom/McCloskey 2024,
https://doi.org/10.1021/acsenergylett.3c01662 . No fitted model parameters.
The reported +/- entries are retained without assuming SD, SEM or CI.
"""
from pathlib import Path
import json
p = Path(__file__).resolve().parent
rows = json.loads((p / 'bergstrom2024_tables.json').read_text())
h = next(x for x in rows if x['ratio'] == '1:2:0')
l = next(x for x in rows if x['ratio'] == '1:2:1')
r = {}
for k in ['eta_mPas', 'kappa_mScm', 'D_1e7_cm2s', 't_lab', 'chi']:
    r[k + '_ratio_LHCE_HCE'] = l[k] / h[k]
r['walden_predicted_kappa_ratio'] = (l['c_M'] / h['c_M']) * (h['eta_mPas'] / l['eta_mPas'])
r['walden_overprediction_factor'] = r['walden_predicted_kappa_ratio'] / r['kappa_mScm_ratio_LHCE_HCE']
r['kappa_t_HCE'] = h['kappa_mScm'] * h['t_lab']
r['kappa_t_LHCE'] = l['kappa_mScm'] * l['t_lab']
r['kappa_t_ratio'] = r['kappa_t_LHCE'] / r['kappa_t_HCE']
r['kappa_ratio_reported_pm_box'] = [
    (l['kappa_mScm'] - l['kappa_err']) / (h['kappa_mScm'] + h['kappa_err']),
    (l['kappa_mScm'] + l['kappa_err']) / (h['kappa_mScm'] - h['kappa_err'])]
r['kappa_t_ratio_reported_pm_box'] = [
    (l['kappa_mScm'] - l['kappa_err']) * (l['t_lab'] - l['t_err']) /
    ((h['kappa_mScm'] + h['kappa_err']) * (h['t_lab'] + h['t_err'])),
    (l['kappa_mScm'] + l['kappa_err']) * (l['t_lab'] + l['t_err']) /
    ((h['kappa_mScm'] - h['kappa_err']) * (h['t_lab'] - h['t_err']))]
r['warning'] = ('Reported plus/minus box extrema, not a statistical confidence interval. '
                'Covariances and original uncertainty interpretation not established from accessible main text.')
(p / 'comparison_results.json').write_text(json.dumps(r, indent=2) + '\n')
print(json.dumps(r, indent=2))
