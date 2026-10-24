#!/usr/bin/env python3
"""Independent finite-interface checks, using NumPy + the owned model files.

The exact mathematical model and the unacquired geometry/loss interface are
kept separate in FINITE_INTERFACE_CONSTRUCTION.md. No experimental data are
generated here. Results are numerical diagnostics unless explicitly bounded.
"""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, BASE / relative)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main():
    tem = module("tem_owned", "tem_twoport.py")
    rod = module("rod_bounded", "trunc_connectors/rod_transfer.py")
    w = np.linspace(0., 15., 200001)
    g = tem.bose(w)
    R, Z, capacitance, delay = 50., 5., 3.8e-12, 95e-12
    wu = 2*1.380649e-23*.1/1.054571817e-34
    physical_w = wu*w
    half = tem.line(physical_w, R, delay/2)
    yy = tem.open_stub_admittance(physical_w, Z, capacitance)
    aa, bb, cc, dd = tem.multiply(tem.multiply(half, tem.shunt(w, yy)), half)
    tt_abcd = 4/np.abs(aa+bb/R+cc*R+dd)**2
    tt_scalar = 1/(1+(R*np.tan(physical_w*Z*capacitance)/(2*Z))**2)
    rr = np.abs((aa+bb/R-cc*R-dd)/(aa+bb/R+cc*R+dd))**2
    assert np.max(np.abs(tt_abcd-tt_scalar)) < 1e-12
    assert np.max(np.abs(tt_abcd+rr-1)) < 1e-12
    a = R*capacitance*wu/2
    U = math.pi/(2*wu*Z*capacitance)
    tail = math.exp(-2*U)*(2*U**2+2*U+1)/(1-math.exp(-2*U))**2
    bound = math.pi/(2*a)+tail
    rounded = dict(T_kelvin=.1, port_R_ohm=R, main_delay_s=delay,
                   stub_Z_ohm=Z, stub_C_F=capacitance,
                   total_C_F=delay/R+capacitance,
                   total_L_H=R*delay+Z**2*capacitance,
                   a=a, first_stub_pole_u=U,
                   tail_after_first_pole_upper=tail, J_analytic_upper=bound,
                   J_numerical=float(tem.simpson(g*tt_abcd,15/(len(w)-1))),
                   abcd_vs_scalar_max_error=float(np.max(abs(tt_abcd-tt_scalar))),
                   passivity_max_error=float(np.max(abs(tt_abcd+rr-1))))

    # A sourced *bulk-constant model scale*, not an acquired 30-nm SiN device.
    E, rho = 280e9, 3140.
    area, length, omega_u = (30e-9)**2, 300e-9, 2*math.pi*1e9
    cl = math.sqrt(E/rho)
    r, mu, side = rod.parameters(length, cl)
    stiffness = E*area/length
    mb = stiffness/(rod.KAPPA*omega_u**2)
    sin_model = dict(E_Pa=E, rho_kg_m3=rho, area_m2=area, a_m=length,
                     c_L_m_s=cl, omega_u_rad_s=omega_u,
                     T_at_theta_half_K=1.054571817e-34*omega_u/(2*1.380649e-23),
                     K_N_m=stiffness, m_backbone_kg=mb,
                     m_rod_kg=rho*area*length,
                     m_side_kg=side*mb, total_cell_mass_kg=rod.MASS*mb,
                     rod_to_backbone_mass_ratio=mu,
                     r=r,
                     scope="Only distributed intercell rod is exact here; side spring/point bodies, bulk-constant extrapolation and axial-only motion remain declared model premises.")
    for mode in ("resonator", "rigid"):
        sin_model[mode] = {}
        for panels in (80000, 320000):
            sin_model[mode][str(panels)] = rod.finite_landauer(mode,r,mu,cells=10,panels=panels)
    result = dict(rounded_one_stub=rounded, SiN_bulk_constant_scale_only=sin_model,
                  scope="Declared passive linear transport models; no fabrication, contact acquisition, cryogenic loss calibration or full phonon-device result.")
    dest=BASE/"interface_checks.json"
    dest.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
