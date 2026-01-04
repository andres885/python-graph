import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Datos consolidados del escenario real 2025
data_points = [
    ('2025-01-01', 109.2),
    ('2025-01-13', 109.96), # Pico "Trump Trade"
    ('2025-02-15', 107.5),  # Dudas fiscales
    ('2025-03-10', 104.5),  # Desaceleración / Decepción
    ('2025-04-02', 104.2),  # Pre-Aranceles
    ('2025-04-07', 102.94), # Impacto Arancelario (Sell-off)
    ('2025-05-15', 101.0),  # Continuación bajista
    ('2025-08-01', 100.5),  # Estancamiento
    ('2025-11-04', 99.0),   # Acuerdos (pero daño hecho)
    ('2025-12-31', 98.25),  # Cierre de año
    ('2026-01-04', 98.10)
]

df = pd.DataFrame(data_points, columns=['Date', 'DXY'])
df['Date'] = pd.to_datetime(df['Date'])

# Interpolación suave
date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
df_interp = df.set_index('Date').reindex(date_range)
df_interp['DXY'] = df_interp['DXY'].interpolate(method='pchip') # pchip para curvas más naturales
df_interp = df_interp.reset_index().rename(columns={'index': 'Date'})

# Plotting
plt.figure(figsize=(12, 6))

# Línea de tendencia
plt.plot(df_interp['Date'], df_interp['DXY'], color='#2c3e50', linewidth=2.5, label='Índice Dólar (DXY)')

# Definición de fases (Colores de fondo)
# Fase 1: Expectativa
plt.axvspan(pd.to_datetime('2025-01-01'), pd.to_datetime('2025-02-01'), color='green', alpha=0.1)
plt.text(pd.to_datetime('2025-01-15'), 111, "FASE 1:\nEXPECTATIVAS", color='green', ha='center', fontsize=9, fontweight='bold')

# Fase 2: Decepción
plt.axvspan(pd.to_datetime('2025-02-01'), pd.to_datetime('2025-04-01'), color='orange', alpha=0.1)
plt.text(pd.to_datetime('2025-03-01'), 111, "FASE 2:\nDECEPCIÓN/DUDAS", color='#d35400', ha='center', fontsize=9, fontweight='bold')

# Fase 3: Realidad (Aranceles)
plt.axvspan(pd.to_datetime('2025-04-01'), pd.to_datetime('2026-01-04'), color='red', alpha=0.05)
plt.text(pd.to_datetime('2025-08-01'), 111, "FASE 3: IMPACTO ARANCELARIO Y AJUSTE", color='red', ha='center', fontsize=9, fontweight='bold')

# Anotaciones de eventos clave
events = [
    ('2025-01-13', 'Promesas Electorales\n(Máximo: 109.96)', 109.96),
    ('2025-03-10', 'Datos Macro Débiles\n(Miedo al Déficit)', 104.5),
    ('2025-04-07', 'Ejecución de Aranceles\n(Reacción Negativa)', 102.94),
    ('2025-12-31', 'Cierre Fiscal 2025\n(Minimos: ~98.2)', 98.25)
]

for date_str, label, y_val in events:
    date_obj = pd.to_datetime(date_str)
    plt.annotate(label, 
                 xy=(date_obj, y_val), 
                 xytext=(date_obj, y_val + 2.5 if y_val < 108 else y_val - 4),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 fontsize=9, ha='center', fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# Títulos y formato
plt.title('Correlación entre Gestión Política y Valor del Dólar (2025)', fontsize=14, y=1.2)
plt.ylabel('Índice Dólar (DXY)', fontsize=12)
plt.xlabel('Cronología de Eventos', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

plt.tight_layout()
plt.savefig('dolar_impacto_gestion_2025.png')
