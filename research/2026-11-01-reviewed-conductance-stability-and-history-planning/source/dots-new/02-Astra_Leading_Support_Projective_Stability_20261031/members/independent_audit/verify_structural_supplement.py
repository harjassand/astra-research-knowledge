#!/usr/bin/env python3
"""Independent reconstruction of larger qualitative support fixtures."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,importlib.util,sys
from verify_projective import p,support
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.modules['projective_mass']=p
spec=importlib.util.spec_from_file_location('receiver',HERE/'frozen_structural_receiver.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
x=json.loads((ROOT/'qualitative_controls_results.json').read_text())
N=5;A=N-1;z=(0,)*N;unit=tuple(int(i==A) for i in range(N));raw=[(z,unit,F(1)),(unit,z,F(1))]
for j in range(N-1):
 u=tuple(2*int(i==j) for i in range(N));v=tuple(int(i==j)+int(i==j+1) for i in range(N));raw.extend([(u,v,F(j+1)),(v,u,F(1,j+1))])
sp=['B1','B2','B3','B4','A'];receipt=x['five_species_chain'];assert support(p.recognize(sp,raw),receipt['support_witness'])
assert s.verify(sp,raw,receipt)==x['five_species_receiving_pass'];assert len(receipt['support_witness']['trials'][0]['steps'])==4
order=10**50;raw2=[((0,0),(1,0),1),((1,0),(0,0),1),((0,order),(1,order-1),1),((1,order-1),(0,order),1)]
r2=x['huge_encoded_order_qualitative'];assert support(p.recognize(['A','B'],raw2),r2['support_witness']);assert s.verify(['A','B'],raw2,r2)==x['huge_receiving_pass']
assert 'Euler_steps_M' not in r2['support_witness'] and r2['work']['Euler_steps_executed']==r2['work']['polynomial_degrees_searched']==0
print(json.dumps({'five_species_chain_independent_raw_support_pass':True,'open_coordinate':4,'longest_supplied_support_chain':4,
 'encoded_order_independent_raw_support_pass':order,'formal_scalar_Euler_fields_absent':True,
 'source_controls_sha256':hashlib.sha256((ROOT/'qualitative_controls.py').read_bytes()).hexdigest(),
 'source_results_sha256':hashlib.sha256((ROOT/'qualitative_controls_results.json').read_bytes()).hexdigest()},indent=2))
