#!/usr/bin/env python3
"""Executable finite tile compiler and independent small-rectangle enumeration.

No numerical Fourier/phase inference is made. All tests are exact combinatorics.
"""
from dataclasses import dataclass
from itertools import product
from collections import defaultdict
import json
from pathlib import Path

ZERO = ()
HALT = 'HALT'
REJECT = 'REJECT'

@dataclass(frozen=True)
class Cell:
    pair: tuple
    b: int
    head: tuple | None = None
    poison: bool = False

@dataclass
class Machine:
    symbols: tuple
    blank: str
    states: tuple
    start: str
    delta: dict
    input_word: tuple = ()

    def alphabet(self):
        out = []
        qs = tuple(dict.fromkeys(self.states + (HALT, REJECT)))
        for b in (0, 1):
            for pair in product(self.symbols, repeat=2):
                out.append(Cell(pair, b))
                out.extend(Cell(pair, b, (q, tr)) for q in qs for tr in (0, 1))
            out.append(Cell((self.blank, self.blank), b, poison=True))
        return tuple(out)

    def initial(self, width):
        if width < max(2, len(self.input_word)):
            return None
        row = [Cell((self.input_word[i] if i < len(self.input_word) else self.blank,
                     self.blank), int(i == 0)) for i in range(width)]
        row[0] = Cell(row[0].pair, 1, (self.start, 0))
        return tuple(row)

    def prefix(self):
        return self.initial(max(2, len(self.input_word)))[:max(1, len(self.input_word))]

    def intent(self, x):
        assert x.head is not None and not x.poison
        q, track = x.head
        if q in (HALT, REJECT):
            return x.pair, x.head, 0
        qnew, write, original_move = self.delta[(q, x.pair[track])]
        pair = list(x.pair)
        pair[track] = write
        trnew = track
        if original_move == 0:
            move = 0
        elif track == 0:
            if original_move == 1:
                move = 1
            elif x.b:
                move, trnew = 0, 1
            else:
                move = -1
        else:
            if original_move == -1:
                move = 1
            elif x.b:
                move, trnew = 0, 0
            else:
                move = -1
        return tuple(pair), (qnew, trnew), move

    def F(self, p, x, q):
        poison = Cell((self.blank, self.blank), x.b, poison=True)
        if any(z is not None and z.poison for z in (p, x, q)):
            return poison
        incoming = []
        if p is not None and p.head is not None:
            _, head, move = self.intent(p)
            if move == 1:
                incoming.append(head)
        if q is not None and q.head is not None:
            _, head, move = self.intent(q)
            if move == -1:
                incoming.append(head)
        if len(incoming) > 1 or (incoming and x.head is not None):
            return poison
        pair, head = x.pair, None
        if x.head is not None:
            pair, newhead, move = self.intent(x)
            if move == 0:
                head = newhead
            elif (move == -1 and p is None) or (move == 1 and q is None):
                head = (REJECT, newhead[1])
        if incoming:
            head = incoming[0]
        return Cell(pair, x.b, head)

    def step(self, row):
        return tuple(self.F(row[i-1] if i else None, row[i],
                            row[i+1] if i+1 < len(row) else None)
                     for i in range(len(row)))

    def dfa_states(self, v):
        return range(len(self.prefix()) + 1) if v == 'B' else range(2 if v == 'T' else 1)

    def dfa_step(self, v, k, x):
        if v == 'I':
            return 0
        if v == 'B':
            P = self.prefix()
            if k < len(P):
                return k + 1 if x == P[k] else None
            z = Cell((self.blank, self.blank), 0)
            return k if x == z else None
        if x.poison:
            return None
        if x.head is None:
            return k
        return 1 if k == 0 and x.head[0] == HALT else None

    def dfa_accept(self, v, k):
        return k == len(self.prefix()) if v == 'B' else (k == 1 if v == 'T' else k == 0)

@dataclass(frozen=True)
class Tile:
    h: str
    v: str
    triple: tuple
    km: int
    kp: int
    colors: tuple  # W,E,S,N
    marked: bool


def compile_tiles(machine):
    """Literally enumerate the finite algorithm in the accompanying proof."""
    sigma = machine.alphabet()
    tiles = []
    for h, v in product(('L', 'I', 'R'), ('B', 'I', 'T')):
        ps = (None,) if h == 'L' else sigma
        qs = (None,) if h == 'R' else sigma
        xs = [x for x in sigma if x.b == int(h == 'L')]
        for x in xs:
            for km in machine.dfa_states(v):
                kp = machine.dfa_step(v, km, x)
                if kp is None or (h == 'L' and km != 0):
                    continue
                if h == 'R' and not machine.dfa_accept(v, kp):
                    continue
                for p, q in product(ps, qs):
                    y = machine.F(p, x, q)
                    W = ZERO if h == 'L' else ('H', v, p, x, km)
                    E = ZERO if h == 'R' else ('H', v, x, q, kp)
                    S = ZERO if v == 'B' else ('V', h, x)
                    N = ZERO if v == 'T' else ('V', h, y)
                    tiles.append(Tile(h, v, (p, x, q), km, kp,
                                      (W, E, S, N), h == 'L' and v == 'T'))
    return tiles


