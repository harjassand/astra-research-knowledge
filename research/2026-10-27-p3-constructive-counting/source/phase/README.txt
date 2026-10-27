ASTRA P3: CONSTRUCTIVE PHASE REPRESENTATIONS — 27 OCTOBER 2026

Start with Astra_P3_Constructive_Phase_Representations.pdf. Its TeX source is
included. This consolidated report controls the scope of the result; earlier
technical notes retain intermediate constructions and secondary extensions.

MAIN RESULT
Conditional on the pinned governing manuscript: fixed-locality, fixed
2-power-root phase products with n independent bits and m=n exp(o(log n))
explicit factors can be summed exactly in poly(L+n) 2^o(n) bit time and
polynomial space. The local tables, replacement forms and summaries are
constructed. The report charges arithmetic, precision and reconstruction.

Applications include checked bounded-degree raw arithmetic programs when
the computed output support and number of requested outputs meet the stated
bounds, plus exact amplitudes and requested marginals for raw circuits with
O(n) Hadamards and n exp(o(log n)) local diagonal phase gates.

EXECUTION STATUS
The Python programs implement raw-description compilation and exact finite
validation. Their counting backends enumerate assignments or subset-union
states. THEY ARE NOT IMPLEMENTATIONS OF THE SUBEXPONENTIAL REPLACEMENT SOLVER.
There is no executed practical-speed claim or fast sampler.

All Python programs use the standard library; executions used Python 3.12.
Keep the directory structure, since two checkers import sibling modules.
Run commands from this directory, for example:

python3 work_root/program_phase_compiler.py --validate --output work_root/program_phase_results.json
python3 work_root/hadamard_phase_compiler.py
python3 work_dense_agent/phase_product_checks.py
python3 work_uniform_audit2/phase_product_audit_checks.py --output work_uniform_audit2/phase_product_audit_results.json
python3 work_dense_agent/dense_grid_alias_checks.py
python3 work_uniform_audit2/hybrid_contraction_checks.py --output work_uniform_audit2/hybrid_contraction_results.json

The corresponding JSON files contain actual saved execution outputs.
The general path compiler's updated tests include arbitrary local phase
tables: 24 circuits, 144 amplitudes, 264 marginals, and four boundary checks.

CONTENT
work_root: raw Boolean program compiler, Hadamard/local-table path compiler,
           wide-circuit compiler, and residual-state obstruction.
work_dense_agent: principal phase proof, independent phase fixtures,
                  dense-grid alias obstruction, Hadamard-extension audit.
work_uniform_audit2: independent phase proof audit, hybrid dense-circuit bound,
                     uniform-width audit, and exact finite checkers.
work_output_agent: prior-art comparison and output-filter precision obstruction.
work_prior_agent: uniform growing-width construction and universal-algebra
                  obstruction, with checkers.
work_tensor_agent: N1077 admissibility tests, interpolation precision obstruction,
                   and width audit. The two stdout-only checkers' outputs are saved.
work_circuit_agent: causality and cyclic-core obstructions; affine-Fourier
                    comparison (a derived benchmark, not a novelty claim).
work_preserved_network: the three supplied latest network-source attachments,
                        unchanged, and the scope of preservation.
governing_source: the user-supplied governing PDF, matched to the pinned blob.

PRESERVATION LIMIT
The latest task-directed network proof and native response are preserved
byte-for-byte. Network numerical/replay claims remain producer reports.
The earlier 510-reaction exact/noise-aware Gram proof and executable files
were not recovered. The latest receipt also records unacquired network code
and results; their filenames are not evidence of acquisition or execution.

RESEARCH BOUNDARY
No claim for arbitrary circuits, dense cubic phases with Theta(n^3) terms,
unrestricted degree or Hadamard count, arbitrary rational weights, or generic
tensor contraction. All source-dependent complexity results remain conditional
and have internal audits, not external peer review. Section 10 of the report
is the compact continuation. No computation continues after this turn ends.
