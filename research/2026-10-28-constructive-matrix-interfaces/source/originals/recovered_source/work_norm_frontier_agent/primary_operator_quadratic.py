#!/usr/bin/env python3
"""Complete checked Lie-unit dispatch for cyclic-primary matrix sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'work_matrix_root'))
sys.path.insert(0,str(ROOT/'work_norm_slice_agent'))


def count_unmarked_primary_lie_source(poly,algebra):
    """Every candidate is followed by full coefficient and operator certification."""
    from lie_source_unit import recover_from_raw_source,binary_solve
    from primary_lie_unit import recover_from_raw_primary_source
    from semisimple_lie_unit import recover_from_raw_semisimple_source
    from arbitrary_operator_lie_unit import recover_from_raw_arbitrary_source
    from operator_quadratic_counter import acquire_operator_linear_refinement,count_acquired_cyclic_refinement
    failures=[]
    for recover in (recover_from_raw_source,recover_from_raw_primary_source,
                    recover_from_raw_semisimple_source,recover_from_raw_arbitrary_source):
        try:
            unit,unit_evidence=recover(poly,algebra)
            inverse_unit=binary_solve(algebra.left_matrix(unit),algebra.one)
            beta,D,phi,eta,evidence=acquire_operator_linear_refinement(poly,algebra,inverse_unit)
            if not beta:raise ValueError('nonzero exterior-square source coefficient required')
            gap,backend=count_acquired_cyclic_refinement(algebra,beta,D,phi,eta)
            evidence.update(lie_source_unit=unit_evidence,
                unit_acquisition_route='certified Lie source unit and polynomial primary/refinement backend')
            return gap,backend,evidence
        except ValueError as error:failures.append(str(error))
    raise ValueError('no certified cyclic-primary Lie source: '+'; '.join(failures))
