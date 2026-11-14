"""Introduced geometric homotopy, not a qualified actuator or shell solver."""
import json
import math
from pathlib import Path
import numpy as np


def main():
    amplitude = .004
    width = .05
    thickness = .0002
    half = thickness / 2
    wave = math.pi / width
    hessian_bound = amplitude * wave ** 2
    gradient_bound = amplitude * wave
    xy = np.asarray([(x, y) for x in np.linspace(-width/2, width/2, 9)
                     for y in np.linspace(-width/2, width/2, 9)])
    output = []
    for t in [0., .25, .5, .75, 1.]:
        points, labels = [], []
        metrics = []
        curvatures = []
        for x, y in xy:
            cx, cy = math.cos(wave*x), math.cos(wave*y)
            sx, sy = math.sin(wave*x), math.sin(wave*y)
            f = t * amplitude * cx * cy
            grad = -t * amplitude * wave * np.asarray([sx*cy, cx*sy])
            hes = t * amplitude * wave**2 * np.asarray([[-cx*cy, sx*sy],
                                                       [sx*sy, -cx*cy]])
            w = math.sqrt(1 + float(grad @ grad))
            first = np.eye(2) + np.outer(grad, grad)
            second = hes / w
            # Credited algebraic bilayer metric inverse, using the prior
            # contract's thickness convention.  No physical field writer.
            metrics.extend([np.linalg.eigvalsh(first + 2*thickness/3 * second),
                            np.linalg.eigvalsh(first - 2*thickness/3 * second)])
            curvatures.extend(np.linalg.eigvals(np.linalg.solve(first, second)))
            normal = np.asarray([-grad[0], -grad[1], 1.]) / w
            middle = np.asarray([x, y, f])
            for z in [-half, 0., half]:
                points.append(middle + z * normal)
                labels.append([x, y])
        points, labels = np.asarray(points), np.asarray(labels)
        horizontal_dist = np.linalg.norm(labels[:, None] - labels[None, :], axis=2)
        physical_dist = np.linalg.norm(points[:, None] - points[None, :], axis=2)
        mask = horizontal_dist > 1e-12
        ratio = float(np.min(physical_dist[mask] / horizontal_dist[mask]))
        bound = 1 - half * t * hessian_bound
        assert ratio >= bound - 1e-12
        metric_min = float(np.min(metrics))
        metric_max = float(np.max(metrics))
        assert metric_min >= 1 - 2 * thickness / 3 * t * hessian_bound - 1e-12
        output.append(dict(homotopy_parameter=t, points=len(points),
                           measured_min_separation_ratio=ratio,
                           analytic_separation_ratio_bound=bound,
                           layer_metric_min_eigenvalue=metric_min,
                           layer_metric_max_eigenvalue=metric_max,
                           max_principal_curvature=float(max(abs(np.asarray(curvatures)))),
                           independent_layer_metric_components_per_sampling_step=6*len(xy)))
    result = dict(scope="INTRODUCED geometry-only graph homotopy; no mechanics, control, fabrication, or novelty claim",
                  target="f=A cos(kx) cos(ky) over a convex square, interpolated by t*f",
                  amplitude_m=amplitude, square_width_m=width, total_thickness_m=thickness,
                  uniform_gradient_bound=gradient_bound,
                  uniform_hessian_bound_per_m=hessian_bound,
                  half_thickness_times_hessian_bound=half*hessian_bound,
                  global_normal_fiber_separation_lower_factor=1-half*hessian_bound,
                  analytic_layer_metric_min_eigenvalue_bound=1-2*thickness/3*hessian_bound,
                  homotopy_cases=output)
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