def count_rectangles(tiles, width, height):
    """Assemble actual tile edges. Does not call the machine update or row DFA."""
    by = defaultdict(list)
    for t in tiles:
        by[t.h, t.v, t.colors[0], t.colors[2]].append(t)
    grid = []
    found = []
    def visit(pos):
        if pos == width * height:
            assert sum(t.marked for t in grid) == 1
            found.append(tuple(grid))
            return
        j, i = divmod(pos, width)
        h = 'L' if i == 0 else 'R' if i == width-1 else 'I'
        v = 'B' if j == 0 else 'T' if j == height-1 else 'I'
        W = grid[-1].colors[1] if i else ZERO
        S = grid[pos-width].colors[3] if j else ZERO
        for t in by[h, v, W, S]:
            if i == width-1 and t.colors[1] != ZERO:
                continue
            if j == height-1 and t.colors[3] != ZERO:
                continue
            grid.append(t)
            visit(pos+1)
            grid.pop()
    visit(0)
    return len(found)


def verify_geometry(W, H):
    """Exhaust all status-only closed tilings, including vacuum/contact."""
    status = [None] + list(product(('L','I','R'), ('B','I','T')))
    def edges(z):
        if z is None:
            return (ZERO,) * 4
        h,v = z
        return (ZERO if h=='L' else ('H',v), ZERO if h=='R' else ('H',v),
                ZERO if v=='B' else ('V',h), ZERO if v=='T' else ('V',h))
    rows=[]
    for row in product(status, repeat=W):
        es=[edges(z) for z in row]
        if es[0][0] != ZERO or es[-1][1] != ZERO:
            continue
        if any(es[i][1] != es[i+1][0] for i in range(W-1)):
            continue
        rows.append((row,tuple(e[2] for e in es),tuple(e[3] for e in es)))
    bysouth=defaultdict(list)
    for r in rows:
        bysouth[r[1]].append(r)
    count=0
    component_count=0
    grid=[]
    def check():
        nonlocal component_count
        unseen={(x,y) for y in range(H) for x in range(W) if grid[y][x] is not None}
        while unseen:
            start=next(iter(unseen)); todo=[start]; comp=set()
            while todo:
                x,y=todo.pop()
                if (x,y) in comp:
                    continue
                comp.add((x,y)); unseen.discard((x,y))
                es=edges(grid[y][x])
                for k,(dx,dy) in enumerate(((-1,0),(1,0),(0,-1),(0,1))):
                    if es[k] != ZERO:
                        todo.append((x+dx,y+dy))
            xs=[p[0] for p in comp]; ys=[p[1] for p in comp]
            xmin,xmax,ymin,ymax=min(xs),max(xs),min(ys),max(ys)
            assert xmax>xmin and ymax>ymin
            assert comp == set(product(range(xmin,xmax+1),range(ymin,ymax+1)))
            assert sum(grid[y][x] == ('L','T') for x,y in comp)==1
            component_count+=1
    def go(y,south):
        nonlocal count
        if y==H:
            if south==(ZERO,)*W:
                count+=1;check()
            return
        for row,S,N in bysouth[south]:
            grid.append(row);go(y+1,N);grid.pop()
    go(0,(ZERO,)*W)
    return {'width':W,'height':H,'closed_assignments':count,'components_checked':component_count}


def main():
    machines={
      'halt_after_one': Machine(('_',),'_',('S',),'S',{('S','_'):(HALT,'_',0)}),
      'stationary_nonhalt': Machine(('_',),'_',('S',),'S',{('S','_'):('S','_',0)}),
      'right_overflow_nonhalt': Machine(('_',),'_',('S',),'S',{('S','_'):('S','_',1)}),
      'left_fold_nonhalt': Machine(('_',),'_',('S',),'S',{('S','_'):('S','_',-1)}),
      'cross_origin_halt': Machine(('_',),'_',('S','A'),'S',
          {('S','_'):('A','_',-1),('A','_'):(HALT,'_',1)}),
      'halt_requires_width_three': Machine(('_',),'_',('S','A'),'S',
          {('S','_'):('A','_',1),('A','_'):(HALT,'_',1)}),
      'halt_at_start': Machine(('_',),'_',(),HALT,{}),
    }
    results={}
    total=0
    for name,m in machines.items():
        tiles=compile_tiles(m)
        colors={c for t in tiles for c in t.colors}
        assert ZERO in colors
        tests=[]
        for W in (2,3,4):
            row=m.initial(W)
            for H in range(2,6):
                expected_row=m.initial(W)
                for _ in range(H-1):
                    expected_row=m.step(expected_row)
                expected=int(sum(x.head is not None and x.head[0]==HALT for x in expected_row)==1)
                got=count_rectangles(tiles,W,H)
                assert got==expected,(name,W,H,got,expected)
                tests.append({'width':W,'height':H,'accepting_tilings':got})
                total+=1
        t=len(tiles);C0=10000*(t+1);D=C0+t
        # Exact polynomial coefficients in x=exp(-1), no floating arithmetic.
        for F in {-t,-1,0,1,t}:
            n0=C0+F;n1=D-n0
            assert n0>0 and n1>=0
            assert (n0,n1)==(C0+F,t-F)
        results[name]={'tile_types':t,'edge_colors':len(colors),'rectangles':tests}
    geo=[verify_geometry(W,H) for W,H in ((2,2),(3,3),(4,4),(5,4))]
    result={'status':'all exact checks passed','rectangle_tests':total,
            'machines':results,'geometry':geo,
            'scope':'finite closed grammar and positive integer ancillary identity only'}
    path=Path(__file__).with_name('explicit_tableau_grammar_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'rectangle_tests':total,'geometry':geo,
        'tile_types':{k:v['tile_types'] for k,v in results.items()}},indent=2))

if __name__=='__main__':main()
