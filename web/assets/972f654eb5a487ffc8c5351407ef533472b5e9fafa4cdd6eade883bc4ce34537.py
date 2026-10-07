"""High-precision gap-free square-root diagnostics, not a certified compiler."""
import json
import math
from pathlib import Path
import mpmath as mp


def run():
    mp.mp.dps = 160
    rotation = mp.matrix([[mp.mpf(3)/5,-mp.mpf(4)/5,0],
                          [mp.mpf(4)/5,mp.mpf(3)/5,0], [0,0,1]])
    tests = []
    for values in [('0','0','0'), ('0','0','.2'), ('0','1e-40','.2'),
                   ('.1','.1','.1')]:
        C = rotation*mp.diag([mp.mpf(x) for x in values])*rotation.T
        true = rotation*mp.diag([mp.sqrt(mp.mpf(x)) for x in values])*rotation.T
        for target in ['1e-8', '1e-20']:
            q = mp.mpf(target)
            alpha = (q/4)**2
            D = C+alpha*mp.eye(3)
            gamma = 1+mp.mpf('.2')+alpha
            X = gamma*mp.eye(3)
            steps = math.ceil(float(mp.log(gamma/mp.sqrt(alpha))/mp.log(mp.mpf(8)/5)))+20
            min_eigenvalue = mp.inf
            for _ in range(steps):
                inverse = X**-1
                X = (X+(D*inverse+inverse*D)/2)/2
                smallest = mp.eigsy(X, eigvals_only=True)[0]
                min_eigenvalue = min(min_eigenvalue, smallest)
            error = mp.norm(X-true, 2)  # Frobenius; hence upper-bounds op norm.
            residual = mp.norm(X*X-D, 2)
            assert error <= q
            assert min_eigenvalue > 0
            tests.append(dict(eigenvalues=list(values), target_error=target,
                              regularization_alpha=mp.nstr(alpha,25), iterations=steps,
                              Frobenius_error=float(error), error_over_target=float(error/q),
                              squared_residual=float(residual),
                              minimum_iterate_eigenvalue=float(min_eigenvalue)))
    data=dict(scope='160-decimal mpmath Newton diagnostics, no interval guarantee or finite-bit sampler.',
              cases=tests)
    path=Path(__file__).with_name('spin_square_root_checks.json')
    path.write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))
    print('Saved',path)


if __name__=='__main__':
    run()
