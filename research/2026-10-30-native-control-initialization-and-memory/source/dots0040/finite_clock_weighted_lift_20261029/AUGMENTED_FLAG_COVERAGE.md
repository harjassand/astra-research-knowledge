# Weighted coverage after adding unary bad-flag tokens
2026-10-30. Extension of WEIGHTED_PROGRESS.md, conditional only on its original SSF container interface and the actual bad-reset charge.

Enlarge the check graph by R token vertices per bad flag C_h. Tokens at h are occupied iff C_h=1; all R copies have identical value. Join the entire local hub footprint and its tokens into a bounded clique, and enlarge the original fixed-radius containers J_C accordingly. Define error components using intersections of these enlarged single-data-vertex footprints. Distinct J_C remain disjoint; sizes and degrees increase by fixed constants. FGL syndrome confinement and active-hub counts concern DATA errors and are unchanged except for these geometric constants.

Let s_A be the number of occupied syndrome vertices in A and b_A the number of occupied token vertices. The augmented weight is
f_A=exp(a|A|) theta^{|A|-s_A-b_A}, a=c log(1/theta).
Assume the actual bad reset at h has positive decrement
D_h^bad >= c_bad C_h sum_{B connected, all R h-tokens subset B} f_B.
All inequalities are diagonal/operator inequalities in the commuting syndrome/flag algebra.

Choose eta in (0,1-c). Partition animals as follows.

1. TOTAL-SPARSE: s_A+b_A<eta|A|. Then f_A<=theta^{(1-c-eta)|A|}, so their weighted sum is <=C0N by bounded rooted animal counting.

2. FLAG-DENSE: b_A>=eta|A|/2. Let H_A be the set of bad hubs with at least one token in A. Then |H_A|>=eta|A|/(2R). Assign |A|f_A evenly to H_A. For each h complete B=A union {all R h-tokens}. It is connected since A already contains an h-token and the token bundle is a clique. Every added token is occupied, so f_B/f_A=exp(a|B\A|)>=1. At most 2^R source animals map to fixed h,B. Consequently
sum_flag-dense |A|f_A <= (2R*2^R/(eta c_bad)) sum_h D_h^bad.
No independence of token copies is used or required.

3. SYNDROME-DENSE REMAINDER: not sparse and not flag-dense, hence s_A>=eta|A|/2. Repeat the rich/poor proof from WEIGHTED_PROGRESS.md with density threshold eta/2, counting ONLY syndrome occupancy for active-hub mass. For rich animals, completing A by an active changed-check clique adds boundedly many vertices; worst-case token occupancy cannot worsen the universal ratio theta^{(1-c)k}. For poor components, the added occupied SYNDROME vertices are still at least alpha|J_C|, where alpha uses the enlarged container constant. Added occupied tokens only improve f_B/f_A. Thus choose c>1-alpha and tiny theta as before. The same one-component completion charge gives
sum_syndrome-dense |A|f_A <= C1 sum_h d_h,
where d_h=(I-Phi_h^*)V_ext includes the full augmented animal sum and Phi_h leaves the bad flags fixed. Strict per-move animal charging is unchanged by the spectator tokens.

Combining the cases yields
W_ext <= C1 sum_h d_h+C2 sum_h D_h^bad+C0N.
No FGL confinement statement is imposed on arbitrary bad-flag components. Flags are handled by their own local reset charge, and syndrome components retain the original confinement-based argument.

Parameter order: fix the finite token multiplicity R and enlarge geometry; obtain the modified container constants; choose c,eta,theta for those constants and the bad-reset charge. All resulting quantities are independent of volume, though potentially extremely poor.
