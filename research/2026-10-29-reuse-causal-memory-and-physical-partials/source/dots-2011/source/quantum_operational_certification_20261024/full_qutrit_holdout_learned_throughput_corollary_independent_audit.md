# Independent learned-throughput certificate audit

27 October2026. PASS, local post-cutoff.

The upper deviation of m/N is a binomial upper tail at the largest integer time strictly below m/[a(1+epsilon)], whose mean is at most m/(1+epsilon). Its Chernoff exponent log(1+epsilon)-epsilon/(1+epsilon) is at least epsilon^2/[2(1+epsilon)^2], hence at least epsilon^2/4 for epsilon<=1/8. For the lower deviation, N>m/[a(1-epsilon)] implies fewer than m successes by floor of that time. Its mean is at least m/(1-epsilon)-1, at least m(1+epsilon/2) when m epsilon>=2. The lower-tail exponent is at least m epsilon^2/[8(1+epsilon/2)]>=m epsilon^2/16. Thus the stated two-tail bound includes rounding correctly. Capping only restricts certificates; it does not create a conditional confidence assertion.

With m>=9216L/nu^2 and epsilon=nu/8, m epsilon^2/16>=9L. Union with the original verifier at accuracy nu/2 and confidence beta/2 yields simultaneous confidence at least1-beta. The erasure-reference channels have exact diamond distance2|a-ahat|. Triangle inequality gives3nu a/4, and ahat>=(1-nu/8)a implies the displayed6nu ahat/7 bound. ahat=m/N lies in[0,1], so it specifies a valid fully known reference channel. It does not equal a hidden nominal p.

Training at nu/16 invokes the separately received probability bridge at targetnu/2 and meets the stricter mismatch thresholdnu^2/6144. Confidence and all actual-throughput/deterministic-cap distinctions remain valid; no additional source calls or entangled holdout are introduced.
