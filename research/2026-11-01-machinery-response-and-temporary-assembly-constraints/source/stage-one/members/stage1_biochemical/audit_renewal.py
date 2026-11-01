#!/usr/bin/env python3
"""Exact renewal audit of a pinned, public PURE CRN plus conditional maintenance LP.

No parameters are fitted and no authors' trajectories are reproduced. The first
part inspects their actual SBML stoichiometry using exact rational arithmetic.
The second part is an explicitly idealized construction/competitor comparison.
Run: python stage1_biochemical/audit_renewal.py
Dependencies: Python 3, scipy. XML uses the standard library.
"""
from pathlib import Path
import hashlib
import json
from fractions import Fraction
import xml.etree.ElementTree as ET
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
BASE = HERE / "public_code" / "PURE_CRN_models"
NS = {"s": "http://www.sbml.org/sbml/level3/version2/core"}
AMINO = "Ala Arg Asn Asp Cys Gln Glu Gly His Ile Leu Lys Met Phe Pro Ser Thr Trp Tyr Val".split()
FACTORS = "CK EFG EFTs EFTu IF1 IF2 IF3 MK MTF NDK PPiase RF1 RF2 RF3 RRF".split() + [x + "RS" for x in AMINO]


def git_blob_sha1(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def load_network(name):
    root = ET.parse(BASE / "Models" / name).getroot()
    species = [s.attrib["id"] for s in root.findall(".//s:species", NS)]
    reactions = []
    for reaction in root.findall(".//s:reaction", NS):
        stoich = {}
        for side, sign in [("listOfReactants", -1), ("listOfProducts", 1)]:
            for sr in reaction.findall("./s:" + side + "/s:speciesReference", NS):
                key = sr.attrib["species"]
                stoich[key] = stoich.get(key, Fraction(0)) + sign * Fraction(sr.attrib.get("stoichiometry", "1"))
        reactions.append((reaction.attrib["id"], stoich))
    return species, reactions


def audit_moiety(species, reactions, weight):
    violations = []
    for rid, column in reactions:
        change = sum((coefficient * weight(s) for s, coefficient in column.items()), Fraction(0))
        if change:
            violations.append({"reaction": rid, "net_change": str(change)})
    return {"species_with_moiety": sum(weight(s) for s in species),
            "violating_reactions": violations,
            "exactly_conserved": not violations}


def conditional_maintenance(nonribosomal_loss, ribosome_loss, ribosome_replacement_capacity):
    """Normalized counterexample, not an experimentally calibrated reactor model.

    Allocations f_E, f_R, f_P share one unit of service. If all service went to E,
    replacement is assumed 0.08 inventories per interval. This number is inspired
    by a published mass recovery, NOT a measured active renewal rate. R capacity
    is supplied as an explicit parameter; zero represents the audited network.
    """
    result = linprog([0., 0., -1.],
        A_ub=[[-0.08, 0., 0.], [0., -ribosome_replacement_capacity, 0.], [1., 1., 1.]],
        b_ub=[-nonribosomal_loss, -ribosome_loss, 1.], bounds=[(0., None)] * 3,
        method="highs")
    return {"nonribosomal_loss_per_interval": nonribosomal_loss,
            "ribosome_loss_per_interval": ribosome_loss,
            "ribosome_replacement_capacity_per_interval": ribosome_replacement_capacity,
            "feasible": bool(result.success),
            "best_fixed_allocations_E_R_product": result.x.tolist() if result.success else None}


def main():
    provenance = json.loads((BASE / "PROVENANCE.json").read_text())
    checks = []
    for item in provenance["files"]:
        obtained = git_blob_sha1((BASE / item["path"]).read_bytes())
        checks.append({"path": item["path"], "expected": item["git_blob_sha1"], "actual": obtained})
        assert obtained == item["git_blob_sha1"], item["path"]

    species, reactions = load_network("TL_PURE_MGapt-deGFP_model.xml")
    audit = {}
    # The supplied species names explicitly distinguish free, bound and elongating
    # ribosomes. Each species below carries one copy of the indicated subunit.
    audit["30S_subunit_material"] = audit_moiety(species, reactions, lambda s: int("RS30S" in s or "RS70S" in s))
    audit["50S_subunit_material"] = audit_moiety(species, reactions, lambda s: int("RS50S" in s or "RS70S" in s))
    for factor in FACTORS:
        audit[factor] = audit_moiety(species, reactions, lambda s, f=factor: int(f in s.split("_")))
    assert len(FACTORS) == 35
    assert all(x["exactly_conserved"] for x in audit.values())
    degraded = [s for s in species if "degraded" in s]
    degraded_reactions = [rid for rid, column in reactions if any("degraded" in s and c != 0 for s, c in column.items())]
    txspecies, txreactions = load_network("CRN_PURE_MGaptTXwTL_updated.xml")
    polymerase = audit_moiety(txspecies, txreactions, lambda s: int("T7RNAP" in s.split("_")))
    assert polymerase["exactly_conserved"]

    result = {
        "source_commit": provenance["commit"],
        "source_file_byte_hash_checks": checks,
        "scope": "Exact stoichiometric audit. Not a kinetic validation, experimental result, or complete constructor model.",
        "translation_network": {"species": len(species), "reactions": len(reactions),
            "moieties": audit, "listed_degraded_species": len(degraded),
            "reactions_changing_a_degraded_species": degraded_reactions},
        "transcription_plus_translation_machinery_network": {"species": len(txspecies), "reactions": len(txreactions),
            "T7RNAP_moiety": polymerase},
        "reported_nonribosome_recovered_mass_ratio": {"numerator_micrograms": 28, "denominator_micrograms": 350,
            "ratio": 28/350, "warning": "Total recovered mass, not per-component active yield or rate."},
        "conditional_maintenance_examples": [
            conditional_maintenance(loss, 0., 0.) for loss in [0., .01, .02, .04, .08]],
        "missing_ribosome_service_counterexample": conditional_maintenance(.02, 0.000001, 0.),
        "supplied_hypothetical_ribosome_service": conditional_maintenance(.02, .002, .01),
        "interpretation": "Zero ribosome renewal gives a strict impossibility certificate for positive ribosome turnover, even when an idealized nonribosomal maintenance LP leaves spare production capacity. Fixed allocation already attains the linear-model upper bound; adaptive scheduling earns no generic resource gain."
    }
    (HERE / "audit_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("All", len(checks), "public files match pinned Git blob hashes.")
    print("Translation network:", len(species), "species,", len(reactions), "reactions.")
    print("Exactly conserved: both ribosome-subunit moieties and all", len(FACTORS), "protein-factor moieties.")
    print("Listed degraded species:", len(degraded), "; reactions changing them:", len(degraded_reactions))
    print("T7RNAP conserved in the separate transcription-containing network:", polymerase["exactly_conserved"])
    for case in result["conditional_maintenance_examples"]:
        print("Idealized nonribosomal loss", case["nonribosomal_loss_per_interval"], "-> fixed E/R/product allocation", case["best_fixed_allocations_E_R_product"])
    print("Any positive ribosome loss with zero renewal: infeasible =", not result["missing_ribosome_service_counterexample"]["feasible"])
    print("Illustrative supplied ribosome renewal (unearned helper):", result["supplied_hypothetical_ribosome_service"]["best_fixed_allocations_E_R_product"])


if __name__ == "__main__":
    main()
