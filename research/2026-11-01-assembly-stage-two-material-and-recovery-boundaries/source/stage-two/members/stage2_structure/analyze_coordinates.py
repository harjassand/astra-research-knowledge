"""Reproduce a small geometry audit of deposited 9DYG and mature 4YBB.

Inputs are real selected coordinate rows, not a generative structural model.
Atom distances do not measure binding energies, accessible on-rates, or release.
9DYG is a 5.27 A cryo-EM model; close atom distances are only geometric proxies.
"""
from pathlib import Path
import json
import numpy as np
from scipy.spatial.distance import cdist

HERE = Path(__file__).resolve().parent


def nearest_pair(a, b):
    if not a or not b:
        return {"distance_A": None, "reason": "missing modeled residue"}
    distances = cdist(np.array([r[5:8] for r in a]), np.array([r[5:8] for r in b]))
    i, j = np.unravel_index(distances.argmin(), distances.shape)
    return {
        "distance_A": float(distances[i, j]),
        "a": {"chain": a[i][0], "residue": a[i][1], "name": a[i][2], "atom": a[i][3]},
        "b": {"chain": b[j][0], "residue": b[j][1], "name": b[j][2], "atom": b[j][3]},
    }


def main():
    source = json.loads((HERE / "coordinate_subset.json").read_text())
    result = {"limitations": [
        "These are minimum modeled heavy-atom distances, not energies or kinetic rates.",
        "9DYG is a 5.27 A cryo-EM fitted model; individual atomic arrangements are uncertain.",
        "9DYG uL13 has backbone atoms only. Protein-distance comparison therefore uses N/CA/C/O in both structures; absent sidechains cannot establish interface atom contacts.",
        "Mature 4YBB is a different experimental sample, method, and strain from 9DYG.",
        "Residue windows used here are explicit numeric selections, not a new helix assignment.",
        "3D-Flex heterogeneity is not a time trajectory and cannot determine transition direction or rates.",
        "Neither solvent exposure nor close contacts proves oligonucleotide access to a bound intermediate.",
    ], "sources": source["sources"], "structures": {}}
    for sid, rows in source["atoms"].items():
        rows = [r for r in rows if r[4] != "H"]
        rna = [r for r in rows if r[0] == "CA"]
        ul13_all = [r for r in rows if r[0] != "CA"]
        ul13 = [r for r in ul13_all if r[3] in ("N", "CA", "C", "O")]
        per_residue = {}
        for n in range(2790, 2806):
            r = [x for x in rna if x[1] == n]
            per_residue[str(n)] = nearest_pair(r, ul13)
        quartet = {}
        for a, b in [(9, 2800), (10, 2629), (9, 2629), (10, 2800)]:
            quartet[f"{a}-{b}"] = nearest_pair(
                [r for r in rna if r[1] == a], [r for r in rna if r[1] == b])
        result["structures"][sid] = {
            "selected_atoms": len(rows), "ul13_chain": sorted(set(x[0] for x in ul13)),
            "ul13_original_atom_count": len(ul13_all), "ul13_matched_backbone_count": len(ul13),
            "quartet_minimum_distances": quartet,
            "H98_apical_neighborhood_to_uL13_backbone": per_residue,
        }
    (HERE / "geometry_results.json").write_text(json.dumps(result, indent=2) + "\n")
    table = ["# Deposited-coordinate geometry audit\n",
             "The table gives minimum modeled heavy-atom distances in angstroms. Protein comparisons use only matched backbone atoms (N/CA/C/O), because 9DYG lacks uL13 sidechains. It does not estimate an interaction strength or rate.\n\n",
             "| Residue pair / selection | Mature 4YBB | RA20-B-c 9DYG |\n",
             "| --- | ---: | ---: |\n"]
    for key in ["9-2800", "10-2629", "9-2629", "10-2800"]:
        vals = [result["structures"][x]["quartet_minimum_distances"][key]["distance_A"] for x in ["4YBB", "9DYG"]]
        table.append(f"| RNA {key} | {vals[0]:.3f} | {vals[1]:.3f} |\n")
    for n in [2797, 2798, 2799, 2800]:
        vals = [result["structures"][x]["H98_apical_neighborhood_to_uL13_backbone"][str(n)]["distance_A"] for x in ["4YBB", "9DYG"]]
        table.append(f"| RNA {n} to uL13 backbone | {vals[0]:.3f} | {vals[1]:.3f} |\n")
    table.append("\nThe native quartet is geometrically absent in the inhibited model, while part of the H98 apical neighborhood approaches uL13. This supports the published interaction-exchange interpretation. It does not establish that the nonnative anchor is harmful, or that suppressing it would improve assembly.\n")
    (HERE / "GEOMETRY.txt").write_text("".join(table))
    print("".join(table))


if __name__ == "__main__":
    main()
