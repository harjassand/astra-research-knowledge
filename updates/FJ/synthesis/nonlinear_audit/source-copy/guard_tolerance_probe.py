"""Probe the copied prototype's tolerance on deliberately invalid probabilities."""
import json


def run():
    # At v=1, tangent=101. Pick a valid one-child mass 0 and an event sum
    # 5e-13 above one. This is within the implementation's 1e-12 tolerance.
    h = 0.1
    rate = 101.0
    p0 = 0.1
    p2 = 0.9000000000005
    R = p0 * rate * h
    B2 = p2 * rate / h
    total = p0 + (1.0 - 101.0 / rate) + B2 * h / rate
    p1 = 0.0
    guard_raises = p1 < -1e-12 or total > 1.0 + 1e-12
    result = {
        "probe": "synthetic non-certificate inputs; event masses sum to 1+5e-13",
        "p0": p0,
        "p1": 0.0,
        "p2": p2,
        "sum": total,
        "guard_tolerance": 1e-12,
        "copied_source_guard_expression": "p1 < -1e-12 or total > 1+1e-12",
        "guard_would_raise": guard_raises,
        "interpretation": "The copied guard accepts this deliberately invalid categorical mass because it lies inside the tolerance; this is not a run of the sampler and is not an observed failure under either supplied exact certificate.",
    }
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
