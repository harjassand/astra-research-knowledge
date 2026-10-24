#!/usr/bin/env python3
"""Finite passive TEM two-port competing realization of the scalar spectrum.

Every inductor is replaced by an exact lossless transmission-line section;
every capacitor is an exact open transmission-line stub. Integrated line C
is included in the common capacitance budget. This is a declared 1D circuit
field model, not a fabricated microwave or phonon-device result.
"""
import json
import math
from pathlib import Path

import numpy as np

CROOT = 4.259874009292292
K = (CROOT*CROOT-3)/4
MT = 4-12/(CROOT*CROOT)
MS = MT-1
KS = 4*MS/MT
R = 1/math.sqrt(K*MT)


def multiply(a, b):
    aa, ab, ac, ad = a
    ba, bb, bc, bd = b
    return (aa*ba+ab*bc, aa*bb+ab*bd, ac*ba+ad*bc, ac*bb+ad*bd)


def identity(w):
    zz = np.zeros_like(w, dtype=complex)
    oo = np.ones_like(w, dtype=complex)
    return oo, zz, zz, oo


def line(w, z, delay):
    phase = w*delay
    cc = np.cos(phase)
    ss = 1j*np.sin(phase)
    return cc, z*ss, ss/z, cc


def shunt(w, yy):
    oo = np.ones_like(w, dtype=complex)
    zz = np.zeros_like(w, dtype=complex)
    return oo, zz, yy, oo


def open_stub_admittance(w, z, capacitance):
    # For an open stub, total static C=delay/Z; its full internal modes remain.
    return 1j*np.tan(w*z*capacitance)/z


def branch_admittance(w, z_series, inductance, z_cap, capacitance):
    aa, bb, cc, dd = line(w, z_series, inductance/z_series)
    load = open_stub_admittance(w, z_cap, capacitance)
    return (cc+dd*load)/(aa+bb*load)


def transmission(abcd):
    aa, bb, cc, dd = abcd
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        tt = 4/np.abs(aa+bb/R+cc*R+dd)**2
    return np.nan_to_num(tt, nan=0., posinf=0., neginf=0.)


def model(w, ncells, z_inductor_ratio=3., z_cap_ratio=.1, kind="side"):
    zl, zc = z_inductor_ratio*R, z_cap_ratio*R
    lb, ls = 1/K, 1/KS
    c_line_b, c_line_s = lb/zl**2, ls/zl**2
    cb, cs = 1-c_line_b, MS-c_line_s
    assert cb > 0 and cs > 0
    # One period is main-line half / node shunt / main-line half.
    half = line(w, zl, lb/(2*zl))
    if kind == "side":
        yy = open_stub_admittance(w, zc, cb)
        yy += branch_admittance(w, zl, ls, zc, cs)
        cell = multiply(multiply(half, shunt(w, yy)), half)
        whole = identity(w)
        for _ in range(ncells):
            whole = multiply(whole, cell)
        integrated_cap = cb+cs+c_line_b+c_line_s
        resource = dict(C_backbone_stub=cb, C_side_stub=cs,
                        C_main_connector=c_line_b, C_side_connector=c_line_s,
                        L_main=lb, L_side=ls)
    elif kind == "rigid":
        cy = MT-c_line_b
        yy = open_stub_admittance(w, zc, cy)
        cell = multiply(multiply(half, shunt(w, yy)), half)
        whole = identity(w)
        for _ in range(ncells):
            whole = multiply(whole, cell)
        integrated_cap = cy+c_line_b
        resource = dict(C_node_stub=cy, C_main_connector=c_line_b, L_main=lb)
    elif kind == "concentrated":
        # Conventional global-budget competitor: same N main-line sections,
        # same N capacitor stubs, all stubs at the centre. Not same per-cell
        # mass distribution; footprint/placement is explicitly different.
        long_half = line(w, zl, ncells*lb/(2*zl))
        cy = MT-c_line_b
        yy = ncells*open_stub_admittance(w, zc, cy)
        whole = multiply(multiply(long_half, shunt(w, yy)), long_half)
        integrated_cap = cy+c_line_b
        resource = dict(C_each_central_stub=cy, central_stubs=ncells,
                        C_main_connector_each=c_line_b, L_main_each=lb)
    else:
        raise ValueError(kind)
    assert abs(integrated_cap-MT) < 1e-12
    tt = transmission(whole)
    assert np.max(tt) < 1+1e-8
    assert abs(tt[0]-1) < 1e-12
    return tt, resource


def bose(w):
    out = np.ones_like(w)
    mask = w > 0
    out[mask] = (2*w[mask]*np.exp(-w[mask])/(-np.expm1(-2*w[mask])))**2
    return out


def simpson(y, h):
    return h/3*(y[0]+y[-1]+4*np.sum(y[1:-1:2])+2*np.sum(y[2:-1:2]))


def integrate(ncells, ratios=(3., .1), ngrid=320001, cutoff=15.):
    ww = np.linspace(0, cutoff, ngrid)
    gg = bose(ww)
    out = {}
    for kind in ("side", "rigid", "concentrated"):
        tt, resources = model(ww, ncells, *ratios, kind=kind)
        jj = float(simpson(gg*tt, cutoff/(ngrid-1)))
        out[kind] = dict(J=jj, resource_per_cell_or_equivalent=resources,
                         T_at_lowest_positive_frequency=float(tt[1]))
    return out


def physical_units(temperature=.1, resistance=50., z_inductor=150., z_cap=5.):
    kb, hb = 1.380649e-23, 1.054571817e-34
    wu = 2*kb*temperature/hb
    c0 = R/(resistance*wu)
    zunit = 1/(wu*c0)
    zl, zc = z_inductor/zunit, z_cap/zunit
    lb, ls = 1/K, 1/KS
    return dict(T_kelvin=temperature, f_unit_Hz=wu/(2*math.pi),
                resistor_ohm=resistance, C_unit_F=c0,
                L_main_H=lb/(wu*wu*c0), L_side_H=ls/(wu*wu*c0),
                C_total_each_period_F=MT*c0,
                Z_inductor_ohm=z_inductor, Z_capacitor_stub_ohm=z_cap,
                main_line_delay_s=lb/(zl*wu), side_line_delay_s=ls/(zl*wu),
                main_line_C_F=lb/zl**2*c0,
                side_line_C_F=ls/zl**2*c0,
                C_backbone_stub_F=(1-lb/zl**2)*c0,
                C_side_stub_F=(MS-ls/zl**2)*c0,
                conductance_prefactor_W_per_K=kb*wu/(2*math.pi))


def main():
    results = {"declared_model": "lossless finite single-TEM transmission-line graph with real resistor ports",
               "physical_example": physical_units(), "cells": {}}
    for nn in (1, 2, 4, 8, 16):
        results["cells"][str(nn)] = integrate(nn)
    results["convergence_N8"] = {str(n):integrate(8, ngrid=n) for n in (80001, 160001, 640001)}
    cutoff=15.
    results["one_TEM_channel_tail_bound_after_15"] = math.exp(-2*cutoff)*(2*cutoff**2+2*cutoff+1)/(1-math.exp(-2*cutoff))**2
    results["scope"] = "TL connector/stub fields are counted exactly. Material dispersion, loss, junction stray modes, additional ports and fabrication are separate inputs; not a phonon-device result or a superiority claim."
    dest = Path(__file__).with_name("tem_twoport.json")
    dest.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
