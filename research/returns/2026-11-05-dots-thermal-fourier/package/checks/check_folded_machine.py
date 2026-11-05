#!/usr/bin/env python3
"""Independent ordinary two-sided tape oracle against the compiled local rule.
This tests finite simulations, not a proof of undecidability or nonhalting.
"""
import importlib.util, sys, random, json
from pathlib import Path
path=Path(__file__).with_name('check_explicit_tableau_grammar.py')
spec=importlib.util.spec_from_file_location('grammar_under_audit',path)
g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
rng=random.Random(20261105)
checks=0; trajectories=0; outcomes={}
for trial in range(160):
    states=('q0','q1','q2')
    delta={(q,s):(rng.choice(states+(g.HALT,)),rng.choice(('0','1')),rng.choice((-1,0,1))) for q in states for s in ('0','1')}
    word=tuple(rng.choice(('0','1')) for _ in range(rng.randrange(0,6)))
    M=g.Machine(('0','1'),'0',states,'q0',delta,word)
    for width in range(max(2,len(word)),9):
        row=M.initial(width)
        tape={i:word[i] for i in range(len(word))}
        head=0;state='q0'
        trajectories+=1
        for step in range(120):
            # Decode the local state into actual signed tape coordinates.
            decoded={}
            hh=[]
            for j,c in enumerate(row):
                assert not c.poison,(trial,width,step,'poison')
                assert c.b==int(j==0)
                decoded[j]=c.pair[0];decoded[-j-1]=c.pair[1]
                if c.head is not None:
                    q,tr=c.head;hh.append((j if tr==0 else -j-1,q))
            assert hh==[(head,state)],(trial,width,step,'head',hh,head,state)
            assert all(decoded[i]==tape.get(i,'0') for i in range(-width,width)),(trial,width,step,'tape')
            checks+=1
            if state in (g.HALT,g.REJECT):
                outcomes[state]=outcomes.get(state,0)+1
                # Absorption is independently checked for three extra steps.
                for _ in range(3):
                    assert M.step(row)==row
                break
            qnew,write,move=delta[state,tape.get(head,'0')]
            tape[head]=write
            target=head+move
            if not (-width<=target<width):
                state=g.REJECT  # overflow takes precedence over HALT
            else:
                head=target;state=qnew
            row=M.step(row)
        else:
            outcomes['bounded_prefix_no_halt']=outcomes.get('bounded_prefix_no_halt',0)+1
result={'seed':20261105,'random_machines':160,'trajectories':trajectories,'independent_state_tape_comparisons':checks,'outcomes':outcomes,'all_checks_passed':True,'scope':'Two-symbol, three-state random machines; ordinary signed-tape oracle; all 120-step finite prefixes only.'}
Path(__file__).with_name('folded_machine_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
