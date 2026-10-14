"""Exact formula for one-step minimax multiplicative interval width.
The endpoint theorem proves no interior rate value can give a larger final
upper/lower ratio. Floating evaluations select queries; final bounds are checked
separately using exact rational residuals.
"""
import numpy as np

def worst_relative(fmax,fmin,vl,vh,rl,rh,width):
    drop_upper=width*vl**2/(1+width*rl)
    raise_lower=width*vh**2/np.maximum(1-width*rh,1e-300)
    if_high=(fmax-drop_upper)/fmin
    if_low=fmax/(fmin+raise_lower)
    return np.maximum(if_low,if_high),np.where(if_high>if_low,1.,0.)
