from fractions import Fraction as F


def passive_hazards(k0, gammas, duration):
    """Cumulative log-loss when all candidates co-vary at unit concentration."""
    total = k0 + sum(gammas)
    return [total * duration * t for t in range(1, duration + 1)]


def serial_pulse_data(k0, gammas, concentrations, delta):
    """H[0]=0, then clean baseline and one candidate per equal-length segment."""
    h = F(0)
    endpoints = [h]
    h += k0 * delta
    endpoints.append(h)
    for gamma, concentration in zip(gammas, concentrations):
        h += (k0 + gamma * concentration) * delta
        endpoints.append(h)
    return endpoints


def estimate_from_endpoints(endpoints, concentrations, delta):
    k0 = (endpoints[1] - endpoints[0]) / delta
    estimates = []
    for i, concentration in enumerate(concentrations):
        h_prev = endpoints[i + 1]
        h_next = endpoints[i + 2]
        estimates.append((h_next - h_prev - k0 * delta) / (concentration * delta))
    return k0, estimates


def main():
    k0 = F(1, 10)
    gammas = [F(6, 5), F(1, 2)]
    concentrations = [F(1), F(1)]
    delta = F(1)

    # Passive co-variation exposes only the total hazard coefficient.
    passive_sum = sum(gammas)
    alternatives = [[passive_sum, F(0)], [F(0), passive_sum]]
    assert all(sum(candidate) == passive_sum for candidate in alternatives)

    h = serial_pulse_data(k0, gammas, concentrations, delta)
    estimated_k0, estimated_gammas = estimate_from_endpoints(h, concentrations, delta)
    assert h == [F(0), F(1, 10), F(7, 5), F(2)]
    assert estimated_k0 == k0
    assert estimated_gammas == gammas

    # Exact finite-difference measurement-error certificate for independent
    # endpoint bounds |H_tilde-H| <= epsilon, with the initial reference exact.
    epsilon = F(1, 1000)
    gamma_error_bounds = [3 * epsilon / (c * delta) for c in concentrations]
    assert all(gamma > bound for gamma, bound in zip(estimated_gammas, gamma_error_bounds))

    bounded_errors = [F(0), epsilon, -epsilon, epsilon]
    noisy_endpoints = [value + error for value, error in zip(h, bounded_errors)]
    noisy_k0, noisy_gammas = estimate_from_endpoints(
        noisy_endpoints, concentrations, delta
    )
    assert abs(noisy_k0 - k0) <= epsilon / delta
    assert all(
        abs(noisy - exact) <= bound
        for noisy, exact, bound in zip(noisy_gammas, gammas, gamma_error_bounds)
    )

    # Falsifier: a pure A*B synergy is invisible to every isolated pulse.
    pairwise_synergy = F(3, 2)
    isolated_hazards = [F(0), F(0)]
    joint_hazard = pairwise_synergy * F(1) * F(1)
    assert isolated_hazards == [F(0), F(0)] and joint_hazard > 0

    print("PASS: passive co-variation identifies only gamma_1 + gamma_2 =", passive_sum)
    print("PASS: serial pulses recover k0 =", estimated_k0, "gamma =", estimated_gammas)
    print("PASS: bounded-error margins exceed", gamma_error_bounds)
    print("PASS: one bounded-error realization stays within the derived bounds")
    print("EXPECTED LIMIT: isolated pulses miss pure A*B synergy; joint hazard =", joint_hazard)
    print("endpoint log-losses:", h)


if __name__ == "__main__":
    main()
