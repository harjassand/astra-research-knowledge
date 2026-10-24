"""Root review checks; supplied finite models, no physical validation.

The bath comparison uses two different numerical constructions at identical
parameters. Clock matrix fixtures check ordered moments alongside the proof.
"""
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def bath_check():
    bath = BASE / "method_comparisons/bath_20261024"
    warm = module("warm_replay", bath / "warm/replay_multiport.py")
    compact = module("compact_replay", bath / "compact/native_multiport_check.py")
    gamma, kappa, variance = .08, .01, 10.5
    gammas = gamma * np.array([.6, .4])
    grid = np.linspace(0, 2*math.pi, 4097)
    pulse = warm.pulse(grid, gamma, kappa)
    kernel = warm.residual_kernel(pulse["rd"], pulse["re"], gammas,
                                  np.sqrt(gammas/gamma))
    continuum = warm.actual_output_G(grid, kernel, gamma, kappa,
                                    gammas, np.full(2, variance-.5), variance)
    cases = []
    for bins in (80, 160, 320):
        model = compact.make_dilation(bins, gamma, kappa)
        discrete = compact.evaluate(model, 1., 1., variance, variance,
                                    variance, "bright_cancel")
        error = np.max(np.abs(np.array(discrete["residual_phase_covariance"])-continuum))
        phase_error = abs(discrete["theta"]-pulse["logical"])
        cases.append({"bins": bins, "max_G_error": float(error),
                      "phase_error": float(phase_error),
                      "remaining_displacement": model["closure_error"]})
    assert cases[-1]["max_G_error"] < cases[0]["max_G_error"]/10
    assert cases[-1]["phase_error"] < cases[0]["phase_error"]/10
    assert cases[-1]["max_G_error"] < 1e-7
    return {"same_parameters": {"gamma": gamma, "kappa": kappa,
                                "all_initial_variances": variance},
            "continuum_G": continuum.tolist(), "continuum_theta": pulse["logical"],
            "collision_comparison": cases}


def swap(qubits, first, second):
    matrix = np.zeros((2**qubits, 2**qubits))
    for column in range(2**qubits):
        bits = [(column >> j) & 1 for j in range(qubits)]
        bits[first], bits[second] = bits[second], bits[first]
        row = sum(bit << j for j, bit in enumerate(bits))
        matrix[row, column] = 1
    return matrix


def clock_check():
    X = np.array([[0.,1,0],[1,0,0],[0,0,0]])
    C = np.array([[0.,0,1],[0,0,1],[1,1,0]])
    I3, ID = np.eye(3), np.eye(8)
    F1, F2 = swap(3,0,1), swap(3,1,2)
    g1, g2, lam = .37, -.82, .25
    H = (g1*(np.kron(np.kron(C,I3),ID)+np.kron(np.kron(X+lam*I3,I3),F1))
         +g2*(np.kron(np.kron(I3,C),ID)+np.kron(np.kron(I3,X+lam*I3),F2)))
    errors = []
    for r2 in (.4,.65,.9):
        angle = .5*math.asin(.25/r2)
        phi = np.array([math.sqrt(r2)*math.cos(angle),
                        -math.sqrt(r2)*math.sin(angle), 1j*math.sqrt(1-r2)])
        phi2 = phi.conj()
        assert abs(np.vdot(phi, X@phi)+.25) < 1e-14
        assert abs(np.vdot(phi, C@phi)) < 1e-14
        isometry = np.kron(np.kron(phi,phi2)[:,None],ID)
        M1 = isometry.conj().T@H@isometry
        M3 = isometry.conj().T@H@H@H@isometry
        predicted = (81/32)*(g1**3*F1+g2**3*F2)
        errors.append(float(np.max(np.abs(M3-predicted))))
        assert np.max(np.abs(M1)) < 1e-14
    assert max(errors) < 2e-14
    local_errors=[]
    for sign in (-1,1):
        local = C+sign*(X+lam*I3)
        eig, vec = np.linalg.eigh(local)
        U = (vec*np.exp(-1j*(2*math.pi/3)*eig))@vec.conj().T
        local_errors.append(float(np.max(np.abs(U-1j*sign*I3))))
    assert max(local_errors) < 1e-14
    return {"overlapping_event_K3_errors": errors,
            "isolated_revival_errors": local_errors,
            "scope": "Finite matrix checks support the written private-product-clock proof only."}


if __name__ == "__main__":
    result={"bath":bath_check(),"clock":clock_check()}
    target=BASE/"root_mathematical_replay.json"
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
