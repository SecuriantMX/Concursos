"""Grafica de probabilidades por partido a partir de salida_2359.json."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.load(open("salida_2359.json"))
filas = d["partidos"] + d["partidos_rev"]
col = ["#2a78d6", "#eb6834", "#1baf7a"]  # local, empate, visita
fondo, tinta, gris = "#fcfcfb", "#0b0b0b", "#52514e"

fig, ax = plt.subplots(figsize=(10, 9.5), dpi=200, facecolor=fondo)
ax.set_facecolor(fondo)
y = list(range(len(filas)))[::-1]
for yi, f in zip(y, filas):
    izq = 0
    for i in range(3):
        w = f["p"][i] * 100
        ax.barh(yi, w - 0.5, left=izq + 0.25, height=0.62, color=col[i])
        if w >= 9:
            ax.text(izq + w / 2, yi, f"{w:.0f}", ha="center", va="center", color="white", fontsize=8.5, fontweight="bold")
        izq += w
    nota = "" if f["conf"] != "nula" else "  (sin estimación)"
    ax.text(-1.5, yi, f"{f['id']}  {f['local']} – {f['visita']}{nota}", ha="right", va="center", color=tinta, fontsize=9)
    ax.text(101.5, yi, f"±{f['ic']*100:.0f}  {f['conf']}", ha="left", va="center", color=gris, fontsize=8)
ax.axhline(6.5, color=gris, lw=0.6, ls=":")
ax.set_xlim(0, 100); ax.set_ylim(-0.7, len(filas) - 0.3)
ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(colors=gris, labelsize=8, length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.xaxis.grid(True, color="#e4e3df", lw=0.6); ax.set_axisbelow(True)
ax.set_xlabel("probabilidad estimada (%)", color=gris, fontsize=9)
ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in col], ["Local", "Empate", "Visita"],
          loc="upper center", bbox_to_anchor=(0.5, 1.045), ncol=3, frameon=False, fontsize=9)
fig.suptitle("Progol 2359 y Revancha: probabilidad por partido", x=0.02, ha="left", color=tinta, fontsize=13, fontweight="bold")
fig.text(0.02, 0.012, "Mezcla de mercado sin margen (Shin), Elo y Poisson con xG donde existe. Consulta: 13-nov-2026. "
         "A la derecha: medio ancho del intervalo y confianza.", color=gris, fontsize=7.5)
plt.subplots_adjust(left=0.36, right=0.89, top=0.93, bottom=0.07)
fig.savefig("probabilidades_2359.png", facecolor=fondo)
