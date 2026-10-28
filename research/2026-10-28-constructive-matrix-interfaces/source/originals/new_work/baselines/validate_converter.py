#!/usr/bin/env python3
"""A small end-to-end check: unique extensions, original count, two solvers.

This control is not a performance fixture. The 72-input benchmark itself is
unaltered. Full CNF truth enumeration here is independent of circuit evaluation.
"""
from collections import Counter
from pathlib import Path
import itertools
import json
import re
import subprocess

from circuit_to_cnf import check_gate_templates, convert

base=Path(__file__).resolve().parent
out=base/'controls'; out.mkdir(exist_ok=True)
check_gate_templates()
circuit={'inputs':3,'gates':[
    {'op':'const','args':[],'value':1},
    {'op':'and','args':[0,1]},
    {'op':'xor','args':[0,2]},
    {'op':'and','args':[4,5]},
    {'op':'xor','args':[6,3]}], 'output':7}
(out/'control.json').write_text(json.dumps(circuit,indent=2)+'\n')
meta=convert(out/'control.json',out/'control.cnf')
clauses=[]
for line in (out/'control.cnf').read_text().splitlines():
    if line and line[0] not in 'cp': clauses.append(list(map(int,line.split()))[:-1])
extensions=Counter()
for assignment in itertools.product((0,1),repeat=8):
    if all(any(assignment[abs(lit)-1]==(lit>0) for lit in clause) for clause in clauses):
        extensions[assignment[:3]]+=1
expected={a for a in itertools.product((0,1),repeat=3)
          if 1 ^ ((a[0]&a[1])&(a[0]^a[2]))}
assert set(extensions)==expected
assert set(extensions.values())=={1}
assert len(expected)==7
commands=[('d4',[str(base/'vendor/d4/d4'),'-mc',str(out/'control.cnf')],base),
          ('sharpsat_td',['./sharpSAT','-decot','1','-decow','100','-tmpdir',str(out),
                           '-cs','100',str(out/'control.cnf')],
           base/'vendor/sharpsat-td/local_build')]
results=[]
for name,command,cwd in commands:
    done=subprocess.run(command,cwd=cwd,text=True,stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,timeout=10)
    (out/(name+'.log')).write_text(done.stdout)
    patterns=[r'^s\s+mc\s+(\d+)\s*$',r'^s\s+(\d+)\s*$',
              r'^c\s+s\s+exact\s+arb\s+int\s+(\d+)\s*$']
    counts=[int(m.group(1)) for pat in patterns for m in re.finditer(pat,done.stdout,re.M)]
    if not counts:
        raise AssertionError((name,'unrecognized count output',done.stdout))
    assert done.returncode==0 and counts[-1]==7,(name,done.returncode,counts)
    results.append({'solver':name,'exit_code':done.returncode,'reported_count':counts[-1]})
result={'original_inputs':3,'original_truth_table_count':7,'cnf_full_truth_table_count':7,
        'unique_internal_extension_verified_for_each_accepted_input':True,
        'gate_templates_truth_table_checked':True,'solvers':results}
(out/'control_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
