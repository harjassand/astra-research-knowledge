#!/usr/bin/env python3
"""Compatibility, complete-coverage and refusal checks for the new constructor."""
from fractions import Fraction as F
from pathlib import Path
import json
import neutral_source_compiler as n

P=Path(__file__).resolve().parent
def main():
    cert=json.loads((P/'results/neutral_source_overlap_certificate.json').read_text());raw=n.overlap()
    assert n.verify_certificate(raw,cert) and n.verify_certificate(list(reversed(raw)),cert)
    profile_rows=[r for r in cert['coverage'] if r['mode']=='neutral_profile']
    assert len(profile_rows)==252 and all(r['I']==[1] for r in profile_rows)
    missing=json.loads(json.dumps(cert));missing['coverage'].remove(next(r for r in missing['coverage'] if r['mode']=='neutral_profile'))
    assert not n.verify_certificate(raw,missing)
    retuned=[]
    for j,(y,z,k) in enumerate(raw):retuned.append((y,z,F(1) if j<4 else F(j+1,10**6)))
    d,canonical=n.canon(retuned);changed=json.loads(json.dumps(cert))
    changed['raw']=[(y,z,str(k)) for y,z,k in canonical];changed['raw_sha256']=n.rawdigest(canonical)
    assert n.verify_certificate(retuned,changed)
    sample=n.select(changed,(0,10**30,0,0),(0,0,0,0))
    assert any(tuple(p['selected_source'])!=tuple(p['carried_mark']) for p in sample['actual_designated_prefixes'])
    budget=n.compile_certificate(raw,word_budget=2)
    assert budget['status']=='REFUSED_BUDGET' and budget['recurrence']=='UNKNOWN'
    finite=[((1,0),(0,1),F(2)),((0,1),(1,0),F(3))]
    fcert=n.compile_certificate(finite);assert n.verify_certificate(finite,fcert) and len(fcert['excluded_faces'])==3
    # Reuse of an accepted predecessor's input is a new-code compatibility check,
    # not a re-audit of that accepted mathematical result.
    cycles=[[(0,0,0),(1,1,0),(1,0,1),(0,1,1)],[(1,0,0),(0,1,0),(0,0,1),(2,0,0)]]
    old=[]
    for cc in cycles:
        for j,y in enumerate(cc):old.append((y,cc[(j+1)%len(cc)],F(2 if y==(2,0,0) else 1)))
    inherited=n.compile_certificate(old);assert inherited['status']=='ADMITTED_NEUTRAL_CLOSURE'
    assert inherited['predecessor_whole_cone_accepted'] and all(r['mode']=='inherited_all_profiles' for r in inherited['coverage'])
    result={'complete_overlap_certificate_verified':True,'raw_order_invariance':True,
            'missing_profile_rejected':True,'rate_retuning_preserves_raw_coverage':True,
            'retuned_selector_uses_actual_source_switch':True,'word_budget_refusal':budget,
            'finite_conservative_classes':{'status':fcert['status'],'exact_excluding_invariants':len(fcert['excluded_faces'])},
            'accepted_predecessor_new_code_compatibility':{'status':inherited['status'],'inherited_rows':len(inherited['coverage']),'new_profile_rows':0},
            'scope':'Same-principal exact implementation checks; no independent mathematical audit or finite-fixture generality claim.'}
    (P/'results/neutral_compiler_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
