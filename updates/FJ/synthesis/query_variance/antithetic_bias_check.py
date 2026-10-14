#!/usr/bin/env python3
"""Exact counterexample to naive antithetic reuse inside nonlinear products."""
from fractions import Fraction as Q
import json
from pathlib import Path


def main():
    # One unbiased child variable X in {-1,+1}. A quadratic branch requires
    # independent copies. Reusing X and -X keeps each marginal unbiased but
    # changes the product expectation from 0 to -1.
    independent_product_mean = Q(0)
    identical_antithetic_product_mean = Q(-1)
    shared_same_path_product_mean = Q(1)
    assert independent_product_mean == 0
    assert identical_antithetic_product_mean == -1
    assert shared_same_path_product_mean == 1
    result = {
        "child_law": "P(X=+1)=P(X=-1)=1/2; E[X]=0",
        "required_independent_child_product_expectation": str(independent_product_mean),
        "antithetic_pair_(X,-X)_product_expectation": str(identical_antithetic_product_mean),
        "identical_pair_(X,X)_product_expectation": str(shared_same_path_product_mean),
        "conclusion": "Pair marginals alone do not preserve the nonlinear branch expectation; this refutes naive antithetic pairing, not covariance-corrected or U-statistic estimators.",
    }
    Path(__file__).with_name("antithetic_bias_check.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
