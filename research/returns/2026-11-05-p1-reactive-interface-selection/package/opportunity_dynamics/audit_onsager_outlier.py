"""Independent read-only audit of one exported transport matrix.

Displayed yerr is only an interval scale, not a validated standard error.
No MD, parameter fit, numerical optimization, or source modification is used.
"""
from pathlib import Path
import json
import hashlib
import csv
import numpy as np
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'opportunity_root' / '41563_2026_2596_MOESM2_ESM.xlsx'
PHASE, TEMP, SCALE = 'Ba4Ti13O30', '1000.0K', 1e18
INDEX = {'Ba': 0, 'Ti': 1, 'O': 2}
workbook = load_workbook(SOURCE, read_only=True, data_only=True)
records, selected = [], []
L, E = np.zeros((3, 3)), np.zeros((3, 3))
for sheet in workbook:
    rows = sheet.iter_rows(values_only=True)
    columns = next(rows)
    for rownum, row in enumerate(rows, 2):
        record = dict(zip(columns, row))
        record.update(sheet=sheet.title, row=rownum)
        records.append(record)
        if record['formula'] == PHASE and record['temperature'] == TEMP:
            pair = record['subplot_ylabel'].split('{')[1].split('}')[0].split('-')
            i, j = map(INDEX.get, pair)
            L[i, j] = L[j, i] = record['y_raw'] / SCALE
            E[i, j] = E[j, i] = record['yerr'] / SCALE
            selected.append(record)

pairs = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
masses = np.array([137.327, 47.867, 15.999])
eigvals = np.linalg.eigvalsh(L)
corr = L / np.sqrt(np.outer(np.diag(L), np.diag(L)))

# Exact completion: retain the exported Ba/Ti principal block, impose Lm=0.
# If H=L[:2,:2] is PSD then this completion B H B^T is PSD automatically.
B = np.vstack([np.eye(2), -masses[:2]/masses[2]])
physical = B @ L[:2,:2] @ B.T
standardized_change = np.abs(physical-L)/E

signed_error_patterns = {}
for sign in (-1, 1):
    group = [r for r in records if sign*r['y_raw'] > 0]
    signed_error_patterns[str(sign)] = {
        'n':len(group),
        'exact_half_absolute_mean':int(sum(np.isclose(r['yerr']/abs(r['y_raw']), .5,
                                          rtol=1e-12, atol=1e-12) for r in group)),
        'largest_relative_error':max(r['yerr']/abs(r['y_raw']) for r in group)}

min_cross_at_one = max(abs(L[0,2])-E[0,2], 0)
max_diag_product_at_one = (L[0,0]+E[0,0])*(L[2,2]+E[2,2])
report = {
    'source':str(SOURCE), 'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'phase':PHASE, 'temperature':TEMP, 'species_order':['Ba','Ti','O'],
    'numerical_scale':SCALE, 'source_rows':selected,
    'L_in_units_1e18':L.tolist(), 'displayed_yerr_in_units_1e18':E.tolist(),
    'eigenvalues_in_units_1e18':eigvals.tolist(),
    'lambda_min_over_max':float(eigvals[0]/eigvals[-1]),
    'pairwise_correlation_matrix':corr.tolist(),
    'mass_null_relative_residual':float(np.linalg.norm(L@masses)/(np.linalg.norm(L,2)*np.linalg.norm(masses))),
    'one_displayed_error_box':{
        'minimum_abs_BaO':float(min_cross_at_one),
        'maximum_sqrt_BaBa_OO':float(np.sqrt(max_diag_product_at_one)),
        'can_be_PSD':bool(min_cross_at_one**2 <= max_diag_product_at_one)},
    'mass_COM_completion':{
        'matrix_in_units_1e18':physical.tolist(),
        'eigenvalues_in_units_1e18':np.linalg.eigvalsh(physical).tolist(),
        'BaTi_block_eigenvalues':np.linalg.eigvalsh(L[:2,:2]).tolist(),
        'entrywise_change_divided_by_displayed_yerr':standardized_change.tolist(),
        'largest_standardized_change':float(np.max(standardized_change)),
        'null_residual':float(np.linalg.norm(physical@masses)/(np.linalg.norm(physical,2)*np.linalg.norm(masses)))},
    'all_workbook_error_patterns':signed_error_patterns,
    'scope':'Algebraic checks of displayed estimates, not statistical inference or MD replication.'
}
archive = ROOT / 'BTO_Transport_Coefficients.csv'
archive_rows = list(csv.DictReader(archive.open()))
target = next(r for r in archive_rows if r['Formula']==PHASE and r['Temperature']==TEMP)
archived_L = np.array([[float(target[f'L{min(i,j)}{max(i,j)}'])
                       for j in range(3)] for i in range(3)])/SCALE
archived_E = np.array([[float(target[f'L{min(i,j)}{max(i,j)}_std'])
                       for j in range(3)] for i in range(3)])/SCALE
archived_physical = B @ archived_L[:2,:2] @ B.T
report['archive_crosscheck'] = {
    'url':'https://ndownloader.figshare.com/files/51681254',
    'archive_doi':'10.6084/m9.figshare.28207292',
    'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
    'source_record':target,
    'L_in_units_1e18':archived_L.tolist(),
    'standard_deviations_in_units_1e18':archived_E.tolist(),
    'mass_COM_completion_in_units_1e18':archived_physical.tolist(),
    'completion_eigenvalues':np.linalg.eigvalsh(archived_physical).tolist(),
    'entrywise_change_divided_by_archive_std':(np.abs(archived_physical-archived_L)/archived_E).tolist(),
    'largest_change_divided_by_archive_std':float(np.max(np.abs(archived_physical-archived_L)/archived_E))}
(ROOT/'onsager_outlier_countercheck.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['source_rows']},indent=2))
