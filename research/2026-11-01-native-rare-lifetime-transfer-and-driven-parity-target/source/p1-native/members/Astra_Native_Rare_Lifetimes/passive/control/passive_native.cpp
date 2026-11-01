#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <set>
#include <random>
#include <stdexcept>
#include <tuple>
#include <vector>

// Diagnostic native source. The observer below receives NO proposal/channel
// labels and NO null events. Source parameters are used only in this class.
// Floating timestamps and a seeded PRNG are a numerical realization, not the
// ideal continuous-time/random-bit theorem.
class NativeSource {
 public:
  static constexpr int n = 8;
  std::array<int,n> a{93,107,101,96,109,91,104,98};
  std::array<int,n-1> b{102,91,108,97,105,94,110};
  std::array<int,n-1> alpha{61,87,53,94,72,58,99};
  static constexpr int D = 100;
  uint64_t proposal_events = 0, state_changes = 0;
  uint64_t state = 0;
  long double t = 0;
  long double pending = 0;
  explicit NativeSource(uint64_t seed): rng(seed) {
    for (int i=0;i<n;i++) for (int c=0;c<4;c++) {
      long double r=(long double)a[i]/D;
      if(i>0 && (c&1)) r*= (long double)b[i-1]/D;
      if(i+1<n && (c&2)) r*= (long double)b[i]/D;
      hb[i][c]=r/(1+r);
    }
    for(int i=0;i<n-1;i++) for(int c=0;c<16;c++) {
      int l=c&1, x=(c>>1)&1, y=(c>>2)&1, r=(c>>3)&1;
      long double v=1;
      if(x) v*= (long double)a[i]/D;
      if(y) v*= (long double)a[i+1]/D;
      if(i>0 && l && x) v*= (long double)b[i-1]/D;
      if(x && y) v*= (long double)b[i]/D;
      if(i+2<n && y && r) v*= (long double)b[i+1]/D;
      cyc[i][c]=((long double)alpha[i]/D)/(2*v);
      if(!(cyc[i][c]>0 && cyc[i][c]<=1)) throw std::runtime_error("bad domination");
    }
    next_time();
  }
  long double next_proposal_time() const {return pending;}
  bool advance_proposal() {
    t=pending; ++proposal_events;
    uint64_t old=state;
    std::uniform_int_distribution<int> event(0,3*n-3);
    int k=event(rng);
    if(k<n) {
      int c=(k>0?bit(k-1):0)+2*(k+1<n?bit(k+1):0);
      uint64_t value=unit()<hb[k][c];
      state=(state&~(uint64_t(1)<<k))|(value<<k);
    } else {
      int i=(k-n)/2;
      int oldpair=bit(i)+2*bit(i+1);
      if(oldpair!=2) {
        int c=(i>0?bit(i-1):0)+2*bit(i)+4*bit(i+1)+8*(i+2<n?bit(i+2):0);
        if(unit()<cyc[i][c]) {
          static const int forward[4]={1,3,2,0}, reverse[4]={3,0,2,1};
          int next=(i&1)?reverse[oldpair]:forward[oldpair];
          uint64_t mask=(uint64_t(3)<<i);
          state=(state&~mask)|(uint64_t(next)<<i);
        }
      }
    }
    bool changed=state!=old;
    if(changed) ++state_changes;
    next_time();
    return changed;
  }
 private:
  std::mt19937_64 rng;
  std::array<std::array<long double,4>,n> hb{};
  std::array<std::array<long double,16>,n-1> cyc{};
  int bit(int i) const {return int((state>>i)&1);}
  long double unit() {
    // Strictly between zero and one at long-double precision on this platform.
    return (static_cast<long double>(rng()>>11)+0.5L)/9007199254740992.0L;
  }
  void next_time() {pending=t-std::log(unit())/(3*n-2);}
};

