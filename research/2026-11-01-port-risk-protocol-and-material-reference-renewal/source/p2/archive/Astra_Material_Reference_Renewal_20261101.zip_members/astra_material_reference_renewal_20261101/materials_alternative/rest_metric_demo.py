"""Finite reference-metric repair under unknown load; NumPy-only minimal model.

The repair policy reads a noisy seven-fold replicated digital rest-length word,
never the true unloaded geometry or external force. One member is replaced per
step, without damage sensing. All physical members turn over. The alternative
policy grows each new member stress-free at the observed, loaded gap.

This is a small-strain spring-truss simulation, not a materials prototype or an
autonomous construction simulation. Nodes, topology, unit calibration, parts
delivery, and the code's logic are idealized explicitly; see mechanism.md.
"""
import json
from pathlib import Path
import numpy as np


def make_lattice(nx=5, ny=4):
    points = np.array([(3.0*x, 4.0*y) for y in range(ny) for x in range(nx)])
    edges = []
    for y in range(ny):
        for x in range(nx):
            a = y*nx+x
            if x+1<nx:
                edges.append((a, a+1))
            if y+1<ny:
                edges.append((a, a+nx))
            if x+1<nx and y+1<ny:
                edges.extend(((a, a+nx+1), (a+1, a+nx)))
    B = np.zeros((len(edges), 2*len(points)))
    lengths = []
    for row, (a,b) in enumerate(edges):
        v = points[b]-points[a]
        length = np.linalg.norm(v)
        lengths.append(length)
        B[row,2*a:2*a+2] = -v/length
        B[row,2*b:2*b+2] = v/length
    return points, edges, B, np.asarray(lengths)


def main():
    rng = np.random.default_rng(64173)
    points, edges, B, target_lengths = make_lattice()
    n, e = len(points), len(edges)
    replicas, code_copies, word_bits, quantum = 3, 7, 13, 0.001
    steps = 3300
    physical_count = replicas*e
    physical_B = np.repeat(B, replicas, axis=0)
    target_physical = np.repeat(target_lengths, replicas)
    K = physical_B.T @ physical_B
    vals, vecs = np.linalg.eigh(K)
    keep = vals>1e-9
    Kplus = (vecs[:,keep]/vals[keep]) @ vecs[:,keep].T
    assert keep.sum()==2*n-3, "Only rigid-body modes may be free."

    # No grounded node: the pseudoinverse fixes a mathematical rigid-motion
    # gauge, and force fields below have no force/torque rigid-mode component.
    assert np.linalg.norm(K@Kplus@K-K)<1e-8
    min_single_removal_stiffness = min(
        np.linalg.eigvalsh(K-np.outer(row,row))[3]
        for row in physical_B)
    assert min_single_removal_stiffness>0

    words = np.rint(target_lengths/quantum).astype(np.uint16)
    bits = ((words[:,None] >> np.arange(word_bits)) & 1).astype(np.uint8)
    code = np.repeat(bits[:,:,None],code_copies,axis=2)
    calibrated = target_physical.copy()
    gap_copy = target_physical.copy()
    replacement_counts = np.zeros(physical_count,dtype=int)
    rows = []
    bit_flips = wrong_decodes = 0
    install_energy = 0.0
    damage_events = 0
    centered = points-points.mean(axis=0)

    def equilibrium(rest, external_force):
        return Kplus @ (physical_B.T@(rest-target_physical)+external_force)

    def score(rest):
        u = equilibrium(rest,np.zeros(2*n)).reshape(n,2)
        return float(np.sqrt(np.mean(np.sum(u*u,axis=1))))

    for t in range(steps):
        flips = rng.random(code.shape)<1e-5
        bit_flips += int(flips.sum())
        code ^= flips.astype(np.uint8)

        # Slow drift affects all members; sparse shocks are localized damage.
        drift = rng.normal(0,2e-5,physical_count)
        if rng.random()<0.03:
            drift[rng.integers(physical_count)] += rng.choice([-1,1])*0.01
            damage_events += 1
        calibrated += drift
        gap_copy += drift

        # Unknown to both policies. Equivalent to a bounded, balanced
        # time-dependent boundary/force field in the linear model.
        affine = centered.copy()
        affine[:,0] *= 0.0004*(1+0.30*np.sin(t/170))
        affine[:,1] *= -0.0001*(1+0.20*np.cos(t/90))
        force = K@affine.ravel()
        j = t % physical_count
        edge = j//replicas
        u_correct = equilibrium(calibrated,force)
        u_gap = equilibrium(gap_copy,force)
        correct_gap = target_physical[j]+physical_B[j]@u_correct
        observed_gap = target_physical[j]+physical_B[j]@u_gap

        # Read majority, scrub its seven physical copies, and manufacture.
        # No pristine target-length lookup occurs in this policy.
        decoded_bits = (code[edge].sum(axis=1)>code_copies//2).astype(np.uint8)
        code[edge] = decoded_bits[:,None]
        decoded_word = int(np.sum(decoded_bits.astype(np.uint16)<<np.arange(word_bits)))
        wrong_decodes += int(decoded_word!=int(words[edge]))  # scoring only
        manufacturing_error = rng.normal(0,1e-4)
        new_rest_length = quantum*decoded_word+manufacturing_error
        calibrated[j] = new_rest_length
        gap_copy[j] = observed_gap+manufacturing_error
        replacement_counts[j] += 1
        install_energy += 0.5*(correct_gap-new_rest_length)**2

        if t%55==0 or t==steps-1:
            rows.append({"step":t+1,
                         "calibrated_unloaded_rms":score(calibrated),
                         "gap_copy_unloaded_rms":score(gap_copy),
                         "calibrated_loaded_rms":float(np.sqrt(np.mean(np.sum(
                             equilibrium(calibrated,force).reshape(n,2)**2,axis=1))))})

    result = {
        "model":"small-strain two-dimensional truss; unit spring stiffness",
        "seed":64173,"nodes":n,"geometric_edges":e,
        "physical_members":physical_count,"memory_bits":int(code.size),
        "steps":steps,"replacement_count":int(replacement_counts.sum()),
        "least_replacements_per_original_member":int(replacement_counts.min()),
        "independent_memory_bit_flips":bit_flips,"wrong_decoded_words":wrong_decodes,
        "localized_rest_length_shocks":damage_events,
        "minimum_nonrigid_stiffness":float(vals[keep].min()),
        "minimum_nonrigid_stiffness_with_any_one_member_removed":float(min_single_removal_stiffness),
        "final_calibrated_unloaded_rms":score(calibrated),
        "final_gap_copy_unloaded_rms":score(gap_copy),
        "post_first_turnover_calibrated_rms_max":max(
            row["calibrated_unloaded_rms"] for row in rows if row["step"]>physical_count),
        "installation_strain_energy_sum_lower_bound":float(install_energy),
        "samples":rows,
    }
    out = Path(__file__).with_name("rest_metric_results.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="samples"},indent=2))


if __name__=="__main__":
    main()
