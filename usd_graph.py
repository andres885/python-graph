import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Set seed for reproducibility (Same as before to keep the graph identical)
np.random.seed(42)

# Define key milestones
anchors = {
    '2025-01-01': 113.5,
    '2025-02-01': 115.0, 
    '2025-02-15': 118.0, 
    '2025-04-05': 120.0, 
    '2025-05-12': 123.8, 
    '2025-06-04': 121.5, 
    '2025-08-01': 115.0, 
    '2025-11-04': 102.0, 
    '2025-12-31': 98.1,
    '2026-01-04': 98.2
}

# Create a weekly date range
dates = pd.date_range(start='2025-01-01', end='2026-01-04', freq='W-FRI') 
df = pd.DataFrame({'Date': dates})

# Interpolation logic
anchor_df = pd.DataFrame(list(anchors.items()), columns=['Date', 'Trend'])
anchor_df['Date'] = pd.to_datetime(anchor_df['Date'])
df = pd.merge(df, anchor_df, on='Date', how='left')
df = df.set_index('Date')
combined_index = df.index.union(anchor_df.set_index('Date').index).sort_values()
df_trend = df.reindex(combined_index)
df_trend.update(anchor_df.set_index('Date'))
df_trend['Trend'] = df_trend['Trend'].interpolate(method='time')
df_final = df_trend.reindex(dates).reset_index().rename(columns={'index': 'Date'})

# Volatility logic
def get_noise(row):
    date = row['Date']
    month = date.month
    if 2 <= month <= 9:
        volatility = 0.8
    else:
        volatility = 0.4
    noise = np.random.normal(0, volatility)
    return row['Trend'] + noise

df_final['DXY_Simulated'] = df_final.apply(get_noise, axis=1)

# Plotting
plt.figure(figsize=(12, 6))

plt.plot(df_final['Date'], df_final['DXY_Simulated'], color='#1f77b4', linewidth=1.5, marker='.', markersize=5, label='Cierre Semanal (Simulado)')
plt.plot(df_final['Date'], df_final['Trend'], color='gray', linestyle='--', alpha=0.3, linewidth=1, label='Tendencia Subyacente')

# Annotations
events = [
    ('2025-02-01', 'Inicio Aranceles', 115),
    ('2025-05-12', 'Máx. Tensión', 123.8),
    ('2025-11-04', 'Acuerdo China', 102)
]

for date_str, label, y_val in events:
    date_obj = pd.to_datetime(date_str)
    plt.annotate(label, 
                 xy=(date_obj, y_val), 
                 xytext=(date_obj, y_val + 4),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 fontsize=9, ha='center', fontweight='bold')

# Title Adjustment: Added 'y=1.08' to push title up
plt.title('Evolución Semanal Detallada del Dólar (DXY) 2025-2026\n(Simulación de Volatilidad de Mercado)', fontsize=14, y=1.12)

plt.ylabel('Valor Índice Dólar (DXY)', fontsize=12)
plt.xlabel('Fecha (Semanas)', fontsize=12)
plt.grid(True, linestyle='-', alpha=0.3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

plt.axvspan(pd.to_datetime('2025-02-01'), pd.to_datetime('2025-10-01'), color='orange', alpha=0.1, label='Alta Volatilidad')

plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('dolar_tarifas_trump_2025_final.png')
