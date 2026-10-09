"""Exact finite search for moment-syndrome collisions inside deletion balls.

For each n-bit word, compute M_r(x)=sum_{i:x_i=1} i^r (1-based positions),
then group it by its moment vector and all length-(n-k) subsequences.
A collision is two distinct words with the same tested moments and a shared
length-(n-k) subsequence. This is an exhaustive finite diagnostic only.
"""
from argparse import ArgumentParser
from itertools import combinations


def moments(word: str, degree: int) -> tuple[int, ...]:
    return tuple(
        sum((i + 1) ** r for i, bit in enumerate(word) if bit == "1")
        for r in range(degree + 1)
    )


def subsequences_after_k_deletions(word: str, k: int) -> set[str]:
    keep = len(word) - k
    return {"".join(word[i] for i in inds)
            for inds in combinations(range(len(word)), keep)}


def first_collision(n: int, k: int, degree: int):
    seen: dict[tuple[tuple[int, ...], str], str] = {}
    for value in range(1 << n):
        word = f"{value:0{n}b}"
        signature = moments(word, degree)
        for received in subsequences_after_k_deletions(word, k):
            key = signature, received
            previous = seen.get(key)
            if previous is not None and previous != word:
                return previous, word, received, signature
            seen[key] = word
    return None


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--k", type=int, default=2,
                        help="number of deletions from each codeword")
    parser.add_argument("--degree", type=int, default=2,
                        help="test all moments M_0 through M_degree")
    parser.add_argument("--max-n", type=int, default=8,
                        help="largest length to exhaust")
    args = parser.parse_args()
    for n in range(args.k + 1, args.max_n + 1):
        collision = first_collision(n, args.k, args.degree)
        if collision is not None:
            x, xp, y, sig = collision
            print(f"collision n={n}, k={args.k}, moments=0..{args.degree}")
            print(f"x={x}\nx'={xp}\ny={y}\nsignature={sig}")
            return
        print(f"no collision n={n}, k={args.k}, moments=0..{args.degree}")


if __name__ == "__main__":
    main()
