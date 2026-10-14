#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

// 8D nonseparable periodic semilinear elliptic point-query benchmark.
// Model and certificate are specified independently in REPORT.md/analyze.py.
// The only algorithm implemented here is the source's bounded tangent-resummed
// branching sampler. All arithmetic and random draws are ordinary floating point.

static constexpr int D = 8;
static constexpr int J = 16;
static constexpr double A_BOUND = 5.0/102.0 + 5.0/103.0;
static constexpr double V_UPPER = 1.0 + A_BOUND;
static constexpr double R_BOUND = 25.0 * (6.0*A_BOUND*A_BOUND + 4.0*A_BOUND*A_BOUND*A_BOUND
                                           + A_BOUND*A_BOUND*A_BOUND*A_BOUND);
static constexpr double LAMBDA_BAR = 1.0 + 100.0*V_UPPER*V_UPPER*V_UPPER;
static constexpr double B2 = 150.0*V_UPPER*V_UPPER;
static constexpr double B3 = 100.0*V_UPPER;
static constexpr double B4 = 25.0;
static constexpr double H = 1.0/40.0;
using Vec = std::array<double, D>;
using IVec = std::array<int, D>;

struct Model {
    std::array<IVec, J> k{};
    std::array<double, J> phase{};

    Model() {
        for (int i = 0; i < D; ++i) k[i][i] = 1;
        for (int i = 0; i < D; ++i) {
            k[D + i][i] = 1;
            k[D + i][(i + 1) % D] = 1;
        }
        for (int j = 0; j < J; ++j) {
            phase[j] = 0.17 * (j + 1) + 0.013 * (j + 1) * (j + 1);
        }
    }

    double g(const Vec& x) const {
        double s = 0.0;
        for (int j = 0; j < J; ++j) {
            double z = phase[j];
            for (int i = 0; i < D; ++i) z += k[j][i] * x[i];
            s += std::cos(z);
        }
        return s / J;
    }

    double e0(const Vec& x) const {
        double s = 0.0;
        for (int j = 0; j < J; ++j) {
            double z = phase[j];
            int norm2 = 0;
            for (int i = 0; i < D; ++i) {
                z += k[j][i] * x[i];
                norm2 += k[j][i] * k[j][i];
            }
            s += (10.0 / J) * std::cos(z) / (101.0 + norm2);
        }
        return s;
    }

    double v(const Vec& x) const { return 1.0 + e0(x); }
    double residual_from_v(double v) const {
        const double z = v - 1.0;
        return -25.0 * (6.0*z*z + 4.0*z*z*z + z*z*z*z);
    }
    double tangent(const Vec& x) const {
        const double w = v(x);
        return 1.0 + 100.0*w*w*w;
    }
};

struct Stats {
    std::uint64_t nodes = 0;
    std::uint64_t source_evals = 0;
    std::uint64_t max_nodes_sample = 0;
};

struct Sampler {
    const Model& m;
    std::mt19937_64 rng;
    std::uniform_real_distribution<double> unif{0.0, 1.0};
    std::normal_distribution<double> normal{0.0, 1.0};
    Stats stats;

    explicit Sampler(const Model& model, std::uint64_t seed) : m(model), rng(seed) {}

    Vec endpoint(const Vec& x) {
        const double tau = -std::log(unif(rng)) / LAMBDA_BAR;
        const double scale = std::sqrt(2.0 * tau);
        Vec y{};
        const double twopi = 2.0 * std::acos(-1.0);
        for (int i = 0; i < D; ++i) {
            double z = x[i] + scale * normal(rng);
            z = std::fmod(z, twopi);
            if (z < 0) z += twopi;
            y[i] = z;
        }
        return y;
    }

    double sample_z(const Vec& x, std::uint64_t& local_nodes) {
        const Vec y = endpoint(x);
        ++stats.nodes;
        ++local_nodes;
        const double vy = m.v(y);
        const double p0 = R_BOUND / (LAMBDA_BAR * H);
        const double p1 = 1.0 - (1.0 + 100.0*vy*vy*vy) / LAMBDA_BAR;
        const double p2 = 150.0*vy*vy * H / LAMBDA_BAR;
        const double p3 = 100.0*vy * H*H / LAMBDA_BAR;
        const double p4 = B4 * H*H*H / LAMBDA_BAR;
        const double t = unif(rng);
        if (t < p0) {
            ++stats.source_evals;
            return m.residual_from_v(vy) / R_BOUND;
        }
        double cut = p0 + p1;
        if (t < cut) return sample_z(y, local_nodes);
        cut += p2;
        if (t < cut) {
            const double a = sample_z(y, local_nodes);
            const double b = sample_z(y, local_nodes);
            return -(150.0*vy*vy/B2)*a*b;
        }
        cut += p3;
        if (t < cut) {
            const double a = sample_z(y, local_nodes);
            const double b = sample_z(y, local_nodes);
            const double c = sample_z(y, local_nodes);
            return -(100.0*vy/B3)*a*b*c;
        }
        cut += p4;
        if (t < cut) {
            const double a = sample_z(y, local_nodes);
            const double b = sample_z(y, local_nodes);
            const double c = sample_z(y, local_nodes);
            const double d = sample_z(y, local_nodes);
            return -(25.0/25.0)*a*b*c*d;
        }
        return 0.0;
    }

