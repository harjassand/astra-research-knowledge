"""Summarize existing floating-point artifacts; does not run an optimizer."""
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
rows = [json.loads(line) for line in (ROOT / 'sdp_results.jsonl').read_text().splitlines()]
group = {}
for row in rows:
    key = (row['d'], row['rank_bound'], 'complex' if 'complex' in row['name'] else 'real',
           'isotropic' if 'isotropic' in row['name'] else ('near_diagonal' if 'delta' in row['name'] else 'random'))
    group[str(key)] = group.get(str(key), 0) + 1

worst = {'max_equality_frobenius_residual': 0., 'min_compatible_R_eigenvalue': 0.,
         'min_compatible_T_eigenvalue': 0., 'min_PPT_E_eigenvalue': 0.,
         'min_PPT_E_partial_transpose_eigenvalue': 0.,
         'min_canonical_PPT_W_eigenvalue': 0.,
         'min_canonical_PPT_W_partial_transpose_eigenvalue': 0.}
residuals = []
for row in rows:
    raw = np.load(ROOT / (row['name'] + '.npz'))
    d = row['d']
    R, J, E, T = (raw[k] for k in ['R', 'J', 'E', 'T'])
    F = np.zeros((d*d, d*d))
    for i in range(d):
        for j in range(d):
            F[i*d+j, j*d+i] = 1
    U = np.zeros((d**3, d**3))
    for i in range(d):
        for j in range(d):
            for k in range(d):
                U[(i*d+j)*d+k, (i*d+k)*d+j] = 1
    eye = np.eye(d)/d
    def margins(Z):
        z = Z.reshape(d,d,d,d)
        return np.trace(z,axis1=0,axis2=2), np.trace(z,axis1=1,axis2=3)
    def pt(Z):
        return Z.reshape(d,d,d,d).transpose(2,1,0,3).reshape(d*d,d*d)
    local = [np.linalg.norm(R-U@R@U.T), np.linalg.norm(J-F@J.T@F),
             np.linalg.norm(E-F@E.T@F),
             np.linalg.norm(J-np.trace(R.reshape(d,d,d,d,d,d),axis1=2,axis2=5).reshape(d*d,d*d))]
    for Z in [J,E]:
        local.extend(np.linalg.norm(m-eye) for m in margins(Z))
    worst['min_compatible_R_eigenvalue'] = min(worst['min_compatible_R_eigenvalue'], float(np.linalg.eigvalsh(R)[0]))
    worst['min_compatible_T_eigenvalue'] = min(worst['min_compatible_T_eigenvalue'], float(np.linalg.eigvalsh(T)[0]))
    worst['min_PPT_E_eigenvalue'] = min(worst['min_PPT_E_eigenvalue'], float(np.linalg.eigvalsh(E)[0]))
    worst['min_PPT_E_partial_transpose_eigenvalue'] = min(worst['min_PPT_E_partial_transpose_eigenvalue'], float(np.linalg.eigvalsh(pt(E))[0]))
    if 'W' in raw:
        W=raw['W']; P=(np.eye(d*d)+F)/2
        local.append(np.linalg.norm(W-P@W@P))
        local.extend(np.linalg.norm(m-eye) for m in margins(W))
        worst['min_canonical_PPT_W_eigenvalue'] = min(worst['min_canonical_PPT_W_eigenvalue'], float(np.linalg.eigvalsh(W)[0]))
        worst['min_canonical_PPT_W_partial_transpose_eigenvalue'] = min(worst['min_canonical_PPT_W_partial_transpose_eigenvalue'], float(np.linalg.eigvalsh(pt(W))[0]))
    worst['max_equality_frobenius_residual'] = max(worst['max_equality_frobenius_residual'],float(max(local)))
    residuals.append({'name':row['name'],'max_equality_frobenius_residual':float(max(local))})

def best(field, random_only=False):
    eligible=[r for r in rows if field in r and (not random_only or 'isotropic' not in r['name'])]
    r=max(eligible,key=lambda r:r[field])
    return {'name':r['name'],'value':r[field]}
result = {'status':'FINITE_DIAGNOSTIC_ONLY','count':len(rows),'groups':group,
          'max_ordinary_PPT_ratio':best('gap_ratio'),
          'max_canonical_PPT_ratio':best('canonical_ppt_ratio'),
          'max_random_canonical_PPT_ratio':best('canonical_ppt_ratio',True),
          'constraint_diagnostics':worst,'per_artifact_equality_diagnostics':residuals,
          'interpretation':'No certified counterexample, optimum, feasibility or EB membership. Ratios use lower bounds on EB losses from PPT relaxations, not unrestricted EB losses.'}
(ROOT/'sdp_summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='per_artifact_equality_diagnostics'},indent=2))
