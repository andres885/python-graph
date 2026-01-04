# VERSIÓN SIN DEPENDER DE FUENTES ESPECÍFICAS
import yfinance as yf
import matplotlib.pyplot as plt

# Obtener datos
dxy = yf.download("DX-Y.NYB", start="2025-01-01", end="2026-01-05")
close_prices = dxy[('Close', 'DX-Y.NYB')]

# Crear gráfico ULTRA minimalista
fig, ax = plt.subplots(figsize=(16, 9), facecolor='white')
ax.plot(close_prices.index, close_prices.values, color='#e63946', linewidth=5)

# Texto simple (usará la fuente por defecto de matplotlib)
ax.text(0.5, 0.08, 'USD 2025-2026',
        transform=ax.transAxes,
        fontsize=40,
        fontweight='bold',
        color='#333333',
        ha='center',
        va='center')

# Remover todo lo demás
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Guardar
plt.savefig('dxy_simple.png', dpi=300, bbox_inches='tight')
plt.show()
