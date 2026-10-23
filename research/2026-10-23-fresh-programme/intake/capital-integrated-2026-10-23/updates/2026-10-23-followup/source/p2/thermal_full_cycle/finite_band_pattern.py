"""Finite-band static susceptibility synthesis; conditional numerical design.

Linear programming gives the largest desired scalar overlap on a stated
piecewise-constant fabrication grid. Every retained mode and resonant pair-
creation channel is then charged in the covariance model. No measured chi,
domain losses or actual fabrication capability are assumed to be known.
"""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog, minimize_scalar
from patterned_converter import primitive,network,pattern_edges

OUT=Path(__file__).resolve().parent
M=10;R=2


def kernels(cells,j,k):
    edges=np.linspace(0,np.pi,cells+1)
    result=np.zeros(cells)
    for n,sign in [(j-k+R,1),(j-k-R,1),(j+k+R,-1),(j+k-R,-1)]:
        result+=sign*np.diff(primitive(n,edges))/4
    return result


def solve_pattern(cells,last_suppressed_j):
    """Suppress all j<=last except desired M, and all j+k=R pairs."""
    target=kernels(cells,M,M+R)
    rows=[kernels(cells,j,j+R) for j in range(1,last_suppressed_j+1) if j!=M]
    rows += [kernels(cells,j,R-j) for j in range(1,R)]
    A=np.array(rows)
    fit=linprog(-target,A_eq=A,b_eq=np.zeros(len(A)),bounds=[(-1,1)]*cells,
                method='highs',options={'dual_feasibility_tolerance':1e-9,
                                       'primal_feasibility_tolerance':1e-9})
    assert fit.success,fit.message
    p=fit.x
    # Symmetry averaging preserves objective and constraints and the norm bound.
    p=(p+p[::-1])/2
    dual=float(-fit.lower.marginals.sum()+fit.upper.marginals.sum())
    residual=float(np.max(abs(A@p)))
    assert residual<1e-9
    assert abs(dual-fit.fun)<1e-9
    return dict(cells=cells,suppressed_lower_indices=list(range(1,last_suppressed_j+1)),
        desired_exception=M,overlap=float(target@p),
        pump_penalty_at_same_desired_g=float((np.pi/4/(target@p))**2),
        primal_residual=residual,discrete_LP_primal_dual_gap=float(abs(dual-fit.fun)),
        maximum_absolute_profile=float(max(abs(p))),
        profile_edges_radians=np.linspace(0,np.pi,cells+1).tolist(),
        profile_values=p.tolist())


def optimize_heat(edges_signs):
    # Bounded power search at 40 modes, then an independent larger-band check.
    # It is a sampled-and-refined scalar search, not a general optimality proof.
    amps=np.r_[0.,np.geomspace(.01,10,61)]
    qs=[network(a,40,edges_signs=edges_signs)['net_cold_heat_over_Q0'] for a in amps]
    i=int(np.argmax(qs))
    if i==0:
        amp=0.
    else:
        fit=minimize_scalar(lambda a:-network(a,40,edges_signs=edges_signs)['net_cold_heat_over_Q0'],
            bounds=(amps[max(0,i-1)],amps[min(i+1,len(amps)-1)]),method='bounded',
            options={'xatol':1e-8})
        amp=float(fit.x)
    small=network(amp,40,edges_signs=edges_signs)
    large=network(amp,88,edges_signs=edges_signs)
    return dict(optimized_amplitude=amp,
        net_heat_over_Q0=large['net_cold_heat_over_Q0'],
        gross_heat_over_Q0=large['cold_heat_over_Q0'],
        work_over_Q0=large['conversion_work_over_Q0'],
        total_absorption_over_Q0=large['total_pump_absorption_over_Q0'],
        wall_COP_before_source_losses=large['wall_COP_before_source_losses'],
        cutoff40_to88_cold_difference=large['cold_heat_over_Q0']-small['cold_heat_over_Q0'],
        cutoff40_to88_work_difference=large['conversion_work_over_Q0']-small['conversion_work_over_Q0'],
        energy_closure_over_Q0=large['energy_closure_over_Q0'])


