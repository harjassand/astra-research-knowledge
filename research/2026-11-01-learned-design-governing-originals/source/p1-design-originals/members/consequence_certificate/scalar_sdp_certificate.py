"""Binary scalar-energy realization of a noisy spectral optimality certificate.

The source simulator aggregates independent Gaussian shot noise exactly in law;
raw shot counts and full-configuration writes are still charged. The numerical
implementation uses ordinary floating point and PRNGs, not interval arithmetic.
Only EnergySource sees the hidden coefficients before post-run validation.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
import math
import time
from pathlib import Path

import numpy as np


class EnergySource:
    def __init__(self, H, b, sigma, seed=0, constant=0.0):
        self.__H = np.asarray(H, dtype=float)
        self.__b = np.asarray(b, dtype=float)
        self.__constant = float(constant)
        self.sigma = float(sigma)
        self.n = len(b)
        self.rng = np.random.default_rng(seed)
        self.shots = 0
        self.averaged_settings = 0
        self.control_writes = 0

    def means(self, states, repetitions=1):
        states = np.asarray(states, dtype=float)
        if states.ndim == 1:
            states = states[None, :]
        if states.shape[1] != self.n or not np.all(np.abs(states) == 1):
            raise ValueError("The physical source accepts only binary states.")
        repetitions = int(repetitions)
        if repetitions < 1:
            raise ValueError("At least one source shot must be paid.")
        count = len(states)
        self.shots += count * repetitions
        self.averaged_settings += count
        self.control_writes += self.n * count * repetitions
        value = (
            self.__constant
            + states @ self.__b
            + np.einsum("ij,jk,ik->i", states, self.__H, states, optimize=True)
        )
        # This is distributionally exactly the average of repetitions Gaussian
        # source errors, but does not claim physically executing those shots.
        return value + self.rng.normal(
            0.0, self.sigma / math.sqrt(repetitions), size=count
        )


class ResidualSource:
    """An actual source minus a digitally evaluable tractable surrogate."""
    def __init__(self, source, surrogate_evaluate):
        self.source = source
        self.surrogate_evaluate = surrogate_evaluate
        self.n = source.n
        self.sigma = source.sigma

    @property
    def shots(self):
        return self.source.shots

    @property
    def averaged_settings(self):
        return self.source.averaged_settings

    @property
    def control_writes(self):
        return self.source.control_writes

    def means(self, states, repetitions=1):
        states=np.asarray(states)
        return self.source.means(states,repetitions)-self.surrogate_evaluate(states)


class ModuleSliceSource:
    """Orient active two-site modules while keeping every occupancy fixed.

    The physical source can contain arbitrary context-dependent nuisance.
    This adapter does not read, estimate, or remove that nuisance. Every
    physical query stays in the same occupancy context, so the differences
    in the certifier cancel it.
    """
    def __init__(self, physical_source, occupancy):
        self.source = physical_source
        self.occupancy = np.asarray(occupancy,dtype=int)
        if physical_source.n != 2*len(self.occupancy):
            raise ValueError("Each physical module must have two controls.")
        if not np.all((self.occupancy>=0)&(self.occupancy<=2)):
            raise ValueError("Occupancy is 0, 1, or 2.")
        self.active = np.flatnonzero(self.occupancy==1)
        self.n = len(self.active)
        self.sigma = physical_source.sigma

    @property
    def shots(self):
        return self.source.shots

    @property
    def averaged_settings(self):
        return self.source.averaged_settings

    @property
    def control_writes(self):
        return self.source.control_writes

    def encode(self, orientations):
        z=np.asarray(orientations,dtype=float)
        if z.ndim==1:
            z=z[None,:]
        if z.shape[1]!=self.n or not np.all(np.abs(z)==1):
            raise ValueError("One binary orientation is needed per active module.")
        k=len(self.occupancy)
        x=np.empty((len(z),2*k))
        active_index=0
        for a,B in enumerate(self.occupancy):
            if B==0:
                x[:,2*a:2*a+2]=-1
            elif B==2:
                x[:,2*a:2*a+2]=1
            else:
                x[:,2*a]=z[:,active_index]
                x[:,2*a+1]=-z[:,active_index]
                active_index+=1
        return x

    def means(self, orientations, repetitions=1):
        return self.source.means(self.encode(orientations),repetitions)


def diagonal_from_flips(source, z, h, multiplier, zeta, delta):
    n = source.n
    m = max(1, math.ceil(source.sigma**2 * math.log(2*n/delta) / (4*zeta*zeta)))
    states = np.repeat(np.asarray(z, float)[None, :], 2*n, axis=0)
    for i in range(n):
        states[2*i+1, i] *= -1
    observations = source.means(states, m).reshape(n, 2)
    d = (observations[:, 0] - observations[:, 1])/4
    d += np.asarray(z) * (np.asarray(h) + multiplier) / 2
    return d, m


def signed_digits(v, bits):
    alpha = float(np.max(np.abs(v)))
    if alpha == 0:
        return alpha, np.empty((0, len(v))), np.zeros_like(v)
    residual = np.asarray(v, float) / alpha
    digits = []
    for _ in range(bits):
        s = np.where(residual >= 0, 1.0, -1.0)
        digits.append(s)
        residual = 2*residual - s
    digits = np.asarray(digits)
    represented = alpha * (np.exp2(-np.arange(1, bits+1)) @ digits)
    return alpha, digits, represented


def binary_hessian_action(source, v, bits, a, coordinate_variance):
    """Compute Hv by actual binary scalar queries; no H entries are read."""
    n = source.n
    alpha, digits, represented = signed_digits(v, bits)
    if alpha == 0:
        return np.zeros(n), 0, represented
    repetitions = max(1, math.ceil(
        source.sigma**2 * alpha**2 / (16*a*a*coordinate_variance)
    ))
    states = np.empty((len(digits), n, 4, n))
    for l, s in enumerate(digits):
        for i in range(n):
            states[l, i, 0] = s
            states[l, i, 1] = s
            states[l, i, 2] = -s
            states[l, i, 3] = -s
            states[l, i, 0, i] = 1
            states[l, i, 1, i] = -1
            states[l, i, 2, i] = 1
            states[l, i, 3, i] = -1
    observations = source.means(states.reshape(-1, n), repetitions)
    observations = observations.reshape(len(digits), n, 4)
    sign_actions = (
        observations[:, :, 0] - observations[:, :, 1]
        - observations[:, :, 2] + observations[:, :, 3]
    ) / 8
    Hv = alpha * (np.exp2(-np.arange(1, bits+1)) @ sign_actions)
    return Hv, repetitions, represented


@dataclass
class TestParameters:
    n: int
    tau: float
    a: float
    delta: float
    entry_cap: float

    def calculate(self):
        if self.a < self.tau:
            raise ValueError("Use a>=tau.")
        kappa = self.tau/self.a
        R = max(1, math.ceil(math.log(1/self.delta)/math.log(4/3)))
        L = math.log(64*self.n*R/(self.delta*kappa))
        T = math.ceil(32*L/kappa)
        eta_det = kappa/32
        s2 = kappa/(256*math.log(64))
        A = (
            math.sqrt(2*(1+T*s2)*math.log(4*self.n*(T+1)*R/self.delta))
            + T*eta_det + 1
        )
        coarse_op_cap = self.n*self.entry_cap
        B = max(1, math.ceil(math.log2(
            max(2, 2*coarse_op_cap*math.sqrt(self.n)*A/(self.a*eta_det))
        )))
        return dict(kappa=kappa, repetitions=R, length=T, eta_det=eta_det,
                    coordinate_variance=s2, threshold=A, bits=B)


def psd_test(source, d_hat, zeta, parameters, seed=1):
    """ACCEPT implies H-diag(d_hat)+zeta I >= -tau I with stated error."""
    p = parameters.calculate()
    rng = np.random.default_rng(seed)
    n = source.n
    steps = 0
    max_amplitude = 0.0
    max_mean_repetitions = 0
    start_shots = source.shots
    for trial in range(p["repetitions"]):
        v = rng.choice([-1.0, 1.0], size=n)
        for t in range(p["length"] + 1):
            amplitude = float(np.max(np.abs(v)))
            max_amplitude = max(max_amplitude, amplitude)
            if amplitude > p["threshold"]:
                return dict(accepted=False, trial=trial, step=t, total_steps=steps,
                            source_shots=source.shots-start_shots,
                            max_amplitude=max_amplitude,
                            max_mean_repetitions=max_mean_repetitions,
                            parameters=p)
            if t == p["length"]:
                break
            Hv, repetitions, _ = binary_hessian_action(
                source, v, p["bits"], parameters.a, p["coordinate_variance"]
            )
            # S=H-diag(d_hat)+zeta I. Its known diagonal is evaluated here.
            v = v - (Hv - d_hat*v + zeta*v) / parameters.a
            max_mean_repetitions = max(max_mean_repetitions, repetitions)
            steps += 1
    return dict(accepted=True, total_steps=steps,
                source_shots=source.shots-start_shots,
                max_amplitude=max_amplitude,
                max_mean_repetitions=max_mean_repetitions,
                parameters=p)


def certify_candidate(source, z, h, cardinality, multiplier, epsilon,
                      delta, a, entry_cap, seed=1):
    if cardinality is None and multiplier != 0:
        raise ValueError("A multiplier requires a cardinality constraint.")
    if cardinality is not None and np.sum(np.asarray(z) > 0) != cardinality:
        raise ValueError("Candidate violates the exact cardinality constraint.")
    zeta = epsilon/16
    tau = epsilon/8
    d_hat, diagonal_repetitions = diagonal_from_flips(
        source, z, h, multiplier, zeta, delta/2
    )
    result = psd_test(
        source, d_hat, zeta,
        TestParameters(source.n, tau, a, delta/2, entry_cap), seed
    )
    result.update(
        target_regret=epsilon*source.n,
        diagonal_repetitions=diagonal_repetitions,
        total_source_shots=source.shots,
        averaged_settings=source.averaged_settings,
        control_writes=source.control_writes,
        d_hat=d_hat.tolist(),
        qualifier="floating-point Gaussian-shot simulation; theoretical constants used",
    )
    return result


def random_psd_kernel(n, z, seed):
    rng = np.random.default_rng(seed)
    P = np.eye(n) - np.outer(z, z)/n
    W = rng.normal(size=(n, n))
    L = P @ (W.T @ W/n) @ P
    L /= np.linalg.eigvalsh(L)[-1]
    return (L+L.T)/2


def run_checks(run_power=True):
    rng = np.random.default_rng(20261101)
    identity_max_error = 0.0
    for _ in range(500):
        n = int(rng.integers(2, 15))
        A = rng.normal(size=(n, n))
        H = (A+A.T)/2
        np.fill_diagonal(H, 0)
        g = rng.normal(size=n)
        x = rng.choice([-1., 1.], n)
        z = rng.choice([-1., 1.], n)
        Q = H-np.diag(z*(H@z+g/2))
        direct = x@H@x+g@x-z@H@z-g@z
        identity_max_error = max(identity_max_error,
                                 abs(direct-(x-z)@Q@(x-z)))
    action_checks = []
    for n in [4, 8, 16]:
        A = rng.normal(size=(n, n))
        H = (A+A.T)/2
        np.fill_diagonal(H, 0)
        b = rng.normal(size=n)
        source = EnergySource(H, b, sigma=0, constant=173.5)
        worst = 0.0
        for _ in range(20):
            v = rng.normal(size=n)
            Hv, _, represented = binary_hessian_action(source, v, 18, 1, .01)
            worst = max(worst, float(np.max(np.abs(Hv-H@represented))))
        action_checks.append(dict(n=n, exact_represented_action_error=worst,
                                  source_shots=source.shots,
                                  control_writes=source.control_writes))
    structural = []
    for n in [16, 64, 256]:
        z = np.r_[np.ones(n//2), -np.ones(n-n//2)]
        L = random_psd_kernel(n, z, seed=33+n)
        H = L-np.diag(np.diag(L))
        # On the balanced cardinality slice, the uniform b is an irrelevant
        # resource price. It is deliberately nonzero in the physical source.
        multiplier = .3
        b = -multiplier*np.ones(n)
        Q = H-np.diag(z*(H@z+(b+multiplier)/2))
        fourier_l2 = math.sqrt(4*np.sum(np.triu(H, 1)**2))
        K = n*(n+1)/2
        structural.append(dict(
            n=n, rank=int(np.linalg.matrix_rank(Q, tol=1e-9)),
            minimum_eigenvalue=float(np.linalg.eigvalsh(Q)[0]),
            maximum_eigenvalue=float(np.linalg.eigvalsh(Q)[-1]),
            residual_l2=fourier_l2,
            frobenius_oscillation_bound=2*math.sqrt(K)*fourier_l2,
            target_extensive_regret=.1*n,
            source_queries_for_this_posthoc_algebra_check=0,
            note="structural post-validator only, not an executed spectral source test",
        ))
    result = dict(identity_checks=500, identity_max_error=identity_max_error,
                  action_checks=action_checks, high_rank_structural_cases=structural)
    # Check the actual resource-slice adapter with a large unlearned context
    # offset. This does not claim a formal floating-point cancellation bound.
    k=5
    physical_n=2*k
    occupancy=np.array([0,1,2,1,1])
    A=rng.normal(size=(physical_n,physical_n))
    physical_H=(A+A.T)/2
    np.fill_diagonal(physical_H,0)
    physical_b=rng.normal(size=physical_n)
    physical=EnergySource(physical_H,physical_b,0,seed=93,constant=10**6+137)
    sliced=ModuleSliceSource(physical,occupancy)
    V=np.zeros((physical_n,sliced.n))
    for j,module in enumerate(sliced.active):
        V[2*module,j]=1
        V[2*module+1,j]=-1
    effective_H=V.T@physical_H@V
    np.fill_diagonal(effective_H,0)
    v=rng.normal(size=sliced.n)
    actual,_,represented=binary_hessian_action(sliced,v,18,1,.01)
    physical_states=sliced.encode(np.array([[1,-1,1],[-1,1,-1]]))
    observed_occupancies=np.sum(physical_states.reshape(-1,k,2)>0,axis=2)
    result["resource_slice_adapter_check"]={
        "physical_modules":k,"active_orientations":sliced.n,
        "occupancy":occupancy.tolist(),
        "every_encoded_state_preserves_occupancy":bool(np.all(observed_occupancies==occupancy)),
        "represented_action_error":float(np.max(np.abs(actual-effective_H@represented))),
        "unknown_offset":10**6+137,
        "scalar_source_shots":sliced.shots,"physical_control_writes":sliced.control_writes,
        "meaning":"The offset was never estimated; every contrast remained in one context."
    }
    if run_power:
        n=6
        z=np.r_[np.ones(3),-np.ones(3)]  # A cheap fixed feasible proposal.
        L=random_psd_kernel(n,z,83)
        multiplier=.3
        b=-multiplier*np.ones(n)
        H=L-np.diag(np.diag(L))
        entry_cap=2.0  # Warranted for the synthetic construction, not estimated.
        source=EnergySource(H,b,.02,seed=84,constant=9)
        start=time.perf_counter()
        good=certify_candidate(source,z,np.zeros(n),3,multiplier,
                               epsilon=1,delta=.25,a=1,
                               entry_cap=entry_cap,seed=85)
        good["wall_seconds"]=time.perf_counter()-start
        good["posthoc_true_Q_min_eigenvalue"]=float(np.linalg.eigvalsh(L)[0])
        # A planted negative curvature direction invalidates this certificate.
        u=np.array([1,-1,0,0,0,0],float)/math.sqrt(2)
        Q_bad=L-8*np.outer(u,u)
        H_bad=Q_bad-np.diag(np.diag(Q_bad))
        bad_source=EnergySource(H_bad,b,.02,seed=86,constant=9)
        start=time.perf_counter()
        bad=certify_candidate(bad_source,z,np.zeros(n),3,multiplier,
                              epsilon=1,delta=.25,a=1,
                              entry_cap=6.0,seed=87)
        bad["wall_seconds"]=time.perf_counter()-start
        bad["posthoc_true_Q_min_eigenvalue"]=float(np.linalg.eigvalsh(Q_bad)[0])
        # Post-run scorer only; the certifier has never read either matrix.
        states=np.array([[1. if (mask>>i)&1 else -1. for i in range(n)]
                         for mask in range(1<<n)])
        feasible=states[np.sum(states>0,axis=1)==3]
        good_values=np.einsum("ij,jk,ik->i",feasible,H,feasible)+feasible@b
        bad_values=np.einsum("ij,jk,ik->i",feasible,H_bad,feasible)+feasible@b
        good["posthoc_true_cardinality_regret"]=float(z@H@z+b@z-np.min(good_values))
        bad["posthoc_true_cardinality_regret"]=float(z@H_bad@z+b@z-np.min(bad_values))
        result["executed_good_case"]=good
        result["executed_bad_case"]=bad
    H_triangle=np.ones((3,3))-np.eye(3)
    z_triangle=np.array([1.,1.,-1.])
    Q_triangle=H_triangle-np.diag(z_triangle*(H_triangle@z_triangle))
    triangle_states=np.array([[1. if (mask>>i)&1 else -1. for i in range(3)]
                              for mask in range(8)])
    triangle_values=np.einsum("ij,jk,ik->i",triangle_states,H_triangle,triangle_states)
    result["sufficient_certificate_not_complete"]={
        "example":"unconstrained antiferromagnetic triangle",
        "candidate_true_regret":float(z_triangle@H_triangle@z_triangle-np.min(triangle_values)),
        "dual_min_eigenvalue":float(np.linalg.eigvalsh(Q_triangle)[0]),
        "meaning":"An exactly optimal candidate need not have this PSD certificate."
    }
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--skip-power",action="store_true")
    args=parser.parse_args()
    result=run_checks(not args.skip_power)
    target=Path(__file__).with_name("scalar_sdp_results.json")
    target.write_text(json.dumps(result,indent=2))
    summary={k:v for k,v in result.items() if k not in ["action_checks"]}
    for name in ["executed_good_case","executed_bad_case"]:
        if name in summary:
            summary[name]={k:v for k,v in summary[name].items() if k!="d_hat"}
    print(json.dumps(summary,indent=2))
