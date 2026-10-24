"""Independent read-only source/formula checks for the released ammonia peer.
Run with the bundled Python. Original XLSX and peer files are never exported
or overwritten. Outputs are review-only scientific arithmetic, not experiments.
"""
from pathlib import Path
from fractions import Fraction as Q
import bisect
import hashlib
import json
import math
import openpyxl

HERE = Path(__file__).resolve().parent
PEER = HERE.parent / 'open_framing'
DATA = PEER / 'sources/41467_2026_71299_MOESM5_ESM.xlsx'
F = 96485.33212
M_H2, M_NH3 = .002016, .017031


def kg_energy(kj_mol):
    return kj_mol/(3600*M_NH3)


def interpolate_by_sorted_j(points, at_j):
    # Independent interpolation after explicit sorting by current density.
    p = sorted(points)
    jj = [x for x, _ in p]
    i = bisect.bisect_left(jj, at_j)
    if i == 0 or i == len(p):
        raise ValueError('target not inside measured range')
    x0, y0 = p[i-1]
    x1, y1 = p[i]
    return y0 + (at_j-x0)*(y1-y0)/(x1-x0)


def main():
    before = hashlib.sha256(DATA.read_bytes()).hexdigest()
    w = openpyxl.load_workbook(DATA, read_only=True, data_only=False)
    s = w['Figure  6c']
    pol = {}
    for conc, cols in [(10, (1, 2)), (100, (7, 8))]:
        p = []
        for row in s.iter_rows(min_row=3, values_only=True):
            a, b = (row[cols[0]-1], row[cols[1]-1])
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                p.append((a, b))
        pol[str(conc)] = interpolate_by_sorted_j(p, 200)

    s = w['Figure  6d']
    seg = []
    for col in range(4, 21, 2):
        obs = []
        for row in s.iter_rows(min_row=2, min_col=col, max_col=col+1, values_only=True):
            if all(isinstance(v, (int, float)) for v in row):
                obs.append(row)
        positive_intervals = [(t1-t0, (v0+v1)/2)
                              for (t0, v0), (t1, v1) in zip(obs, obs[1:])
                              if t1 > t0]
        duration = math.fsum(dt for dt, _ in positive_intervals)
        integrated_v = math.fsum(dt*mv for dt, mv in positive_intervals)
        seg.append((duration, integrated_v))
    time = math.fsum(t for t, _ in seg)
    voltage = math.fsum(v for _, v in seg)/time
    fe = [row[1] for row in s.iter_rows(min_row=2,min_col=1,max_col=2,values_only=True)
          if all(isinstance(v,(int,float)) for v in row)]

    s = w['Supplementary Figure 21']
    ni = [(s[f'R{r}'].value, s[f'S{r}'].value, s[f'T{r}'].value)
          for r in range(4, 10)]
    initial = ni[0][1]
    residual = max(abs(a+b-initial) for _, a, b in ni)
    formulas = [s.cell(r, c).coordinate for r in range(4, 10) for c in (18, 19, 20)
                if s.cell(r, c).data_type == 'f']
    # 85.75663ug N/mL *30mL, divide by g/mol N and by100min*0.6cm2.
    partial_j = ni[-1][2]*30/1e6/14.007 * 6*F/(100*60*.6)*1000

    # Exact alkali/ion closure, all coefficients in integer-molecule modules.
    species = {
        'KNO2': {'K':1,'N':1,'O':2}, 'KNO3': {'K':1,'N':1,'O':3},
        'KOH': {'K':1,'O':1,'H':1}, 'H2': {'H':2}, 'H2O': {'H':2,'O':1},
        'N2': {'N':2}, 'O2': {'O':2}, 'NH3': {'N':1,'H':3},
    }
    reactions = {
        'nitrite_reduction': {'KNO2':-1,'H2':-3,'NH3':1,'KOH':1,'H2O':1},
        'nitrate_reduction': {'KNO3':-1,'H2':-4,'NH3':1,'KOH':1,'H2O':2},
        'nitrite_loading': {'N2':-1,'O2':-Q(3,2),'KOH':-2,'KNO2':2,'H2O':1},
        'nitrate_loading': {'N2':-1,'O2':-Q(5,2),'KOH':-2,'KNO3':2,'H2O':1},
    }
    for name, r in reactions.items():
        atoms = {}
        for sp, coeff in r.items():
            for atom, num in species[sp].items():
                atoms[atom] = atoms.get(atom, 0)+coeff*num
        assert all(x == 0 for x in atoms.values()), (name, atoms)

    # Source point gives gross anodic HOR; net fresh hydrogen needs gas fate.
    fe_n = .81
    exported = kg_energy(8*F*.1/1000/fe_n)
    gross = 4/fe_n
    h2_cases = []
    for chi, rho in [(0, 0), (.19, 1)]:
        qfresh = gross*(1-rho*chi)
        hinput = qfresh*M_H2/M_NH3*50
        h2_cases.append({
            'NH3_FE': fe_n, 'conditional_cathodic_H2_FE': chi,
            'conditional_H2_recovery_fraction': rho,
            'fresh_H2_mol_per_NH3': qfresh,
            'fresh_H2_electricity_kWh_kgNH3': hinput,
            'net_after_same_export_kWh_kgNH3': hinput-exported,
            'HB_overhead_threshold_before_candidate_fixation_separation_kWh_kgNH3':
                hinput-exported-1.5*M_H2/M_NH3*50})

    # Keep the distinct primary Bunea conditions distinct. The93% case is
    # retained only as an unresolved jointV/FE sensitivity, not a verified point.
    no_cases = []
    for V, FE, label in [(1.9,.78,'primary standard voltage sweep;approxFE'),
                          (2.1,.57,'primary 0.51mmol_cm2_h yield point'),
                          (1.9,.93,'jointV/FE conditional until Fig6 verified')]:
        e = kg_energy(5*F*V/1000/FE)
        no_cases.append({'voltage_V':V,'NH3_FE':FE,'source_scope':label,
                         'cell_electricity_kWh_kgNH3':e,
                         'plus_absorbed_plasma_420kJ_molN_kWh_kgNH3':e+kg_energy(420)})

    G_H, G_NH3, G_NO = 237.141, -16.367, 86.600
    target = G_NH3+1.5*G_H
    ideal_floor = {}
    for q, name in [(3,'nitrite'),(4,'nitrate'),(2.5,'NO')]:
        wH = 50*M_H2*3600
        ideal_floor[name] = kg_energy(target+q*(wH-G_H))

    after = hashlib.sha256(DATA.read_bytes()).hexdigest()
    assert before == after
    out = {
        'source_xlsx_hash_before_and_after': before,
        'source_unchanged': True,
        'independent_LSV_consumed_V_at200mA_cm2': pol,
        'independent_time_series': {'integrated_duration_h':time,
                                    'mean_consumed_voltage_V':voltage,
                                    'number_of_voltage_series':len(seg),
                                    'FE_arithmetic_mean_percent':math.fsum(fe)/len(fe),
                                    'FE_sample_count':len(fe),
                                    'scope':'no independent integrated NH3 assay or closed inventory'},
        'nitrite_original_R4_T9': ni,
        'nitrite_column_formula_cells': formulas,
        'nitrite_max_Nsum_residual_ug_ml': residual,
        'nitrite_NH3_column_equivalent_partial_j_mA_cm2': partial_j,
        'exact_atom_balance_checks':list(reactions),
        'q_for_nitrate_fraction_f':'3+f only at complete NH3 conversion and matched carrier states',
        'gross_anodic_H2_mol_NH3':gross,
        'export_energy_at_source_0p1V_kWh_kgNH3':exported,
        'fresh_H2_conditions':h2_cases,
        'Bunea_separated_conditions':no_cases,
        'same_state_ideal_other_stages_floor_kWh_kgNH3_at50kWh_kgH2':ideal_floor,
        'same_state_NO_OER_reversible_V':(target-G_NO)*1000/(5*F),
        'plasma_absorbed_to_applied_power_ratio':.76/.1,
        'same_yield_applied_MJ_molNOx':.42*.76/.1,
        'scope':'all process values conditional; gas-fate and joint-source-point repairs are material'}
    (HERE/'review_open_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
