# Reciprocal broadcast programming with a fixed control alphabet

This is an internal constructive result for an explicitly specified mechanical energy model. It does not assert an acquired material, a practical advantage, thermal reliability, or historical priority. The construction is stronger than a finite state-graph example: it includes a reciprocal energy, reset, local transition inequalities, and an induction for every positive integer array length.

## Statement and exact model

For every positive integer `N`, the construction below has `5N+2` movable coordinates, `6N+1` reciprocal pair couplings, maximum graph degree four, and coefficients drawn from a fixed finite set. One scalar parameter `H` writes any target word of `N` stationary output bits from any previously written word. It uses nine fixed field levels and at most `3N+8` commands, including reset and return to `H=0`. Its quasistatic hard-stop operation has a non-switching margin of at least two at each intended event and a margin of at least one at each final pulse level. No threshold resolution or local address input grows with `N`.

Let every movable coordinate lie in `[-1,1]` and define

\[
E(x,H)=\sum_i\frac{c_i}{2}(1-x_i^2)
 -H\sum_i g_i x_i-\sum_i b_i x_i
 -\sum_{i<j}J_{ij}x_ix_j,\qquad J_{ij}=J_{ji}.
\]

The interval endpoints are mechanical stops. Damped downhill relaxation supplies dissipation. For endpoint signs `s_i` define

\[
f_i=g_iH+b_i+\sum_jJ_{ij}s_j,
\qquad m_i=c_i+s_if_i.
\]

The endpoint is stable in coordinate `i` exactly when `m_i>0`. It switches from `-1` to `+1` when `f_i>c_i`, and conversely when `f_i<-c_i`. If an intended coordinate has `d f_i>c_i`, then along its entire crossing `d x_i` increases: the force in the direction `d` is `c_i d x_i+d f_i>0`. Consequently this endpoint model follows from the continuous reciprocal potential; directed transition rules have not been inserted separately.

This onsite potential is a concave quadratic between stops, with finite barrier height. It is not the initially considered triangular cusp. Its finite-compliance continuation is a separate companion construction, discussed below.

## Cells and couplings

Use track cells `q_1,...,q_(2N+1)`, an auxiliary `z_i` for every track cell, and output memories `m_1,...,m_N`. Here `m_i` denotes a memory coordinate, distinct from a stability margin when used as a subscripted cell name. Define `a_i=(-1)^(i+1)`.

| Family | c | g | Couplings |
|---|---:|---:|---|
| Track q_i | 10 | 1 | `J(q_i,q_(i+1))=-10`; `J(q_i,z_i)=-4a_i` |
| Auxiliary z_i | 40 | 2 | Reciprocal coupling to its track cell |
| Memory m_j | 13 | 1 | `J(m_j,q_(2j))=J(m_j,q_(2j+1))=+1` |

Clamp two reference endpoints, `q_0=+1` and `q_(2N+2)=-1`, with coupling `-10` to the adjacent track ends. Equivalently, use `b_(q1)=-10`, `b_(qLast)=+10`, and all other `b=0`. These are two fixed structural references, not dynamically addressed cells.

The weighted variable degree is at most 25 for track cells, four for auxiliaries, and two for memories. The only field gains are one and two. The only coercivity parameters are 10, 13, and 40.

All pair terms can be decomposed into passive signed spring couplings plus local onsite curvature. If `d_i=sum_j |J_ij|`, then

\[
\sum_{i<j}\frac{|J_{ij}|}{2}(x_i-\operatorname{sgn}(J_{ij})x_j)^2
=\frac12\sum_i d_i x_i^2-\sum_{i<j}J_{ij}x_ix_j.
\]

An onsite negative curvature `c_i+d_i` therefore supplies the required energy after adding these ordinary positive spring energies; opposite lever orientation supplies the coupling sign. The largest required onsite curvature is 44. This is an energy decomposition, not an acquired fabrication drawing or evidence that an actual snap element has the exact law.

