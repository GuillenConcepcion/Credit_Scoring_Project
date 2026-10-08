# End-to-End Credit Scoring, Risk Modeling & Intelligent Decisioning Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-CRISP--DM%20%26%20MLOps-success.svg)](#-arquitectura-y-metodolog%C3%ADa)
[![Status](https://img.shields.io/badge/Pipeline-Verified%20%26%20Reproducible-brightgreen.svg)](#-ejecuci%C3%B3n-del-pipeline)
[![Dashboard](https://img.shields.io/badge/Dashboard-FastAPI%20%26%20Vanilla%20Dark-cyan.svg)](#-dashboard-interactivo-de-credit-scoring--decisi%C3%B3n-en-tiempo-real)
[![Regulation](https://img.shields.io/badge/Compliance-Basel%20III%20%2F%20IFRS%209%20%2F%20Fair%20Lending-orange.svg)](#-motor-de-decisiones-inteligente-credit-decisioning-engine)

Solución integral y de grado de producción para la evaluación de riesgo crediticio, estimación de probabilidad de default (PD), suscripción automatizada y tarificación dinámica (*Risk-Based Pricing*), diseñada bajo estándares bancarios internacionales (Basilea III / IFRS 9) y mejores prácticas MLOps.

Abarca desde la ingesta exploratoria, ingeniería temporal y tratamiento robusto de datos sin fuga (*No Data Leakage*), hasta el análisis de estabilidad poblacional (PSI < 0.10), selección de variables en 4 etapas mediante K-Fold CV, un **Motor de Decisiones Inteligente** con políticas de rechazo/aprobación (*Knockouts*) y un **Dashboard Web Interactivo en Tiempo Real**.

---

## 📌 Tabla de Contenidos
- [👨‍💻 Perfil del Desarrollador](#-perfil-del-desarrollador)
- [🏗 Arquitectura y Metodología](#-arquitectura-y-metodología)
- [🚀 Fases del Pipeline Analítico](#-fases-del-pipeline-analítico)
- [🏛 Motor de Decisiones Inteligente (Credit Decisioning Engine)](#-motor-de-decisiones-inteligente-credit-decisioning-engine)
- [🖥️ Dashboard Interactivo en Tiempo Real](#-dashboard-interactivo-en-tiempo-real)
- [📁 Estructura del Repositorio](#-estructura-del-repositorio)
- [🛠 Requisitos e Instalación](#-requisitos-e-instalación)
- [⚡ Ejecución del Pipeline](#-ejecución-del-pipeline)
- [📊 Resultados Clave y Artefactos](#-resultados-clave-y-artefactos)
- [🛡 Buenas Prácticas MLOps y Gobernanza](#-buenas-prácticas-mlops-y-gobernanza)

---

## 👨‍💻 Perfil del Desarrollador

**Guillén Concepción**  
*Senior Data Scientist & MLOps Engineer*

> Experto en diseño, desarrollo y despliegue de soluciones integrales de Inteligencia Artificial. Pragmático y centrado en el valor de negocio, abarcando desde la fase de investigación (CRISP-DM) hasta sistemas de producción escalables, resilientes y auditables utilizando arquitecturas Cloud-Native y prácticas MLOps.

- **LinkedIn:** [linkedin.com/in/guillen-concepcion-25266b127](https://www.linkedin.com/in/guillen-concepcion-25266b127)
- **GitHub:** [github.com/GuillenConcepcion](https://github.com/GuillenConcepcion)
- **Email:** [guillenconcepcion@gmail.com](mailto:guillenconcepcion@gmail.com)

---

## 🏗 Arquitectura y Metodología

El proyecto implementa un ciclo de vida analítico riguroso estructurado sobre la metodología **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), acoplado a un motor de decisión en tiempo real:

```
[Raw Dataset (32,581 registros)]
           │
           ▼
[Fase 1: Ingesta, Feat. Eng. & EDA] ──► Vintage temporal (2013-2022) & Target Def
           │
           ├──────────────────────────────┐
           ▼ (<= 2021: 26,616 obs)        ▼ (== 2022: 5,965 obs)
[Train / Test Histórico]             [OOT: Out-Of-Time Validation]
           │
           ▼
[Fase 2: Split Estratificado, IQR & Imputación] ──► Train (21,292), Test (5,324), OOT
           │
           ▼
[Fase 3: Asociación Estadística & Multicolinealidad] (Kruskal-Wallis, Cramér's V, Spearman)
           │
           ▼
[Fase 4: Discriminación & Storytelling] ──► Contingencia Chi-cuadrado & Gráficos Cole
           │
           ▼
[Fase 5: Monotonía & Estabilidad PSI] ──► Year-to-Year & Train vs Test vs OOT (< 0.10)
           │
           ▼
[Fase 6: K-Fold CV & Selección de Variables (4 Reglas)]
           │
           ▼
[Set Óptimo Seleccionado (7 variables robustas)] ──► Test AUC: 0.8329 | Gini: 0.6658
           │
           ├──────────────────────────────────────────────┐
           ▼                                              ▼
[Motor de Decisiones Inteligente]              [Dashboard Web Interactivo]
(Knockouts, Policy Matrix, Pricing, IFRS 9)     (FastAPI, Dark Mode, Simulador FICO)
```

---

## 🚀 Fases del Pipeline Analítico

### Fase 1: Ingesta de Datos, Feature Engineering & EDA
- **Dataset:** Ingesta del dataset de riesgo crediticio (32,581 observaciones).
- **Ingeniería Temporal:** Reconstrucción de cohortes anuales (`year = 2024 - cb_person_cred_hist_length`, acotado a 2013-2022).
- **Partición Temporal:**
  - **Ventana Histórica (Train/Test):** Años 2013 a 2021 (26,616 registros).
  - **Validación Fuera de Tiempo (OOT - Out of Time):** Año 2022 (5,965 registros).
- **Reportes:** Generación automática de reportes de distribución por antigüedad, cohorte y cuartiles de edad con exportación a Excel.

### Fase 2: Partición Estratificada, Tratamiento de Outliers e Imputación
- **Estratificación Robusta:** División 80% Train (21,292 obs) y 20% Test (5,324 obs) estratificada por `def_year` (combinación de target y cohorte), preservando la tasa de default (~21.4% en Train/Test y 23.6% en OOT).
- **Tratamiento de Valores Extremos (IQR):** Límites de clipping $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$ calculados **exclusivamente sobre el conjunto de entrenamiento** para evitar fuga de información (*data leakage*), y propagados a Test y OOT.
- **Auditoría e Imputación:**
  - Inserción de variables indicadoras de ausencia (`person_emp_length_missing`, `loan_int_rate_missing`).
  - Imputación conservadora de antigüedad laboral (`emp_length = 0`) y mediana calculada en Train para tasa de interés (`loan_int_rate = median`).

### Fase 3: Asociación Estadística y Multicolinealidad
- **Variables Continuas vs Target:** Test no paramétrico de Kruskal-Wallis ($p$-value y estadístico KW).
- **Variables Categóricas vs Target:** V de Cramér con corrección de sesgo de contingencia.
- **Multicolinealidad:** Matrices de correlación de Spearman para continuas y Cramér's V inter-categórica para detectar redundancia estructural.

### Fase 4: Discriminación de Atributos y Visualización Ejecutiva
- Análisis de contingencia y test Chi-cuadrado para variables críticas como `person_home_ownership` ($\chi^2 = 1,248.48, p < 10^{-200}$).
- Generación de visualizaciones ejecutivas bajo principios de *Storytelling with Data* (formato Cole Knaflic), exportadas en alta resolución (`default_by_ownership.png`).

### Fase 5: Análisis de Monotonía y Estabilidad Poblacional (PSI)
- **Agrupamiento Robusto:** Reclasificación de modalidades infrecuentes (`home_ownership_3`: OWN, MORTGAGE, OTHER_RENT) para asegurar soporte muestral en todos los periodos.
- **PSI Interanual (Year-to-Year):** Evaluación de estabilidad ventana a ventana deslizante entre 2013 y 2021.
- **PSI de Población (Train vs Test vs OOT):** Verificación de deriva de datos (*data drift*). Todos los predictores seleccionados exhiben un $PSI < 0.10$ (**Estabilidad Máxima Confirmada**).

### Fase 6: Selección de Variables Robusta (K-Fold Multi-Regla)
Implementación de un procedimiento de selección en 4 etapas sobre validación cruzada estratificada (4 Folds):
1. **Regla 1 (Continuas vs Target):** Se eliminan variables no significativas ($p \ge 0.05$) en cualquiera de los 4 folds.
2. **Regla 2 (Categóricas vs Target):** Se filtran variables con asociación débil ($V < 0.10$).
3. **Regla 3 (Multicolinealidad Continua):** Para pares con $|\rho_{Spearman}| \ge 0.50$, se descarta la variable con menor asociación al target crediticio.
4. **Regla 4 (Multicolinealidad Categórica):** Para pares con $V \ge 0.50$, se elimina el predictor redundante.

**Set Final de Variables Seleccionadas (7 predictores clave):**
1. `person_income` (Ingresos anuales)
2. `person_age` (Edad del prestatario)
3. `person_emp_length` (Estabilidad laboral)
4. `loan_int_rate` (Tasa de interés de la operación)
5. `loan_percent_income` (Ratio cuota/ingreso o apalancamiento DTI)
6. `person_home_ownership` (Tipo de tenencia de vivienda)
7. `cb_person_default_on_file` (Historial crediticio previo con default)

---

## 🏛 Motor de Decisiones Inteligente (Credit Decisioning Engine)

El módulo [`src/decision_engine/`](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/src/decision_engine/decision_engine.py) implementa un motor de decisión bancaria de producción que va más allá de la simple estimación de probabilidades:

### 1. Reglas de Exclusión Dura (*Knockouts / Hard Cutoffs*)
Filtros pre-scoring que detienen el procesamiento ante condiciones no negociables:
- **KO-01:** Menor de edad legal ($< 18$ años).
- **KO-02:** Edad superior al límite asegurable de desgravamen ($> 80$ años).
- **KO-03:** Ingreso anual por debajo del umbral de subsistencia ($< \$8,000$ USD).
- **KO-04:** Endeudamiento crítico patrimonial ($\text{DTI} > 0.65$).

### 2. Matriz de Políticas y Risk Tiers (Escala FICO 300 - 850)
Mapeo log-odds calibrado ($PDO = 20$, Base = $600$ en $1:50$):

$$\text{Odds} = \frac{PD}{1 - PD}, \quad \text{Score} = \text{Offset} - \text{Factor} \times \ln(\text{Odds})$$

| Tramo de Riesgo | Rango Score | Prob. Default | Decisión de Política | Límite Máximo | Spread Tasa |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **Tier A (Prime)** | **750 – 850** | $< 4.5\%$ | **Aprobación Automática (STP)** | $125\%$ monto | $+150\text{ bps}$ |
| **Tier B (Bajo Riesgo)** | **670 – 749** | $4.5\% – 12.0\%$ | **Aprobado Estándar** *(DTI $\le 28\%$)* | $100\%$ monto | $+250\text{ bps}$ |
| **Tier C (Near-Prime)** | **600 – 669** | $12.0\% – 24.0\%$ | **Revisión Manual / Condicionado** | $80\%$ monto | $+450\text{ bps}$ |
| **Tier D (Subprime)** | **530 – 599** | $24.0\% – 42.0\%$ | **Aprobación con Aval / Colateral** | $50\%$ monto | $+750\text{ bps}$ |
| **Tier E (Crítico)** | **300 – 529** | $> 42.0\%$ | **Rechazado por Política** | $0\%$ | N/A |

### 3. Tarificación Dinámica (*Risk-Based Pricing*) & Pérdida Esperada (IFRS 9)
- **Tasa Asignada:** $\text{Coste Fondos (5.50%)} + \text{Spread Crediticio (150 a 750 bps)}$.
- **Pérdida Esperada:** $\text{EL} = \text{PD} \times \text{LGD} \times \text{EAD}$, con LGD quirografaria del $55\%$.
- **Explicabilidad (Fair Lending / FCRA):** Generación automática de razones de adjudicación (*Reason Codes*) y factores positivos/negativos que afectaron la calificación.

#### Ejemplo de Uso en Python:
```python
import sys
sys.path.insert(0, "Credit_scoring_project-main")

from src.decision_engine import IntelligentDecisionEngine, ApplicantProfile

engine = IntelligentDecisionEngine()
perfil = ApplicantProfile(
    person_income=65000,
    person_age=32,
    person_emp_length=5,
    loan_amnt=12000,
    loan_int_rate=10.5,
    loan_percent_income=0.18,
    person_home_ownership="MORTGAGE",
    cb_person_default_on_file="N"
)

resultado = engine.evaluate(perfil)
print(f"Decisión: {resultado.decision.value}")
print(f"Score: {resultado.credit_score} | Tramo: {resultado.tier.value}")
print(f"Tasa Asignada: {resultado.recommended_interest_rate}%")
print(f"Pérdida Esperada: ${resultado.expected_loss:,.2f} USD")
```

---

## 🖥️ Dashboard Interactivo en Tiempo Real

El proyecto incluye una aplicación web moderna (FastAPI + Vanilla CSS/JS Dark Mode + Chart.js) para exploración ejecutiva y simulación de scoring en vivo:

```bash
# Iniciar servidor y abrir automáticamente en navegador
python run_dashboard.py

# O en Windows hacer doble clic en:
run_dashboard.bat
```

La plataforma se despliega en: **`http://localhost:8088`** *(Docs OpenAPI en `/docs`)*.

### Módulos del Dashboard:
- ⚡ **Simulador de Scoring en Tiempo Real:** Sliders interactivos, cálculo reactivo de FICO Score (300-850), Gauge radial animado, probabilidad de impago, dictamen (Tier A-E) y factores determinantes (*waterfall drivers*). Botones de prueba rápida (*Cliente Prime*, *Riesgo Medio*, *Alto Riesgo*).
- 📊 **Visión Ejecutiva & Datasets:** KPIs globales (32,581 solicitudes, 21.82% default, AUC 83.3%) y comparativa de particiones Train / Test / OOT.
- 🎯 **Discriminación de Atributos & Storytelling:** Gráficos Cole Knaflic de tasa de mora por tenencia de vivienda y gradiente monótono por grados de crédito.
- 🛡️ **Monitor de Estabilidad Poblacional (PSI):** Matriz temporal (2013-2021) y entre particiones (todos los predictores con PSI < 0.10).
- 🔬 **Pipeline de Selección de Variables:** Documentación de las 4 reglas estadísticas y tabla detallada del set de 7 predictores.

---

## 📁 Estructura del Repositorio

```plaintext
DS-Credit_Scoring_Project/
├── run_pipeline.py                  # Orquestador raíz del pipeline analítico end-to-end
├── run_dashboard.py                 # Lanzador del dashboard web FastAPI con auto-open browser
├── run_dashboard.bat                # Acceso directo 1-clic para Windows
├── README.md                        # Documentación ejecutiva del proyecto
├── requirements.txt                 # Dependencias base del proyecto
├── default_by_ownership.png         # Gráfico ejecutivo de discriminación crediticia
│
├── dashboard/                       # Aplicación Web y Servidor de Inferencia
│   ├── server.py                    # API REST FastAPI + Scorecard ML en producción
│   └── static/                      # Frontend web en Vanilla HTML/CSS/JS (Dark Mode)
│       ├── index.html               # Interfaz semántica con 5 pestañas ejecutivas
│       ├── style.css                # Sistema de diseño Obsidian Glassmorphism
│       └── app.js                   # Lógica reactiva de simulación y gráficos Chart.js
│
└── Credit_scoring_project-main/
    ├── config.py                    # Configuración centralizada y resolución de rutas dinámicas
    ├── run_pipeline.py              # Script de ejecución modular de las 6 fases
    ├── main_data_analysis.qmd       # Cuaderno Quarto / Jupyter: Fase 1 (EDA e Ingesta)
    ├── main_data_cleaning.qmd       # Cuaderno Quarto / Jupyter: Fase 2 (Limpieza e Imputación)
    ├── main_correlations.qmd        # Cuaderno Quarto / Jupyter: Fase 3 (Correlaciones)
    ├── main_feature_discrimination_viz.qmd # Cuaderno Quarto: Fase 4 (Discriminación)
    ├── main_monotonie_stability.qmd # Cuaderno Quarto / Jupyter: Fase 5 (PSI y Monotonía)
    ├── main_variable_selection.qmd  # Cuaderno Quarto / Jupyter: Fase 6 (Selección de Variables)
    │
    ├── src/                         # Código fuente modular
    │   ├── __init__.py
    │   ├── decision_engine/         # 🏛 Motor de Decisiones Inteligente
    │   │   ├── __init__.py
    │   │   └── decision_engine.py   # Knockouts, FICO mapping, Risk-Based Pricing, IFRS 9
    │   ├── data_analysis/
    │   │   ├── __init__.py
    │   │   ├── data_analysis_utils.py          # Utilidades para reportes formateados Excel
    │   │   ├── data_cleaning.py                # Lógica de outliers e imputación
    │   │   ├── correlations.py                 # Kruskal-Wallis y matrices de correlación
    │   │   ├── feature_discrimination_plots.py # Gráficos de discriminación
    │   │   └── monotony_stability.py           # Cálculo de PSI y monotonía
    │   └── correlation/
    │       ├── __init__.py
    │       └── functions_for_var_selection.py  # Reglas de selección sobre K-Fold
    │
    ├── datasets/                    # Datasets procesados y persistidos
    │   ├── credit_risk_dataset.csv  # Dataset crudo (32,581 registros)
    │   ├── train_test_data.csv      # Conjunto histórico (2013-2021)
    │   ├── oot_data.csv             # Conjunto Out-of-Time (2022)
    │   ├── train_data.csv           # Train estratificado (80%)
    │   ├── test_data.csv            # Test estratificado (20%)
    │   ├── train_imputed.csv        # Train limpio e imputado (21,292 registros)
    │   ├── test_imputed.csv         # Test limpio e imputado (5,324 registros)
    │   ├── oot_imputed.csv          # OOT limpio e imputado (5,965 registros)
    │   ├── year_to_year.xlsx        # Reporte PSI interanual
    │   └── psi_stability.xlsx       # Reporte PSI Train vs Test vs OOT
    │
    ├── data_analysis_output/        # Salidas analíticas y reportes generados
    │   ├── eda_output/              # Reportes Excel de la Fase 1
    │   ├── data_cleaning_output/    # Tablas de distribución, outliers y nulos
    │   ├── correlation/             # Matrices Kruskal-Wallis, Spearman y Cramér
    │   └── final_selected_features.xlsx # Resumen de variables seleccionadas
    │
    └── folds/                       # Folds de validación cruzada serializados
        ├── fold_0.pkl
        ├── fold_1.pkl
        ├── fold_2.pkl
        └── fold_3.pkl
```

---

## 🛠 Requisitos e Instalación

Entorno recomendado: Python 3.10 o superior (compatible con Python 3.11, 3.12 y 3.13 en Windows, Linux y macOS).

```bash
# Clonar el repositorio
git clone https://github.com/GuillenConcepcion/DS-Credit_Scoring_Project.git
cd DS-Credit_Scoring_Project

# Instalación de dependencias del proyecto
pip install pandas numpy scipy scikit-learn matplotlib seaborn openpyxl xlsxwriter kagglehub fastapi uvicorn
```

---

## ⚡ Ejecución del Pipeline

Para ejecutar el pipeline analítico completo de punta a punta, ejecuta el orquestador principal:

```bash
python run_pipeline.py
```

El script valida automáticamente la existencia de los datos, ejecuta secuencialmente las 6 fases analíticas en menos de **5 segundos**, genera los reportes tabulares y gráficos, y presenta el resumen de variables seleccionadas en consola con codificación UTF-8 garantizada.

---

## 📊 Resultados Clave y Artefactos

1. **Estabilidad Poblacional Comprobada (PSI < 0.10):**
   | Variable | PSI Train vs Test | PSI Train vs OOT | PSI Test vs OOT | Diagnóstico Regulatorio |
   | :--- | :---: | :---: | :---: | :---: |
   | `person_income` | 0.0010 | 0.0184 | 0.0113 | ✅ Estable |
   | `person_emp_length` | 0.0006 | 0.0136 | 0.0087 | ✅ Estable |
   | `loan_int_rate` | 0.0000 | 0.0001 | 0.0001 | ✅ Estable |
   | `loan_percent_income` | 0.0002 | 0.0020 | 0.0010 | ✅ Estable |
   | `home_ownership_3` | 0.0002 | 0.0034 | 0.0020 | ✅ Estable |
   | `cb_person_default_on_file` | 0.0000 | 0.0001 | 0.0002 | ✅ Estable |

2. **Poder Predictivo del Scorecard:**
   - **Test AUC:** `0.8329`
   - **Test Gini:** `0.6658`
   - **Brier Score:** `0.1261`

3. **Artefactos Principales Generados:**
   - [intelligent_decision_engine.md](file:///C:/Users/Guillen/.gemini/antigravity-ide/brain/ab9db139-4b31-466b-9e8f-a7b9022821a2/intelligent_decision_engine.md): Especificación técnica del motor de decisiones y políticas de riesgo.
   - [final_selected_features.xlsx](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/data_analysis_output/final_selected_features.xlsx): Listado consolidado de variables candidatas.
   - [dataset_default_distribution.xlsx](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/data_analysis_output/data_cleaning_output/dataset_default_distribution.xlsx): Métricas de partición y tasas de default.
   - [default_by_ownership.png](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/default_by_ownership.png): Gráfico ejecutivo de discriminación crediticia.

---

## 🛡 Buenas Prácticas MLOps y Gobernanza

- **Reproducibilidad Garantizada:** Semillas pseudo-aleatorias fijadas (`random_state=42`) en todas las operaciones estocásticas (particiones y K-Fold).
- **Aislamiento Antifuga (*No Data Leakage*):** Todos los estadísticos de imputación, límites de outliers y validaciones cruzadas se calculan de forma estricta sobre la muestra de entrenamiento correspondiente.
- **Rutas Relativas y Portabilidad:** Soporte dinámico para Windows, macOS y Linux mediante `pathlib.Path` en [config.py](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/config.py).
- **Consistencia UTF-8 Multiplataforma:** Reconfiguración de streams de salida para evitar fallos de serialización en consolas Windows con códec `cp1252`.
- **Código Modular y Tipado:** Arquitectura orientada a objetos en [decision_engine.py](file:///d:/LabD/DS-Credit_Scoring_Project/Credit_scoring_project-main/src/decision_engine/decision_engine.py) con *dataclasses*, enumeraciones tipadas y separación estricta de responsabilidades entre ingesta, modelado y decisión.
