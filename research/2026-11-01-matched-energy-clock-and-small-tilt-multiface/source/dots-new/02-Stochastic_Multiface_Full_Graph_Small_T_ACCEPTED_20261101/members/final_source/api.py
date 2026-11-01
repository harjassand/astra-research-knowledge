"""Separate status/budget adapter around frozen pending author constructor.
Qualitative architecture recognition does not enumerate independent sets.
"""
import multiface as M

def qualitative(raw):
 r=M.recognize(raw)
 return dict(status='RAW_ARCHITECTURE_MATCHED_THEOREM_PENDING_INDEPENDENT_WHOLE_REVIEW',raw_sha256=r['raw_sha256'],normalized_reaction_sha256=r['normalized_reaction_sha256'],input_list_sha256=M.input_list_sha256(raw),family='reversible-square-free-binary-one-port-hub-with-every-satellite-arm',candidate_conclusion='nonexplosion, irreducible positive recurrence, and existence of one acquired nonzero exponential total-count moment',not_claimed=['every finite exponential moment','arbitrary weak reversibility','independent acceptance'],independent_sets_enumerated=0)

def construct(raw,max_masks=1000000):
 if type(max_masks)is not int or max_masks<0:raise ValueError('exact nonnegative integer mask budget')
 q=qualitative(raw)
 try:c=M.construct(raw,max_masks=max_masks)
 except M.BudgetRefusal as exc:return dict(status='QUANTITATIVE_MASK_BUDGET_REFUSAL',qualitative=q,reason=str(exc),stability_refuted=False)
 return dict(status=c['status'],qualitative=q,certificate=c)

def pointwise_profile(p,j,max_exponent=100000,max_power_bits=1000000):
 if type(j)is not int or j<0:raise ValueError('exact nonnegative resource')
 if type(max_exponent)is not int or max_exponent<0 or type(max_power_bits)is not int or max_power_bits<0:raise ValueError('exact nonnegative computation budgets')
 exponent=j+p['s0'];base_bits=max(p['q'].numerator.bit_length(),p['q'].denominator.bit_length())
 if exponent*base_bits>max_power_bits:raise M.BudgetRefusal('profile rational-power intermediate bit bound '+M.integer_text(exponent*base_bits))
 return M.profile(p,j,max_power=max_exponent)
