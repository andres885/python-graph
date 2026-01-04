import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

# Configuración de fechas
fecha_inicio = "2025-01-01"
fecha_fin = "2026-01-05"

print(f"Obteniendo datos REALES del DXY desde {fecha_inicio} hasta {fecha_fin}...")

try:
    # Descargar datos reales
    dxy = yf.download("DX-Y.NYB",
                     start=fecha_inicio,
                     end=fecha_fin,
                     progress=False)

    print(f"Datos obtenidos: {len(dxy)} registros")
    print(f"Período cubierto: {dxy.index[0].date()} a {dxy.index[-1].date()}")

    # Simplificar columnas MultiIndex
    if isinstance(dxy.columns, pd.MultiIndex):
        new_columns = []
        for col in dxy.columns:
            if col[0]:  # Si el primer nivel no está vacío
                new_columns.append(col[0])
            else:
                new_columns.append(col[1])
        dxy.columns = new_columns

    print(f"\nColumnas disponibles: {dxy.columns.tolist()}")
    print(f"\nMuestra de datos de volumen (primeros 5 días):")
    print(dxy['Volume'].head())

    # Verificar si hay volumen real
    volumen_total = dxy['Volume'].sum()
    print(f"\nVolumen total del período: {volumen_total:,.0f}")

    # Crear figura - SOLO gráfico de precios (sin volumen si es 0)
    if volumen_total > 0:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                       gridspec_kw={'height_ratios': [3, 1]},
                                       sharex=True)
        tiene_volumen = True
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(14, 7))
        tiene_volumen = False
        print("NOTA: No hay datos de volumen disponibles. Mostrando solo gráfico de precios.")

    # Gráfico de precios
    ax1.plot(dxy.index, dxy['Close'],
            color='#1f77b4',
            linewidth=2.5,
            label='DXY (Cierre)')

    # Bandas de precio (High-Low)
    ax1.fill_between(dxy.index,
                    dxy['Low'],
                    dxy['High'],
                    alpha=0.15,
                    color='lightblue',
                    label='Rango diario')

    # Medias móviles
    dxy['MA_20'] = dxy['Close'].rolling(window=20, min_periods=1).mean()
    dxy['MA_50'] = dxy['Close'].rolling(window=50, min_periods=1).mean()

    ax1.plot(dxy.index, dxy['MA_20'],
            color='red',
            linestyle='--',
            linewidth=1.5,
            label='MA 20 días',
            alpha=0.7)

    ax1.plot(dxy.index, dxy['MA_50'],
            color='orange',
            linestyle='--',
            linewidth=1.5,
            label='MA 50 días',
            alpha=0.7)

    # Configurar gráfico de precios
    ax1.set_title(f'Índice Dólar (DXY) - Enero 2025 a Enero 2026',
                 fontsize=16,
                 fontweight='bold',
                 pad=20)
    ax1.set_ylabel('Valor DXY', fontsize=12)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(loc='best')

    # Formatear fechas
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Gráfico de volumen (solo si hay datos)
    if tiene_volumen:
        ax2.bar(dxy.index, dxy['Volume'],
               color='lightgray',
               alpha=0.7,
               width=0.8)
        ax2.set_ylabel('Volumen', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.xaxis.set_major_locator(mdates.MonthLocator())
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    else:
        # En lugar de volumen vacío, mostramos análisis técnico
        ax1.text(0.02, 0.98, "NOTA: Sin datos de volumen\nMostrando solo análisis de precios",
                transform=ax1.transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3),
                verticalalignment='top')

    # Estadísticas detalladas
    cambio_total = ((dxy['Close'].iloc[-1] / dxy['Close'].iloc[0]) - 1) * 100
    volatilidad = dxy['Close'].pct_change().std() * 100

    # Encontrar máximos y mínimos
    max_idx = dxy['High'].idxmax()
    min_idx = dxy['Low'].idxmin()

    stats_text = f"""Estadísticas DXY ({dxy.index[0].date()} a {dxy.index[-1].date()}):
• Días analizados: {len(dxy)}
• Primer cierre: {dxy['Close'].iloc[0]:.2f}
• Último cierre: {dxy['Close'].iloc[-1]:.2f}
• Cambio total: {cambio_total:+.2f}%
• Máximo: {dxy['High'].max():.2f} ({max_idx.date()})
• Mínimo: {dxy['Low'].min():.2f} ({min_idx.date()})
• Volatilidad diaria: {volatilidad:.2f}%
• Media 20 días: {dxy['MA_20'].iloc[-1]:.2f}
• Media 50 días: {dxy['MA_50'].iloc[-1]:.2f}"""

    ax1.text(0.02, 0.02, stats_text, transform=ax1.transAxes, fontsize=9,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'),
             verticalalignment='bottom', fontfamily='monospace')

    plt.tight_layout()

    # GUARDAR IMAGEN
    nombre_imagen = f"dxy_{fecha_inicio}_{fecha_fin}.png"
    plt.savefig(nombre_imagen, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico guardado como: {nombre_imagen}")

    # También guardar como PDF (vectorial, mejor calidad)
    nombre_pdf = f"dxy_{fecha_inicio}_{fecha_fin}.pdf"
    plt.savefig(nombre_pdf, bbox_inches='tight')
    print(f"✓ Gráfico guardado como PDF: {nombre_pdf}")

    plt.show()

    # GUARDAR DATOS CSV Y MOSTRAR CÓMO VISUALIZARLOS
    nombre_csv = f"dxy_datos_{fecha_inicio}_{fecha_fin}.csv"
    dxy.to_csv(nombre_csv)
    print(f"\n✓ Datos guardados en CSV: {nombre_csv}")

    # Mostrar cómo visualizar el CSV
    print("\n" + "="*70)
    print("CÓMO VISUALIZAR EL ARCHIVO CSV:")
    print("="*70)
    print("\n1. Con pandas (en Python):")
    print(f"   import pandas as pd")
    print(f"   datos = pd.read_csv('{nombre_csv}', index_col=0, parse_dates=True)")
    print(f"   print(datos.head())")

    print("\n2. Con Excel/LibreOffice:")
    print(f"   - Abre el archivo '{nombre_csv}' con Excel")
    print(f"   - Selecciona 'Datos' -> 'Desde texto/CSV'")
    print(f"   - Establece la codificación UTF-8 y separador coma")

    print("\n3. Con línea de comandos:")
    print(f"   # Linux/Mac:")
    print(f"   head -n 10 {nombre_csv}")
    print(f"   ")
    print(f"   # Windows PowerShell:")
    print(f"   Get-Content {nombre_csv} -TotalCount 10")

    # Mostrar resumen del CSV
    print(f"\n" + "="*70)
    print("RESUMEN DEL ARCHIVO CSV GUARDADO:")
    print("="*70)
    print(f"• Filas: {len(dxy)}")
    print(f"• Columnas: {len(dxy.columns)}")
    print(f"• Columnas disponibles:")
    for i, col in enumerate(dxy.columns, 1):
        print(f"  {i}. {col}")

    # Mostrar primeras y últimas filas del CSV
    print(f"\nPrimeras 3 filas del CSV:")
    print(dxy.head(3).to_string())

    print(f"\nÚltimas 3 filas del CSV:")
    print(dxy.tail(3).to_string())

    # Análisis adicional
    print("\n" + "="*70)
    print("ANÁLISIS TÉCNICO DXY 2025-2026")
    print("="*70)

    # Señales de trading simples
    dxy['Signal'] = np.where(dxy['MA_20'] > dxy['MA_50'], 'ALCISTA', 'BAJISTA')

    # Contar días de cada señal
    dias_alcistas = (dxy['Signal'] == 'ALCISTA').sum()
    dias_bajistas = (dxy['Signal'] == 'BAJISTA').sum()

    print(f"\nAnálisis de medias móviles:")
    print(f"- Días con tendencia alcista (MA20 > MA50): {dias_alcistas} días ({dias_alcistas/len(dxy)*100:.1f}%)")
    print(f"- Días con tendencia bajista (MA20 < MA50): {dias_bajistas} días ({dias_bajistas/len(dxy)*100:.1f}%)")

    # Calcular RSI simplificado
    delta = dxy['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    print(f"\nAnálisis RSI (último valor): {rsi.iloc[-1]:.1f}")
    if rsi.iloc[-1] > 70:
        print("  → SOBRECOMPRADO (posible corrección)")
    elif rsi.iloc[-1] < 30:
        print("  → SOBREVENDIDO (posible rebote)")
    else:
        print("  → ZONA NEUTRA")

    # Recomendación final
    print("\n" + "="*70)
    print("RECOMENDACIONES:")
    print("="*70)
    print("1. El gráfico se guardó como PNG y PDF en el directorio actual")
    print("2. Los datos completos están en el archivo CSV")
    print("3. Para análisis más detallado:")
    print("   - Usa pandas para cargar el CSV")
    print("   - Importa a Excel para análisis visual")
    print("   - Agrega más indicadores técnicos según necesidad")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

    # Versión de emergencia si todo falla
    print("\n" + "="*70)
    print("CREANDO GRÁFICO DE EMERGENCIA...")
    print("="*70)

    try:
        dxy_simple = yf.download("DX-Y.NYB", start=fecha_inicio, end=fecha_fin, progress=False)
        close_prices = dxy_simple[('Close', 'DX-Y.NYB')]

        plt.figure(figsize=(14, 7))
        plt.plot(close_prices.index, close_prices.values, 'b-', linewidth=2)
        plt.title(f'DXY - {fecha_inicio} a {fecha_fin}')
        plt.ylabel('Valor DXY')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)

        # Guardar imagen de emergencia
        plt.savefig(f'dxy_emergencia_{fecha_inicio}_{fecha_fin}.png', dpi=300, bbox_inches='tight')
        plt.show()

        print(f"✓ Gráfico de emergencia guardado")

    except Exception as e2:
        print(f"Error en gráfico de emergencia: {e2}")
