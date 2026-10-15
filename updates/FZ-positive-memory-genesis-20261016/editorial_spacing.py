#!/usr/bin/env python3
"""Create a whitespace-only editorial proposal from the exact root v1 curation."""
from pathlib import Path
import copy
import json
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fz_common import digest, encoded, need

INPUT_SHA256 = "20275c535a2943d8303e3193124ec9eed45987c5cb30cf0951288b01711bcbf2"

BRIDGES = [
    {
        "source_subclaim": "One finite ROC completion iff one finite QC completion, with coefficients allowed to differ.",
        "destination_obligation": "QC of unchanged positive sharp J_r at all backgrounds.",
        "source_interface": {"objects": "Quartic quotient mod H", "regime_and_quantifiers": "Existence after deleting H", "supplied_information": "Existing finite-H theorem", "guarantee": "Some finite QC coefficient"},
        "destination_interface": {"objects": "Fixed J_r", "regime_and_quantifiers": "All compatible gradients/all affine B", "supplied_information": "Exact source coefficients", "guarantee": "Same coefficient QC", "costs": "No extra coefficient allowed"},
        "falsifier": "A valid changed-coefficient proof cannot by itself discharge unchanged coefficient conclusion.",
    },
    {
        "source_subclaim": "Same fixed decoder corrects every Pauli word on one good location schedule.",
        "destination_obligation": "Joint-input factorization and 2p_bad error for persistent finite bath faults.",
        "source_interface": {"regime_and_quantifiers": "Simultaneous over every history, exogenous locations", "supplied_information": "Source universal certificate and named probability imports", "guarantee": "Fixed decoder scalar identity on each decoded Kraus", "costs": "All charged location rates/geometry"},
        "destination_interface": {"objects": "Memory plus persistent finite bath", "regime_and_quantifiers": "Every joint logical bath reference input", "supplied_information": "Arbitrary supported CPTP fault policies", "guarantee": "Id_L tensor Lambda_B on good h; diamond<=2p_bad", "costs": "Fresh location law retained; no continuous bath conversion"},
        "alignment": "Operator-valued Pauli expansion preserves chronological bath products; fixed recovery supplies correctable span.",
        "missing_lemma": "External classical certificate review and physical realization remain missing; no internal quantum lift lemma remains.",
        "falsifier": "State-dependent clocks, separately chosen decoders or unscheduled data interactions break receiver.",
    },
    {
        "source_subclaim": "Exact Choi block gives CPTP proposal iff D PSD/a range/rate bound.",
        "destination_obligation": "Admit structured Hamiltonian/signed dissipative faults at charged Poisson rates.",
        "source_interface": {"objects": "Fixed finite Pauli catalog with K closure", "regime_and_quantifiers": "Finite patch signed Hermitian C/scalar h", "supplied_information": "Acquired coefficients/floors/supports", "guarantee": "Exact CPTP uniformization and minimal rate", "costs": "All proposal rates counted"},
        "destination_interface": {"objects": "Universal good-schedule memory receiver", "regime_and_quantifiers": "Completed corrector/exogenous bounded-support proposals", "supplied_information": "Same geometry/support incidence", "guarantee": "Inherited 2p_bad bound", "costs": "No useful numerical threshold or free physical floor"},
        "alignment": "Exact supported channel representation supplies receiver, with full rate and incidence conversion.",
        "missing_lemma": "Acquire corrector/floors/noise bounds; externally review probability tail. Missing K directions not admitted.",
        "falsifier": "Negative kernel/principal minor examples defeat missing product range at any rate.",
    },
    {
        "source_subclaim": "Full original voltage/fixed power order 2 and degree 4 bound products.",
        "destination_obligation": "Universal lower reciprocal cut containment.",
        "source_interface": {"objects": "Normalized degree 4 complex voltage functional", "regime_and_quantifiers": "All original M2/localizers/equalities", "supplied_information": "Exact rational table", "guarantee": "Legal relaxation point"},
        "destination_interface": {"objects": "Lower cut q²-z²", "regime_and_quantifiers": "Same original algebraic class", "supplied_information": "No extra current localizers", "guarantee": "Would require Lcut>=0", "costs": "No full PGLib/stronger incumbent claim"},
        "alignment": "The final legal functional has cut=-897/10000, including connected passive endpoint embedding.",
        "missing_lemma": "Full selected case constraints and practical baseline remain unresolved; degree 6 sufficiency retained.",
        "falsifier": "Executed exact negative cut is the scoped falsifier.",
    },
    {
        "source_subclaim": "All state exact decimal generator Lyapunov overflow <1e-9.",
        "destination_obligation": "Certified absolute first hit truncation error for retained 0..162.",
        "source_interface": {"objects": "Unbounded 8 count CTMC", "regime_and_quantifiers": "T1, init50, symmetric open 2x4", "supplied_information": "Exact decimal rates", "guarantee": "Poverflow163<=7.569068427e-10", "costs": "111 scalar evaluations"},
        "destination_interface": {"objects": "Absorbing overflow FSP or coupled suppressed cap", "regime_and_quantifiers": "Same target/deadline/generator inside box", "supplied_information": "Exact cap semantics", "guarantee": "FSP bracket or suppressed absolute bias", "costs": "163^8 states and inside accuracy still charged"},
        "alignment": "Coupling up to overflow preserves hit decision; absorbing and suppressed versions have distinct directions.",
        "missing_lemma": "Certified compressed inside solve and IEEE/residual error.",
        "falsifier": "Different cap inclusion, unsymmetric diffusion or changed rates require a new bound.",
    },
    {
        "source_subclaim": "Eventual Perron second moment divergence and eventual 1/kappa work.",
        "destination_obligation": "Same quantitative obstruction for fixed deadline 1.",
        "source_interface": {"objects": "Eventual hitting likelihood estimator", "regime_and_quantifiers": "Infinite horizon", "supplied_information": "Exact small chain rates", "guarantee": "Eventual moment/work statement", "costs": "Expected work may infinite"},
        "destination_interface": {"objects": "Fixed deadline estimator", "regime_and_quantifiers": "T1 same finite chain", "supplied_information": "Integrated matrix exponential", "guarantee": "Finite moments; conditional work ->1+lambdaT/2", "costs": "Actual first hit output/relative accuracy retained"},
        "alignment": "Finite-horizon moment integrals and same parameter counterfamily disprove the named inference; source eventual theorem retained.",
        "missing_lemma": "An actual deadline work/variance/acquisition theorem matched to 8 site output.",
        "falsifier": "At illustrative params T1 growth 1.00039912, not eventual infinity.",
    },
    {
        "source_subclaim": "Conditional complete fresh-cohort fate after preadmission pulse/sham/common read.",
        "destination_obligation": "Separate changed fresh feed processing from direct purge of old carbon/conservative downstream delay.",
        "source_interface": {"objects": "Label-resolved new feed cohort", "regime_and_quantifiers": "All fresh carbon admitted after write, common read/chase", "supplied_information": "Calibrated exposure, tag closure/errors", "guarantee": "Old product cannot carry fresh label", "costs": "Acquisition/chase/calibration paid"},
        "destination_interface": {"objects": "Chemical decision", "regime_and_quantifiers": "Same conditions and complete fate", "supplied_information": "Distinct ethylene/acetylene labels", "guarantee": "Conditional purge/delay exclusion, not uniquely electronic state", "costs": "Work/reset/isolated product comparison still required"},
        "alignment": "Conditional carbon chronology and conservation supply the narrow causal contrast; no experiment executed.",
        "missing_lemma": "Acquire common-regime measurement/exposure/complete fate; hidden H/reactive transport remain alternatives.",
        "falsifier": "Missing tag, changed exposure or retained fresh product countermodels defeat wider inference.",
    },
]