def optimize_cop(edges_signs=None,only_target=False,kind='pattern'):
    def evaluate(amp):
        z=network(amp,88,kind=kind,edges_signs=edges_signs,only_target=only_target)
        cop=z['wall_COP_before_source_losses']
        return (-1. if cop is None else cop),z
    amps=np.geomspace(.01,10,61)
    values=[evaluate(a)[0] for a in amps]
    i=int(np.argmax(values))
    if values[i]<0:
        return dict(status='NO_POSITIVE_COOLING_ON_STATED_SEARCH')
    fit=minimize_scalar(lambda a:-evaluate(a)[0],bounds=(amps[max(0,i-1)],amps[min(i+1,len(amps)-1)]),
        method='bounded',options={'xatol':1e-8})
    cop,z=evaluate(float(fit.x))
    return dict(status='BOUNDED_NUMERICAL_COP_MAXIMUM',amplitude=float(fit.x),
        wall_COP_before_source_losses=float(cop),net_heat_over_Q0=z['net_cold_heat_over_Q0'],
        work_over_Q0=z['conversion_work_over_Q0'],absorption_over_Q0=z['total_pump_absorption_over_Q0'])


def main():
    scenarios=[]
    for last in [9,12,16,24,40]:
        design=solve_pattern(192,last)
        design['full_network_at_amplitude2']=network(2.,88,
            edges_signs=(np.array(design['profile_edges_radians']),np.array(design['profile_values'])))
        design['net_heat_optimization']=optimize_heat(
            (np.array(design['profile_edges_radians']),np.array(design['profile_values'])))
        design['COP_optimization']=optimize_cop(
            (np.array(design['profile_edges_radians']),np.array(design['profile_values'])))
        scenarios.append(design)
    binary=optimize_heat(pattern_edges())
    # Resolution evidence concerns the discretized feasible design, not an
    # asserted continuum optimum or actual minimum printable feature.
    refinement=[]
    for cells in [96,192,384,1024]:
        for last in [12,24,40]:
            z=solve_pattern(cells,last)
            refinement.append({k:z[k] for k in ['cells','overlap','pump_penalty_at_same_desired_g',
                'primal_residual','discrete_LP_primal_dual_gap'] } | {'last_suppressed_j':last})
    result=dict(status='SYNTHETIC_FINITE_BAND_STATIC_CONTROL_DESIGN',
        actual_fabrication_and_loss='UNKNOWN',novelty='UNKNOWN',
        scalar_profile_constraints='192 equal cells, real |chi/chi0|<=1, mirror averaging; fractional cells allowed',
        objective='Maximum target overlap with exact forbidden-edge zeros; not globally maximum wall COP.',
        net_heat_search='Amplitude [0,10], 61 logarithmic samples and local refinement; 40-mode search checked at 88 modes.',
        pump_and_baths='Same declared synthetic conditions as patterned_converter.py.',
        warning='Fractional-valued susceptibility and cell boundaries require a separate fabrication, absorption and tensor calculation.',
        designs=scenarios,binary_pattern_optimized_net_heat=binary,
        binary_pattern_optimized_COP=optimize_cop(pattern_edges()),
        fictitious_ideal_pair_optimized_COP=optimize_cop(only_target=True,kind='uniform'),
        grid_refinement=refinement)
    (OUT/'finite_band_pattern_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(binary=binary,designs=[dict(last=a['suppressed_lower_indices'][-1],
        overlap=a['overlap'],pump_penalty=a['pump_penalty_at_same_desired_g'],
        net_heat_optimization=a['net_heat_optimization'],COP_optimization=a['COP_optimization']) for a in scenarios],
        binary_COP=result['binary_pattern_optimized_COP'],
        ideal_pair_COP=result['fictitious_ideal_pair_optimized_COP']),indent=2))


if __name__=='__main__':main()
