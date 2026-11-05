#!/usr/bin/env python3
"""Finite checks for a sparse, cohort-preserving autonomous circuit adapter.

This checks the NEW adapter on directed live-wire paths and cycles. It does
not implement the concatenated error-correcting code or establish a burst
threshold. The analytical source theorem supplies those separate guarantees.

At every tick apply the same local layers:
  1. SWAP(A_v,B_v) at every retained vertex.
  2. SWAP(B_v,A_succ(v)) on every directed continuation edge.
  3. RESET_0(A_v) at open-path sources.
  4. Fixed gates between equal-phase A vertices.

Open ends reflect into the backward B track. Returned junk reaches the
forward track only through a reset. Every retained edge is local; missing
sites are genuinely absent hardware, not mutable blank cells of a filled
translation-invariant lattice.

The symbolic scaling example has one data wire making a local out-and-back
walk over width B, with a two-node ancilla path. It uses 4(B+1) registers
instead of the full rectangular conveyor's 4B(B+1), a factor B.

The quantum example uses a 2-node data cycle and a 2-node ancilla path.
The ancilla is reset, coupled by CNOT, uncomputed next phase, then discarded.
It must preserve the unknown data/reference marginal despite arbitrary
initial junk and arbitrary channels on nonselected cohorts.

Requires NumPy. Run --self-test.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import json
import math
import numpy as np


@dataclass(frozen=True)
class Vertex:
    name: str
    x: int
    phase: int


@dataclass
class SparseGraph:
    period: int
    vertices: tuple[Vertex, ...]
    edges: tuple[tuple[int, int], ...]
    gates: tuple[tuple[int, int], ...]
    data_zero: int

    def __post_init__(self):
        self.pred = {}
        self.succ = {}
        for u, v in self.edges:
            assert u not in self.succ and v not in self.pred
            self.succ[u] = v
            self.pred[v] = u
            vu, vv = self.vertices[u], self.vertices[v]
            assert (vv.phase - vu.phase) % self.period == 1
            assert abs(vv.x - vu.x) <= 1
        for u, v in self.gates:
            assert self.vertices[u].phase == self.vertices[v].phase
            assert abs(self.vertices[u].x - self.vertices[v].x) <= 1
        self.sources = tuple(v for v in range(len(self.vertices)) if v not in self.pred)
        self.ends = tuple(v for v in range(len(self.vertices)) if v not in self.succ)
        used = set()
        for u, v in self.gates:
            assert u not in used and v not in used
            used.update((u, v))

    @staticmethod
    def a(v):
        return 2 * v

    @staticmethod
    def b(v):
        return 2 * v + 1

    @property
    def register_count(self):
        return 2 * len(self.vertices)

    def initial_labels(self):
        labels = np.empty(self.register_count, dtype=int)
        for v, node in enumerate(self.vertices):
            labels[self.a(v)] = -node.phase % self.period
            labels[self.b(v)] = -1000 - v
        return labels

    def swap_layers(self):
        return (
            tuple((self.a(v), self.b(v)) for v in range(len(self.vertices))),
            tuple((self.b(u), self.a(v)) for u, v in self.edges),
        )


def triangle_graph(padding):
    assert padding >= 3
    period = 2 * padding
    xs = [min(t, period - t) for t in range(period)]
    vertices = [Vertex(f"d{t}", xs[t], t) for t in range(period)]
    first = len(vertices)
    vertices.extend((Vertex("ancilla_birth", xs[1] + 1, 1),
                     Vertex("ancilla_end", xs[2] + 1, 2)))
    edges = [(t, (t + 1) % period) for t in range(period)]
    edges.append((first, first + 1))
    return SparseGraph(period, tuple(vertices), tuple(edges),
                       ((1, first), (2, first + 1)), 0)


def small_quantum_graph():
    # The ancilla path wraps phase 1 -> phase 0. First CNOT at phase 1,
    # second CNOT at phase 0, immediately before that ancilla is discarded.
    vertices = (Vertex("d0", 0, 0), Vertex("d1", 0, 1),
                Vertex("ancilla_birth", 1, 1), Vertex("ancilla_end", 1, 0))
    return SparseGraph(2, vertices, ((0, 1), (1, 0), (2, 3)),
                       ((1, 2), (0, 3)), 0)


def symbolic_case(padding, laps):
    graph = triangle_graph(padding)
    labels = graph.initial_labels()
    phase_checks = gate_checks = source_checks = returns = 0
    for tick in range(1, graph.period * laps + 1):
        old = labels.copy()
        for layer in graph.swap_layers():
            touched = set()
            for u, v in layer:
                assert u not in touched and v not in touched
                touched.update((u, v))
                labels[u], labels[v] = labels[v], labels[u]
        # Verify the exact open-path/cycle transport identities before reset.
        for v in range(len(graph.vertices)):
            expected_a = old[graph.a(graph.pred[v])] if v in graph.pred else old[graph.b(v)]
            expected_b = old[graph.b(graph.succ[v])] if v in graph.succ else old[graph.a(v)]
            assert labels[graph.a(v)] == expected_a
            assert labels[graph.b(v)] == expected_b
        for v in graph.sources:
            labels[graph.a(v)] = (tick - graph.vertices[v].phase) % graph.period
            source_checks += 1
        for v, node in enumerate(graph.vertices):
            assert labels[graph.a(v)] == (tick - node.phase) % graph.period
            phase_checks += 1
        for u, v in graph.gates:
            assert labels[graph.a(u)] == labels[graph.a(v)]
            gate_checks += 1
        if tick % graph.period == 0:
            assert labels[graph.a(graph.data_zero)] == 0
            returns += 1
    width = padding + 1
    sparse = graph.register_count
    dense = 2 * width * graph.period
    ticks = graph.period * laps
    assert dense == padding * sparse
    return dict(padding=padding,period=graph.period,laps=laps,
                retained_vertices=len(graph.vertices),live_slots_per_phase_at_most=2,
                sparse_registers=sparse,full_rectangle_registers=dense,
                hardware_reduction_factor=dense // sparse,
                fixed_rule_ticks=ticks,
                sparse_all_register_updates=sparse*ticks,
                full_rectangle_all_register_updates=dense*ticks,
                sparse_all_register_microphase_updates=4*sparse*ticks,
                full_rectangle_all_register_microphase_updates=4*dense*ticks,
                phase_ownership_checks=phase_checks,gate_cohort_checks=gate_checks,
                source_reset_checks=source_checks,selected_port_returns=returns,
                maximum_unwrapped_wire_step=math.sqrt(2),
                maximum_same_phase_gate_length=1,
                all_registers_and_idle_microphases_counted=True)


SWAP=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],dtype=complex)
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)


def axis_matrix(vector, matrix, targets):
    n=vector.size.bit_length()-1
    assert vector.size==1<<n
    order=tuple(targets)+tuple(q for q in range(n) if q not in targets)
    a=vector.reshape((2,)*n).transpose(order).reshape(1<<len(targets),-1)
    return (matrix@a).reshape((2,)*n).transpose(np.argsort(order)).reshape(-1)


def conjugate(rho, matrix, targets):
    n=rho.shape[0].bit_length()-1
    flat=axis_matrix(rho.reshape(-1),matrix,targets)
    flat=axis_matrix(flat,matrix.conj(),tuple(n+q for q in targets))
    return flat.reshape(rho.shape)


def reset_zero(rho, target):
    n=rho.shape[0].bit_length()-1
    order=(target,)+tuple(q for q in range(n) if q!=target)
    axes=order+tuple(n+q for q in order)
    a=rho.reshape((2,)*(2*n)).transpose(axes).reshape(2,1<<(n-1),2,1<<(n-1))
    traced=a[0,:,0,:]+a[1,:,1,:]
    out=np.zeros_like(a)
    out[0,:,0,:]=traced
    return out.reshape((2,)*(2*n)).transpose(np.argsort(axes)).reshape(rho.shape)


def marginal(rho, keep):
    n=rho.shape[0].bit_length()-1
    order=tuple(keep)+tuple(q for q in range(n) if q not in keep)
    axes=order+tuple(n+q for q in order)
    a=rho.reshape((2,)*(2*n)).transpose(axes)
    a=a.reshape(1<<len(keep),1<<(n-len(keep)),1<<len(keep),1<<(n-len(keep)))
    return np.einsum('aibi->ab',a)


def random_unitary(d, rng):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    q,r=np.linalg.qr(z)
    diag=np.diag(r)
    return q*(diag/np.abs(diag)).conj()


def initial_density(graph, kind, rng):
    n=graph.register_count+1
    ref=n-1
    data=graph.a(graph.data_zero)
    if kind=="bell_with_junk":
        bell=np.array([1,0,0,1],dtype=complex)/math.sqrt(2)
        junk=rng.normal(size=1<<(n-2))+1j*rng.normal(size=1<<(n-2))
        junk/=np.linalg.norm(junk)
        ordered=(data,ref)+tuple(q for q in range(n) if q not in (data,ref))
        psi=np.kron(bell,junk).reshape((2,)*n)
        psi=psi.transpose(tuple(ordered.index(q) for q in range(n))).reshape(-1)
    else:
        psi=rng.normal(size=1<<n)+1j*rng.normal(size=1<<n)
        psi/=np.linalg.norm(psi)
    return np.outer(psi,psi.conj())


def quantum_case(kind, outside_noise, laps, rng):
    graph=small_quantum_graph()
    labels=graph.initial_labels()
    rho=initial_density(graph,kind,rng)
    ref=graph.register_count
    keep=(graph.a(graph.data_zero),ref)
    expected=marginal(rho,keep)
    faults=0
    errors=[]
    trace_defects=[]
    def corrupt_outside(rho):
        nonlocal faults
        if not outside_noise:
            return rho
        outside=[q for q in range(graph.register_count) if labels[q]!=0]
        assert len(outside)>=2
        targets=tuple(int(q) for q in rng.choice(outside,2,replace=False))
        rho=conjugate(rho,random_unitary(4,rng),targets)
        if faults % 3==0:
            rho=reset_zero(rho,targets[0])
        faults+=1
        return rho
    for tick in range(1,graph.period*laps+1):
        for layer in graph.swap_layers():
            for u,v in layer:
                rho=conjugate(rho,SWAP,(u,v))
                labels[u],labels[v]=labels[v],labels[u]
            rho=corrupt_outside(rho)
        for v in graph.sources:
            rho=reset_zero(rho,graph.a(v))
            labels[graph.a(v)]=(tick-graph.vertices[v].phase)%graph.period
        rho=corrupt_outside(rho)
        for u,v in graph.gates:
            assert labels[graph.a(u)]==labels[graph.a(v)]
            rho=conjugate(rho,CNOT,(graph.a(u),graph.a(v)))
        rho=corrupt_outside(rho)
        if tick % graph.period==0:
            got=marginal(rho,keep)
            error=float(np.abs(np.linalg.eigvalsh(got-expected)).sum()/2)
            errors.append(error)
            trace_defects.append(float(abs(np.trace(rho)-1)))
            assert error<1e-9,error
    return dict(initial_state=kind,outside_channels=outside_noise,laps=laps,
                installed_qubits=graph.register_count,external_reference_qubits=1,
                arbitrary_outside_cptp_channels=faults,
                delivery_trace_distances=errors,
                maximum_reference_inclusive_error=max(errors),
                maximum_trace_defect=max(trace_defects),
                unchanged_fixed_update_at_every_tick=True)


def self_test(seed=20261105):
    rng=np.random.default_rng(seed)
    symbolic=[symbolic_case(b,k) for b in (3,8,16,31) for k in (1,5,17)]
    quantum=[quantum_case(kind,noisy,3,rng)
             for kind in ("bell_with_junk","fully_correlated")
             for noisy in (False,True)]
    return dict(passed=True,seed=seed,
                scope="Finite sparse-adapter identities only; no physical concatenated-code simulation or noise-threshold estimate.",
                immutable_premises="Fixed static sparse graph, fixed local channel law, synchronous ticks; all state-bearing registers mutable.",
                symbolic_case_count=len(symbolic),symbolic_cases=symbolic,
                quantum_case_count=len(quantum),quantum_cases=quantum,
                maximum_delivery_trace_distance=max(c["maximum_reference_inclusive_error"] for c in quantum),
                numpy_version=np.__version__)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--seed",type=int,default=20261105)
    args=parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(args.seed),indent=2))
    else:
        parser.print_help()
