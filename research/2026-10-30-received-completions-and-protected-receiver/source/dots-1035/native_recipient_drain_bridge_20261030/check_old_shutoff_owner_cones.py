"""Exact accepted two-owner label table: zero-LOAD owner-cone invariance.
This verifies predicate identities on all malformed labels, not a probability or
threshold simulation. Physical DATA classification is supplied by the gate list.
No accepted file is edited or imported with its top-level file-writing test.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json
root=Path('producer-workspace/native_locc_rollback_integration_20261030')
p=root/'check_extended_owner_table.py'
source=p.read_text(); ns={}
exec(compile(source.split('states=list(product')[0], str(p)+'[definitions]', 'exec'),ns)
phases,locks,supports,trans=(ns[x] for x in ('phases','lockoptions','supports','trans'))
def active(s,h):
    return not(s[0][h][0] in {'I','Q'} and all(s[1][r] not in {f'o{h}',f'z{h}'} for r in supports[h]))
def Q(S,s):return all(h in S or not active(s,h) for h in range(2))
def owner(s,ss):
    changed=[h for h in range(2) if s[0][h]!=ss[0][h]]
    assert len(changed)==1
    return changed[0]
payload={'gate','ungate','rollback_inverse','rollback_forward'}
states=list(product(product(*phases),product(*locks)))
counts=Counter(); q_checks=0; data_checks=0
for s in states:
    for ss,kind,coherent in trans(s,False):
        counts[kind]+=1
        for mask in range(4):
            S={h for h in range(2) if mask>>h&1}
            if Q(S,s):
                assert Q(S,ss),(s,ss,kind,S)
                q_checks+=1
                if kind in payload:
                    h=owner(s,ss)
                    assert h in S and active(s,h) and active(ss,h)
                    data_checks+=1
        if kind in payload:
            assert coherent
            h=owner(s,ss)
            assert s[0][h][0] in {'C','B'} and ss[0][h][0] in {'C','B'}
            assert all(active(s,g)==active(ss,g) for g in range(2))
# An explicit consistent nonzero B rail can stay auxiliary-stalled after all
# payload edges are shut off; the support theorem does not need its completion.
stalled=((('B',1,1),('I',0)),('o0','o0','f'))
assert stalled in states
out=list(trans(stalled,False))
remaining=[(ss,k) for ss,k,c in out if k not in payload]
assert all(ss[0][0]==('B',1,1) for ss,k in remaining)
result={
 'accepted_definition_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'basis_configurations':len(states),
 'zero_LOAD_directed_transitions':sum(counts.values()),
 'source_Q_S_preservation_checks':q_checks,
 'payload_inside_S_checks':data_checks,
 'all_zero_LOAD_terms_preserve_every_source_FREE_predicate':True,
 'only_C_and_B_edges_carry_DATA_in_actual_gate_inventory':sorted(payload),
 'explicit_stalled_B_phase_after_payload_shutoff':['B',1,1],
 'stalled_phase_can_remain_without_invalidating_DATA_decoupling':True,
 'scope':'all finite fixture label predicates; physical quantum coefficient and bath support follow separately from exact source resolution and owner-cone proof'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