## Preparation and reset

At `H=-64`, every movable cell has negative force large enough to end at `-1`, independent of its neighbors. For a track cell,

\[
f_i\le -64+|b_i|+\sum_j|J_{ij}|\le-39<-10.
\]

The corresponding bounds are `-124<-40` for an auxiliary and `-62<-13` for a memory. Thus reset has a unique final all-minus state, independent of avalanche order or the old data word.

Now apply these fixed levels, letting each event settle:

| Command | End level | Exact critical event | Result |
|---|---:|---:|---|
| prepare | -10 | -13 | Odd track cells `q_3,q_5,...` become plus; `q_1` stays minus |
| align | 8 | 6 | `q_1` becomes plus, so all track cells equal `a_i` |
| temporary set | 15 | 13 | All memories become plus |
| arm | 24 | 22 | All auxiliaries become plus, reversing the track's staggered preference |
| nucleate | -10 | -6 | `q_1` becomes minus |
| erase | -16 | -13 | All memories become minus |

Every switching group in this table consists of mutually uncoupled cells. Their transitions therefore commute. For example, at the auxiliary event `H=22`, every auxiliary has force `2H-4=40`. For any partial set of switched auxiliaries, an even track cell remains minus: its worst force is `22+4-20+1=7<10`. At the final arm level 24 this force is nine, leaving margin one. No transient avalanche can advance that track cell while the auxiliary group switches.

At the end of preparation, the canonical start state is

\[
q_1=-1,\quad q_i=a_i\;(i\ge2),\quad z_i=+1,\quad m_j=-1.
\]

The track has one `--` domain wall. The auxiliary layer is essential in this particular construction: without it, a simple staggered antiferromagnetic counter favors its final phase and does not provide this repeatable global preparation operation.

## Writing by spatial induction

Before writing bit `i`, maintain the invariant

\[
q_j=-a_j\quad(j\le2i-1),\qquad
q_j=a_j\quad(j\ge2i),\qquad z_j=+1,
\]

with memories before `i` equal to their requested bits and all remaining memories minus.

1. **Position at H=10.** The next track cell `q_(2i)` has force `H+4-1=H+3` because its track-neighbor forces cancel and its unwritten memory is minus. It switches up at `H=7`. The wall is now `++` at the memory pair `(q_(2i),q_(2i+1))`. No other memory pair is parallel. At the endpoint, the selected memory has force `10+2=12<13` and therefore does not write automatically.

2. **Optional write at H=12.** For a requested one, increase the same scalar field to 12. The selected memory crosses its threshold at `H=11`, since its force is `H+2`. Every unselected memory has force `H` and cannot switch: `12<13`. A requested zero omits this overshoot. The memory's reciprocal force change on the adjacent track cells is at most two; the track inequalities remain strict.

3. **Advance at H=-10.** The next track cell `q_(2i+1)` has force `H-4+m_i`. It switches down at `H=-5` if the memory is minus or `H=-7` if plus. The preceding cell `q_(2i)` cannot switch backward: at these events its force is `-2`, leaving stability margin eight. The selected output's coupling returns to zero and it holds its stored sign.

This restores the invariant with `i` replaced by `i+1`. The initial canonical start supplies the base case. After all `N` bits, return `H` to zero. All outputs retain the target word, the track equals `-a_i`, and all auxiliaries remain plus. The same reset sequence can now rewrite the array.

The following minima are obtained directly by substituting the local force formulas, taking every unknown old memory as either sign and every intended moving coordinate throughout `[-1,1]`:

| Event | Minimum wrong-cell margin at critical field | Minimum endpoint margin | Field overshoot beyond intended event |
|---|---:|---:|---:|
| prepare | 8 | 16 | 3 |
| align | 7 | 5 | 2 |
| temporary set | 18 | 14 | 2 |
| arm | 3 | 1 | 2 |
| nucleate | 7 | 3 | 4 |
| erase | 10 | 4 | 3 |
| position | 4 | 1 | 3 |
| write | 2 | 1 | 1 |
| advance | 6 | 3 | at least 3 |