SPACING = {
    "real2x2": "real 2x2", "margin1/32": "margin 1/32", "margin1/44": "margin 1/44", "extraH": "extra H",
    "workerEq22": "worker Eq22", "shearEq16": "shear Eq16", "ratio0.693155287785": "ratio 0.693155287785",
    "energy0.233568631102": "energy 0.233568631102", "asynchronous4D": "asynchronous 4D", "supportedCPTP": "supported CPTP",
    "rangeD": "range D", "are2max_c": "are 2max_c", "and2max_c": "and 2max_c", "sumh²/gamma": "sum h²/gamma",
    "bounded-density3D": "bounded-density 3D", "rangeOmega": "range Omega", "additionallyOmega": "additionally Omega",
    ")sites": ") sites", "Shang-FrancaEq4": "Shang-Franca Eq4", "priorityUNKNOWN": "priority UNKNOWN",
    "allT": "all T", "is2nu/d²": "is 2nu/d²", "and36": "and 36", "order2": "order 2", "degree6": "degree 6",
    "order3": "order 3", "degree4": "degree 4", "to2.": "to 2.", "throughdegree": "through degree",
    "complex-as-real45x45matrix": "complex-as-real 45x45 matrix", "realM2rank13": "real M2 rank 13",
    "all8localizersPD": "all 8 localizers PD", "positiveunitconductances": "positive unit conductances",
    "direct2x2Hermitian": "direct 2x2 Hermitian", "casebytes": "case bytes", "open2x4Schloegl": "open 2x4 Schloegl",
    "initially50": "initially 50", "firstentrymax<=15": "first entry max<=15", "byT1": "by T1",
    "through110": "through 110", "andP(any countreaches163 by1)": "and P(any count reaches 163 by 1)",
    "Retaining0..162": "Retaining 0..162", "deadline1": "deadline 1", "Birth2.676": "Birth 2.676",
    ";death.040": "; death .040", "symmetricdiffusion8.2207nsource": "symmetric diffusion 8.2207nsource",
    "maximumdegree3": "maximum degree 3", "notIEEE": "not IEEE", "at103": "at 103",
    "firstoverflow163": "first overflow 163", "inclusivecap162": "inclusive cap 162",
    "box163^8=498311414318121121states": "box 163^8=498311414318121121 states", "billion-eventSSA": "billion-event SSA",
    "FiniteT": "Finite T", "sourceeventual": "source eventual", "atT1": "at T1", "killedhtransform": "killed h transform",
    "FeynmanKac": "Feynman Kac", "work-secondmoment": "work-second moment", "SubasiTheorem1prior": "Subasi Theorem1 prior",
    "has37%empiricalSE": "has 37% empirical SE", "NeuralM85": "Neural M85", "dynamicPdacetylene": "dynamic Pd acetylene",
    "postwrite": "post write", "ratio.2211756904": "ratio .2211756904", "suppression7.766125527s": "suppression 7.766125527s",
    "and2.484329497events/Pd": "and 2.484329497 events/Pd", "separate10s/1sV/Itrace": "separate 10s/1s V/I trace",
    ".278055400742J": ".278055400742 J", "optimum10s/.1swaveform": "optimum 10s/.1s waveform",
    "commonread": "common read", "completefate": "complete fate", "directoldproductpurge": "direct old product purge",
    "hiddenH": "hidden H", "carbonbalance": "carbon balance", "siteinventory": "site inventory",
    "missingtag": "missing tag", "freshcohort": "fresh cohort", "originalprimaryworkbooks": "original primary workbooks",
    "condition-specificflux": "condition-specific flux", "hiddenstate": "hidden state", "terminalVI": "terminal VI",
    "usefuloutput": "useful output", "OriginalXuSI/Fig2/Fig6workbooks": "Original Xu SI/Fig2/Fig6 workbooks",
    "separate5kHztrace": "separate 5kHz trace", "Wangarticle/SI": "Wang article/SI", ";200hat2sccm": "; 200h at 2sccm",
    "not100sccm": "not 100sccm", "Optimumwaveform": "Optimum waveform", "retainedfreshproduct": "retained fresh product",
    "localexposure": "local exposure", "electronicstate": "electronic state", "carbontracer": "carbon tracer",
    "subsurfaceH-C": "subsurface H-C", "WangChem2026continuous": "Wang Chem 2026 continuous",
    "usefulproduct": "useful product", "heldout": "held out", "energyadvantage": "energy advantage",
    "Externalfulltexts": "External fulltexts", "rawarrays": "raw arrays", "publicGit": "public Git",
    "Every1/Qcriterion hasQ>0 withdegeneratecase": "Every 1/Q criterion has Q>0 with degenerate case",
    "Bathfactorization": "Bath factorization", "catalogrange/product": "catalog range/product",
    "proposalrates/incidence": "proposal rates/incidence", "actualpositive": "actual positive",
    "bathHamiltonians": "bath Hamiltonians", "allowedzero-rate": "allowed zero-rate",
    "originalM2": "original M2", "passiveendpoint": "passive endpoint", "Order3sufficiency": "Order3 sufficiency",
    "universalcontainment": "universal containment", "pinnedcompleteOPF/strongerincumbents": "pinned complete OPF/stronger incumbents",
    "remainUNKNOWN": "remain UNKNOWN", "Eventualinfinitevariance/work": "Eventual infinite variance/work",
    "todeadline1": "to deadline 1", "Exactdecimaloverflow163bounds": "Exact decimal overflow163 bounds",
    "retained0..162": "retained 0..162", "suppressedcap": "suppressed cap", "hasabsolute": "has absolute",
    "absorbingoverflowFSP": "absorbing overflow FSP", "hasone-sidedbracket": "has one-sided bracket",
    "NoIEEE": "No IEEE", "insideprobability": "inside probability", "Separate10s/1s": "Separate 10s/1s",
    "optimum10s/.1schemistry": "optimum 10s/.1s chemistry", "Wang200h/2sccm": "Wang 200h/2sccm",
    "and100sccm/two-cell": "and 100sccm/two-cell", "Freshcohort": "Fresh cohort", "notidentified": "not identified",
    "Completeall-gradientproofatunchangedcoefficient": "Complete all-gradient proof at unchanged coefficient",
    "independentlycertifiednegativecompatibleprimal": "independently certified negative compatible primal",
    "Restrictedclasses,dualvaluebelow2": "Restricted classes, dual value below2", "orfiniteFourierminimado notpass": "or finite Fourier minima do not pass",
    "Reviewallload-bearingclassical/topologicalstepsatpinnedversions": "Review all load-bearing classical/topological steps at pinned versions",
    "andquantifiers": "and quantifiers", "Quantumspan/finitechecks do notsubstitute": "Quantum span/finite checks do not substitute",
    "keepinit/corrector/readoutmodel": "keep init/corrector/readout model", "andnumericalconstants": "and numerical constants",
    "Samearchitecturecontrol/noiseacquisition": "Same architecture control/noise acquisition",
    "allincidence/preparation/reset/readout/3Dresources": "all incidence/preparation/reset/readout/3D resources",
    "usablethresholds": "usable thresholds", "andmatchedmemorycomparison": "and matched memory comparison",
    "nomathematicalmodelpromotion": "no mathematical model promotion",
    "Exactmodelbytes/allconstraints": "Exact model bytes/all constraints", "verifiedduallowerandfeasibleupperbounds": "verified dual lower and feasible upper bounds",
    "matchedprecision/setup/separation/memory/runtime": "matched precision/setup/separation/memory/runtime",
    "standalonepseudo-momentisnotfullinstanceevidence": "standalone pseudo-moment is not full instance evidence",
    "Certifiedresidual/roundoffandabsolute/relativeoutputcontract": "Certified residual/roundoff and absolute/relative output contract",
    "identicalgenerator/target/deadline": "identical generator/target/deadline",
    "fullacquisition/evaluation/memory/runtime": "full acquisition/evaluation/memory/runtime",
    "againststrongestequallyinformedFSP/tensor/splitting": "against strongest equally informed FSP/tensor/splitting",
    "freshfeedfate": "fresh feed fate", "Executepreregisteredpulse/shambeforefreshlabel": "Execute preregistered pulse/sham before fresh label",
    "completefate/exposure/missingtagerrors": "complete fate/exposure/missing tag errors",
    "optimumsamewaveformswitchingwork": "optimum same waveform switching work",
    "usefulproduct/reset/feed/solvent/lifetimecomparison": "useful product/reset/feed/solvent/lifetime comparison",
    "Electroniccarrieridentityrequiresadditionaldistinguishingmeasurement": "Electronic carrier identity requires additional distinguishing measurement",
}


