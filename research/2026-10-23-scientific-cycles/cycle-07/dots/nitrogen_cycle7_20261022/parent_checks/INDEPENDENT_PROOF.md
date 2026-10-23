# Principal-owner independent heat-path check

The reusable statement is conditional, not an observed exchanger. It changes the retrofit decision: existing cold-feed yield cannot be retained as evidence for a preheated-feed reactor, and the location of heat loss is decisive even if total energy rejection is large.

## 1. Nonuniform flow and a calorimetric acceptance threshold

For each conserved molecular species i, let e_i(T) be sensible enthalpy above the declared reference T0. Fix the total species rates, not a uniform temperature. Let dF_i(T) describe arbitrary nonnegative outgoing temperature distributions. Set Hs=sum integral e_i(T)dF_i, S(Td)=sum F_i e_i(Td), and A=sum integral max(e_i(T)-e_i(Td),0)dF_i. Then A>=Hs-S(Td) and A>=0, term by term. No Jensen approximation, common heat capacity, centerline-temperature identification or fitted mode temperature is required. With a verified steady, complete energy balance Hs=Wa-Hchem-L, a lower bound on Wa and upper bounds on Hchem, L and S give a sufficient available-duty bound.

This is sensible availability above Td, not an exergy bound and not delivered duty from a finite exchanger. For a sink at Tu with finite positive approach dT use Td=Tu+dT. Chemical evolution within the added device changes the fixed-species enthalpy construction; actual preservation must be identified. Treating every watt above Td as a free electrical watt is invalid.

The binary hypothesis is concrete: a measured loss bound or exit calorimetry can decide positive recoverable heat at a specified grade. In contrast, NOx yield and reported power do not locate the rejected energy. A completion that rejects it before the recovery port and a completion that carries it to that port satisfy the same total balance. These are energy-boundary countermodels, not validated replacements for the kinetic apparatus.

## 2. Exact interior-pinch counterexample

For countercurrent streams with strictly increasing enthalpy functions, any proposed duty Q must obey at every q in [0,Q]:
Th(Hh,in-q)-Tc(Hc,in+Q-q)>=dT.
The two terminal inequalities are necessary but not sufficient for variable heat capacities.

A fully explicit positive-capacity example uses arbitrary consistent heat units:
- Hot inlet600K, cold inlet300K, minimum approach20K.
- Hot heat-capacity rate:1 on300–400K,10 on400–500K,1 on500–600K.
- Cold heat-capacity rate:1 on300–500K,10 on500–600K.

Terminal limits permit Q=1000. At internal duty q=100 the hot stream is500K and cold stream570K, a temperature crossing. The true countercurrent maximum is280. Necessity follows at q=100: cold must be at most480K, whose cold enthalpy above300K is180; hence Q<=100+180=280. Sufficiency follows by checking the finite breakpoints of the piecewise-affine temperature gap: at q=0,80,100,280 its values are92,20,20,182K. Every intervening gap is affine and nonnegative above20K.

The exact-rational script verifies these claims, including arbitrarily small positive excess duties. This is a diagnostic/counterexample to a proposed two-end-only maximum, not an experimental heat-capacity model or proof by finite sampling of arbitrary functions. The general all-position criterion follows directly from local passive heat transfer.

Rejected implementation detail retained: v1 asserted the minimizer occurred uniquely at q=100. It first occurs at80 and is flat through100. Only that location assertion failed; the minimum20K, duty280 and physical conclusion were unchanged. The original script is preserved and is not a receiving entrypoint.

## 3. The unchanged-port trap

At the reactor interface, keeping both inlet streams' mass, composition, pressure and enthalpy unchanged fixes incoming enthalpy. An external recuperator cannot both increase that enthalpy and leave it unchanged. If a recooler restores the original inlet state, its rejected heat equals the preheat credit absent another explicit work/heat export. A periodic unreset storage transient cannot pay this balance. This retires only the free-feed-preheat retrofit while inheriting the cold-feed performance; it does not forbid external useful-heat export, a new preheated-feed operating point, staged recovery or heat-to-work assistance.

At matched final chemical product, pressure and temperature, formation enthalpy is the same in both configurations. More absorbed input can leave more recoverable heat. Both ordinary and split flow must receive the same heat-use opportunity and the same real demand. The next scientific comparison cannot credit all split-flow rejected heat while denying the ordinary reactor its rejection stream.
