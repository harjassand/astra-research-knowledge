# Executable local-source acquisition

This program acquires exact classical specifications for the paper circuit construction. It does not synthesize rotations or execute the retained quantum simulator.

Use Python 3.12 or a compatible Python with fractions/dataclasses. Production acquisition uses only the standard library. The small dense tests additionally use NumPy. The separate spectral diagnostics use NumPy and SciPy.

From this directory:

    python3 test_threshold_acquisition.py
    python3 test_threshold_independent.py

Minimal API example:

    from acquire_threshold_source import ThresholdSource, verify_spec
    s = ThresholdSource([[1,1]]*3, [[[2,1],[1,2]]]*2)
    spec = s.specification([0,1,3])
    assert verify_spec(spec)
    assert spec['return_admitted']
    column = s.column(0)
    assert sum(row['probability'] for row in column) == 1

Onsite factors are one positive rational pair per spin. Edges are one positive rational 2-by-2 matrix per nearest-neighbor edge of an OPEN chain. Entries can be integers, rational strings or Fraction values; floats and nonpositive values are rejected. Bit zero is the first spin. No fitting to experimental data is performed: the raw factors are supplied program inputs.

The program derives exact local heat-bath rates, threshold colors, preimages, conditional probability columns, transfer-matrix reference probabilities, optional Z-string means, a Dobrushin contraction certificate when it passes, and a conservative integer return horizon. The n64 example uses local data and transfer messages, not an enumerated 2^64-state matrix.

verify_spec recomputes the record from its raw factors. A valid record can have return_admitted=False: that is an honest failure to obtain this sufficient return certificate, not a successful simulator admission. The verifier checks the optional means present in the record, not an external manifest of quantities a caller intended to request. It does not authenticate the physical truth of the input factors.

Numerical dense diagnostics only validate small instances. Spectral gaps are not substituted for the separately proved operator return effects. The geometric-merge and threshold sources have different quantum jump structures and distinct certificates; do not transfer one certificate to the other.

The coupling-to-qsample mechanism is established prior work. See PRIOR_ART_CORRECTION_TEMME_WOCJAN.md in the accompanying comparison folder. The paper-level controlled-simulation receiving construction, acquired operations, resource costs and limitations are in Glauber_COUPLING_COMPILER_RECEIVING_CANDIDATE.md and its separate whole review. No practical crossover, general quantum-source breakthrough or historical originality is established.