def whitespace_key(value):
    return re.sub(r"\s", "", value)


def replace_prose(value):
    if isinstance(value, str):
        result = value
        for before, after in sorted(SPACING.items(), key=lambda pair: -len(pair[0])):
            result = result.replace(before, after)
        need(whitespace_key(value) == whitespace_key(result), "Non-whitespace editorial mutation")
        return result
    if isinstance(value, list):
        return [replace_prose(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_prose(item) for key, item in value.items()}
    return value


def differences(before, after, path=""):
    need(type(before) is type(after), "Editorial structure/type changed: " + path)
    if isinstance(before, dict):
        need(list(before) == list(after), "Editorial keys/order changed: " + path)
        for key in before:
            yield from differences(before[key], after[key], path + "/" + key)
    elif isinstance(before, list):
        need(len(before) == len(after), "Editorial list length changed: " + path)
        for index, (old, new) in enumerate(zip(before, after)):
            yield from differences(old, new, path + "/" + str(index))
    elif before != after:
        need(isinstance(before, str) and whitespace_key(before) == whitespace_key(after), "Non-whitespace change: " + path)
        yield {"path": path, "before": before, "after": after}


def main():
    here = Path(__file__).resolve().parent
    input_path = here / "CURATION_INPUT.root-final.v0001.json"
    raw = input_path.read_bytes()
    need(digest(raw) == INPUT_SHA256, "Root v1 bytes changed")
    original = json.loads(raw)
    edited = copy.deepcopy(original)
    for item, updates in zip(edited["bridges"], BRIDGES):
        for key, value in updates.items():
            if isinstance(value, dict):
                for field, text in value.items():
                    need(whitespace_key(item[key][field]) == whitespace_key(text), "Bridge non-whitespace edit: " + key + "/" + field)
                    item[key][field] = text
            else:
                need(whitespace_key(item[key]) == whitespace_key(value), "Bridge non-whitespace edit: " + key)
                item[key] = value
    prose_fields = {
        "cards": ("scientific_scope", "statement", "reported_status", "proof_availability_scope", "assumptions", "proof_spine", "costs", "information_acquisition", "obstruction", "comparator", "missing_lemma", "next_decisive_step", "read_review_depth", "paragraphs"),
        "notices": ("issue", "clarification"), "gates": ("title", "question", "pass_condition"),
    }
    for collection, fields in prose_fields.items():
        for item in edited[collection]:
            for key in fields:
                if key in item:
                    item[key] = replace_prose(item[key])
    changes = list(differences(original, edited))
    need(changes, "No editorial changes")
    result = encoded(edited)
    output_path = here / "CURATION_INPUT.editorial.v0002.json"
    with output_path.open("xb") as stream:
        stream.write(result)
    report = {"schema": "astra.fz-whitespace-editorial-proposal.v1", "input_path": input_path.name,
              "input_sha256": INPUT_SHA256, "output_path": output_path.name, "output_sha256": digest(result),
              "changed_prose_fields": len(changes), "all_non_whitespace_characters_unchanged": True,
              "all_keys_types_list_orders_and_reference_IDs_unchanged": True,
              "selected_freeze_unchanged": edited["selected_freeze"] == original["selected_freeze"],
              "scope": "Whitespace-only editorial proposal; no mathematics, claims, quantifiers, statuses or references changed. Root must explicitly adopt a final hash before apply.",
              "changes": changes}
    with (here / "EDITORIAL_CHANGELOG.v0002.json").open("xb") as stream:
        stream.write(encoded(report))
    print(json.dumps({key: value for key, value in report.items() if key != "changes"}, indent=2))


if __name__ == "__main__":
    main()
