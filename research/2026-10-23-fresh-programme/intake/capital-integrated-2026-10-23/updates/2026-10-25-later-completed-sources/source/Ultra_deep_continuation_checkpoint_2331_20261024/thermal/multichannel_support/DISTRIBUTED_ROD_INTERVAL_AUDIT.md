# Distributed-rod interval arithmetic audit

Let \(N\ge12\) be a positive multiple of 12, \(0<\mu\le0.01\), and
\[
b_n=\frac{12\mu(N-n)}{N^2(N^2-1)},\qquad
I_n=\left[\frac\pi n+\frac{b_n}{\pi/n},
\frac\pi n+\frac{2b_n}{\pi/n}\right],
\quad \frac{2N}{3}\le n\le\frac{3N}{4}.
\]
The endpoints are integers by the divisibility condition.

The interval width is \(|I_n|=b_nn/\pi\). Since \(n\ge2N/3\) and
\(N-n\ge N/4\), each weighted width obeys
\[
n|I_n|=\frac{12\mu}{\pi N^2(N^2-1)}n^2(N-n)
\ge\frac{12\mu}{\pi N^2(N^2-1)}\frac{N^3}{9}.
\]
There are \(N/12+1\ge N/12\) indices, hence
\[
\sum_{n=2N/3}^{3N/4}n|I_n|
\ge\frac{\mu N^2}{108\pi(N^2-1)}\,N^2
\ge\frac{\mu}{9\pi}.
\]
Equivalently, the coarser sum estimate used here is
\(\sum n^2(N-n)\ge N^4/108\ge N^2(N^2-1)/108\).

For disjointness, the unshifted centers satisfy
\[
\frac\pi n-\frac\pi{n+1}=\frac\pi{n(n+1)}
\ge\frac{16\pi}{9N^2},
\]
because \(n+1\le3N/4\). On this index range \(k(N-k)\) decreases with \(k\), so
\[
\frac{2b_k}{\pi/k}
=\frac{24\mu k(N-k)}{\pi N^2(N^2-1)}
\le\frac{16\mu}{3\pi(N^2-1)}
\quad (2N/3\le k\le3N/4).
\]
The latter is strictly smaller than \(16\pi/(9N^2)\): the ratio is at most
\(3\mu N^2/[\pi^2(N^2-1)]<1\). Thus the upper endpoint of \(I_{n+1}\) lies
strictly below \(\pi/n\), which itself is no greater than the lower endpoint
of \(I_n\). Consecutive intervals are ordered and disjoint, so all the \(I_n\)
are pairwise disjoint.

Both \(\pi/n\) and \(n(N-n)\) decrease over this range. Therefore the largest
upper endpoint occurs at \(n=2N/3\), and
\[
\max_n\sup I_n
\le\frac{3\pi}{2N}+\frac{16\mu}{3\pi(N^2-1)}
\le\frac{3\pi}{2N}+\frac{3\mu}{N^2}.
\]
The last inequality follows from \(16N^2\le9\pi(N^2-1)\), valid for
\(N\ge12\). All three requested bounds hold with the stated constants.

## Explicit correction to the summed lower-bound display

The multiplication of the common coefficient by the summed bound is
\[
\frac{12\mu}{\pi N^2(N^2-1)}\cdot\frac{N^4}{108}
=\frac{\mu N^2}{9\pi(N^2-1)}
\ge\frac{\mu}{9\pi}.
\]
This is the correct intermediate expression for the lower bound above.
