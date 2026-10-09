"""Reproduce the three-state quasistatic loop-work calculation (stdlib only)."""
import math


def stationary(energies, clockwise, counterclockwise):
    q = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        j = (i + 1) % 3
        delta = energies[j] - energies[i]
        q[i][j] = clockwise * math.exp(-delta / 2)
        q[j][i] = counterclockwise * math.exp(delta / 2)
    tau = [
        q[1][0] * q[2][0] + q[1][0] * q[2][1] + q[1][2] * q[2][0],
        q[0][1] * q[2][1] + q[0][1] * q[2][0] + q[0][2] * q[2][1],
        q[0][2] * q[1][2] + q[0][2] * q[1][0] + q[0][1] * q[1][2],
    ]
    z = sum(tau)
    return [weight / z for weight in tau]


def square_work(delta, panels, clockwise, counterclockwise):
    vertices = [
        ([0.0, 0.0, 0.0], [delta, 0.0, 0.0]),
        ([delta, 0.0, 0.0], [delta, delta, 0.0]),
        ([delta, delta, 0.0], [0.0, delta, 0.0]),
        ([0.0, delta, 0.0], [0.0, 0.0, 0.0]),
    ]
    work = 0.0
    for start, end in vertices:
        d_energy = [end[i] - start[i] for i in range(3)]
        force_samples = []
        for j in range(panels + 1):
            u = j / panels
            energy = [start[i] + u * d_energy[i] for i in range(3)]
            pi = stationary(energy, clockwise, counterclockwise)
            force_samples.append(sum(pi[i] * d_energy[i] for i in range(3)))
        work += (0.5 * force_samples[0] + sum(force_samples[1:-1])
                 + 0.5 * force_samples[-1]) / panels
    return work


if __name__ == "__main__":
    for k in (10, 20, 50, 100, 200, 1000):
        driven = square_work(1.0, k, 2.0, 1.0)
        equilibrium = square_work(1.0, k, 1.0, 1.0)
        print(f"K={k:4d} driven={driven:.14f} equilibrium={equilibrium:.3g}")
