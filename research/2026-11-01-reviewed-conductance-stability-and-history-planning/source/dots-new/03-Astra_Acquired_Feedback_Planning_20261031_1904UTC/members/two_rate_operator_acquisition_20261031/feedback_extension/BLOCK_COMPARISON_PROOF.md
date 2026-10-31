# Polynomial sufficient residual geometry, actually acquired

Separate unreviewed extension, not in the accepted routing-certificate ZIP.
The inequality below is the standard block-norm comparison/small-gain
argument, not a new principle of matrix analysis. Its role is to replace
explicit m^r policy norm acquisition by paid local observation-derived checks.

Let F_a=Q C_a Q and decompose vectors by acquired blocks. For each source
block g and target block h, acquire a simultaneous upper bound

    u_gh >= max_a ||Q_g C_a[g,h] Q_h||_2,
    Q_g=I_g−1_g 1_g^T/|g|.

The nonnegative r-by-r comparison matrix U=(u_gh) is learned from the data;
its entries or a useful spectral bound are not supplied. For any policy pi
selecting one action per output/source block and any vector x,

    ||(Q C_pi Q x)_g||_2 <= sum_h u_gh ||x_h||_2.

Taking the Euclidean norm of these block norms proves

    max_pi ||Q C_pi Q||_2 <= ||U||_2.

Acquire/check ||U||_2 with an exact small-dimensional PSD norm test. Together
with the simultaneous full-matrix observation event, the true family bound is

    alpha_feedback <= ||U||_2 + sqrt(m)*t.

This can fail even if all actual policies contract: blockwise absolute norms
discard cancellation and alignment. Thus it is a sufficient tractable
certificate, not an algorithm for optimal switched-norm recognition and not
a refutation of the earlier scoped hard certification language.

For unequal block sizes, the executable embeds each rectangular observed
block as the upper-right block of a zero square matrix on |g|+|h| coordinates.
The two-block projection acts by Q_g and Q_h. Its norm is exactly the norm
of Q_g C_a[g,h] Q_h. The inherited count normalizer is corrected by the
known rational factor n*N_block/[(|g|+|h|)*N_coarse]. Zero observed blocks
have exact zero observed norm (their true uncertainty remains in t).

There are m r² local checks with failure delta/(8m r²) each, all using probes
fresh after data/partition selection. This replaces the old norm event in
the final certificate, rather than adding unbudgeted probability. Each
observed nonzero count appears in exactly one block per action, although
each local power iteration revisits it and projections/state work are extra.
The sparse multiply count is O(p*sum_a nnz(C_a)); local state/projection work
is O(p*m*n*r), and there are O(mr²) scalar norm admissions. This is polynomial
in acquired rank, but not free or necessarily cheap. Poor partitions or
large residual interactions may cause refusal.

All original observation acquisition remains paid. The experimental order
first constructed/enumerated m^r policies and then tested this improvement;
its cumulative work includes BOTH. A standalone polynomial-first algorithm
could try this check before a fallback, but that prospective lower ledger
must not be substituted for the measured cumulative experiment. Ordinary
model-reduction and reduced-MDP methods are entitled to the same U and data.

An exact stochastic counterexample to completeness is executed in
`check_comparison_failure.py`: the n=6 residual satisfies ||QAQ||<=15/16,
while a lower block-comparison matrix has squared norm at least
2881033435601/2748779069440 > 1. Thus this route can refuse even when a true
complement contraction exists. No statement about the example's other
leakage/task requirements is implied.
