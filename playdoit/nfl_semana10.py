"""
Parlay NFL semana 10 (domingo 15-nov-2026) en Playdoit.

Probabilidad justa: momios de moneyline de 8 casas (vegasinsider.com, actualizado
13-nov-2026 14:16 hora del este; orden Bet365, BetMGM, DraftKings, Caesars,
FanDuel, HardRock, Fanatics, Kalshi), cada una sin margen por Shin y promediadas.
Momios de Playdoit: capturas del usuario, 14-nov-2026 11:15 CDMX.
"""
import sys
from itertools import combinations
sys.path.insert(0, "../progol")
from modelo import shin

def dec(a):
    return 1 + a / 100 if a > 0 else 1 + 100 / -a

# (equipo A, equipo B, momios A por casa, momios B por casa, Playdoit A, Playdoit B)
J = [
 ("NE Patriots", "DET Lions", [127,125,124,130,128,130,125,133], [-152,-145,-148,-154,-152,-150,-150,-138], 128, -146),
 ("KC Chiefs", "ATL Falcons", [-169,-175,-170,-182,-172,-185,-180,-170], [144,145,142,153,144,155,150,163], -166, 144),
 ("MIN Vikings", "GB Packers", [129,125,124,130,130,135,130,138], [-154,-145,-148,-154,-154,-155,-155,-144], 129, -148),
 ("BUF Bills", "NY Jets", [-440,-450,-425,-420,-460,-475,-450,-400], [340,350,330,330,360,350,340,376], -417, 342),
 ("JAX Jaguars", "TEN Titans", [-600,-650,-700,-590,-670,-700,-600], [450,500,500,425,490,475,430], -667, 515),
 ("MIA Dolphins", "IND Colts", [180,175,180,169,176,175,175,194], [-220,-210,-218,-205,-210,-210,-215,-203], 185, -215),
 ("CAR Panthers", "NO Saints", [119,115,114,113,118,120,115], [-139,-135,-135,-137,-138,-140,-140], 117, -133),
 ("HOU Texans", "CLE Browns", [-235,-235,-238,-235,-230,-240,-235,-212], [190,190,195,192,194,195,190,203], -233, 200),
 ("SEA Seahawks", "LV Raiders", [-300,-295,-305,-310,-300,-325,-300,-270], [240,240,245,240,245,240,240,257], -310, 262),
 ("LA Rams", "ARZ Cardinals", [-500,-475,-520,-480,-520,-500,-475,-426], [375,375,390,360,400,375,360,400], -527, 421),
 ("SF 49ers", "DAL Cowboys", [-220,-220,-218,-218,-220,-210,-215,-194], [180,180,180,183,184,175,175,186], -215, 185),
 ("PIT Steelers", "CIN Bengals", [157,155,154,154,150,155,155,163], [-187,-190,-185,-182,-178,-185,-190,-170], 160, -184),
]

def shin2(a, b):
    # el Shin de modelo.py esta escrito para tres resultados; con dos funciona igual
    return shin([a, b])[0]

lados = []
print(f"{'lado':15}{'justa':>7}{'rango casas':>14}{'Playdoit':>9}{'dec':>6}{'EV':>8}")
for a, b, ma, mb, pa, pb in J:
    ps = [shin2(dec(x), dec(y)) for x, y in zip(ma, mb)]
    fa = sum(p[0] for p in ps) / len(ps)
    lo, hi = min(p[0] for p in ps), max(p[0] for p in ps)
    for nom, f, l, h, pd in ((a, fa, lo, hi, pa), (b, 1 - fa, 1 - hi, 1 - lo, pb)):
        ev = f * dec(pd) - 1
        lados.append(dict(lado=nom, p=f, lo=l, hi=h, am=pd, dec=dec(pd), ev=ev, juego=a))
        print(f"{nom:15}{f*100:6.1f}%  {l*100:5.1f}-{h*100:4.1f}%{pd:>+9}{dec(pd):6.2f}{ev*100:+7.1f}%")
    margen = 1 / dec(pa) + 1 / dec(pb) - 1
    print(f"{'':15}margen de Playdoit en este juego: {margen*100:.1f}%")

orden = sorted(lados, key=lambda x: -x["ev"])
print("\nMejores lados por valor esperado:")
for x in orden[:8]:
    print(f"  {x['lado']:15} {x['am']:+5}  p={x['p']*100:.1f}%  EV={x['ev']*100:+.1f}%  EV con la casa mas pesimista={(x['lo']*x['dec']-1)*100:+.1f}%")

def parlay(sel):
    p = d = 1.0
    for x in sel:
        p *= x["p"]; d *= x["dec"]
    return p, d, p * d - 1

print("\nParlays armados con los lados de mejor valor (un lado por juego):")
for n in (2, 3, 4):
    usados, sel = set(), []
    for x in orden:
        if x["juego"] not in usados:
            sel.append(x); usados.add(x["juego"])
        if len(sel) == n:
            break
    p, d, ev = parlay(sel)
    print(f"  {n} selecciones: {' + '.join(s['lado'] for s in sel)}")
    print(f"     momio {d:.2f} ({(d-1)*100:+.0f}), probabilidad {p*100:.1f}%, EV {ev*100:+.1f}%")
