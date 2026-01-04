import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración estética minimalista
plt.style.use('default')  # Reset a estilo limpio

# Datos
fecha_inicio = "2025-01-01"
fecha_fin = "2026-01-05"

print("Creando infografía minimalista del DXY...")

try:
    # Obtener datos
    dxy = yf.download("DX-Y.NYB", start=fecha_inicio, end=fecha_fin, progress=False)

    # Simplificar columnas
    if isinstance(dxy.columns, pd.MultiIndex):
        close_prices = dxy[('Close', 'DX-Y.NYB')]
    else:
        close_prices = dxy['Close']

    # Configuración de figura - FORMATO INFOGRAFÍA
    fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')

    # Fondo degradado sutil
    ax.set_facecolor('#f8f9fa')

    # LÍNEA PRINCIPAL - ROJO INTENSO Y GRUESA
    line_color = '#e63946'  # Rojo vibrante
    line_width = 4

    ax.plot(close_prices.index,
            close_prices.values,
            color=line_color,
            linewidth=line_width,
            solid_capstyle='round')

    # Añadir sombra sutil debajo de la línea
    ax.fill_between(close_prices.index,
                   close_prices.values,
                   close_prices.min() * 0.99,
                   color=line_color,
                   alpha=0.1)

    # REMOVER TODO LO NO ESENCIAL
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    # Grid sutil solo horizontal
    ax.yaxis.grid(True, linestyle='-', alpha=0.1, linewidth=0.5)
    ax.xaxis.grid(False)

    # Formatear eje X - minimalista
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # Rotar fechas ligeramente
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center', fontsize=10)

    # Eje Y minimalista
    ax.tick_params(axis='y', length=0, labelsize=11, pad=8)
    ax.tick_params(axis='x', length=0, labelsize=11, pad=10)

    # Título minimalista pero impactante
    ax.text(0.02, 0.98, 'DÓLAR AMERICANO',
            transform=ax.transAxes,
            fontsize=32,
            fontweight='bold',
            color='#2a2a2a',
            verticalalignment='top',
            fontfamily='sans-serif')

    ax.text(0.02, 0.90, 'Índice DXY 2025-2026',
            transform=ax.transAxes,
            fontsize=18,
            color='#6c757d',
            verticalalignment='top',
            fontfamily='sans-serif')

    # Valores clave minimalistas
    primer_valor = close_prices.iloc[0]
    ultimo_valor = close_prices.iloc[-1]
    cambio = ((ultimo_valor / primer_valor) - 1) * 100

    # Valor actual - grande y destacado
    ax.text(0.98, 0.15, f'{ultimo_valor:.1f}',
            transform=ax.transAxes,
            fontsize=48,
            fontweight='bold',
            color=line_color,
            verticalalignment='center',
            horizontalalignment='right',
            fontfamily='sans-serif')

    ax.text(0.98, 0.08, 'VALOR ACTUAL',
            transform=ax.transAxes,
            fontsize=14,
            color='#6c757d',
            verticalalignment='center',
            horizontalalignment='right',
            fontfamily='sans-serif')

    # Cambio porcentual - color según si es positivo o negativo
    cambio_color = '#2a9d8f' if cambio >= 0 else '#e63946'  # Verde si sube, rojo si baja

    ax.text(0.98, 0.25, f'{cambio:+.1f}%',
            transform=ax.transAxes,
            fontsize=24,
            fontweight='bold',
            color=cambio_color,
            verticalalignment='center',
            horizontalalignment='right',
            fontfamily='sans-serif')

    ax.text(0.98, 0.30, 'VARIACIÓN 2025-2026',
            transform=ax.transAxes,
            fontsize=12,
            color='#6c757d',
            verticalalignment='center',
            horizontalalignment='right',
            fontfamily='sans-serif')

    # Puntos clave en el gráfico
    # Máximo y mínimo del período
    max_idx = close_prices.idxmax()
    min_idx = close_prices.idxmin()

    # Punto máximo
    ax.scatter([max_idx], [close_prices.max()],
              color='#ff9f1c', s=120, zorder=5, edgecolors='white', linewidth=2)

    ax.annotate(f'Máx: {close_prices.max():.1f}',
               xy=(max_idx, close_prices.max()),
               xytext=(0, 20),
               textcoords='offset points',
               ha='center',
               fontsize=12,
               fontweight='bold',
               color='#ff9f1c')

    # Punto mínimo
    ax.scatter([min_idx], [close_prices.min()],
              color='#457b9d', s=120, zorder=5, edgecolors='white', linewidth=2)

    ax.annotate(f'Mín: {close_prices.min():.1f}',
               xy=(min_idx, close_prices.min()),
               xytext=(0, -30),
               textcoords='offset points',
               ha='center',
               fontsize=12,
               fontweight='bold',
               color='#457b9d')

    # Ajustar límites para que respire
    y_min, y_max = close_prices.min(), close_prices.max()
    y_range = y_max - y_min
    ax.set_ylim(y_min - y_range * 0.05, y_max + y_range * 0.15)

    # Ajustar márgenes
    plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15)

    # Guardar en alta calidad para infografía
    nombre_infografia = f"infografia_dxy_{fecha_inicio}_{fecha_fin}.png"
    plt.savefig(nombre_infografia, dpi=300, facecolor='white', edgecolor='none', bbox_inches='tight')

    # También versión para redes sociales (formato cuadrado)
    fig_social, ax_social = plt.subplots(figsize=(8, 8), facecolor='white')
    ax_social.set_facecolor('#f8f9fa')

    # Línea más gruesa para formato cuadrado
    ax_social.plot(close_prices.index, close_prices.values,
                  color=line_color, linewidth=6, solid_capstyle='round')

    # Relleno sutil
    ax_social.fill_between(close_prices.index, close_prices.values,
                          close_prices.min() * 0.99, color=line_color, alpha=0.15)

    # Remover bordes
    ax_social.spines['top'].set_visible(False)
    ax_social.spines['right'].set_visible(False)
    ax_social.spines['left'].set_visible(False)
    ax_social.spines['bottom'].set_visible(False)

    # Sin ejes
    ax_social.set_xticks([])
    ax_social.set_yticks([])

    # Título para redes
    ax_social.text(0.5, 0.93, 'DXY 2025-2026',
                  transform=ax_social.transAxes,
                  fontsize=28,
                  fontweight='bold',
                  color='#2a2a2a',
                  ha='center',
                  fontfamily='sans-serif')

    ax_social.text(0.5, 0.87, f'{ultimo_valor:.1f}  |  {cambio:+.1f}%',
                  transform=ax_social.transAxes,
                  fontsize=36,
                  fontweight='bold',
                  color=line_color,
                  ha='center',
                  fontfamily='sans-serif')

    # Guardar versión redes sociales
    nombre_social = f"dxy_social_{fecha_inicio}_{fecha_fin}.png"
    plt.savefig(nombre_social, dpi=300, facecolor='white', edgecolor='none', bbox_inches='tight')

    plt.show()

    print(f"\n✅ INFOGRAFÍAS CREADAS:")
    print(f"   1. {nombre_infografia} (formato horizontal)")
    print(f"   2. {nombre_social} (formato cuadrado para redes)")
    print(f"\n📊 DATOS CLAVE:")
    print(f"   • Período: {close_prices.index[0].date()} a {close_prices.index[-1].date()}")
    print(f"   • Valor inicial: {primer_valor:.1f}")
    print(f"   • Valor final: {ultimo_valor:.1f}")
    print(f"   • Cambio: {cambio:+.1f}%")
    print(f"   • Máximo: {close_prices.max():.1f}")
    print(f"   • Mínimo: {close_prices.min():.1f}")

except Exception as e:
    print(f"Error: {e}")

    # Versión de emergencia ultra minimalista
    print("\nCreando versión minimalista de emergencia...")

    try:
        dxy_simple = yf.download("DX-Y.NYB", start=fecha_inicio, end=fecha_fin, progress=False)
        close_prices = dxy_simple[('Close', 'DX-Y.NYB')]

        fig, ax = plt.subplots(figsize=(16, 8), facecolor='white')
        ax.plot(close_prices.index, close_prices.values, color='#e63946', linewidth=5)

        # Remover todo
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        # Solo el valor actual
        ax.text(0.95, 0.95, f'{close_prices.iloc[-1]:.1f}',
                transform=ax.transAxes,
                fontsize=48,
                fontweight='bold',
                color='#e63946',
                ha='right',
                va='top')

        plt.savefig(f'dxy_minimal_emergencia.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("✅ Versión minimalista de emergencia creada: dxy_minimal_emergencia.png")

    except Exception as e2:
        print(f"Error en versión de emergencia: {e2}")