For instance, the write-event minimum two is the unwritten unselected memory's margin `13-11`. The position-event minimum four is the selected memory's margin `13-(7+2)`. Farther cells have only the two alternating bulk environments; boundary cells have the fixed reference forces already included. Thus the table contains all local environments for arbitrary `N`. The all-`N` conclusion follows from the local inequalities and induction, not from extrapolating a small-array simulation.

## Constant deterministic tolerance

The finite margins imply a nonzero coefficient and command tolerance independent of array length, on the declared bounded-degree graph. For example, let each `c,g,b`, existing edge coefficient, and commanded field have absolute error at most `epsilon=0.001`. At any command endpoint, the total margin error is at most

\[
(1+64+1+4+2)\epsilon+\epsilon^2
=0.072001<0.1.
\]

Critical-field shifts are also bounded independently of `N`, since `g>=1-epsilon`. Using the conservative coefficient-only bound `70epsilon/(1-epsilon)<0.071`, an event's wrong-cell margin remains greater than `2-0.1-2.001(0.071)>1.75`. Targets remain reached before their fixed endpoint levels. This tolerance concerns bounded deterministic errors in the specified local forces. It does not permit an extensive sum of unbudgeted long-range cross-talk, arbitrary bit flips, thermal global-success claims, or an unacquired uniform drive bus.

## Complete ideal-cycle work

All completed words at `H=0` have the same energy, `-28N-4`; the memory terms cancel because each memory couples to an antiparallel track pair. Let `p_old` and `p_new` be the numbers of ones in the old and new words.

The full rewrite flips `4N+2` track cells, `4N+2` auxiliaries, and `2N+p_old+p_new` memories. A quasistatic uncoupled threshold flip dissipates `2c_i`. Hence

\[
\#\mathrm{flips}=10N+4+p_{old}+p_{new},
\]

\[
W_{net}=D_{hyst}
=452N+200+26(p_{old}+p_{new}).
\]

This includes resetting the old word, temporary setting and erasing every memory, and arming/resetting the auxiliaries. It is ideal net work with reactive energy recovery. It is not actuator or wall-plug energy.

For the explicit source work convention `dW=-sum(g_i s_i)dH`, the positive part without recovery is not linear. In the zero-overshoot limit,

\[
W_+(0^N\to1^N)=88N^2+856N+348,
\]

\[
W_+(1^N\to0^N)=60N^2+850N+348.
\]

Source balancing, field-storage choices and energy recovery change this positive-part accounting and must be specified physically. The net formula alone cannot establish cheap large-array programming.

## Exact checks and scope of verification

`network.py` integrates quasistatic relay events using rational arithmetic and checks reciprocal energy decrease and the work balance. `check_construction.py` checks all 126 target words for `N<=6`; 252 old/new/order cases for `N<=3`, using three event relaxation orders; and 154 local continuous-transition certificates. Resource traces extend to `N=32`. Every stored test passes. A tiny rational field overshoot `1e-9` resolves the exact marginal event; its additional dissipation is retained, equal on a canonical rewrite to `2e-9(14N+6+p_old+p_new)`.

One certificate helper initially left the last advanced track cell in the old phase. The direct lifecycle tests had passed; correcting that prefix encoding made the independent local certificates agree. This was a verification implementation error, not a discarded failed material example.

The model theorem supplies the precise local contract used in the parent [finite-compliance continuation](/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/parent/SOFT_STOP_EMBEDDING.md). That companion adds ten event holds, uses nineteen field levels, and replaces stops by a finite `C3` soft potential. Its arithmetic and local continuation inequalities were checked independently here. The hard-stop work figures above do not transfer to that different dynamics. Neither model acquires a manufactured structure, spatially uniform global driver, loaded useful output, or finite-temperature global fidelity.
