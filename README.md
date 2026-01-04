# Visualización de Datos Financieros: Índice Dólar (DXY) 📈

Colección de scripts en Python diseñados para la extracción, análisis y visualización del Índice Dólar (DXY). Este repositorio contiene herramientas que van desde el análisis técnico detallado con datos reales hasta la generación de infografías minimalistas y proyecciones de escenarios económicos.

## 📋 Descripción General

Los scripts se dividen en tres categorías principales:
1. **Datos Reales y Análisis Técnico:** Conexión con Yahoo Finance para obtener datos históricos y calcular indicadores.
2. **Visualización de Escenarios:** Gráficos basados en proyecciones manuales para ilustrar narrativas de mercado (ej. impacto de aranceles).
3. **Estilo e Infografía:** Scripts enfocados en la estética visual (clean/minimal) para presentaciones o redes sociales.

## 🛠️ Requisitos

El proyecto funciona con **Python 3.x**. Las dependencias principales son:

* `yfinance`: Para descargar datos de mercado reales.
* `pandas`: Manipulación y análisis de estructuras de datos.
* `matplotlib`: Generación de gráficos estáticos.
* `numpy`: Cálculos matemáticos y estadísticos.

Puedes instalar todo lo necesario con:

```bash
pip install yfinance pandas matplotlib numpy
```

## 📂 Catálogo de Scripts

### 1. Análisis Técnico Completo (`graph_ds.py`)
Es el script más robusto del repositorio.
* **Fuente:** Descarga datos reales de Yahoo Finance (Ticker: `DX-Y.NYB`).
* **Funcionalidades:**
    * Gráfico de precios de cierre con Medias Móviles (MA20 y MA50).
    * Bandas de rango diario (High/Low).
    * Cálculo de RSI y señales de tendencia (Alcista/Bajista).
    * Estadísticas detalladas (volatilidad, máximos, mínimos).
* **Salida:** Genera imagen (`.png`, `.pdf`) y exporta los datos crudos a `.csv`.

### 2. Infografías Minimalistas
Scripts enfocados en el diseño visual, ideales para compartir resultados rápidos.

* **`graph_simple.py`:** Genera una infografía moderna con estilo "flat".
    * Crea dos versiones: una horizontal (presentaciones) y una cuadrada (redes sociales).
    * Destaca el valor actual y el cambio porcentual con colores condicionales.
* **`graph_simple_v3.py`:** Versión ultra-ligera sin dependencias de fuentes específicas, garantizando que el gráfico se genere correctamente en cualquier sistema operativo.

### 3. Simulación de Escenarios y Proyecciones
Estos scripts utilizan datos predefinidos ("hardcoded") para visualizar tesis de inversión o escenarios hipotéticos.

* **`graph.py`:** Visualiza una narrativa de "Gestión Política vs Valor". Divide el cronograma en fases coloreadas (Expectativa, Decepción, Realidad) e incluye anotaciones de texto explicativas. Utiliza interpolación `pchip` para curvas suaves.
* **`usd_graph.py`:** Simula volatilidad de mercado. Toma una tendencia base y le aplica "ruido" aleatorio (`numpy.random`) para simular el comportamiento errático de los precios semanales, manteniendo la tendencia de fondo.
* **`usd_graph_month.py`:** Visión macro mensual. Elimina el ruido diario para mostrar la tendencia pura a largo plazo con hitos clave marcados.

## 🚀 Uso

Simplemente ejecuta el script deseado desde tu terminal:

```bash
# Para análisis con datos reales
python3 graph_ds.py

# Para generar infografía
python3 graph_simple.py
```

Los archivos generados (imágenes PNG/PDF y datos CSV) se guardarán automáticamente en el mismo directorio.

## 📝 Notas
* Algunos scripts de proyección contienen datos ficticios para propósitos de demostración de escenarios (2025-2026). Para análisis real de mercado, utiliza siempre `graph_ds.py`.
* Las fechas están configuradas por defecto para el periodo 2025-2026, pero son fácilmente editables al inicio de cada archivo.

---

## 🧾 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**.  
Consulta la licencia completa aquí: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)

---

## 🧑‍💻 Autor

Desarrollado por [**X Software**](https://xsoftware.es).  
Desarrollo de software Linux, soluciones web y automatización de sistemas.
