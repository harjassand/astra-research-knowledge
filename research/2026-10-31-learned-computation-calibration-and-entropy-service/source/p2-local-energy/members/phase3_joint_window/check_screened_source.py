"""Electrostatic summability witness for a two-dimensional charge source.

All numbers are dimensionless.  A source occupation is 0 or 1.  The data
transition density is constructed from orthonormalized Gaussian orbitals.
The table contrasts an image-screened plane with unscreened Coulomb fields.
It is not a material/device calculation.
"""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.hermite import hermgauss

def calculate(radius, screen=True, spacing=2., a=.8, sigma=.4,
              data_z=1., source_z=2., coulomb=1.):
    indices=np.arange(-radius,radius+1)
    xx,yy=np.meshgrid(indices*spacing,indices*spacing,indexing='ij')
    x=xx.ravel()
    y=yy.ravel()
    nodes,weights=hermgauss(64)
    weights=weights/np.sqrt(np.pi)
    def expectation(center):
        points=center+sigma*nodes
        rsq=(points[None,:]-x[:,None])**2+y[:,None]**2
        potential=1/np.sqrt(rsq+(source_z-data_z)**2)
        if screen:
            potential-=1/np.sqrt(rsq+(source_z+data_z)**2)
        return coulomb*(potential@weights)
    el,er,ec=expectation(-a),expectation(a),expectation(0.)
    s=np.exp(-a*a/sigma**2)
    gain_coeff=s*(ec-(el+er)/2)/(1-s*s)
    conditional_coeff=(er-el)/np.sqrt(1-s*s)
    radii=np.sqrt(x*x+y*y)
    mask=radii>0
    interaction=1/radii[mask]
    if screen:
        interaction-=1/np.sqrt(radii[mask]**2+4*source_z**2)
    return {'radius_sites':radius,'number_sites':len(x),
            'sum_absolute_gain_coefficients':float(np.abs(gain_coeff).sum()),
            'sum_absolute_conditional_shift_coefficients':float(np.abs(conditional_coeff).sum()),
            'central_site_coulomb_interaction_sum':float(coulomb*interaction.sum()),
            'screening':screen}

if __name__=='__main__':
    rows=[]
    for radius in [4,8,16,32,64]:
        rows.append(calculate(radius,True))
        rows.append(calculate(radius,False))
    Path(__file__).with_name('screened_source_results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
