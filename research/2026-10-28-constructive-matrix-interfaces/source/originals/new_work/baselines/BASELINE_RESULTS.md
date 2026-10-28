# Same-circuit ordinary counting and compilation baselines

Measured 2026-10-28 on the unaltered recovered
`work_phase_diamond/matrix_affine_diamond_native_n72.json`.
This fixture has **72 original inputs and 24,676 ordinary gates**. The output
task is the number of original assignments making its actual output wire true.
The recovered audit's `native.population` is **71,210,970,084,540,416**.

The full-equivalence Tseitin export took **0.088431 seconds** and produced
24,748 declared CNF variables and 95,631 clauses (1,794,955 bytes).
Every original input has a unique internal-wire extension. Therefore counting
all declared CNF variables preserves exactly the requested original-input
count; it does not promote gate wires to independent choices.

| Official implementation | Version (commit) | Solver elapsed | Export + solver elapsed | Peak child RSS | Outcome |
| --- | --- | ---: | ---: | ---: | --- |
| d4 count mode | `333370cc1e843dd0749c1efe88516e72b5239174` | 120.008462 s | 120.096893 s | 185.762 MiB | Timed out; no count |
| SharpSAT-TD | `0c234c11b77115bad89484e80e1d2fc95dd42317` | 120.009332 s | 120.097763 s | 321.918 MiB | Timed out during preprocessing; no count |
| d4 decision-DNNF compilation | `333370cc1e843dd0749c1efe88516e72b5239174` | 119.920110 s | 120.008541 s | 189.945 MiB | Timed out; empty artifact; sampling not reached |

The two count-only runs each had a 120-second solver wall budget. For the
separate compilation attempt, the total budget was 120 seconds including
the measured 0.088431-second export: the compiler allowance was
119.911569 seconds. Process termination overhead accounts for its measured
120.008541-second total. Each run had an 8-GiB address-space limit. The
solver timer includes parsing, preprocessing, and any decomposition work. Reported
RSS is Linux `getrusage(RUSAGE_CHILDREN).ru_maxrss` from a fresh one-child
runner invocation; it is not a sum of simultaneous process RSS values.
Timeout handling kills only the run's own process group. The runs were
sequential; no baseline build overlapped these solver timers.

The large fixture was not solved by these routes within their budgets. The
recovered exact count is **not** independently confirmed by these two timed-out
counting runs. The separately attempted compilation-to-sampling route left
a zero-byte output file after timeout, so no valid compilation artifact,
original witness, or exact uniform sample was obtained. Sampling was not
reached, and no sampling-speed ratio is claimed. Count-only timeouts do not
establish that finding one witness is difficult.
A single fixture and these parameter choices do not establish a general
advantage over ordinary counting or other representations.

## Reproduction and controls

- `circuit_to_cnf.py` contains the exporter and truth-table checks of its gate
  templates; it rejects non-topological wire references.
- `validate_converter.py` exhaustively evaluates all original assignments and
  all CNF assignments of a small mixed AND/XOR/constant circuit. It confirms
  the count 7 and unique internal extension, then checks that both built
  solvers report 7. `controls/control_results.json` and complete logs preserve
  these checks. This control is not a performance benchmark.
- `run_timed.py` captures commands, timings, resource use, exit status and
  full logs. `baseline_summary.json` combines the measured results.
- `diamond_n72_translation.json` records exact file hashes, dimensions and
  export time. The original fixture SHA256 is
  `2bd5a46c493ea94ed3c211b2a8ac3e384dde71daa7cf2d7548721d59148f05f2`.
- `d4_build.json` and `sharpsat_td_build.json` pin source commits and build
  commands. Official sources: https://github.com/crillab/d4 and
  https://github.com/Laakeri/sharpsat-td . Their tracked source files were not
  changed. Missing development libraries were extracted locally from official
  Ubuntu packages; no system package installation occurred.
- `dependency_archives.json` pins URLs, sizes and SHA256 hashes of these
  public build dependencies. The large `vendor` directory is reproducible
  setup material, not the substantive result.

The environment has g++ 13.3.0 on Ubuntu 24.04.3 LTS. CMake was absent, so
`build_sharpsat_td.py` expands the official source lists, compiler options and
library choices from its CMake files into ordinary compiler commands. That
unchanged-source build took 34.234231 seconds. The d4 build succeeded but its
setup time was not instrumented; it is explicitly left unmeasured. Downloads
and one-time builds are identified separately from per-instance acquisition
and counting.

Commands, using the baseline directory as the working directory for d4:

```sh
python circuit_to_cnf.py ../../recovered_source/work_phase_diamond/matrix_affine_diamond_native_n72.json diamond_n72.cnf --metadata diamond_n72_translation.json
python run_timed.py --timeout 120 --result diamond_n72_d4_count.json --log diamond_n72_d4_count.log -- ./vendor/d4/d4 -mc diamond_n72.cnf
python run_timed.py --timeout 119.91156900199712 --result diamond_n72_d4_compile.json --log diamond_n72_d4_compile.log -- ./vendor/d4/d4 -dDNNF diamond_n72.cnf -out=diamond_n72_d4.nnf
```

SharpSAT-TD must be run with its `flow_cutter_pace17` executable in the current
directory; the recorded command uses `-decot 10 -decow 100 -cs 3500` and an
explicit local temporary directory. Its full command and absolute input path
are preserved in `diamond_n72_sharpsat_td_count.json`. The selected 10-second
decomposition allowance is inside, not in addition to, the 120-second total.

## Attempted ordinary compilation-to-sampling route

The official d4 compiler can emit decision-DNNF with
`d4 -dDNNF input.cnf -out=output.nnf`. The official
https://github.com/crillab/decdnnf_rs provides exact count, conditioned model
extraction, direct access and uniform sampling; its `--n-vars` option should
retain the full declared variable universe. Since the CNF translation has
unique internal extensions, uniform full models would project uniformly to
the original inputs. This is the concrete route attempted in the separate
third run. The compilation timed out before producing a usable artifact;
the resulting `diamond_n72_d4.nnf` is zero bytes, is invalid, and must not be
used as a compiled representation. Consequently decdnnf_rs was not invoked,
and its count, witness and sampling stages were not reached. The run's
command, resource measurements and artifact status are preserved in
`diamond_n72_d4_compile.json` and its complete log.

The primary tool paper is
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.38 .
The earlier KUS approach also compiles to d-DNNF before uniform sampling:
https://www.cs.toronto.edu/~meel/Papers/lpar18.pdf .
These are established baseline capabilities, not new consequences of the P3
construction.

The evidence is one constructed fixture, three specified invocations, and
finite time budgets in a shared research environment. Alternative XOR-aware
encodings, BDD routes, native-circuit d4v2 modes, and parameter portfolios
were not exhaustively tested. The constructive theorem's scope is separate
from these limited comparative measurements.
