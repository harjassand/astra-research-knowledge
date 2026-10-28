# Exact same-count ordering witness for the six-state source

28 October 2026. Two positive reciprocal substochastic operators have
observably different length-20 programs with ten uses of each operator.
The source construction and witness are exact. A separate direct-execution
comparator demonstrates that deciding this one pair is inexpensive relative
to a large reusable model acquisition.

## Source and physical port

In boundary/hidden coordinates, define

\[
A_i=\begin{pmatrix}B_i& I_3/500\\ I_3/500&C\end{pmatrix},
\qquad C=\operatorname{diag}(1/4,1/3,2/5),
\]

\[
B_0=\begin{pmatrix}4/5&9/50&0\\9/50&79/100&1/100\\0&1/100&97/100\end{pmatrix},
\quad
B_1=\begin{pmatrix}97/100&0&1/100\\0&4/5&9/50\\1/100&9/50&79/100\end{pmatrix}.
\]

These equal the specified I-(1/5)L_i boundary blocks. The hidden diagonal
is shared between modes. All entries are nonnegative, both matrices are
symmetric, and every diagonal strictly exceeds its off-diagonal row sum.
Gershgorin therefore proves positivity. The maximum row sum is 491/500,
so ||A_i||<=491/500<99/100. Complete each row with a transition to an
absorbing cemetery to obtain the physical killed Markov process.

Prepare boundary state b=e_0 and read only the final predicate X=b.
The scalar word convention is chronological:
f(i_1...i_H)=b^T A_(i_H)...A_(i_1)b.
No hidden-state identity is needed by the direct observer.

## Rationally checked programs

The high program is 00000000001111111111, or ten zeros followed by ten ones.
The low program is 00101101011010110100. Both have length 20 and counts
(10,10). Their exact returns are

\[
f_{\rm high}=
\frac{52512750620844476898897977567705050478121709842232972738897}
{168940544128417968750000000000000000000000000000000000000000},
\]

\[
f_{\rm low}=
\frac{62667871131866112226315557602078382107444310275485929869933}
{253410816192626953125000000000000000000000000000000000000000}.
\]

Their difference is

\[
\frac{1288100383952048249762512699958335488779060359029082339073}
{20272865295410156250000000000000000000000000000000000000000}
>63/1000.
\]

Numerically the returns are .31083569010484297 and .2472975387294832,
with difference .06353815137535977. The proof is the finite rational
recurrence v_0=e_0, v_j=A_(i_j)v_(j-1), recorded and asserted by
check_multiboundary_order.py.

An exhaustive floating-point screen of all 184,756 length-20 words with
these counts selected the pair. Global optimality is not certified.
Reversal of either entire program has exactly the same scalar response,
by reciprocity. In particular, reversing the two large blocks would not
have supplied an order witness.

## Main transport witness

For initial boundary 0 and terminal boundary 2, the same-count words
0^10 1^10 and 1^10 0^10 give .17891663822251888 and .058450345371997975.
Their exactly checked difference is
293063631311525000822746197821825973244864764966329154091 /
2432743835449218750000000000000000000000000000000000000000,
which exceeds .12. Both exact probabilities are preserved in the result.
Reciprocity swaps initial and terminal ports when reversing a word;
it does not equate these two fixed 0-to-2 experiments.

The direct comparator below concerns the original return pair. The
physical branch separately executed the 0-to-2 direct comparator.
These distinct costs must not be silently reassigned between the tasks.

## Executed equally observed direct comparator for the return pair

The checker executed 10,000 independent trajectories for each word with
integer-random transition probabilities of denominator 1500. The observer
received only final membership bits. It obtained 3051 and 2405 returns.

For each count X in N trials, enclosing rational square roots form

\[
p_L=\max(0,[X-\sqrt{20X}]/N),\quad
p_U=\min(1,[X+10+\sqrt{100+20X}]/N).
\]

The four confidence tails have total failure probability at most
4 exp(-10)<0.001. The observed intervals certify
f_high-f_low>=.01694327497961317>0. This is a data-based ordering
certificate, not an oracle assertion of the hidden matrices.

The complete charge is 20,000 logical trials, 400,000 primitive steps,
and 20,000 endpoint membership readings. A known b endpoint starts the
next trial without a physical reset. Restoring b after outside endpoints
and including initial preparation gives at most 14,546 preparations.
The software's knowledge of cemetery and other hidden states is private
to the transition simulator and is not used to shorten a trajectory.

This budget is sufficient for this executed comparison; it is not an
optimality or lower-bound claim. The reusable compiler must earn its
cost across many future programs, or at a more demanding precision or
execution horizon. This one order decision does not justify an expensive
acquisition by itself.

Files: MULTIBOUNDARY_SEARCH.json records the floating screen;
MULTIBOUNDARY_ORDER_RESULTS.json records the exact witness, observed
counts, rational confidence intervals and full cost.