    double sample(const Vec& x) {
        std::uint64_t local = 0;
        const double z = sample_z(x, local);
        if (local > stats.max_nodes_sample) stats.max_nodes_sample = local;
        return H*z;
    }
};

struct RunResult {
    std::string label;
    std::uint64_t samples = 0;
    std::uint64_t nodes = 0;
    std::uint64_t source_evals = 0;
    std::uint64_t max_nodes_sample = 0;
    double estimate = 0.0;
    double correction_mean = 0.0;
    double correction_variance = 0.0;
    double seconds = 0.0;
};

RunResult run(const Model& model, const Vec& x, std::uint64_t n,
              std::uint64_t seed, const std::string& label) {
    Sampler sampler(model, seed);
    double sum = 0.0, sum2 = 0.0;
    const auto t0 = std::chrono::steady_clock::now();
    for (std::uint64_t i = 0; i < n; ++i) {
        const double z = sampler.sample(x);
        sum += z;
        sum2 += z*z;
    }
    const auto t1 = std::chrono::steady_clock::now();
    const double mean = sum / n;
    RunResult out;
    out.label = label;
    out.samples = n;
    out.nodes = sampler.stats.nodes;
    out.source_evals = sampler.stats.source_evals;
    out.max_nodes_sample = sampler.stats.max_nodes_sample;
    out.correction_mean = mean;
    out.correction_variance = (sum2 - n*mean*mean) / (n-1);
    out.estimate = model.v(x) + mean;
    out.seconds = std::chrono::duration<double>(t1-t0).count();
    return out;
}

int main(int argc, char** argv) {
    std::uint64_t diagnostic_n = 100000;
    if (argc > 1) diagnostic_n = std::strtoull(argv[1], nullptr, 10);
    Model model;
    Vec x{};
    for (int i = 0; i < D; ++i) x[i] = 0.21 + 0.19*i;
    const auto certified = run(model, x, 47, 2026101401ULL, "certified_95pct_epsilon_0.01");
    const auto diagnostic = run(model, x, diagnostic_n, 2026101402ULL, "diagnostic_large_run");
    const int timing_repeats = 1000;
    std::uint64_t timing_nodes = 0;
    const auto timing_start = std::chrono::steady_clock::now();
    for (int rep = 0; rep < timing_repeats; ++rep) {
        Sampler sampler(model, 2026200000ULL + rep);
        for (int i = 0; i < 47; ++i) sampler.sample(x);
        timing_nodes += sampler.stats.nodes;
    }
    const auto timing_stop = std::chrono::steady_clock::now();
    const double timed_seconds = std::chrono::duration<double>(timing_stop-timing_start).count();
    std::cout << std::setprecision(17);
    std::cout << "{\n  \"dimension\": 8,\n  \"modes\": 16,\n  \"query\": [";
    for (int i = 0; i < D; ++i) std::cout << (i ? ", " : "") << x[i];
    std::cout << "],\n  \"runs\": [\n";
    const RunResult* arr[2] = {&certified, &diagnostic};
    for (int j = 0; j < 2; ++j) {
        const auto& a = *arr[j];
        std::cout << "    {\"label\": \"" << a.label << "\", \"samples\": " << a.samples
                  << ", \"nodes\": " << a.nodes << ", \"source_evals\": " << a.source_evals
                  << ", \"max_nodes_sample\": " << a.max_nodes_sample
                  << ", \"predictor_at_query\": " << model.v(x)
                  << ", \"estimate\": " << a.estimate
                  << ", \"correction_mean\": " << a.correction_mean
                  << ", \"correction_sample_variance\": " << a.correction_variance
                  << ", \"seconds\": " << a.seconds << "}"
                  << (j == 0 ? ",\n" : "\n");
    }
    std::cout << "  ],\n  \"timing_1000_certified_queries\": {\"queries\": " << timing_repeats
              << ", \"nodes\": " << timing_nodes << ", \"seconds\": " << timed_seconds
              << ", \"seconds_per_query\": " << timed_seconds/timing_repeats << "}\n}\n";
}
