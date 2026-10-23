function h(T,a){const t=T/1000;const[A,B,C,D,E,F,G,H]=a;return A*t+B*t*t/2+C*t**3/3+D*t**4/4-E/t+F-H;}
const N2high=[35.51872,1.128728,-.196103,.014662,-4.553760,-18.97091,224.981,0];
const O2high=[20.91111,10.72071,-2.020498,.146449,9.245722,5.337651,237.6185,0];
const N2mid=[19.50583,19.88705,-8.598535,1.369784,.527601,-4.935202,212.390,0];
const O2mid=[30.03235,8.772972,-3.988133,.788313,-.741599,-11.32468,236.1663,0];
const NO=[35.99169,.957170,-.148032,.009974,-3.004088,73.10787,246.1619,90.29114];
const rows=[2100,2000,1800,1500,3100].map(T=>({T,N2:h(T,T>=2000?N2high:N2mid),O2:h(T,T>=2000?O2high:O2mid),air79_21:.79*h(T,T>=2000?N2high:N2mid)+.21*h(T,T>=2000?O2high:O2mid),NO:h(T,NO)}));
text(rows);store("shomateRows",rows);
text({air_2100_per_mol_NO_at_045:rows[0].air79_21/.045,cost_from_2_7:(2700-rows[0].air79_21/.045)/1000,cost_from_120:(120-rows[0].air79_21)/.045/1000,minimum_eff_to_reach1_5:(2700-1500)/(rows[0].air79_21/.045),minimum_eff_to_reach1_0:(2700-1000)/(rows[0].air79_21/.045)});
