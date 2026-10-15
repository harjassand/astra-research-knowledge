"""Calculations from acquired cells; no physical response is synthesized or fitted."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import statistics
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources"
OUT = ROOT / "derived"

def sheet(name, tab):
    book = openpyxl.load_workbook(SRC / name, read_only=True, data_only=False)
    return book, book[tab]

def frac(value):
    return Fraction(str(value))

results = {
    "scope": "Independent arithmetic and a conditional pooling bound on published source data. No rerun of experiments.",
    "astra_pin": "b32943eeb62d0d79929a9e572a344219a785ebf9",
    "checks": [],
}

book, tab = sheet("Source_Data_ED_Fig.6.xlsx", "Fig. 6e")
ga = []
for row in range(3, 6):
    p = frac(tab[f"B{row}"].value) / 100
    y = frac(tab[f"D{row}"].value) / 100
    ga.append({
        "voltage": tab[f"A{row}"].value,
        "reported_purity_percent": float(p * 100),
        "reported_purity_std_percent": tab[f"C{row}"].value,
        "reported_yield_percent": float(y * 100),
        "reported_yield_std_percent": tab[f"E{row}"].value,
        "reported_non_target_to_target_ratio": float((1-p)/p),
        "source": {"file": "Source_Data_ED_Fig.6.xlsx", "sheet": "Fig. 6e", "range": f"A{row}:E{row}"},
    })
results["gallium_published_responses"] = ga
results["pooling_bound"] = {
    "assumptions": [
        "The reported purity uses one common, fully inventoried mass denominator for all selected fractions.",
        "Fractions are combined without further separation, selective loss, reaction or reprocessing.",
        "Means are descriptive source values, not deterministic bounds on future outcomes.",
    ],
    "statement": "For nonnegative masses m_j with common-denominator target fractions p_j, p_pool=sum(m_j*p_j)/sum(m_j) is at most max(p_j).",
    "published_mean_upper_percent": max(item["reported_purity_percent"] for item in ga),
    "nominal_99_5_percent_pooling_target_met": max(item["reported_purity_percent"] for item in ga) >= 99.5,
    "failure_scope": "Only pooling of these three published mean outputs. Does not bound new pulse histories, serial processing, new feeds, purification, or experimental variation.",
}
book.close()

book, tab = sheet("Source_Data_Fig.2.xlsx", "Fig. 2f")
indium = []
for row in range(3, 7):
    p = [tab[f"{col}{row}"].value for col in "BCD"]
    y = [tab[f"{col}{row}"].value for col in "GHI"]
    entry = {"voltage_V": tab[f"A{row}"].value,
             "purity_mean_recomputed_percent": statistics.mean(p),
             "purity_mean_source_percent": tab[f"E{row}"].value,
             "yield_mean_recomputed_percent": statistics.mean(y),
             "yield_mean_source_percent": tab[f"J{row}"].value,
             "source_range": f"'Fig. 2f'!A{row}:K{row}"}
    assert abs(entry["purity_mean_recomputed_percent"] - entry["purity_mean_source_percent"]) < 1e-5
    assert abs(entry["yield_mean_recomputed_percent"] - entry["yield_mean_source_percent"]) < 1e-5
    indium.append(entry)
results["indium_ito_source_triplet_recomputed_means"] = indium
results["checks"].append("All 8 In ITO mean checks agree with source rounded means within 1e-5 percentage points.")
book.close()

book, tab = sheet("Source_Data_Fig.3.xlsx", "Fig. 3g")
ta = []
conditions = [
    {"ETC_voltage_V": 130, "ETC_duration_s": 40, "ETCC_voltage_V": 110, "ETCC_duration_s": 40},
    {"ETC_voltage_V": 130, "ETC_duration_s": 40, "ETCC_voltage_V": 100, "ETCC_duration_s": 40},
    {"ETC_voltage_V": 130, "ETC_duration_s": 60, "ETCC_voltage_V": 100, "ETCC_duration_s": 40},
]
for row, condition in zip(range(3, 6), conditions):
    ta.append({"condition": condition,
               "condition_source": "chemrxiv_v1_article.pdf, visually checked PDF page 10 Fig. 3g; xlsx has only conditions 1, 2, 3",
               "purity_percent": tab[f"B{row}"].value,
               "purity_std_percent": tab[f"C{row}"].value,
               "yield_percent": tab[f"D{row}"].value,
               "yield_std_percent": tab[f"E{row}"].value,
               "source_range": f"'Fig. 3g'!A{row}:E{row}"})
results["tantalum_published_two_step_conditions"] = ta
book.close()

book, tab = sheet("Source_Data_Fig.4.xlsx", "Fig. 4f")
results["tantalum_scale_check"] = [
    {"input_sample": tab[f"A{row}"].value,
     "purity_raw_fraction": tab[f"B{row}"].value,
     "yield_raw_fraction": tab[f"C{row}"].value,
     "purity_percent": tab[f"B{row}"].value * 100,
     "yield_percent": tab[f"C{row}"].value * 100,
     "source_range": f"'Fig. 4f'!A{row}:C{row}"}
    for row in (3, 4)
]
book.close()

book, tab = sheet("Source_Data_ED_Fig.10.xlsx", "Fig. 10d")
results["model_energy_column_label_discrepancy"] = {
    "file": "Source_Data_ED_Fig.10.xlsx", "sheet": "Fig. 10d",
    "headers_B2_D2": [tab[f"{c}2"].value for c in "BCD"],
    "rows": [
        {"range": f"B{r}:D{r}", "values": [tab[f"{c}{r}"].value for c in "BCD"],
         "B_minus_mean_of_C_D": tab[f"B{r}"].value - (tab[f"C{r}"].value + tab[f"D{r}"].value)/2}
        for r in range(3, 7)
    ],
    "interpretation": "C numerically exceeds B and D; B is the midpoint of C and D within rounding. Header words imply a different order. No silent repair, uncertainty inference or measured energy advantage is made.",
}
assert all(abs(r["B_minus_mean_of_C_D"]) < 1e-4 for r in results["model_energy_column_label_discrepancy"]["rows"])
book.close()

# These are chemically balanced inventory identities, not reactor measurements.
M_GA = frac("69.723")
M_CL = frac("35.45")
results["chlorine_inventory_identity"] = {
    "reaction": "2 GaN + 3 Cl2 -> 2 GaCl3 + N2",
    "moles_Cl2_in_product_per_mole_Ga": "3/2",
    "g_chlorine_in_product_per_g_Ga": float(3*M_CL/M_GA),
    "atomic_mass_values_g_per_mol": {"Ga": float(M_GA), "Cl": float(M_CL)},
    "oxide_conversion_identity": "2 GaCl3 + 3 H2O -> Ga2O3 + 6 HCl",
    "scope": "Recovering unreacted Cl2 does not restore chlorine exported in chloride product. Oxide conversion moves it to HCl; subsequent chlorine regeneration is a separate paid operation if demanded by the output contract.",
}
results["clock_arithmetic"] = {
    "source": "chemrxiv_v1_article.pdf PDF pages 14, 17; Fig. 3g PDF page 10",
    "one_g_batch_every_10_min_nominal_feed_g_per_day": 1 * 86400 / (10*60),
    "Ta_best_small_sample_reported_ETC_plus_ETCC_s": 60+40,
    "reported_capacitor_feed_calcination_s": 2*3600,
    "prep_duration_divided_by_active_stage_duration": 2*3600/(60+40),
    "scope": "Descriptive recipe clocks. No uninterrupted 24-hour demonstration, product throughput, industrial dwell-time lower bound or measured energy follows.",
}

manifest = json.loads((SRC / "SOURCE_MANIFEST.json").read_text())
checked = 0
for entry in manifest["downloads"]:
    if entry["status"] == "acquired":
        data = (ROOT / entry["local"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry["sha256"]
        if entry["local"].endswith(".xlsx"):
            assert hashlib.md5(data).hexdigest() == entry["repository_md5"]
            checked += 1
results["checks"].append(f"{checked} source xlsx files verified against repository MD5 and local SHA-256 pins.")
results["checks"].append("All source pins verified against the saved downloaded bytes.")
assert checked == 11

(OUT / "CALCULATIONS.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({
    "status": "PASS_SCOPED_ARITHMETIC_AND_BYTE_INTEGRITY",
    "checks": results["checks"],
    "gallium_responses": ga,
    "pooling_bound": results["pooling_bound"],
    "chlorine_g_per_g_Ga": results["chlorine_inventory_identity"]["g_chlorine_in_product_per_g_Ga"],
}, indent=2))
