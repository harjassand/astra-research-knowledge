"""Exact candidate-dependent preflight scope check and invalid role-selection witness."""
from fractions import Fraction as F
from pathlib import Path
import json
p=F(1,3);expected_actual=F(0);expected_estimate=F(0);active_mass=F(0)
# Candidate publication changes source loss; runtime-cap survival depends on candidate.
for candidate,cprob in [(0,F(1,2)),(1,F(1,2))]:
 survival=F(1) if candidate==0 else F(1,2)
 # A public-candidate-reactive source is allowed by direct conditional soundness.
 loss=F(candidate)
 for role,rprob in [('learn',p),('service',1-p)]:
  mass=cprob*survival*rprob;active_mass+=mass
  expected_actual+=mass*loss
  expected_estimate+=mass*(loss/p if role=='learn' else 0)
assert expected_actual==expected_estimate==F(1,4)
assert active_mass==F(3,4)
# INVALID alternative: draw role first, then survive depending on that role.
# Unit loss; all learning calls survive but only half services.
actual=p+(1-p)/2;estimated=p/p
assert actual==F(2,3) and estimated==1
out=dict(valid_candidate_dependent_preflight=dict(expected_active_selected_loss=str(expected_actual),expected_inverse_probability_counter=str(expected_estimate),survival_mass=str(active_mass)),invalid_role_dependent_selection=dict(actual_active_loss=str(actual),misweighted_counter=str(estimated)),scope='Finite scalar diagnostic of the ordering proof; not a quantum hardware construction.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
