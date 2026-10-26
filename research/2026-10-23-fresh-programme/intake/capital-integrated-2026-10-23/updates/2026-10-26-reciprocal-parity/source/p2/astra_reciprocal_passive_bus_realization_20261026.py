#!/usr/bin/env python3
"""Two local emitters + two physical side oscillators with symmetric real couplings.
G = g_d I + g_cross sigma_x; H_side = Omega0 I + J sigma_x.
Parity transform reproduces the exact two compensated Fano poles. No synthetic flux.
"""
from astra_reciprocal_parity_design_probe_20261026 import params
import numpy as np,json
from math import sqrt
from numpy.linalg import norm,eigvalsh
P=params('1.1','1');rp=P[0]['r'];rm=P[1]['r'];op=P[0]['Omega'];om=P[1]['Omega']
gp=sqrt(rp);gm=sqrt(rm)
gdirect=(gp+gm)/2;gcross=(gp-gm)/2
Omega0=(op+om)/2;J=(op-om)/2
sigma=np.array([[0.,1.],[1.,0.]])
G=gdirect*np.eye(2)+gcross*sigma
Hside=Omega0*np.eye(2)+J*sigma
up=np.array([1,1])/sqrt(2);um=np.array([1,-1])/sqrt(2)
Pmatrix=np.vstack([up,um]).T
for e in np.linspace(1.452,1.548,101):
 exact=Pmatrix@np.diag([rp/(op-e),rm/(om-e)])@Pmatrix.T
 physical=G@np.linalg.inv(Hside-e*np.eye(2))@G.T
 assert norm(physical-exact)<2e-13
assert eigvalsh(Hside).min()>0
out={'physical_aux_graph':'two ordinary positive-energy harmonic side sites with mutual real hopping J, each coupling directly and across to the two emitters',
     'side_site_frequency_Omega0':Omega0,'side_side_hopping_J':J,
     'direct_emitter_aux_coupling_gdirect':gdirect,
     'cross_emitter_aux_coupling_gcross':gcross,
     'cross_to_direct_coupling_ratio':gcross/gdirect,
     'side_graph_energies':eigvalsh(Hside).tolist(),
     'max_resolvent_difference_101_samples':'less than 2e-13',
     'local_only_obstruction':'With g_cross=0 and symmetric local contacts, the two parity residues must be equal; the certified design has residues 51.9213 and 0.14491. This exact target needs a cross-contact or a different larger/more complex network.',
     'scope':'Exact unitary basis transformation in the finite signal Hamiltonian; numerical samples only audit the algebra. Does not establish device fabricability, independent radiation suppression, or passive static spatial delays.'}
with open('/mnt/data/astra_reciprocal_passive_bus_results_20261026.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
