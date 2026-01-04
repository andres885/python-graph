import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Data points (Key anchors for the trend)
data = {
    'Date': [
        '2025-01-01', '2025-02-01', '2025-02-15', '2025-04-05',
        '2025-05-12', '2025-06-04', '2025-08-01', '2025-11-04',
        '2025-12-31', '2026-01-04'
    ],
    'DXY': [113.5, 115.0, 118.0, 120.0, 123.8, 121.5, 115.0, 102.0, 98.1, 98.2]
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Interpolate to get a daily series for a smooth line (removing noise)
date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')
df_interp = df.set_index('Date').reindex(date_range)
df_interp['DXY'] = df_interp['DXY'].interpolate(method='time')
df_interp = df_interp.reset_index().rename(columns={'index': 'Date'})

# Plotting
plt.figure(figsize=(12, 6))

# Plot the smooth trend line (no noise, no markers as it's a trend view)
plt.plot(df_interp['Date'], df_interp['DXY'], color='#1f77b4', linewidth=2, label='Tendencia DXY')

# Annotations (keeping the style and positions from the previous version)
events = [
    ('2025-02-01', 'Inicio Aranceles', 115),
    ('2025-05-12', 'Máx. Tensión', 123.8),
    ('2025-11-04', 'Acuerdo China', 102)
]

for date_str, label, y_val in events:
    date_obj = pd.to_datetime(date_str)
    plt.annotate(label,
                 xy=(date_obj, y_val),
                 xytext=(date_obj, y_val + 5), # Slightly higher text position for clean look
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                 fontsize=9, ha='center', fontweight='bold')

# Title with the y=1.08 fix to prevent overlapping
plt.title('Evolución del Índice Dólar (DXY) tras las Tarifas de Trump (2025-2026)', fontsize=14, y=1.2)
plt.ylabel('Valor Índice Dólar (DXY)', fontsize=12)
plt.xlabel('Fecha', fontsize=12)

# Styling from the latest version (grid, orange zone)
plt.grid(True, linestyle='-', alpha=0.3)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))

# Highlight the area of "Tariff Stress" / High Volatility Period
plt.axvspan(pd.to_datetime('2025-02-01'), pd.to_datetime('2025-10-01'), color='orange', alpha=0.1, label='Periodo de Alta Tensión')

plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('dolar_tarifas_trump_2025_clean_fixed.png')
