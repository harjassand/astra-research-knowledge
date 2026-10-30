# Final exact-version receipt

2026-10-30 00:33 UTC. The integrated review applies to:

- Circuit: `16800ef773d2d3d07d6b94aad92b0d12f83177b3e207dfe88852fc58ab638080`
- Integer-energy D0/D1: `ee20086606b7263403232a386e7daedbd68bbc67cdc2506c08cc68d74262c9f1`
- Unary-energy lift: `ccc4cc644ccc9923fe64e3cd336a12414847d015baeef78b2c6d11058e418995`
- Reset-budget scope: `d3dad9650d13f6e362c63248a8c1a088bcb39e3866b0b10618a2a504becb818f`
- Status index: `469a37333cd645dfb72a76ea8528d494f819eba80ddebd84f5c03681aaf5bd8f`

Diff-verified final circuit changes explicitly preserve A-phase acquisition reversal and add the one-D0-root terminal GPT decoding argument. Earlier reviewed bytes and hashes are retained.

**Scoped PASS:** Tanner-specific interfaces for the ideal atomic continuous/common-bath route, ideal Poisson route, native grouped-qudit finite-rate Poisson route, and system-local onsite Markov-cushion corollary are discharged against their separately accepted theorem inputs. No blanket practical/native continuous-bath or noisy-retrieval claim is accepted. Detailed reasoning and imported-versus-discharged contract classification appear in `INDEPENDENT_REVIEW.md`.
