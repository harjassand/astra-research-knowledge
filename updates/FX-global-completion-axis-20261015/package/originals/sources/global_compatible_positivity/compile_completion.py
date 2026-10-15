#!/usr/bin/env python3
"""Compile an exact rational instance of the universal completion theorem.

Examples:
    python compile_completion.py --r=-11/4 --alpha=27
    python compile_completion.py --r=1/2 --method=trace --output=positive_r.json

Run verify_global_structure.py first to check the universal input identities.
The output is a certificate for P_{alpha,r}-H, not just P_{alpha,r}.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sympy as s
from verify_global_structure import load_certificate, completion_at, require


def matrix_text(M: s.Matrix) -> list[list[str]]:
    return [[str(v) for v in row] for row in M.tolist()]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--r",required=True,help="exact rational parameter, e.g. --r=-11/4")
    parser.add_argument("--alpha",help="optional rational coefficient, at least the computed sufficient bound")
    parser.add_argument("--method",choices=["gershgorin","trace"],default="gershgorin")
    parser.add_argument("--certificate",type=Path,default=Path(__file__).with_name("GLOBAL_COMPLETION_CERTIFICATE.json"))
    parser.add_argument("--output",type=Path,default=Path("COMPILED_COMPLETION.json"))
    args=parser.parse_args()
    try:
        parameter=s.Rational(args.r)
        p=load_certificate(args.certificate)
        comp=completion_at(p,parameter,args.method)
        alpha=s.Rational(args.alpha) if args.alpha is not None else s.ceiling(comp["alpha_star"])
        require(alpha>=comp["alpha_star"],"requested alpha is below this construction's sufficient bound; no impossibility is implied")
        S=comp["gram_for_subtracted_integrand"]+(alpha-comp["alpha_star"])*p["SH"]
        C=p["C"].subs(p["r"],parameter)
        L,D=S.LDLdecomposition(hermitian=False)
        require(L*D*L.T==S and all(v>0 for v in D.diagonal()),"compiled exact Gram positivity")
        output=dict(schema="astra-completed-rational-instance-v1",r=str(parameter),alpha=str(alpha),
                    beta=str(parameter*(parameter-1)/6),gamma="1",delta=str(parameter),
                    subtracted_H="1",integrated_margin="4/1875",diffusion=[[1,0],[0,1]],
                    method=args.method,alpha_sufficient_bound=str(comp["alpha_star"]),
                    lambda_value=str(comp["lambda_value"]),C=matrix_text(C),S=matrix_text(S),
                    omega=matrix_text(comp["omega"]),positive_ldl_pivots=[str(v) for v in D.diagonal()],
                    matrix_entry_order=p["data"]["matrix_entry_order"],
                    jet_derivative_order=p["data"]["jet_derivative_order"],
                    bilinear_order="matrix index outer, second-jet index inner",
                    omega_pairs=p["data"]["omega_pairs"],omega_monomials=p["data"]["omega_monomials"],
                    scope="Universal identities and analytic proof are in the accompanying verifier/report. A sufficient coefficient, not an optimality certificate.")
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
        print(f"Exact completed certificate written: {args.output}")
        print(f"r={parameter}; alpha={alpha}; sufficient bound={comp['alpha_star']}")
    except (ValueError,TypeError,AssertionError,OSError) as exc:
        parser.exit(1,f"Completion failed: {exc}\n")


if __name__=="__main__":
    main()
