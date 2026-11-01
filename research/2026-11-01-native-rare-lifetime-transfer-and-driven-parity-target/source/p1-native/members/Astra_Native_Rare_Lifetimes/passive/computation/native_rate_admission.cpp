// Native unmarked n=4 fixture: all observable aggregate local rate cells.
// Simulation provider knows Q; receiver receives only (holding time, x, y).
// No resets, clamps, failed proposals, channel labels, or stationary start.
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <vector>

struct Cell {
    int mask, context_mask, context_value;
    double reference_rate;
    long double exposure = 0;
    uint64_t count = 0;
};

int main(int argc, char** argv) {
    if (argc != 2) throw std::runtime_error("usage: native_rate_admission output_file");
    constexpr int n = 4, states = 1 << n;
    constexpr long double quota = 100000;
    constexpr double mismatch = 0.003;
    std::array<std::array<double, states>, states> q0{}, q{};
    const double alpha[] = {0.6, 0.8, 0.7};
    const int fwd[] = {1, 3, 2, 0}, inv[] = {3, 0, 2, 1};
    for (int x = 0; x < states; ++x) {
        for (int i = 0; i < n; ++i) q0[x][x ^ (1 << i)] += 0.5;
        for (int i = 0; i < n - 1; ++i) {
            int code = (x >> i) & 3;
            int next = (i % 2 == 0 ? fwd : inv)[code];
            if (code != next) q0[x][x ^ ((code ^ next) << i)] += alpha[i];
        }
    }
    std::vector<Cell> cells;
    std::array<std::vector<int>, states> active;
    std::array<std::array<int, states>, states> cell_of_jump{};
    for (auto& row : cell_of_jump) row.fill(-1);
    for (int x = 0; x < states; ++x) {
        for (int y = 0; y < states; ++y) {
            if (q0[x][y] == 0) continue;
            int mask = x ^ y;
            int i = __builtin_ctz(static_cast<unsigned>(mask));
            int width = (__builtin_popcount(static_cast<unsigned>(mask)) == 1 ? 1 : 2);
            int context_mask = 0;
            for (int j = std::max(0, i - 1); j < std::min(n, i + width + 1); ++j)
                context_mask |= 1 << j;
            int val = x & context_mask;
            int index = -1;
            for (int k = 0; k < static_cast<int>(cells.size()); ++k) {
                const Cell& z = cells[k];
                if (z.mask == mask && z.context_mask == context_mask && z.context_value == val) {
                    index = k;
                    if (std::abs(z.reference_rate - q0[x][y]) > 1e-13)
                        throw std::runtime_error("reference cell is not constant");
                    break;
                }
            }
            if (index < 0) {
                index = cells.size();
                cells.push_back(Cell{mask, context_mask, val, q0[x][y]});
            }
            active[x].push_back(index);
            cell_of_jump[x][y] = index;
            int sign = ((__builtin_popcount(static_cast<unsigned>(val)) + i) % 2 == 0 ? 1 : -1);
            q[x][y] = q0[x][y] * (1 + mismatch * sign);
        }
    }
    if (cells.size() != 32) throw std::runtime_error("unexpected cell inventory");
    // The provider precomputes jump totals, without exposing them to receiver.
    std::array<double, states> total{};
    for (int x = 0; x < states; ++x)
        for (int y = 0; y < states; ++y) total[x] += q[x][y];
    std::mt19937_64 gen(720411831);
    auto uniform = [&]() {
        return (static_cast<long double>(gen()) + 0.5L) / 18446744073709551616.0L;
    };
    int x = 0; // Deliberately deterministic, no burn-in needed for coverage.
    int unfinished = cells.size();
    uint64_t jumps = 0;
    long double elapsed = 0;
    while (unfinished) {
        // Provider emits next actual holding time and destination, no nulls.
        long double holding = -std::log(uniform()) / total[x];
        long double cutoff = uniform() * total[x];
        int y = states - 1;
        for (int j = 0; j < states; ++j) {
            cutoff -= q[x][j];
            if (cutoff < 0) { y = j; break; }
        }
        if (cell_of_jump[x][y] < 0) throw std::runtime_error("invalid native jump");

        // Receiver integrates every active context over the holding interval.
        long double last_quota_offset = 0;
        bool chosen_still_active_at_jump = cells[cell_of_jump[x][y]].exposure + holding < quota;
        for (int k : active[x]) {
            Cell& z = cells[k];
            if (z.exposure >= quota) continue;
            long double remaining = quota - z.exposure;
            if (holding >= remaining) {
                z.exposure = quota;
                --unfinished;
                last_quota_offset = std::max(last_quota_offset, remaining);
            } else z.exposure += holding;
        }
        if (!unfinished) {
            elapsed += last_quota_offset;
            break;
        }
        elapsed += holding;
        if (chosen_still_active_at_jump) ++cells[cell_of_jump[x][y]].count;
        ++jumps;
        x = y;
    }
    std::ofstream out(argv[1]);
    out << std::setprecision(21);
    out << "{\n  \"n\":4,\n  \"seed\":720411831,\n  \"quota\":" << quota
        << ",\n  \"actual_relative_rate_error\":" << mismatch
        << ",\n  \"native_elapsed_time\":" << elapsed
        << ",\n  \"native_jumps\":" << jumps << ",\n  \"cells\":[\n";
    for (size_t k = 0; k < cells.size(); ++k) {
        const Cell& z = cells[k];
        out << "    {\"mask\":" << z.mask << ",\"context_mask\":" << z.context_mask
            << ",\"context_value\":" << z.context_value << ",\"reference_rate\":"
            << z.reference_rate << ",\"exposure\":" << z.exposure << ",\"count\":" << z.count
            << "}" << (k + 1 == cells.size() ? "\n" : ",\n");
    }
    out << "  ]\n}\n";
    std::cout << "cells=" << cells.size() << " jumps=" << jumps
              << " elapsed=" << static_cast<double>(elapsed) << '\n';
}
