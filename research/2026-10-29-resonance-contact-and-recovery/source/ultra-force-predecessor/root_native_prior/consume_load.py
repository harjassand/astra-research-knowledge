"""Conditional assembly load receiver; no physical calibration is assumed."""
from pathlib import Path
import json, random, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

started = time.perf_counter()
rng = random.Random(29102026)
side = 64
occupied = set()
frontier = {(1, 1)}
rows, columns = {}, {}
max_stress = 0
max_residual = 0
checks = 0
while frontier:
    v = rng.choice(sorted(frontier))
    frontier.remove(v)
    i, j = v
    assert (i == 1 or (i-1, j) in occupied)
    assert (j == 1 or (i, j-1) in occupied)
    occupied.add(v)
    rows[j] = i
    columns[i] = j
    for a, b in ((i+1, j), (i, j+1)):
        if a <= side and b <= side and (a, b) not in occupied:
            if (a == 1 or (a-1, b) in occupied) and (b == 1 or (a, b-1) in occupied):
                frontier.add((a, b))
    def tail(a, b, last):
        return (-1)**(a+b) if (last-a+1) % 2 else 0
    for a, b in occupied:
        tx = tail(a, b, rows[b])
        tx_next = tail(a+1, b, rows[b]) if a < rows[b] else 0
        ty = tail(b, a, columns[a])
        ty_next = tail(b+1, a, columns[a]) if b < columns[a] else 0
        sigma = (-1)**(a+b)
        residual = max(abs(tx-tx_next-sigma), abs(ty-ty_next-sigma))
        max_stress = max(max_stress, abs(tx), abs(ty))
        max_residual = max(max_residual, residual)
        checks += 1
assert len(occupied) == side**2
assert max_stress == 1 and max_residual == 0

def elastic_rectangle(L, shear):
    """Linear x-displacement model: horizontal spring1, vertical shear k_s.

    Both axis seeds pinned; top/right free. This is not a nonlinear tile
    simulation. k_s is a paid MODEL INPUT, not an acquired joint property.
    """
    rr, cc, vv, rhs = [], [], [], np.empty(L*L)
    for j in range(L):
        for i in range(L):
            q = j*L+i
            rhs[q] = (-1)**(i+j)
            diagonal = 0.0
            for di, dj, k in ((-1,0,1.), (1,0,1.), (0,-1,shear), (0,1,shear)):
                a, b = i+di, j+dj
                if a >= L or b >= L:
                    continue
                diagonal += k
                if a >= 0 and b >= 0:
                    rr.append(q); cc.append(b*L+a); vv.append(-k)
            rr.append(q); cc.append(q); vv.append(diagonal)
    K = coo_matrix((vv,(rr,cc)),shape=(L*L,L*L)).tocsc()
    u = spsolve(K,rhs).reshape((L,L))
    hx = np.diff(np.column_stack((np.zeros(L),u)),axis=1)
    vy = np.diff(np.vstack((np.zeros(L),u)),axis=0)
    return {'L':L, 'shear_stiffness':shear,
            'max_abs_displacement':float(np.max(np.abs(u))),
            'max_horizontal_extension':float(np.max(np.abs(hx))),
            'max_vertical_transverse_slip':float(np.max(np.abs(vy))),
            'max_vertical_shear_force':float(shear*np.max(np.abs(vy))),
            'linear_solve_residual':float(np.max(np.abs(K@u.ravel()-rhs)))}

elastic = [elastic_rectangle(L,s) for s in (0.,.01,.1,1.) for L in (8,16,32,64,128)]
for e in elastic:
    if e['shear_stiffness'] == 0:
        assert abs(e['max_vertical_transverse_slip']-e['L']) < 1e-7

receipt = {
    'status':'CONDITIONAL_STATICS_ONLY; PHYSICAL_STABILITY_NOT_ACQUIRED',
    'exact_integer_prefix_consumer':{
        'tiles':len(occupied),'prefixes':len(occupied),'node_equilibrium_checks':checks,
        'max_component_tension_unit_drive':max_stress,'max_equilibrium_residual':max_residual,
        'uniform_drive_max_component_tension':side},
    'spring_compatibility_failure':{
        'formula':'adjacent-row endpoint slip = L*Fx/k for even L, zero shear stiffness',
        'example_Fx_over_k':.001,'L':64,'slip_in_pitch_units':.064,
        'illustrative_registration_tolerance':.005,
        'physical_calibration':'NONE'},
    'coherent_bias_cut_bound':{
        'formula':'abs(delta)*abs(F)*L <= 2*Fc',
        'illustration_delta':.01,'illustration_Fc_over_F':1.,'max_L_necessary':200,
        'supports':'only 2L seed joints; no floor-friction support granted'},
    'elastic_regularization_diagnostics':elastic,
    'elapsed_after_import_seconds':time.perf_counter()-started,
    'limitations':['No native body-drive acquisition','No inertia/contact dynamics',
                   'No nonlinear elastic or bond failure consumer',
                   'Finite elastic diagnostics are not size-independent stability proof']}
out = Path(__file__).with_name('LOAD_RECEIPT.json')
out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'elastic_regularization_diagnostics'},indent=2))
print(json.dumps({'elastic_max_residual':max(e['linear_solve_residual'] for e in elastic),
                  'regularized_L128':[e for e in elastic if e['L']==128]},indent=2))
