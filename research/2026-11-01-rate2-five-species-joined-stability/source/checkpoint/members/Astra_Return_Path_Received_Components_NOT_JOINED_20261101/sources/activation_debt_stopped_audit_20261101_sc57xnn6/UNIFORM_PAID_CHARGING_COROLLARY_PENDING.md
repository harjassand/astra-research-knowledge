# Uniform paid charging from the stopped debt theorem

Status: conditional corollary of the pending cutoff-two debt theorem, not a global return or stability result. It uses that theorem at r=1; this endpoint must be included in its received scope.

Let N>=1 be the initial population and sigma the first time tau<2 (sigma=0 if already there). The full actual rate2 process has unit-rate immigration, and the proposed stopped theorem gives

 E exp(3 sigma/20) <= exp(tau(x)) [1+20 A²/(B+1)].

Since tau<=(3N/200)^(1/3)<N^(1/3)/4 and A²/(B+1)<=N², the right side is at most exp(7N^(1/3)). Indeed log(1+20N²)<=log21+2log N, log N<=3(N^(1/3)-1), and log21<6. Markov's inequality therefore proves the uniform actual-time bound

 P_x(sigma>100 N^(1/3)) <= exp(-8 N^(1/3)).

This holds from every integer state, not only the balanced corner, provided the cutoff-two source theorem is correct. It retains all reactions and no resets. The constants are conservative, not physical performance estimates. This route is slower than the candidate N^(1/5) activation law but its uniformity is directly useful.

For N>=3000, 100N^(1/3)<=N/2. Poisson domination and the elementary Chernoff bound then give

 P_x(N(X_sigma)>2N, sigma<=100N^(1/3)) <= exp[-(log2-1/2)N] < exp(-N/6).

No independence is required: event inclusion into the single immigration tail suffices. Thus the actual exit is reached within paid time with controlled total population, except for the stated exponentially small events. The state at exit is NOT prepared afresh.

What the exit supplies is algebraic, not an assumed service: with c=A+C,d=A+D,Z=B-A+E, tau<2 implies

 (1/100)Z < E+4cd+4(c+d)+16/3

whenever the positive root exists; when H<=0, the same inequality follows from E>=(1/100)Z. Hence either stored E or a catalytic product/linear reserve is present relative to B. This does not yet imply macroscopic A occupation or actual removal. The missing receiving construction must cover all such exit states, including highly unbalanced C,D, continuing reactions, and repeat crossings.

This corollary cannot on its own be inserted into the sampled population-contraction consumer: that consumer requires a population REDUCTION block, whereas the present operation only discharges activation debt and permits a controlled increase in total population.
