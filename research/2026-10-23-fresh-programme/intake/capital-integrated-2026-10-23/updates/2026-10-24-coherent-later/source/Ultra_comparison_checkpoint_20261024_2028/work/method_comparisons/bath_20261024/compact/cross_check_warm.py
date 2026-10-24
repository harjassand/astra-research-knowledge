#!/usr/bin/env python3
"""Post-release independent finite-collision check of the warm fixture.

Uses the compact arm's frozen exact mechanical flow, but no warm executable
code.  The warm JSON is read only as a comparison target.  The augmented
covariance [mechanics, two integrated output phases] has dimension six.
"""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("owned_compact", HERE / "native_multiport_check.py")
owned = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owned)


def responses(t, gamma=1e-4, kappa=0.01):
    derivatives = []
    for order in range(5):
        val = np.full_like(t, 5 / 16 if order == 0 else 0.0)
        for k, a in [(1, -15/32), (2, 3/16), (3, -1/32)]:
            val += a * k**order * np.cos(k*t + order*math.pi/2)
        derivatives.append(val)
    u, up, upp, u3, u4 = derivatives
    z = 1 + gamma*gamma/4
    d, dp, dpp = upp+gamma*up+z*u, u3+gamma*upp+z*up, u4+gamma*u3+z*upp
    rd = np.stack([d, dp+gamma*d/2], axis=1)
    re = -kappa*np.stack([u, up+gamma*u/2], axis=1)
    rdp = np.stack([dp, dpp+gamma*dp/2], axis=1)
    return rd, re, rdp


def kernel_at(t, native_rates, h, relative_gain):
    rd, re, _ = responses(np.array([t]))
    rd, re = rd[0], re[0]
    native = np.sqrt(native_rates)
    own = native-relative_gain*np.dot(h, native)*h
    displacements = np.zeros((8, 2))
    for port in range(2):
        displacements[2*port:2*port+2, 0] = own[port]*rd
        displacements[2*port:2*port+2, 1] = native[port]*re
        displacements[4+2*port:6+2*port, 0] = native[port]*re
        displacements[4+2*port:6+2*port, 1] = own[port]*rd
    k = np.empty_like(displacements)
    k[0::2] = displacements[1::2]
    k[1::2] = -displacements[0::2]
    return k


def collision_G(bins, h, gain=1.0, input_n=(1000,500), mechanics_v=1000.5):
    duration, gamma, kappa = 2*math.pi, 1e-4, 0.01
    dt = duration/bins
    native_rates = gamma*np.array([0.6,0.4])
    mode = np.zeros((4,8))
    for port in range(2):
        mode[:2,2*port:2*port+2] = math.sqrt(native_rates[port]/gamma)*np.eye(2)
        mode[2:,4+2*port:6+2*port] = math.sqrt(native_rates[port]/gamma)*np.eye(2)
    flow = owned.mechanical_flow(dt/2,kappa)
    tau_root = math.exp(-gamma*dt/2)
    reflect = math.sqrt(-math.expm1(-gamma*dt))
    bath_out = np.eye(8)-(1-tau_root)*mode.T@mode
    vv = np.repeat(np.tile(np.array(input_n)+0.5,2),2)
    covariance = np.zeros((6,6))
    covariance[:4,:4] = mechanics_v*np.eye(4)
    for index in range(bins):
        k = kernel_at((index+0.5)*dt,native_rates,h,gain)
        aa = np.eye(6)
        aa[:4,:4] = tau_root*flow@flow
        aa[4:,:4] = -math.sqrt(dt)*reflect*k.T@mode.T@flow
        bb = np.zeros((6,8))
        bb[:4] = reflect*flow@mode
        bb[4:] = math.sqrt(dt)*k.T@bath_out
        covariance = aa@covariance@aa.T+(bb*vv)@bb.T
    return covariance[4:,4:]


def main():
    warm = json.loads((HERE.parent/"warm"/"REPLAY_RESULTS.json").read_text())["fine"]
    gamma, kappa = 1e-4,0.01
    continuum = owned.continuum_values(gamma,kappa)
    amp2 = (math.pi/4)/abs(continuum["phase_ideal"])
    tgrid = (np.arange(4096)+0.5)*(2*math.pi/4096)
    rd, _, rdp = responses(tgrid)
    ratio = float(np.sum(rdp*rdp)/np.sum(rd*rd))
    eta = (1/3)/(1+ratio/25)*0.9
    w = (1-eta)/(2*eta)
    a = continuum["own_norm2"]
    bright = np.sqrt(np.array([0.6,0.4]))
    results = []
    for bins in [256,512,1024]:
        full = (collision_G(bins,bright)+w*a*np.eye(2))*amp2
        port1 = collision_G(bins,np.array([1.0,0.0]))*amp2
        cold_hot = collision_G(bins,bright,gain=0,input_n=(0,0))*amp2
        full_target = np.array(warm["full_native_hybrid_filtered_homodyne"]["G"])
        partial_target = np.array(warm["perfect_port1_only_port2_absent"]["G"])
        results.append({
            "bins":bins,
            "full_G_max_error_vs_warm_continuum":float(np.max(np.abs(full-full_target))),
            "port1_G_max_error_vs_warm_continuum":float(np.max(np.abs(port1-partial_target))),
            "full":owned.spin_channel_metrics(-math.pi/4,full),
            "cold_inputs_hot_initial_mechanics":{
                "G":cold_hot.tolist(),
                **owned.spin_channel_metrics(continuum["raw_phase"]*amp2,cold_hot),
            },
        })
    # Optimize the SAME port-1-only scalar gain (not arbitrary optimal POVM).
    h = np.array([1.0,0.0])
    g0,g1,g2 = [collision_G(1024,h,gain=z) for z in [0,1,2]]
    quad = (g2-2*g1+g0)/2
    linear = g1-g0-quad
    optimum = float(-linear[0,0]/(2*quad[0,0]))
    gopt = collision_G(1024,h,gain=optimum)*amp2
    theta_opt = (continuum["raw_phase"]+0.6*optimum*continuum["feedback_phase"])*amp2
    result = {
        "not_hardware":True,
        "independent_construction":"6x6 augmented forward covariance; exact bright/native beam-splitter collision and exact mechanical half-step; midpoint target-output kernel",
        "eta_from_independent_temporal_norms":eta,
        "eta_warm":warm["eta_total"],
        "same_actual_phase_target_amplitude_squared":amp2,
        "convergence":results,
        "port1_scalar_gain_optimum":{
            "gain":optimum,"G":gopt.tolist(),**owned.spin_channel_metrics(theta_opt,gopt)
        },
    }
    output = HERE/"CROSS_INDEPENDENT_COLLISION.json"
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