// This is the complete acquisition interface. It gets initial state once and
// on_change(new_state, timestamp) for actual state changes. Own quota timers
// need no source information. All contexts are fixed cylinders of <=4 bits.
class PassiveObserver {
 public:
  struct Context {
    uint64_t mask=0,pattern=0,count=0;
    long double exposure=0, start=0, deadline=0;
    int version=0;
    bool active=false,done=false;
  };
  struct Record {long double t; uint64_t oldstate,newstate;};
  const int n;
  const uint64_t quota;
  std::vector<Context> contexts;
  uint64_t observed_changes=0, own_timer_events=0, record_digest=1469598103934665603ULL;
  long double completed_time=0;
  std::vector<Record> first_records;
  PassiveObserver(int sites,uint64_t exposure_quota,uint64_t initial_state):
    n(sites),quota(exposure_quota),state(initial_state),by_bit(sites) {
    for(int i=0;i<n;i++) {
      for(int right=0;right<(i+1<n?2:1);right++) {
        uint64_t mask=uint64_t(1)<<i, pat=uint64_t(!(i&1))<<i;
        if(i>0) mask|=uint64_t(1)<<(i-1); // left neighbor zero
        if(i+1<n) {mask|=uint64_t(1)<<(i+1); pat|=uint64_t(right)<<(i+1);}
        add_context(mask,pat);
      }
    }
    for(int i=0;i<n-1;i++) {
      uint64_t mask=uint64_t(3)<<i,pat=0;
      if(!(i&1)) {
        pat=mask; // even cycle: 11 -> 00, outer neighbors zero
        if(i>0) mask|=uint64_t(1)<<(i-1);
        if(i+2<n) mask|=uint64_t(1)<<(i+2);
      }
      add_context(mask,pat); // odd cycle: 00 -> 11, outside unrestricted
    }
    for(int c=0;c<(int)contexts.size();c++) {
      for(int i=0;i<n;i++) if((contexts[c].mask>>i)&1) by_bit[i].push_back(c);
      if(matches(c,state)) activate(c,0);
    }
  }
  bool finished() const {return finished_count==(int)contexts.size();}
  long double next_timer() {
    return timers.empty()?std::numeric_limits<long double>::infinity():timers.begin()->first;
  }
  void on_clock(long double now) {
    while(next_timer()<=now) {
      auto [deadline,c]=*timers.begin(); timers.erase(timers.begin());
      auto &z=contexts[c];
      z.exposure=quota; z.done=true; z.active=false; ++z.version;
      ++finished_count; ++own_timer_events;
      if(finished()) completed_time=deadline;
    }
  }
  void on_change(uint64_t newstate,long double now) {
    if(newstate==state) throw std::runtime_error("observer was given a null");
    if(now<last_record_time) throw std::runtime_error("unordered timestamps");
    on_clock(now);
    if(finished()) throw std::runtime_error("record delivered after observation completed");
    uint64_t changed=state^newstate;
    if(first_records.size()<24) first_records.push_back({now,state,newstate});
    ++observed_changes;
    record_digest^=state; record_digest*=1099511628211ULL;
    record_digest^=newstate; record_digest*=1099511628211ULL;
    // Digest includes a coarse deterministic timestamp encoding; it is a
    // diagnostic checksum, not a preserved full trajectory or cryptographic hash.
    record_digest^=uint64_t(now*1048576.0L); record_digest*=1099511628211ULL;
    if((changed&(changed-1))==0) {
      int i=__builtin_ctzll(changed);
      int right=i+1<n?int((state>>(i+1))&1):0;
      int c=2*i+right;
      if(contexts[c].active && !contexts[c].done) ++contexts[c].count;
    } else {
      int i=__builtin_ctzll(changed);
      if(changed!=(uint64_t(3)<<i)) throw std::runtime_error("unexpected jump support");
      int c=2*n-1+i;
      if(contexts[c].active && !contexts[c].done) ++contexts[c].count;
    }
    std::vector<int> affected;
    for(uint64_t z=changed;z;z&=z-1) {
      int i=__builtin_ctzll(z);
      affected.insert(affected.end(),by_bit[i].begin(),by_bit[i].end());
    }
    std::sort(affected.begin(),affected.end());
    affected.erase(std::unique(affected.begin(),affected.end()),affected.end());
    for(int c:affected) {
      auto &z=contexts[c];
      if(z.done) continue;
      if(z.active) {timers.erase({z.deadline,c});z.exposure+=now-z.start; z.active=false; ++z.version;}
      if(matches(c,newstate)) activate(c,now);
    }
    state=newstate; last_record_time=now;
  }
 private:
  uint64_t state;
  int finished_count=0;
  long double last_record_time=0;
  std::vector<std::vector<int>> by_bit;
  std::set<std::pair<long double,int>> timers;
  void add_context(uint64_t mask,uint64_t pattern) {
    Context c;c.mask=mask;c.pattern=pattern;contexts.push_back(c);
  }
  bool matches(int c,uint64_t x) const {return (x&contexts[c].mask)==contexts[c].pattern;}
  void activate(int c,long double now) {
    auto &z=contexts[c];z.active=true;z.start=now;++z.version;
    z.deadline=now+(quota-z.exposure);timers.emplace(z.deadline,c);
  }
};

template<class T> void output_array(const T &a) {
  std::cout<<"[";bool first=true;for(auto z:a){if(!first)std::cout<<",";first=false;std::cout<<z;}std::cout<<"]";
}
int main(int argc,char **argv) {
  uint64_t R=argc>1?std::stoull(argv[1]):200000;
  uint64_t seed=argc>2?std::stoull(argv[2]):2026110201ULL;
  if(R==0) return 2;
  NativeSource source(seed);
  PassiveObserver observer(NativeSource::n,R,source.state);
  while(!observer.finished()) {
    long double timer=observer.next_timer();
    if(timer<=source.next_proposal_time()) observer.on_clock(timer);
    else if(source.advance_proposal()) observer.on_change(source.state,source.t);
  }
  std::cout<<std::setprecision(20);
  std::cout<<"{\"n\":"<<source.n<<",\"R\":"<<R<<",\"seed\":"<<seed
    <<",\"completed_time\":"<<observer.completed_time
    <<",\"actual_observed_state_changes\":"<<observer.observed_changes
    <<",\"observer_quota_timers\":"<<observer.own_timer_events
    <<",\"hidden_source_proposals_for_diagnostic_cost_only\":"<<source.proposal_events
    <<",\"record_digest\":"<<observer.record_digest
    <<",\"truth_denominator\":"<<source.D<<",\"truth_a\":";
  output_array(source.a);std::cout<<",\"truth_b\":";output_array(source.b);
  std::cout<<",\"truth_alpha\":";output_array(source.alpha);
  std::cout<<",\"counts\":[";
  for(int c=0;c<(int)observer.contexts.size();c++) {if(c)std::cout<<",";std::cout<<observer.contexts[c].count;}
  std::cout<<"],\"exposures\":[";
  for(int c=0;c<(int)observer.contexts.size();c++) {if(c)std::cout<<",";std::cout<<observer.contexts[c].exposure;}
  std::cout<<"],\"first_actual_records\":[";
  bool first=true;for(auto z:observer.first_records) {if(!first)std::cout<<",";first=false;std::cout<<"["<<z.t<<","<<z.oldstate<<","<<z.newstate<<"]";}
  std::cout<<"]}\n";
}
