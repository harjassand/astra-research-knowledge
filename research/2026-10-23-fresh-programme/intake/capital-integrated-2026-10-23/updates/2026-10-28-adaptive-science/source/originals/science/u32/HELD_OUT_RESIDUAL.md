# Tested held-out observable-residual alternative

The square-gauge theorem bounds uncertainty by separately bounding H and H_z.
This experiment instead validates the fitted operator's observable residual
on an independent block. It is an ordinary statistical-design alternative;
the matched full-data interval method was better in the executed comparison.

For each of seven legal settings, a fresh acquisition generated 500,000
independent reset episodes. Before this data was generated the algorithm,
seven-candidate gauge grid, split sizes and confidence pool were fixed in
residual_validation.py. A seeded multivariate-hypergeometric split selects
100,000 pilot and 400,000 validation shots per setting. Unconditionally this
is the same law as two independent multinomial batches, by exchangeability
of the underlying independent shots. The split does not create new shots.

The pilot determines S and fitted What_z. Conditional on the pilot, these
coefficients are fixed and the validation settings are independent. Each
entry of the true residual

    R_z=(H S) What_z-H_z S

is a known linear combination of probabilities of legal events. Group all
terms drawn from the same setting before computing an error bar: if that
setting's per-shot statistic has range length b_s and n_s validation shots,
Hoeffding gives

    Pr(|Rhat-R|>w | pilot)
       <=2 exp[-2w^2/(sum_s b_s^2/n_s)].

This retains exact cancellations and correlations within a count table.
The code uses a rational upward square root satisfying
w^2>=(11/2)sum_s b_s^2/n_s. It also certifies H's inverse using two
validation event intervals with w_H^2>=11/(2n). There are
K=2+7*16=114 covered events/contrasts, so return-and-invalid probability is
at most 228 exp(-11), approximately 0.00380799. This probability statement
is unconditional over acquisition and the split; conditioning on the
algorithm returning PASS would require an additional calculation.

If |(H S)^{-1}|<=M and |Rhat-R|<=D_R, then

    |What_z-W_z| <= M [|Rhat_z|+D_R,z].

The usual positive lower margin and stochastic-column checks therefore
give the same full-law deployment guarantee. The check is exact rational
arithmetic. No plant module or first-experiment counts are imported by the
residual learner.

The fresh data cost 3,500,000 resets and 7,000,000 native interventions.
The selected s=1/4 has positive lower margin approximately 0.0141393,
local TV bound approximately 0.0341673, and clocked-operation bound
approximately 0.0487524 at delta=0.4.

On the SAME fresh counts, the full-data method, with exact rational
width 303/100000 and failure bound 36 exp(-9.1809), approximately
0.00370756, gives local TV approximately 0.0283408 and operation TV
approximately 0.0407777. Thus the held-out residual alternative is weaker
here, even though grouping shared statistics is analytically valid. Its
pilot estimation cost outweighed its contrast benefit. No improvement is
claimed. The source quotient-norm calculation on these same counts has
e approximately 0.862595, violating gamma e<delta for delta=0.4.

Both count experiments together used 10,500,000 synthetic reset episodes
and 21,000,000 native interventions. The old source's count fixture was
read as frozen existing data and was not reacquired. Replaying generation
with the same seed only verifies the stored integer tables; it is not a
claim of additional independent data or laboratory throughput.
