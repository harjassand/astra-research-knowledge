"""Small proof-of-mechanism; not a numerical certification implementation."""

import numpy as np


def cyclic_compile(apply_ops, n, rng, tol=1e-10):
    """Close a Gaussian vector under all supplied symmetric operators."""
    g = rng.normal(size=n)
    columns = [g / np.linalg.norm(g)]
    images = [[] for _ in apply_ops]
    j = 0
    while j < len(columns):
        for i, apply in enumerate(apply_ops):
            image = apply(columns[j])
            images[i].append(image)
            residual = image.copy()
            for _ in range(2):
                q = np.column_stack(columns)
                residual -= q @ (q.T @ residual)
            length = np.linalg.norm(residual)
            if length > tol:
                columns.append(residual / length)
                if len(columns) > n:
                    raise RuntimeError("Numerical rank test exceeded ambient dimension")
        j += 1
    q = np.column_stack(columns)
    compressed = []
    closure_residuals = []
    for raw_images in images:
        action = np.column_stack(raw_images)
        b = q.T @ action
        compressed.append((b + b.T) / 2)
        closure_residuals.append(np.linalg.norm(action - q @ b, 2))
    return q, compressed, closure_residuals, sum(map(len, images))


def main():
    rng = np.random.default_rng(20261031)
    r, multiplicity = 3, 40
    n = r * multiplicity
    u, _ = np.linalg.qr(rng.normal(size=(n, n)))
    small = []
    large = []
    for _ in range(2):
        b = rng.normal(size=(r, r))
        b = (b + b.T) / 2
        b /= np.linalg.norm(b, 2)
        small.append(b)
        large.append(u @ np.kron(np.eye(multiplicity), b) @ u.T)
    q, compressed, residuals, calls = cyclic_compile(
        [lambda v, a=a: a @ v for a in large], n, rng
    )
    print(f"N={n}, hidden_irrep_dimension={r}, multiplicity={multiplicity}")
    print(f"acquired_dimension={q.shape[1]}, expected={r*r}, matvec_calls={calls}")
    print(f"max_closure_residual={max(residuals):.3e}")
    errors = []
    for theta in np.linspace(-0.8, 0.8, 17):
        a1, a2 = large
        b1, b2 = compressed
        original = np.eye(n) + a1 @ a1 + a2 @ a2 + theta * (a1 @ a2 + a2 @ a1)
        compact = np.eye(q.shape[1]) + b1 @ b1 + b2 @ b2 + theta * (b1 @ b2 + b2 @ b1)
        full_value = np.linalg.slogdet(original)[1] / n
        compact_value = np.linalg.slogdet(compact)[1] / q.shape[1]
        errors.append(abs(full_value - compact_value))
    print(f"unseen_17_parameter_normalized_logdet_max_error={max(errors):.3e}")
    p_large = np.linalg.matrix_power(large[0] @ large[1], 12)
    p_small = np.linalg.matrix_power(compressed[0] @ compressed[1], 12)
    print(f"unseen_noncommuting_power_norm_error={abs(np.linalg.norm(p_large,2)-np.linalg.norm(p_small,2)):.3e}")


if __name__ == "__main__":
    main()
