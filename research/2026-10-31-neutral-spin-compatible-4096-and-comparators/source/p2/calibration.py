"""Ordinary finite-dimensional charge-Rabi calibration, for illustration.

Every input is a prepared local double occupancy, not a clean mediator
spin. Synthetic exact data test identifiability at one working point.
This is NOT a device experiment, certified box inversion, or shot bound.
The coarse scalar box and model bias must be independently qualified.
"""
import math
import numpy as np
from scipy.linalg import expm
from scipy.optimize import least_squares


def probabilities(parameters,times):
    U,g,eps=parameters
    h=np.array([[0.,-math.sqrt(2)*g,-math.sqrt(2)*g],
                [-math.sqrt(2)*g,U+eps,0.],
                [-math.sqrt(2)*g,0.,U-eps]],complex)
    out=[]
    for t in times:
        u=expm(-1j*t*h)
        # Probability of separated charge (1,1) from D_L or D_R.
        out.extend([abs(u[0,1])**2,abs(u[0,2])**2])
    return np.array(out)


def check_calibration():
    times=np.array([.3,.7,1.1,1.6,2.2])
    actual=np.array([1.07,.41,.12])
    data=probabilities(actual,times)
    fit=least_squares(lambda x:probabilities(x,times)-data,
                      [.9,.35,.05],bounds=([.5,.1,-.3],[1.5,.7,.3]),
                      ftol=1e-13,xtol=1e-13,gtol=1e-13)
    U,g=1.07,.41
    omega=math.sqrt(U*U/4+4*g*g)
    exact=2*g*g/omega**2*np.sin(omega*times)**2
    resonant=probabilities([U,g,0.],times).reshape(-1,2)
    return dict(synthetic_parameters=actual.tolist(),
                fitted_parameters=fit.x.tolist(),
                fit_error=float(np.linalg.norm(fit.x-actual)),
                observation_jacobian_singular_values=
                    np.linalg.svd(fit.jac,compute_uv=False).tolist(),
                zero_detuning_Rabi_formula_error=
                    float(np.max(np.abs(resonant-exact[:,None]))),
                input_states=['D_L','D_R'],durations=times.tolist(),
                caveat='Synthetic noiseless check at one point; not a certified uncertainty box or acquired physical qualification.')
