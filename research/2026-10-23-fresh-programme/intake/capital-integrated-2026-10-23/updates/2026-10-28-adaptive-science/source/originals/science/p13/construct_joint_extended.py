"""Exact further finite-cost members, without claiming global coverage."""
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
from intervals import I,full_conductance
from certify_joint_cap import design
from construct_joint_family import propose_h

HERE=Path(__file__).resolve().parent
jobs=[('20.01',('.0001','.0003')),('20.1',('.001','.003')),
      ('21',('.01','.03')),('30',('.08','.12')),('100',('.14','.18'))]
lines=['Additional exact finite-resource members at C=1/20.',
       'kappa | h | H | k | J | eta | nu']
for Ks,start in jobs:
    C,kappa=Q(1,20),Q(Ks)
    h=propose_h(C,kappa,start)
    sc=10**40;center=int(mp.floor(h*sc));lo=Q(center-1,sc);hi=Q(center+2,sc)
    left,right=design(lo,C,kappa),design(hi,C,kappa)
    assert left['res'].lo>0>right['res'].hi
    row=design(I(lo,hi),C,kappa)
    assert all(row[k].lo>0 for k in ['h','b','H','k','eta','nu'])
    J=full_conductance(row['edges'])
    lines.append(' | '.join([Ks,row['h'].decimal(16),row['H'].decimal(16),
                              row['k'].decimal(16),J.decimal(20),
                              row['eta'].decimal(16),row['nu'].decimal(20)]))
lines.append('PASS: proper exact five-edge candidates; universal five-root theorem proves globality.')
text='\n'.join(lines)+'\n'
(HERE/'CERTIFIED_JOINT_EXTENDED.txt').write_text(text)
print(text)
