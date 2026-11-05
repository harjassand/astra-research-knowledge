"""Reproduce isotope rank, measurement sensitivity and archived MC covariance checks.

Input archive: Riddell-Young (2025), DOI 10.5281/zenodo.17238656,
Riddell-Young_2025_dD_GlobMean.zip. No empirical OH estimate is inferred.
The covariance calculation uses the supplied ensemble trajectories without
rerunning the authors' stochastic global-mean reconstruction.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import openpyxl

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'dD_GlobMean/Riddell-Young_2025_dD_GlobMean/output'

def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + '\n')

def atom_coordinate(delta, standard_ratio):
    # Exact affine isotope-abundance coordinate, using fraction rather than ratio.
    return delta / (1 + standard_ratio * (1 + delta / 1000))

cm, cf, dm, df = -62., -44., -304.7, -193.4
catm, datm = -47.3, -78.4
kc, kd = 1.0054, 1.294
co = (1000 + catm) / kc - 1000
do = (1000 + datm) / kd - 1000
beta = (df - dm) / (cf - cm)
intercept = dm - beta * cm
transverse = do - intercept - beta * co
matrix = np.array([[1, 1, -1], [cm, cf, -co], [dm, df, -do]])
burden, separation, duration = 5400., 14.3, 3.
geometry = {
    'scope': 'Supplied endmembers and effective sink KIEs; trace coordinates for illustrative numerics, not a global OH inversion.',
    'matrix': matrix.tolist(),
    'rank': int(np.linalg.matrix_rank(matrix)),
    'determinant': float(np.linalg.det(matrix)),
    'source_line_slope': beta,
    'source_line_intercept': intercept,
    'OH_sink_c': co,
    'OH_sink_d': do,
    'transverse_contrast_per_mil': transverse,
    'assumed_inventory_Tg': burden,
    'OH_difference_Tg_per_year': separation,
    'D_signal_per_mil_over_3years': separation * abs(transverse) * duration / burden,
    'sigma_three_year_contrast_for_95percent_halfwidth_7point15_Tg_per_year': separation / 2 * abs(transverse) * duration / (burden * 1.96),
    'sigma_independent_endpoint_for_same_target': separation / 2 * abs(transverse) * duration / (burden * 1.96 * np.sqrt(2)),
}
standard_c, standard_d = .0111802, .00015576
cm1, cf1 = [atom_coordinate(x, standard_c) for x in [cm, cf]]
dm1, df1 = [atom_coordinate(x, standard_d) for x in [dm, df]]
co1, do1 = atom_coordinate(co, standard_c), atom_coordinate(do, standard_d)
beta1 = (df1 - dm1) / (cf1 - cm1)
intercept1 = dm1 - beta1 * cm1
transverse1 = do1 - intercept1 - beta1 * co1
matrix1 = np.array([[1, 1, -1], [cm1, cf1, -co1], [dm1, df1, -do1]])
geometry['exact_atom_fraction_coordinate_check'] = {
    'definition': 'c=1000[(13C fraction)/(standard 13C fraction)-1], d analogous D atomic fraction. Sink ratios still require supplied effective fractionation.',
    'standard_R_C': standard_c, 'standard_R_D': standard_d,
    'matrix': matrix1.tolist(), 'source_line_slope': beta1,
    'source_line_intercept': intercept1, 'transverse_contrast': transverse1,
    'determinant': float(np.linalg.det(matrix1)),
    'signal_over_3years_per_mil_fraction_coordinate': separation * abs(transverse1) * duration / burden,
}
save('dual_isotope_inverse.json', geometry)

covariance_results, design_results, manifest = [], [], []
for file in sorted(OUTPUT.glob('GlobMean_dD_iterations*.xlsx')):
    data = np.array(list(openpyxl.load_workbook(file, read_only=True, data_only=True).active.values), dtype=float)
    years, samples = data[:, 0].astype(int), data[:, 1:]
    index = {int(y): i for i, y in enumerate(years)}
    covariance = np.cov(samples)
    difference = samples[index[2022]] - samples[index[2019]]
    second_difference = samples[index[2022]] - 2 * samples[index[2019]] + samples[index[2016]]
    covariance_results.append({
        'file': file.name, 'N_MC': samples.shape[1],
        'total_change_mean': float(np.mean(samples[-1] - samples[0])),
        'total_change_sigma': float(np.std(samples[-1] - samples[0], ddof=1)),
        'change_2019_2022_mean': float(np.mean(difference)),
        'change_2019_2022_sigma': float(np.std(difference, ddof=1)),
        'rho_2019_2022': float(np.corrcoef(samples[index[2019]], samples[index[2022]])[0, 1]),
        'second_difference_2016_2019_2022_mean': float(np.mean(second_difference)),
        'second_difference_sigma': float(np.std(second_difference, ddof=1)),
        'OH_sigma_from_three_year_D_difference_Tg_per_year': float(np.std(difference, ddof=1) * burden / (duration * abs(transverse))),
        'OH_sigma_from_three_year_D_second_difference_Tg_per_year': float(np.std(second_difference, ddof=1) * burden / (duration * abs(transverse))),
    })
    np.savetxt(ROOT / (file.stem + '_covariance.csv'), covariance, delimiter=',', header=','.join(map(str, years)), comments='')
    manifest.append({'file': str(file.relative_to(ROOT)), 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    # Local Fisher/GLS design: constant burden and OH baseline, fixed signatures;
    # a step change in OH loss begins at 2020. Include D-isotope relaxation.
    # This is a prescribed temporal restriction, not a consequence of the data.
    for last in [2022, 2023]:
        selected = data[data[:, 0] <= last]
        times = selected[:, 0] + .5
        C = np.cov(selected[:, 1:])
        Cinv = np.linalg.inv(C)
        age = np.maximum(times - 2020, 0)
        relaxation = .1 / kd
        response = -transverse / burden * (-np.expm1(-relaxation * age)) / relaxation
        for nuisance in ['none', 'intercept', 'intercept+linear']:
            information = float(response @ Cinv @ response)
            if nuisance != 'none':
                X = np.ones((len(times), 1)) if nuisance == 'intercept' else np.c_[np.ones(len(times)), times-times.mean()]
                information -= float(response @ Cinv @ X @ np.linalg.solve(X.T @ Cinv @ X, X.T @ Cinv @ response))
            design_results.append({'file': file.name, 'through': last, 'nuisance': nuisance,
                'sigma_OH_step_Tg_per_year': information ** -.5,
                'signal_14point3_Tg_over_sigma': separation * information ** .5,
                'covariance_condition': float(np.linalg.cond(C))})

save('dual_isotope_covariance_check.json', {
    'scope': 'Supplied archived atmospheric-isotope MC trajectories only; no source-signature, sink fractionation, carbon isotope or 3-D transport error added. Calibration variants retained separately.',
    'results': covariance_results})
save('dual_isotope_GLS_design_check.json', {
    'scope': 'Local restricted-design calculation, not an empirical best fit. Fixed 5400 Tg burden, 0.1/year baseline OH, effective KIEs, source endmembers, and step onset2020. Carbon and nuisance fields supplied.',
    'results': design_results})
save('dual_isotope_input_hashes.json', manifest)
for r in covariance_results:
    print(r['file'], 'sigma difference=', round(r['change_2019_2022_sigma'], 6),
          'OH sigma=', round(r['OH_sigma_from_three_year_D_difference_Tg_per_year'], 4))
