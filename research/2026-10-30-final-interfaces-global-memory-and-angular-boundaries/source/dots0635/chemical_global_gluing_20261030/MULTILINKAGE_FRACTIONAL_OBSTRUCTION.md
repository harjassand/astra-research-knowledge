# The single-linkage hypothesis in the new bulk certificate is substantive

Internal exact calculation; no recurrence counterexample.

Consider the weakly reversible network

    2A --100--> A+B --1-->2A,
    0 <--> A, 0 <--> B (all four rates1).

The first linkage conserves total population and is quadratic. The second is lower-order and gives a full-rank unbounded communicating class. For mu_alpha=(A!B!)^(−alpha), alpha∈(0,1), along A~c n,B~n the leading quadratic adjoint coefficient is

    F_alpha(c)=100 c^(2−alpha)+c^(1+alpha)−100c²−c.

F_alpha(1)=0 and F_alpha'(1)=−99alpha<0. Therefore for every fixed alpha>0 there exists c<1 sufficiently close to1 with F_alpha(c)>0. All exact factorial errors and the inflow/outflow linkage terms are lower-order than n². Hence L*mu_alpha>0 on an infinite interior ray.

Thus choosing alpha smaller does not extend the unweighted fractional-factorial bulk certificate to arbitrary multiple linkages. A fast closed linkage can create positive adjoint divergence while the genuinely confining linkage acts at lower order. This network itself is positive recurrent: the fast reaction preserves A+B and the slow network has total-population drift2−(A+B).

A fixed fugacity correction can repair this particular fast reversible linkage, so this example does not rule out a general corrected measure. Its purpose is to prevent importing the single-linkage proper-support contraction into a case where an entire fast linkage has no killing.
