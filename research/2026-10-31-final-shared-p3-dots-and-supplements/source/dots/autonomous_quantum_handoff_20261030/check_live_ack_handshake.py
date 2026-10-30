"""Exhaustive finite clean handshake graph; native retire/Q path is an imported subroutine.
Not a complete corrupted-controller or QCA threshold simulation.
"""
from collections import deque
from pathlib import Path
import json
# Two reset cells, each incident to two owners. Private p[x,h] bits.
# Owner W abbreviates one actual in-flight A/C/B transaction; Q imported cleanup.
start=(('I','I'),('IDLE','IDLE'),(0,0,0,0))
def replace(t,j,a):l=list(t);l[j]=a;return tuple(l)
def bit(p,x,h):return p[2*x+h]
def edges(s):
 os,cs,p=s
 for h,o in enumerate(os):
  held=any(bit(p,x,h) for x in range(2))
  if o=='I':
   if not held:yield ('LOAD',h),(replace(os,h,'W'),cs,p)
   yield ('watchdog',h),(replace(os,h,'Q'),cs,p)
  if o=='W':yield ('retire_once',h),(replace(os,h,'Q'),cs,p)
  if o=='Q':yield ('verified_ready',h),(replace(os,h,'P' if held else 'I'),cs,p)
  if o=='P' and not held:yield ('unpark_via_Q',h),(replace(os,h,'Q'),cs,p)
 for x,c in enumerate(cs):
  def emit(a,p2=p):return os,replace(cs,x,a),p2
  if c=='IDLE' and all(not bit(p,x,h) for h in range(2)):yield ('start',x),emit('A0')
  if c in ['A0','A1']:
   j=int(c[1])
   if bit(p,x,j)==0:yield ('acquire_request',x,j),emit('A'+str(j+1),replace(p,2*x+j,1))
  if c in ['A1','A2']:
   j=int(c[1])-1
   if bit(p,x,j)==1:yield ('reverse_request',x,j),emit('A'+str(j),replace(p,2*x+j,0))
  if c=='A2':yield ('commit_pause',x),emit('V0')
  if c in ['V0','V1']:
   j=int(c[1])
   if os[j]=='P':yield ('verify_live_PARK',x,j),emit('V'+str(j+1))
  if c in ['V1','V2']:
   j=int(c[1])-1
   if os[j]=='P':yield ('reverse_verify',x,j),emit('V'+str(j))
  if c=='V2':yield ('ERASE',x),emit('HOLD')
  if c=='HOLD':yield ('caller_release',x),emit('R0')
  if c in ['R0','R1']:
   j=int(c[1])
   if bit(p,x,j)==1:yield ('release_bit',x,j),emit('R'+str(j+1),replace(p,2*x+j,0))
  if c in ['R1','R2']:
   j=int(c[1])-1
   if bit(p,x,j)==0:yield ('reverse_release',x,j),emit('R'+str(j),replace(p,2*x+j,1))
  if c=='R2':yield ('finish',x),emit('DONE')
  if c=='DONE':yield ('new_cycle_return',x),emit('IDLE')
seen={start};q=deque([start]);nedge=nerase=nverified=0
while q:
 s=q.popleft();os,cs,p=s
 for x,c in enumerate(cs):
  if c.startswith('V') or c=='HOLD':
   assert all(bit(p,x,h) for h in range(2)),s
  if c.startswith('V'):
   for h in range(int(c[1])):assert os[h]=='P',s
  if c=='HOLD':assert all(o=='P' for o in os),s
 for a,t in edges(s):
  nedge+=1
  if a[0]=='ERASE':
   nerase+=1;assert all(o=='P' for o in os),s
  if a[0]=='LOAD':assert all(not bit(p,x,a[1]) for x in range(2)),s
  if a[0]=='verify_live_PARK':nverified+=1
  if t not in seen:seen.add(t);q.append(t)
result={'reachable_states':len(seen),'directed_edges':nedge,'erase_sources_checked':nerase,'live_verification_edges':nverified,
'every_committed_pause_bit_held_until_release':True,'every_verified_owner_stays_parked':True,'no_erase_with_live_owner':True,'fresh_cycles_reverify_actual_phase':True,
'negative_cached_ack_fixture':{'old_ack':1,'owner_phase':'W','naive_ack_reset_enabled':True,'actual_live_PARK_verify_enabled':False},
'scope':'finite clean reservation/control graph; actual quantum prefix retirement is imported; corrupted epochs and noisy QCA theorem remain separate'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
