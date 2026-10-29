# Stronger ordinary empirical control when the teacher has full support

30 October 2026. T supplied this analytical control after the general wrapper
was frozen; root reconstructed it. No source or numerical instance was run.
This is ordinary pseudocount prediction, not a new Astra invention.

If Q has FULL SUPPORT, every prefix can be queried safely. At each node use one
memoized independent batch of m conditional samples, and the Laplace row
qhat_o=(X_o+1)/(m+O). This defines one lazy, consistent full-support teacher.
For a fixed true token probability q>0 and X~Binomial(m,q),

    E[1/(X+1)] = [1-(1-q)^(m+1)]/[(m+1)q].

Jensen therefore gives

    E log(q/qhat) <= log[(m+O)/(m+1)].

Using the exact KL identity and averaging over the fixed P prefix law,

    E_tree D(P||Qhat)
       <=D(P||Q)+T log[(m+O)/(m+1)].

This is a stronger ordinary KL adapter than our rare-edge/global-mixture bound
on the FULL-SUPPORT subclass. There is no minimum nonzero probability premise.
It does not pay the original positive-Q-only zero-support interface: sampling
a floor-created impossible prefix would be invalid there. The accepted support-
safe general wrapper remains valid at that larger domain, and is not refactored
after freezing. The substantive new learning interface is the asymmetric,
arbitrary-truth predictive-width acquisition; generic empirical simulation and
positivity bookkeeping remain credited ordinary machinery.
