# A sharper full-cycle inverse-m interface

30 October 2026. Synthesis completion conditional only on the actual profile-preserving repair already constructed in the full candidate Sections 2–3. It does not assume recurrence or independent outputs.

Start at active B=q with the section-cycle flag unset. Every cycle has a first connector event. All three possible first connector events are EXACTLY r-neutral at B=q, and their output phases are respectively q+1, 2q-1, and 0. These are fixed phases.

The actual repair, including all dormant Green excursions and inactive seeding, transports w f_m from each such phase with a uniform fixed constant. Therefore

`P[w(r_next) f_m(A_next)] <= C w(r_in) E[f_m(A_first_connector_out)]`.

The three compensators give

- immigration: `i E integral f_m(A+1)dt <= i T`;
- activation: `t q E integral A f_m(A+m-1)dt <= C T`;
- clearing: `d(q)_q E integral (A)_m f_m(A-m)dt <= C T`.

Thus the UNRESTRICTED section output obeys

`P[w_next f_m(A_next)] <= C w T`.                       (FM)

Here T is the complete first-connector time, allowing repeated local dormant/seeded transitions. There is no additional direct dormant-entry term: such transitions precede the first connector and are already included in T and the actual output law.

This strengthens the frozen candidate's interface (M+) and gives all bad-entry bounds using the same quantity T:

- On positive-D input, T<=C/r, so P(w f_m)<=Cw/r.
- On dormant input, T<=C f_m(A_in), so P(w f_m)<=Cw f_m(A_in).
- On good input of either type, T/U<=C/(1+A_in), so correction leakage controlled by f_m is o(Uw).

For the w/r terminal weight and threshold A_next<=K(r_next), repeat the actual repair with the corresponding fixed polynomial residual factor. This gives the matrix entries K^m/r times these same bounds. It is not an independence argument, nor a replacement of r_next by r_in without its weighted kernel estimate.

The non-small purely dormant R00 Green and the small seed-mediated B0->B0 perturbation are still required. Identity (FM) alone does not make the dormant row a contraction. The negative good-input activation margin likewise remains a separate requirement.
