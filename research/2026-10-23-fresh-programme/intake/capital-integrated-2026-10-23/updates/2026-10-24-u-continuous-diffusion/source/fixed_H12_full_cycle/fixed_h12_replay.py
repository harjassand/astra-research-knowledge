#!/usr/bin/env python3
"""One fixed-H full-cycle finite-volume replay; no parameter search."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np

from cyclic_solver import apply_generator, bernoulli, resolvent, solver_check

BASE=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location(
    "continuous_model",BASE/"opportunity_diffusion/lead/continuous_model.py")
model=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(model)


def build_rates(x,dx,h,kappa):
    U,_=model.potential(x,h)
    dU=np.roll(U,-1)-U
    xi=model.FORCE*dx-dU
    return bernoulli(-xi)/(dx*dx*kappa),bernoulli(xi)/(dx*dx*kappa),U,dU


def one_cycle(p0,nsteps,with_ledger=False):
    n=len(p0); dx=model.LENGTH/n
    slow_period=2*math.pi/model.SLOW_FREQUENCY
    dt=slow_period/nsteps
    kappa=model.kappa()
    x=np.arange(n)*dx
    f=model.profiles(x)[4]
    p=np.asarray(p0,dtype=float).copy()
    stats={
        "Wh_BE":0.0,"Wh_trapezoid":0.0,"WF":0.0,"Qbath":0.0,
        "Sigma":0.0,"max_mass_error":0.0,"min_mass":float(np.min(p)),
        "max_raw_mass_error":0.0,"max_mass_projection":0.0,
        "max_imaginary_solve":0.0,"BE_step_energy_closure_max":0.0,
        "mass_instantaneous_generator_error":0.0,
    }
    h0,hdot0=model.waveform(0.0)
    hdot0=hdot0/kappa
    U0,_=model.potential(x,h0)
    E0=float(np.dot(p,U0)); S0=float(-np.sum(p*np.log(np.maximum(p,1e-300))))
    Eold=E0
    for k in range(nsteps):
        u0=k*dt; u1=(k+1)*dt
        h_old,hdot_old_phys=model.waveform(u0/kappa)
        h_new,hdot_new_phys=model.waveform(u1/kappa)
        hdot_old=hdot_old_phys/kappa
        hdot_new=hdot_new_phys/kappa
        a,b,Unew,dU=build_rates(x,dx,h_new,kappa)
        rhs=p/dt
        pnew_complex=resolvent(a,b,1.0/dt,rhs)
        stats["max_imaginary_solve"]=max(stats["max_imaginary_solve"],
                                             float(np.max(np.abs(pnew_complex.imag))))
        pnew=pnew_complex.real
        raw_mass=float(pnew.sum())
        stats["max_raw_mass_error"]=max(stats["max_raw_mass_error"],abs(raw_mass-1.0))
        if not np.isfinite(raw_mass) or raw_mass<=0:
            raise FloatingPointError(f"invalid raw mass {raw_mass}")
        stats["max_mass_projection"]=max(stats["max_mass_projection"],abs(raw_mass-1.0))
        pnew=pnew/raw_mass
        Qp=apply_generator(a,b,pnew)
        stats["mass_instantaneous_generator_error"]=max(
            stats["mass_instantaneous_generator_error"],float(abs(Qp.sum())))
        J=a*pnew-b*np.roll(pnew,-1)
        force_rate=model.FORCE*dx*float(J.sum())
        heat_rate=float(np.dot(J,model.FORCE*dx-dU))
        flux_entropy=np.log(a*np.maximum(pnew,1e-300)
                            /(b*np.maximum(np.roll(pnew,-1),1e-300)))
        sigma_rate=float(np.dot(J,flux_entropy))
        dh=h_new-h_old
        wh_be=-dh*float(np.dot(f,p))
        wh_trap=-0.5*dt*(hdot_old*float(np.dot(f,p))
                         +hdot_new*float(np.dot(f,pnew)))
        wf=dt*force_rate; qb=dt*heat_rate; sig=dt*sigma_rate
        Enew=float(np.dot(pnew,Unew))
        dE=Enew-Eold
        closure=dE-(wh_be+wf-qb)
        stats["BE_step_energy_closure_max"]=max(
            stats["BE_step_energy_closure_max"],abs(closure))
        if with_ledger:
            stats["Wh_BE"]+=wh_be
            stats["Wh_trapezoid"]+=wh_trap
            stats["WF"]+=wf; stats["Qbath"]+=qb; stats["Sigma"]+=sig
        p=pnew; Eold=Enew
        stats["max_mass_error"]=max(stats["max_mass_error"],abs(float(p.sum())-1.0))
        stats["min_mass"]=min(stats["min_mass"],float(p.min()))
    h_end,_=model.waveform(slow_period/kappa)
    Uend,_=model.potential(x,h_end)
    E1=float(np.dot(p,Uend))
    S1=float(-np.sum(p*np.log(np.maximum(p,1e-300))))
    stats["delta_E"]=E1-E0
    stats["delta_S"]=S1-S0
    stats["p_end"]=p
    if with_ledger:
        stats["first_law_BE_cycle_residual"]=(stats["delta_E"]
            -(stats["Wh_BE"]+stats["WF"]-stats["Qbath"]))
        stats["first_law_trapezoid_cycle_residual"]=(stats["delta_E"]
            -(stats["Wh_trapezoid"]+stats["WF"]-stats["Qbath"]))
        stats["entropy_cycle_residual"]=(stats["delta_S"]+stats["Qbath"]-stats["Sigma"])
        stats["power_on_per_physical_time"]=(stats["Wh_trapezoid"]
            /(slow_period/kappa))
        stats["force_power_input_per_physical_time"]=(stats["WF"]
            /(slow_period/kappa))
        stats["heat_rate_per_physical_time"]=(stats["Qbath"]
            /(slow_period/kappa))
    return stats


def simulate(n=300,nsteps=1200,tol=1e-8,max_warm_cycles=30):
    dx=model.LENGTH/n
    p=np.full(n,1.0/n)
    warmup=[]
    for cycle in range(1,max_warm_cycles+1):
        result=one_cycle(p,nsteps,with_ledger=True)
        pnext=result.pop("p_end")
        delta=float(np.linalg.norm(pnext-p,1))
        warmup.append({"cycle":cycle,"start_state_l1_change":delta,
                       "Wh_trapezoid":result["Wh_trapezoid"],
                       "WF":result["WF"],"Qbath":result["Qbath"]})
        p=pnext
        if delta<tol:
            break
    periodic=result
    pnext=periodic.pop("p_end",None)
    # `result` is the final warm-up cycle; recompute its work ledger from the
    # converged start distribution rather than treating the last transient as
    # the periodic-cycle measurement.
    start=p.copy()
    periodic=one_cycle(start,nsteps,with_ledger=True)
    periodic_distance=float(np.linalg.norm(periodic["p_end"]-start,1))
    periodic.pop("p_end")
    tau=model.period()
    return {
        "model":"provided continuous_model.py; fixed H=12, fixed waveform/force",
        "height":model.HEIGHT,"n_cells":n,"dx":dx,"steps_per_period":nsteps,
        "dt_slow":(2*math.pi/model.SLOW_FREQUENCY)/nsteps,
        "kappa":model.kappa(),"physical_period":tau,
        "warmup_cycles_from_uniform":len(warmup),"warmup_trace":warmup,
        "periodic_start_l1_residual":periodic_distance,
        "periodic_tolerance":tol,"periodic_cycle":periodic,
        "solver_check_max_error":solver_check(),
        "scope":"fixed-H finite-volume replay; bounded refinements are summarized in FULL_CYCLE_RESULTS.md; force-work mesh error remains visible",
        "startup_note":"uniform numerical start and modeled warm-up are shown; no physical preparation-cost claim",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cells",type=int,default=300)
    ap.add_argument("--steps",type=int,default=1200)
    ap.add_argument("--tol",type=float,default=1e-8)
    ap.add_argument("--max-warm-cycles",type=int,default=30)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    model.self_check()
    result=simulate(args.cells,args.steps,args.tol,args.max_warm_cycles)
    out=json.dumps(result,indent=2)
    if args.output:
        args.output.write_text(out+"\n")
    print(out)


if __name__=="__main__":
    main()
