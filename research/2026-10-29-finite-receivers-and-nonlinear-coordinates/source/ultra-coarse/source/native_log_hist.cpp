// Independent direct Gillespie consumer of ALL pinned local catalog rules.
// Standard binary64/mt19937 numerical experiment, not a physical trajectory.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>
struct Rule { double rate; int group,react,n; std::array<int,2> site,from,to; };
int main(int argc,char**argv){
  if(argc!=7){std::cerr<<"input.csv output.csv episodes seed COscale Oscale\n";return 2;}
  auto start=std::chrono::steady_clock::now();
  std::ifstream in(argv[1]);int nx,ny,P;double T;in>>nx>>ny>>P>>T;
  std::vector<Rule> events;
  for(int p=0;p<P;p++){
    double rate;int group,react,n;in>>rate>>group>>react>>n;
    int typ[2],dx[2],dy[2],from[2],to[2];
    for(int j=0;j<n;j++)in>>typ[j]>>dx[j]>>dy[j]>>from[j]>>to[j];
    for(int y=0;y<ny;y++)for(int x=0;x<nx;x++){
      Rule r;r.rate=rate;r.group=group;r.react=react;r.n=n;
      for(int j=0;j<n;j++){
        int xx=(x+dx[j]+nx)%nx,yy=(y+dy[j]+ny)%ny;
        r.site[j]=2*(xx+nx*yy)+typ[j];r.from[j]=from[j];r.to[j]=to[j];
      }
      events.push_back(r);
    }
  }
  const int M=2*nx*ny,E=events.size();
  int samples=std::stoi(argv[3]);std::mt19937_64 rng(std::stoull(argv[4]));
  double scale[3]={1.,std::stod(argv[5]),std::stod(argv[6])};
  std::uint64_t words=0,steps=0,checks=0,gas_events=0;
  auto uniform=[&](){words++;return (double(rng()>>11)+.5)*0x1p-53;};
  std::ofstream out(argv[2]);out<<std::setprecision(17);
  out<<"NCO,NO2,ACO,AO2,COcoverage,Ocoverage,CO2hit,events,Ivac,Ipair_lower,Ipair_upper";
  for(int v=0;v<=M;v++)out<<",Tv"<<v;
  out<<'\n';
  std::vector<int> state(M);std::vector<double> w(E);
  double sumco=0,sumo=0,sumhit=0;
  for(int rep=0;rep<samples;rep++){
    std::fill(state.begin(),state.end(),0);double t=0,Aco=0,Ao=0,Iv=0,Il=0,Iu=0;
    int nc=0,no=0,hit=0,jumps=0;std::vector<double> residence(M+1,0.);
    while(t<T){
      double total=0,aco=0,ao=0;
      for(int e=0;e<E;e++){
        const auto&r=events[e];bool valid=true;
        for(int j=0;j<r.n;j++){checks++;if(state[r.site[j]]!=r.from[j]){valid=false;break;}}
        if(valid){w[e]=r.rate*scale[r.group];total+=w[e];
          if(r.group==1)aco+=r.rate;else if(r.group==2)ao+=r.rate;
        }else w[e]=0;
      }
      int vac=std::count(state.begin(),state.end(),0);
      if(total<=0){double dt=T-t;Aco+=aco*dt;Ao+=ao*dt;
        Iv+=vac*dt;Il+=std::max(0,4*vac-2*M)*dt;Iu+=2*vac*dt;residence[vac]+=dt;t=T;break;}
      double wait=-std::log(uniform())/total;
      double dt=std::min(wait,T-t);Aco+=aco*dt;Ao+=ao*dt;t+=dt;
      Iv+=vac*dt;Il+=std::max(0,4*vac-2*M)*dt;Iu+=2*vac*dt;residence[vac]+=dt;
      if(wait>=dt && t>=T)break;
      double ticket=uniform()*total,cum=0;int chosen=-1;
      for(int e=0;e<E;e++){cum+=w[e];if(ticket<cum){chosen=e;break;}}
      if(chosen<0){std::cerr<<"numeric categorical failure\n";return 3;}
      const auto&r=events[chosen];for(int j=0;j<r.n;j++)state[r.site[j]]=r.to[j];
      if(r.group==1)nc++;else if(r.group==2)no++;
      if(r.group)gas_events++;if(r.react)hit=1;jumps++;steps++;
    }
    double co=double(std::count(state.begin(),state.end(),1))/M;
    double ox=double(std::count(state.begin(),state.end(),2))/M;
    out<<nc<<','<<no<<','<<Aco<<','<<Ao<<','<<co<<','<<ox<<','<<hit<<','<<jumps
       <<','<<Iv<<','<<Il<<','<<Iu;
    for(double v:residence)out<<','<<v;
    out<<'\n';
    sumco+=co;sumo+=ox;sumhit+=hit;
  }
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<std::setprecision(17)<<"{\"episodes\":"<<samples<<",\"COscale\":"<<scale[1]
    <<",\"Oscale\":"<<scale[2]<<",\"horizon_seconds\":"<<T<<",\"sites\":"<<M
    <<",\"local_event_instances\":"<<E<<",\"native_events\":"<<steps
    <<",\"gas_events\":"<<gas_events<<",\"condition_checks\":"<<checks
    <<",\"rng_words64\":"<<words<<",\"compute_and_write_seconds\":"<<sec
    <<",\"mean_CO\":"<<sumco/samples<<",\"mean_O\":"<<sumo/samples
    <<",\"CO2hit_probability\":"<<sumhit/samples<<"}\n";
}
