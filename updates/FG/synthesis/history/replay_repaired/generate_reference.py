"""Regenerate reference grid; no experimental data or fitted molecular lifetimes."""
from pathlib import Path
import json
import numpy as np
from rotor_exact import build_model, signal, theta_from_fluence


def pair(z):
    return [float(np.real(z)), float(np.imag(z))]


def main():
    out = []
    for fluence in (0.0275, 0.11):
        for centre in (3703.3, 3783.0):
            model, p = build_model(jmax=70, steps=200, center=centre,
                                   theta=theta_from_fluence(fluence*1e4))
            for t3 in (.8, 1., 1.5, 2., 3.):
                S, X = signal(model, T=1., t1=1., t3=t3)
                out.append(dict(center_cm=centre, fluence_each_J_cm2=fluence,
                                p_single_reference=p, t1_ps=1., T_ps=1., t3_ps=t3,
                                S=pair(S), XL=pair(X[0]), XR=pair(X[1])))
    path=Path('rotor_reference_results.json')
    path.write_text(json.dumps(out, indent=2))
    print(f'Wrote {len(out)} calculated cases to {path}; these are not laboratory measurements.')

if __name__ == '__main__':
    main()
