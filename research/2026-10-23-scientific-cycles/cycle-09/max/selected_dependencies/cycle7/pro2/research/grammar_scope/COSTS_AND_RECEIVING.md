# Structural scope contribution: costs and receiving instruction

## Result and receiving use

The arbitrary-series P2/P3-with-stubs grammar does not cover all chordless
degree-four series-parallel atoms. Its two-connected cores have an even number
of degree-four vertices. The supplied A_L family has exactly one, for every
L>=2; A_2 is saved explicitly. The independent necessary balanced-port condition
also excludes K_(2,4). These are graph-representation exclusions, not coloring
or query lower bounds.

Root may use Lemmas 1-2 to state the scope of a new all-depth coloring operation
without claiming the general chordless class. The concrete omitted interface
has unequal parallel-child endpoint loads: two at one end and one at the other,
with final degree totals four and three. A more general theorem must account for
these actual loads, or supply another admitted representation. Merely permitting
both series parities does not change the parity obstruction.

The inclusion Theta(2,2,2,L), L>=4, is also proved explicitly, so the note does
not overstate the exclusion to all four-path theta atoms. A_2 has a saved
star-three coloring, directly demonstrating that omission by the grammar is
not hardness of the recovery problem.

## Source and computation

Read the native Cycle6 PROOF.md and research/chordless/PROOF.md. No old scientific
calculation was replayed. No external source, package installation, optimization,
floating solver, upload, public sharing or outreach was used.

First and only execution:

    python cycle7_pro2/research/grammar_scope/check_scope.py

The exact checker passed on both actual saved inputs. It verifies all simple
cycles, chordlessness, absence of vertex/edge clique cuts, degree counts, a
supplied width-two decomposition and the necessary balanced-port condition;
it also checks A_2's star-three coloring. All-size claims depend on the proof,
not enumeration of these inputs.

Measured body wall: 0.00030826600414002314 seconds.
Measured body CPU: 0.00030596600000000126 seconds.
Peak process RSS: 10,223,616 bytes.

The body timer includes input construction and checking. Imports, process
startup and result serialization are excluded. Discovery, inference, authoring,
source reading and proof review costs are unknown and not represented by these
timings. There were no failed numerical executions or precision sweeps.

## Development decisions and limitations

The first scope witness considered was K_(2,4), a finite obstruction already
relevant to the inherited boundary-color restrictions. The paired-degree
invariant gave the stronger unbounded A_L family and the unequal-load receiving
interface. This was mathematical strengthening, not an unsuccessful run.

The proof concerns exactly the stated grammar with single exterior terminal
edges and the extraction of a two-connected core by deleting its two terminal
leaves. It does not exclude larger graph grammars, additional leaf-module
families, a different decomposition, or designs outside coordinates. Conditions
in Lemma 2 are necessary, not a full recognition algorithm. Historical novelty
is not assessed or claimed for these elementary scope lemmas.
