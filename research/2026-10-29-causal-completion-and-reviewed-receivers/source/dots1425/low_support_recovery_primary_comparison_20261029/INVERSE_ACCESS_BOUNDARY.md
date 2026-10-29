# Fresh inverse-access boundary
2026-10-29. Source abstract checked; full proof not independently reviewed.

Arihara, Yoshida, Taranto and Murao, *An exponential query advantage from access to Stinespring dilation unitaries in quantum channel learning*, arXiv2609.40001v1 (30 September2026), https://arxiv.org/abs/2609.40001 .

The reported task is estimating optimal average gate fidelity to the set of unitary channels. For constant Kraus rank it separates black-box channel queries from dilation-unitary plus inverse queries: the abstract states an Omega(sqrt(d)) black-box lower bound and polylog(d) dilation/inverse upper bound at constant accuracy. It consequently rules out a universal efficient simulator for arbitrary algorithms using random dilation and inverse access.

This is not a lower bound against the present fixed-small-input, bounded-hidden-support decoder. It reinforces an interface distinction: the parallel random-dilation superchannel of2512.21260 is not automatically a reusable controlled/inverse oracle. Do not transfer a dilation/inverse algorithm without implementing or charging its actual access requirements.
