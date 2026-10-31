"""An exact rational mixture correction with genuinely active spectral clipping."""
from fractions import Fraction as F
from pathlib import Path
import json


def run():
    # M(c)=I+c(e1 e2^T+e2 e1^T). Its eigenvalues are1-c,1+c,1.
    theta=[F(1,4),F(3,4)]
    true=[F(2,5),F(2,5)]
    models=[F(0),F(0)]
    mu,L=F(3,5),F(7,5)
    noise,omega=F(1,20),F(1,20)
    observed=sum(t*c for t,c in zip(theta,true))+noise
    a=observed
    h=a*(a-omega)
    # G_j has equal off-diagonal entries theta_j*a/2.
    gradients=[t*a/2 for t in theta]
    gradient_norm_squared=2*sum(g*g for g in gradients)
    increments=[h*g/gradient_norm_squared for g in gradients]
    updated=[b+d for b,d in zip(models,increments)]
    clipped=[max(mu-1,min(L-1,c)) for c in updated]
    potential=lambda xs:2*sum((x-c)**2 for x,c in zip(xs,true))
    before,after,after_clip=map(potential,[models,updated,clipped])
    update_norm_squared=2*sum(d*d for d in increments)
    mixture_s=sum(t*t for t in theta)
    guaranteed=(a-omega)**2/mixture_s
    inner=2*sum(g*(c-b) for g,c,b in zip(gradients,true,models))
    assert inner==h
    assert before-after==update_norm_squared
    assert update_norm_squared==h*h/gradient_norm_squared
    assert update_norm_squared>=guaranteed
    assert after_clip<=after
    assert clipped!=updated
    assert all(mu<=1-abs(c) and 1+abs(c)<=L for c in clipped)
    return {'status':'exact_halfspace_projection_passed','ambient_dimension':3,
        'source_count':2,'weights':[str(x) for x in theta],
        'observed_residual_norm':str(a),'chosen_noise_and_mismatch_budget':str(omega),
        'compatible_comparator_offdiagonal':[str(x) for x in true],
        'updated_offdiagonal':[str(x) for x in updated],
        'clipped_offdiagonal':[str(x) for x in clipped],
        'halfspace_is_tight':True,'spectral_clipping_is_active':True,
        'potential_before':str(before),'potential_after_update':str(after),
        'potential_after_clipping':str(after_clip),
        'exact_projection_drop':str(update_norm_squared),
        'guaranteed_margin_drop':str(guaranteed)}


if __name__=='__main__':
    result=run()
    Path(__file__).with_name('halfspace_exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
