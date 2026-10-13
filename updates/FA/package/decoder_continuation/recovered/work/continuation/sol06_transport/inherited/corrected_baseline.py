#!/usr/bin/env python3
"""Replay the digitised unactuated-baseline and calibration sensitivity."""
from dataclasses import replace
from pathlib import Path
import json

import numpy as np

from nonlinear_transport import Parameters,unactuated_rate,unactuated_matched


def main():
    p=Parameters()
    anchor_scale=.2/float(unactuated_rate(100.,p))
    sensitivity=[]
    for scale in (1.,.9,anchor_scale,.8,.7,1.1):
        pp=replace(p,rate_scale=scale)
        rows=[]
        for factor in (.5,1.,1.25,1.5,2.,3.,5.):
            gradient,power=unactuated_matched(.003125*factor,pp)
            rows.append({'throughput_factor':factor,'G':gradient,
                'wall_gamma':float(unactuated_rate(gradient*pp.radius/2,pp)),
                'electric':power})
        sensitivity.append({'rate_scale':scale,'rows':rows})
    result={'status':'figure-digitised unactuated control; source is a separate rheometer/sample run',
      'rate_scale_to_match_100Pa_0.2_per_s':anchor_scale,
      'raw_control_and_calibration_sensitivity':sensitivity}
    Path(__file__).with_name('corrected_baseline.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
