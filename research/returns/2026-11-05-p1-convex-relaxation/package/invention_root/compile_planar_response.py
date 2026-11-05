"""Compile an ideal bounded convex planar response, with thermal error.

Run from the unpacked research record with Python + NumPy + SciPy:
  python invention_root/compile_planar_response.py --input target.json

Input JSON: {"target": [[...,...],[...,...]], "cap": 1.0,
             "diffusion": 1.0, "confidence": 0.95}
Units must be consistent. No specimen data or endpoint fit is used.
The output is a mathematical control schedule, not a laboratory program.
"""
from pathlib import Path
import argparse
import json
import math
import sys
import time
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'invention_variation'))
from gradient_rotation import (compile_target, fastest_shape_then_cool,
                               radial_quantile, rotation)


def compile_operation(request):
    start = time.perf_counter()
    target = np.asarray(request['target'], dtype=float)
    cap = float(request.get('cap', 1.0))
    diffusion = float(request.get('diffusion', 1.0))
    confidence = float(request.get('confidence', 0.95))
    if target.shape != (2, 2) or not np.isfinite(target).all():
        raise ValueError('target must be a finite real 2-by-2 matrix')
    if not math.isfinite(cap) or cap <= 0 or not math.isfinite(diffusion) or diffusion <= 0:
        raise ValueError('cap and diffusion must be positive finite numbers')
    if not 0 < confidence < 1:
        raise ValueError('confidence must lie strictly between zero and one')
    program = compile_target(target, cap)
    base = dict(model='dX=-A(t)X dt+sqrt(2D)dW; symmetric 0<=A<=cap I',
                scope='Prescribed open-loop controls, ideal switching, constant isotropic bath',
                physical_implementation=False, target=target.tolist(), cap=cap,
                diffusion=diffusion, reachable=program['reachable'],
                log_determinant_contraction=program['s'],
                minimum_shape_length=program['distance'])
    if not program['reachable']:
        base['reason']='Requested contraction is less than the established horizontal distance.'
        base['runtime_seconds']=time.perf_counter()-start
        return base
    endpoint = fastest_shape_then_cool(program, diffusion=diffusion)
    d, s = program['distance'], program['s']
    stages=[]
    if d > 1e-14:
        tg=2*d/cap
        stages.append(dict(kind='rotating_rank_one_convex_potential',
                           duration=tg, angle_at_start=program['alpha'],
                           angular_rate=program['w']/tg,
                           drift_eigenvalues=[0.,cap],
                           formula='A=(cap/2)(I+R(angle) diag(1,-1) R(angle)^T)'))
    if s-d > 1e-14:
        stages.append(dict(kind='isotropic_maximal_relaxation',duration=(s-d)/cap,
                           formula='A=cap I',drift_eigenvalues=[cap,cap]))
    eig=np.linalg.eigvalsh(endpoint['Q'])
    # Floating residuals are checks, not interval arithmetic certificates.
    residual=float(np.linalg.norm(endpoint['M']-target))
    relative=residual/max(float(np.linalg.norm(target)),np.finfo(float).tiny)
    normalized=float(np.linalg.norm(math.exp(s)*endpoint['M']-math.exp(s)*target))
    if not np.isfinite(normalized) or normalized>2e-7:
        raise ArithmeticError('Floating implementation did not resolve this target; use higher precision.')
    base.update(minimum_duration=program['T'],stages=stages,
                input_and_output_apparatus='A=cap I; endpoint changes included in net work',
                endpoint_mean_matrix=endpoint['M'].tolist(),
                additive_error_distribution='Centered Gaussian, independent of input',
                added_covariance=endpoint['Q'].tolist(),
                added_covariance_eigenvalues=eig.tolist(),confidence=confidence,
                radial_error_quantile=radial_quantile(confidence,eig),
                net_mean_potential_work_in_kBT=2*d,
                optimality='Minimum duration, then all radial error thresholds among duration minimizers',
                mean_map_absolute_residual=residual,mean_map_relative_residual=relative,
                normalized_map_residual=normalized,
                runtime_seconds=time.perf_counter()-start)
    return base


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,help='JSON request; omitted gives a 90-degree demonstration')
    parser.add_argument('--output',type=Path,help='Optional output JSON path')
    args=parser.parse_args()
    if args.input:
        request=json.loads(args.input.read_text())
    else:
        theta=math.pi/2
        ell=math.sqrt(theta*theta+2*math.pi*theta)
        request={'target':(math.exp(-ell)*rotation(theta)).tolist(),
                 'cap':1.,'diffusion':1.,'confidence':.95}
    result=compile_operation(request)
    content=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(content)
    else:
        print(content,end='')


if __name__=='__main__':
    main()
