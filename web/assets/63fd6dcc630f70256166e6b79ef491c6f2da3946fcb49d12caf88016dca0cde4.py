from fractions import Fraction as F


def signed_margin(target_energy, competitor_energy_at_half):
    return target_energy - competitor_energy_at_half


def main():
    # Binary A-B panel: A at x_B=0, B at x_B=1, AB at x_B=1/2.
    predicted = {"A": F(0), "B": F(0), "AB": F(-100, 1000)}
    x_b = {"A": F(0), "B": F(1), "AB": F(1, 2)}
    beta_a, beta_b = F(3, 10), F(-1, 5)

    affine = {
        name: (1 - x_b[name]) * beta_a + x_b[name] * beta_b
        for name in predicted
    }
    shifted = {name: predicted[name] + affine[name] for name in predicted}

    # At x_B=1/2 the only endpoint decomposition is 1/2 A + 1/2 B.
    endpoint_hull = (predicted["A"] + predicted["B"]) / 2
    shifted_endpoint_hull = (shifted["A"] + shifted["B"]) / 2
    margin = signed_margin(predicted["AB"], endpoint_hull)
    shifted_margin = signed_margin(shifted["AB"], shifted_endpoint_hull)

    # Residual intervals are [-5,5] meV/atom for every phase. Worst target
    # energy is -95 meV; lowest endpoint hull is -5 meV: robustly stable.
    eps = F(5, 1000)
    robust_target_upper = predicted["AB"] + eps
    robust_competitor_lower = (predicted["A"] - eps + predicted["B"] - eps) / 2
    robust_stable = robust_target_upper <= robust_competitor_lower

    # Hidden A2B: x_B=1/3, E=-300 meV; 3/4 A2B + 1/4 B has x_B=1/2.
    hidden_energy = F(-300, 1000)
    hidden_x_b = F(1, 3)
    weight_a2b = F(3, 4)
    mixture_x_b = weight_a2b * hidden_x_b + (1 - weight_a2b) * F(1)
    hidden_mixture_energy = weight_a2b * hidden_energy
    hidden_target_gap = predicted["AB"] - hidden_mixture_energy

    assert margin == shifted_margin
    assert abs(shifted["AB"] - predicted["AB"]) > 2 * eps
    assert robust_stable
    assert mixture_x_b == F(1, 2)
    assert hidden_target_gap > 0

    print(f"panel margin before/after affine shift: {float(margin):.3f}/{float(shifted_margin):.3f} eV/atom")
    print(f"absolute target shift: {float(shifted['AB'] - predicted['AB']):.3f} eV/atom")
    print(f"robust stable on declared panel with residual radius 5 meV: {robust_stable}")
    print(f"hidden mixture energy at x_B=1/2: {float(hidden_mixture_energy):.3f} eV/atom")
    print(f"target above hidden mixture: {float(hidden_target_gap):.3f} eV/atom")


if __name__ == "__main__":
    main()
