"""Audit published measurements and Table S2 from Szymanski et al. (2024).

Source DOI: 10.1126/sciadv.adp3309. Table S2 is transcribed explicitly below.
Input workbook is the unchanged publisher supplement adp3309_data_s1.xlsx.
This script reanalyses published observations; it creates no synthetic evidence.
Run with the bundled scientific Python. Requires pandas, numpy, matplotlib.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ROWS = []

def add(phases, cases):
    for reactants, energies, observed in cases:
        ROWS.append(dict(reactants=reactants, phases=phases.split(),
                         energies_meV_per_atom=energies, observed_first=observed))

add('Li3NbO4 LiNbO3 LiNb3O8', [
 ('Li2CO3-Nb2O5',[-35,-30,-21],'LiNbO3'),
 ('LiOH-Nb2O5',[-127,-62,-37],'Li3NbO4')])
add('Li2MnO3 LiMnO2 LiMn2O4', [
 ('Li2CO3-MnO',[-224,-262,-367],'LiMn2O4'),
 ('Li2CO3-Mn3O4',[-93,-47,-89],'LiMn2O4'),
 ('Li2CO3-Mn2O3',[-97,-46,-37],'LiMn2O4'),
 ('Li2CO3-MnO2',[-53,-10,-39],'LiMn2O4'),
 ('LiOH-MnO',[-255,-309,-425],'LiMn2O4'),
 ('LiOH-Mn3O4',[-141,-108,-124],'LiMnO2'),
 ('LiOH-Mn2O3',[-129,-94,-98],'LiMnO2'),
 ('LiOH-MnO2',[-238,-71,-141],'Li2MnO3'),
 ('Li2O-MnO2',[-250,-67,-147],'Li2MnO3')])
add('NaMnO2 Na2Mn3O7',[
 ('Na2CO3-MnO',[-278,-321],'Na2Mn3O7'),
 ('Na2CO3-Mn3O4',[-57,-91],'Na2Mn3O7'),
 ('Na2CO3-MnO2',[-82,-214],'Na2Mn3O7'),
 ('NaNO3-MnO',[-240,-302],'Na2Mn3O7'),
 ('NaNO3-Mn2O3',[-86,-97],'Na2Mn3O7'),
 ('NaNO3-MnO2',[-132,-114],'Na2Mn3O7')])
add('Li5FeO4 Li2FeO3 LiFeO2',[
 ('Li2CO3-Fe3O4',[38,-28,-79],'LiFeO2'),
 ('LiOH-Fe3O4',[92,-56,-116],'LiFeO2')])
add('Na3FeO3 NaFeO2',[
 ('Na2CO3-Fe3O4',[42,-71],'NaFeO2'),
 ('NaNO3-Fe3O4',[-156,-287],'NaFeO2')])
add('Na3NbO4 NaNbO3 NaNb3O8',[
 ('Na2CO3-Nb2O5',[-7,-74,-24],'NaNbO3'),
 ('NaNO3-Nb2O5',[-107,-128,-66],'Na2Nb4O11')])
add('Li4MoO5 Li2MoO4',[
 ('Li2CO3-MoO2',[-81,-205],'Li2MoO4'),
 ('LiOH-MoO2',[-165,-276],'Li2MoO4')])
add('Na4MoO5 Na2MoO4 Na2Mo2O7',[
 ('Na2CO3-MoO2',[-43,-211,-258],'Na2MoO4'),
 ('Na2CO3-MoO3',[32,-44,-62],'Na2MoO4'),
 ('NaNO3-MoO2',[21,-72,-174],'Na2Mo2O7')])
add('Li3VO4 LiVO3 LiV3O8',[
 ('Li2CO3-VO2',[-112,-134,-132],'LiVO3'),
 ('Li2CO3-V2O5',[-84,-68,-31],'LiV2O5')])
add('Na3VO4 NaVO3',[
 ('Na2CO3-VO2',[-153,-357],'NaVO3'),
 ('Na2CO3-V2O5',[-94,-139],'NaxV2O5')])
add('Li6CoO4 LiCoO2 LiCo2O4',[
 ('Li2CO3-Co3O4',[81,-32,-38],'LiCoO2')])
add('Li6Zr2O7 Li2ZrO3',[
 ('Li2CO3-ZrO2',[-37,-47],'Li2ZrO3')])
add('Li4TiO4 Li2TiO3 Li4Ti5O12',[
 ('Li2CO3-TiO2',[-26,-82,-45],'Li2TiO3')])
add('Na8Ti5O12 Na4Ti5O12 Na2Ti3O7',[
 ('Na2CO3-TiO2',[-139,-181,-63],'Na4Ti5O12'),
 ('NaNO3-TiO2',[-220,-241,-134],'Na2Ti3O7')])


def run():
    assert len(ROWS) == 37
    derived=[]
    for row in ROWS:
        vals=np.array(row['energies_meV_per_atom'])
        order=np.argsort(vals)
        predicted=row['phases'][int(order[0])]
        derived.append({**row, 'predicted_first':predicted,
                        'margin_meV_per_atom':int(vals[order[1]]-vals[order[0]]),
                        'matches_observation':predicted==row['observed_first']})
    high=[r for r in derived if r['margin_meV_per_atom'] >= 60]
    low=[r for r in derived if r['margin_meV_per_atom'] < 60]
    outcome_summary={
        'all':{'n':len(derived),'matches':sum(r['matches_observation'] for r in derived)},
        'margin_at_least_60':{'n':len(high),'matches':sum(r['matches_observation'] for r in high)},
        'margin_below_60':{'n':len(low),'matches':sum(r['matches_observation'] for r in low)},
        'maximum_failed_margin':max(r['margin_meV_per_atom'] for r in derived if not r['matches_observation']),
        'threshold_status':'in-sample, selected after seeing these measurements; not an independently validated universal threshold',
        'energy_temperature':'evaluated at experimentally observed onset; not a prediction of onset temperature',
        'source_inconsistency':'NaNO3-TiO2 table assigns -220 to Na8Ti5O12 and -134 to observed Na2Ti3O7; main text assigns -220 to observed Na2Ti3O7. Top-two margin is 21 either way; no silent correction made.',
    }
    missing=[r for r in derived if r['observed_first'] not in r['phases']]
    conservative=[r for r in derived if r['observed_first'] in r['phases']
                  and r['reactants'] != 'NaNO3-TiO2']
    conservative_low=[r for r in conservative if r['margin_meV_per_atom'] < 60]
    outcome_summary['candidate_inventory_audit']={
        'observed_product_absent_from_ranked_candidates':[
            {'reactants':r['reactants'],'observed_first':r['observed_first']} for r in missing],
        'conservative_comparable_subset':{'n':len(conservative),
            'matches':sum(r['matches_observation'] for r in conservative)},
        'conservative_margin_below_60':{'n':len(conservative_low),
            'matches':sum(r['matches_observation'] for r in conservative_low)},
        'interpretation':'Three mismatches include an observed product absent from the ranked stable-phase inventory; one additional case has a source energy-label inconsistency. Excluding all four leaves ten mismatches. No mismatch alone proves a kinetic mechanism or excludes free-energy error.'}
    book=ROOT/'phase_data/adp3309_data_s1.xlsx'
    sheets=pd.read_excel(book,sheet_name=None)
    lookup={r['reactants']:r for r in derived}
    first_rows=[]
    trajectories=[]
    sums=[]
    for name,df in sheets.items():
        precursors=set(name.split('-'))
        products=[c for c in df.columns if c != 'Temperature' and c not in precursors
                  and (('Li' in c) or ('Na' in c))]
        sums.extend(df.drop(columns='Temperature').sum(axis=1).tolist())
        for _,r in df.iterrows():
            for phase in df.columns[1:]:
                trajectories.append({'reactants':name,'temperature_C':float(r['Temperature']),
                                     'phase':phase,'refined_weight_fraction':float(r[phase])})
        for threshold in [0.01,0.02,0.05,0.10]:
            detections=[]
            for phase in products:
                mask=df[phase].to_numpy() >= threshold
                # Require two consecutive detections. This is a sensitivity rule,
                # not a replacement for the authors' pattern-level judgment.
                inds=np.flatnonzero(mask[:-1]&mask[1:])
                if len(inds):
                    i=int(inds[0]);detections.append((float(df.iloc[i]['Temperature']),phase))
            if detections:
                temp=min(x[0] for x in detections)
                phases=sorted(x[1] for x in detections if x[0]==temp)
            else:temp=None;phases=[]
            first_rows.append(dict(reactants=name,threshold_weight_fraction=threshold,
                                   detected_temperature_C=temp,first_phase_set=phases,
                                   published_first=lookup[name]['observed_first'],
                                   agrees_published=lookup[name]['observed_first'] in phases))
    robust=[]
    for name in sheets:
        rr=[r for r in first_rows if r['reactants']==name]
        robust.append(dict(reactants=name,
                           all_thresholds_match=all(r['agrees_published'] for r in rr),
                           phase_set_invariant=len({tuple(r['first_phase_set']) for r in rr})==1,
                           onset_spread_C=(max(r['detected_temperature_C'] for r in rr if r['detected_temperature_C'] is not None)
                                           -min(r['detected_temperature_C'] for r in rr if r['detected_temperature_C'] is not None))))
    outcome_summary['workbook']={
        'sha256':hashlib.sha256(book.read_bytes()).hexdigest(),
        'sheets':len(sheets),'temperature_rows':sum(len(x) for x in sheets.values()),
        'max_weight_sum_deviation_from_one':max(abs(np.array(sums)-1)),
        'phase_identity_invariant_all_four_thresholds':sum(r['phase_set_invariant'] for r in robust),
        'published_phase_matched_all_four_thresholds':sum(r['all_thresholds_match'] for r in robust),
        'agreement_by_threshold':{str(t):sum(r['agrees_published'] for r in first_rows if r['threshold_weight_fraction']==t)
                                  for t in [0.01,0.02,0.05,0.10]},
        'median_onset_spread_C':float(np.median([r['onset_spread_C'] for r in robust])),
        'max_onset_spread_C':max(r['onset_spread_C'] for r in robust),
        'caution':'Rietveld fitted fractions, no independent replicate-derived errors in these sheets; thresholds are sensitivity diagnostics only.'}
    (ROOT/'thermodynamic_audit.json').write_text(json.dumps(outcome_summary,indent=2))
    (ROOT/'table_s2_transcribed.json').write_text(json.dumps(derived,indent=2))
    (ROOT/'onset_sensitivity.json').write_text(json.dumps(first_rows,indent=2))
    (ROOT/'onset_sensitivity_by_reaction.json').write_text(json.dumps(robust,indent=2))
    (ROOT/'phase_trajectories.json').write_text(json.dumps(trajectories,indent=2))
    print(json.dumps(outcome_summary,indent=2))
    return derived,first_rows


if __name__=='__main__':
    run()
