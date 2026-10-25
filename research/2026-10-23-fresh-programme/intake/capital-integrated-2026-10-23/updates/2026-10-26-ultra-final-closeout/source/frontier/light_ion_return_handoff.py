#!/usr/bin/env python3
"""Whole-operation handoff boundary, not merely on-light threshold crossings."""
import json
import numpy as np
import finite_ion_model as f
import light_ion_return_model as m


def main():
    bath=f.ClosedBath();inj=bath.integrate(bath.initial(),600.,pump=0.)
    initial=inj.y[:,-1]
    doc=dict(status='conditional finite-bath Na-photopump withdrawal discrimination',cases=[])
    specs=[(100.,0.,300.),(100.,0.,600.),(110.,0.,600.),(120.,0.,600.),
      (130.,0.,600.),(150.,0.,200.),(150.,0.,300.),
      (250.,1.,300.),(275.,1.,300.),(300.,1.,300.),(350.,1.,120.)]
    for current,nat,seconds in specs:
        tag=f'handoff_{int(current)}pa_{int(100*nat)}nat_{int(seconds)}s'
        row=m.run_case(initial,current,light_s=seconds,nat=nat,tag=tag)
        doc['cases'].append(row)
        (m.OUT/'light_ion_handoff_results.json').write_text(json.dumps(doc,indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
