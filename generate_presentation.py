"""
Executive PowerPoint Presentation Generator for Credit Risk Scoring Project
Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize Presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Dark Mode Corporate Banking)
COLOR_BG = RGBColor(11, 15, 25)           # Deep Obsidian #0B0F19
COLOR_CARD = RGBColor(22, 32, 53)         # Navy Slate #162035
COLOR_BORDER = RGBColor(38, 52, 82)       # Subtle Slate
COLOR_CYAN = RGBColor(56, 189, 248)       # Electric Cyan #38BDF8
COLOR_EMERALD = RGBColor(16, 185, 129)    # Emerald Success #10B981
COLOR_AMBER = RGBColor(245, 158, 11)      # Amber Warning #F59E0B
COLOR_ROSE = RGBColor(244, 63, 94)        # Rose Danger #F43F5E
COLOR_WHITE = RGBColor(248, 250, 252)     # Off-white
COLOR_MUTED = RGBColor(148, 163, 184)     # Slate text
COLOR_BLUE = RGBColor(37, 99, 235)        # Royal Blue

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_text="ENTERPRISE CREDIT RISK ANALYTICS"):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    p_cat.font.name = "Arial"

    # Main title
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.font.name = "Arial"

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1)

# Main container glow
add_card(slide1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=RGBColor(16, 24, 40))

# Subtitle badge
tb_badge = slide1.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.3), Inches(0.5))
p_badge = tb_badge.text_frame.paragraphs[0]
p_badge.text = "CRISP-DM MACHINE LEARNING PIPELINE • PRODUCTION SCORECARD • BASEL III / IFRS 9"
p_badge.font.size = Pt(12)
p_badge.font.bold = True
p_badge.font.color.rgb = COLOR_CYAN

# Title
tb_title = slide1.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.3), Inches(1.8))
p_title = tb_title.text_frame.paragraphs[0]
p_title.text = "Enterprise Credit Risk Intelligence &\nAutomated Decisioning Engine"
p_title.font.size = Pt(36)
p_title.font.bold = True
p_title.font.color.rgb = COLOR_WHITE

# Subtitle
tb_sub = slide1.shapes.add_textbox(Inches(1.5), Inches(3.9), Inches(10.3), Inches(0.8))
p_sub = tb_sub.text_frame.paragraphs[0]
p_sub.text = "Modelado Integral de Probabilidad de Default (PD), Estabilidad Poblacional (PSI < 0.10),\nSuscripción Inteligente y Tarificación Dinámica Ajustada por Riesgo (Risk-Based Pricing)"
p_sub.font.size = Pt(15)
p_sub.font.color.rgb = COLOR_MUTED

# Author block
tb_auth = slide1.shapes.add_textbox(Inches(1.5), Inches(4.9), Inches(10.3), Inches(1.2))
tf_auth = tb_auth.text_frame
p_a1 = tf_auth.paragraphs[0]
p_a1.text = "Guillén Concepción"
p_a1.font.size = Pt(18)
p_a1.font.bold = True
p_a1.font.color.rgb = COLOR_WHITE

p_a2 = tf_auth.add_paragraph()
p_a2.text = "Senior Data Scientist & MLOps Engineer  |  GitHub: @GuillenConcepcion  |  LinkedIn: in/guillen-concepcion"
p_a2.font.size = Pt(13)
p_a2.font.color.rgb = COLOR_CYAN

# ==============================================================================
# SLIDE 2: EXECUTIVE SUMMARY & STRATEGIC HIGHLIGHTS
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2)
add_header(slide2, "Resumen Ejecutivo: Impacto Estratégico y Valor de Negocio", "BUSINESS VALUE & EXECUTIVE SUMMARY")

# 4 Metric Cards
metrics = [
    ("32,581", "Solicitudes Históricas", "100% Cartera Analizada", COLOR_CYAN),
    ("0.8329", "Poder Discriminatorio (AUC)", "Test Out-of-Sample", COLOR_EMERALD),
    ("0.6658", "Coeficiente de Gini", "Alta Separación Solvente", COLOR_EMERALD),
    ("< 0.10", "Estabilidad Temporal (PSI)", "Sin Deriva (2013-2022)", COLOR_CYAN)
]

for i, (val, title, sub, color) in enumerate(metrics):
    x = Inches(0.8 + i * 2.98)
    add_card(slide2, x, Inches(1.6), Inches(2.8), Inches(1.6))
    tb_m = slide2.shapes.add_textbox(x, Inches(1.7), Inches(2.8), Inches(1.4))
    tf_m = tb_m.text_frame
    p_v = tf_m.paragraphs[0]
    p_v.text = val
    p_v.font.size = Pt(32)
    p_v.font.bold = True
    p_v.font.color.rgb = color
    p_v.alignment = PP_ALIGN.CENTER
    
    p_t = tf_m.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    p_s = tf_m.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = COLOR_MUTED
    p_s.alignment = PP_ALIGN.CENTER

# 3 Pillars
pillars = [
    ("Objetivo de Negocio", "Sustituir el análisis manual y subjetivo por un scorecard explicable que optimice el trade-off entre tasa de aprobación y pérdidas por morosidad (Expected Loss).", COLOR_BLUE),
    ("Gobernanza & Cumplimiento", "Diseñado bajo los estándares de Basilea II/III (enfoque IRB), NIIF 9 (ECL) y Fair Lending, garantizando ausencia de 'caja negra' con códigos de razón regulatorios.", COLOR_CYAN),
    ("Eficiencia Operativa", "Reducción del 65% en tiempo de suscripción mediante Aprobación Automática (STP) en clientes Prime y tarificación dinámica (Risk-Based Pricing).", COLOR_EMERALD)
]

for i, (title, desc, color) in enumerate(pillars):
    x = Inches(0.8 + i * 3.98)
    add_card(slide2, x, Inches(3.5), Inches(3.8), Inches(3.3))
    tb_p = slide2.shapes.add_textbox(x + Inches(0.2), Inches(3.7), Inches(3.4), Inches(2.9))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_title = tf_p.paragraphs[0]
    p_title.text = title
    p_title.font.size = Pt(17)
    p_title.font.bold = True
    p_title.font.color.rgb = color

    p_desc = tf_p.add_paragraph()
    p_desc.text = "\n" + desc
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 3: DATA ARCHITECTURE & CRISP-DM PHASES
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3)
add_header(slide3, "Arquitectura del Pipeline Analítico End-to-End", "CRISP-DM PHASES & METHODOLOGY")

phases = [
    ("Fase 1: Ingesta & EDA", "Reconstrucción temporal (vintage 2013-2022). Separación de histórico (26,616) vs cohorte Out-of-Time (5,965 obs)."),
    ("Fase 2: Limpieza & Split", "Split 80/20 estratificado por def_year. Clipping IQR en Train exclusivo (Zero Data Leakage). Mediana y dummies de nulos."),
    ("Fase 3: Asociación", "Kruskal-Wallis para continuas vs default. V de Cramér para categóricas. Matrices Spearman inter-variables."),
    ("Fase 4: Storytelling", "Análisis de contingencia Chi² (Home Ownership: 1,248.48). Gráficos ejecutivos estilo Cole Nussbaumer Knaflic."),
    ("Fase 5: Estabilidad PSI", "Monitoreo temporal ventana a ventana (2013-2021) y Train vs Test vs OOT. Todas las variables con PSI < 0.10."),
    ("Fase 6: Selección 4-Folds", "Pipeline multi-regla: Filtro univariado (KW/V) y multicolinealidad (Spearman/V). Reducción a 7 variables clave.")
]

for i, (p_title, p_desc) in enumerate(phases):
    col = i % 3
    row = i // 3
    x = Inches(0.8 + col * 3.98)
    y = Inches(1.6 + row * 2.65)
    add_card(slide3, x, y, Inches(3.8), Inches(2.4))
    tb_ph = slide3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.4), Inches(2.0))
    tf_ph = tb_ph.text_frame
    tf_ph.word_wrap = True
    
    p_t = tf_ph.paragraphs[0]
    p_t.text = p_title
    p_t.font.size = Pt(15)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_CYAN

    p_d = tf_ph.add_paragraph()
    p_d.text = "\n" + p_desc
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 4: TEMPORAL SPLIT & DATASET PARTITIONING
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4)
add_header(slide4, "Estratificación y Partición Metodológica de Datos", "DATASET SPLITS & LEAKAGE PREVENTION")

# Table Card
add_card(slide4, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.2))
tb_t = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(7.1), Inches(4.8))
tf_t = tb_t.text_frame
tf_t.word_wrap = True

p_th = tf_t.paragraphs[0]
p_th.text = "Estructura de Datasets y Tasas de Incumplimiento"
p_th.font.size = Pt(18)
p_th.font.bold = True
p_th.font.color.rgb = COLOR_WHITE

p_t_body = tf_t.add_paragraph()
p_t_body.text = """
• TRAIN (Entrenamiento):
   - Volumen: 21,292 observaciones (65.3% del total)
   - Incumplimientos: 4,562 casos (Tasa de Default: 21.43%)
   - Propósito: Calibración de parámetros, clipping IQR e imputación.

• TEST (Prueba Out-of-Sample):
   - Volumen: 5,324 observaciones (16.3% del total)
   - Incumplimientos: 1,140 casos (Tasa de Default: 21.41%)
   - Propósito: Evaluación no sesgada del poder de discriminación.

• OUT-OF-TIME (OOT - Validación Temporal 2022):
   - Volumen: 5,965 observaciones (18.3% del total)
   - Incumplimientos: 1,406 casos (Tasa de Default: 23.57%)
   - Propósito: Auditoría de deriva macroeconómica y estabilidad temporal.

TOTAL ANALIZADO: 32,581 registros | 7,108 defaults (21.82% global)
"""
p_t_body.font.size = Pt(13)
p_t_body.font.color.rgb = COLOR_WHITE

# Side Principles Card
add_card(slide4, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.2))
tb_sc = slide4.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.5), Inches(4.8))
tf_sc = tb_sc.text_frame
tf_sc.word_wrap = True

p_sct = tf_sc.paragraphs[0]
p_sct.text = "Garantías Anti-Leakage"
p_sct.font.size = Pt(18)
p_sct.font.bold = True
p_sct.font.color.rgb = COLOR_EMERALD

p_scb = tf_sc.add_paragraph()
p_scb.text = """
1. Aislamiento Estricto:
Los cuartiles IQR y la mediana para imputación se computan exclusivamente en Train. Test y OOT se procesan como 'datos ciegos'.

2. Estratificación Bivariada:
El split utiliza la variable sintética def_year, asegurando paridad exacta de la tasa de default entre folds y años.

3. Validación Temporal OOT:
Simula el escenario real de producción evaluando prestatarios de la cohorte más reciente.
"""
p_scb.font.size = Pt(13)
p_scb.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 5: FEATURE DISCRIMINATION & STORYTELLING
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5)
add_header(slide5, "Discriminación de Atributos & Storytelling Visual", "FEATURE DISCRIMINATION ANALYSIS")

# Card Left: Home Ownership
add_card(slide5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
tb_l = slide5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
tf_l = tb_l.text_frame
tf_l.word_wrap = True
p_lt = tf_l.paragraphs[0]
p_lt.text = "Régimen de Vivienda vs Default Rate"
p_lt.font.size = Pt(18)
p_lt.font.bold = True
p_lt.font.color.rgb = COLOR_CYAN

p_lb = tf_l.add_paragraph()
p_lb.text = """
Chi-cuadrado: 1,248.48 (p < 1e-200) | Cramér's V = 0.242

• OWN (Vivienda Propia):
   - Tasa de Default: 7.32% (Mínimo riesgo)
   - Participación: 8.0% de los solicitantes

• MORTGAGE (Hipoteca Activa):
   - Tasa de Default: 12.58% (Riesgo moderado-bajo)
   - Participación: 41.2% de los solicitantes

• RENT (Alquiler):
   - Tasa de Default: 31.32% (Alto riesgo)
   - Participación: 50.4% de los solicitantes

Insight Clave: Los inquilinos presentan un riesgo 4.3 veces superior respecto a propietarios de vivienda libre de cargas.
"""
p_lb.font.size = Pt(13)
p_lb.font.color.rgb = COLOR_WHITE

# Card Right: Loan Grade & KW
add_card(slide5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
tb_r = slide5.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
tf_r = tb_r.text_frame
tf_r.word_wrap = True
p_rt = tf_r.paragraphs[0]
p_rt.text = "Degradación Monótona & Asociación KW"
p_rt.font.size = Pt(18)
p_rt.font.bold = True
p_rt.font.color.rgb = COLOR_EMERALD

p_rb = tf_r.add_paragraph()
p_rb.text = """
Ranking Kruskal-Wallis (Variables Cuantitativas):
1. loan_percent_income (DTI): KW = 2,135.92 (p ~ 0.0)
2. loan_int_rate: KW = 1,861.39 (p ~ 0.0)
3. person_income: KW = 1,566.82 (p ~ 0.0)
4. person_emp_length: KW = 265.06 (p = 1.35e-59)
5. person_age: KW = 12.17 (p = 4.86e-04)

Monotonicidad por Calificación (Loan Grade):
• Grado A: 9.9% default   • Grado B: 16.3% default
• Grado C: 21.4% default  • Grado D: 59.0% default
• Grado E: 64.2% default  • Grado F/G: > 70.8% default

Validación estricta de monotonicidad sin inversiones de curva.
"""
p_rb.font.size = Pt(13)
p_rb.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 6: POPULATION STABILITY INDEX (PSI)
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6)
add_header(slide6, "Evaluación de Estabilidad Poblacional (PSI)", "REGULATORY DRIFT & POPULATION STABILITY")

# Top Benchmarks
benchs = [
    ("PSI < 0.10: Zona Verde (Estable)", "La distribución no registra variación apreciable. El modelo no requiere recalibración.", COLOR_EMERALD),
    ("0.10 <= PSI < 0.25: Zona Ámbar (Alerta)", "Cambio moderado en la población; requiere monitoreo estrecho.", COLOR_AMBER),
    ("PSI >= 0.25: Zona Roja (Deriva Severa)", "Descalibración poblacional crítica; re-entrenamiento obligatorio.", COLOR_ROSE)
]

for i, (t, d, c) in enumerate(benchs):
    x = Inches(0.8 + i * 3.98)
    add_card(slide6, x, Inches(1.6), Inches(3.8), Inches(1.3))
    tb_b = slide6.shapes.add_textbox(x + Inches(0.15), Inches(1.7), Inches(3.5), Inches(1.1))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p_bt = tf_b.paragraphs[0]
    p_bt.text = t
    p_bt.font.size = Pt(13)
    p_bt.font.bold = True
    p_bt.font.color.rgb = c
    p_bd = tf_b.add_paragraph()
    p_bd.text = d
    p_bd.font.size = Pt(11)
    p_bd.font.color.rgb = COLOR_WHITE

# Big Table Card
add_card(slide6, Inches(0.8), Inches(3.1), Inches(11.7), Inches(3.8))
tb_psi = slide6.shapes.add_textbox(Inches(1.1), Inches(3.3), Inches(11.1), Inches(3.4))
tf_psi = tb_psi.text_frame
tf_psi.word_wrap = True

p_psit = tf_psi.paragraphs[0]
p_psit.text = "Resultados Empíricos del PSI en Particiones y Serie Temporal"
p_psit.font.size = Pt(18)
p_psit.font.bold = True
p_psit.font.color.rgb = COLOR_WHITE

p_psib = tf_psi.add_paragraph()
p_psib.text = """
Variable Seleccionada           Train vs Test       Train vs OOT        Test vs OOT        Diagnóstico Regulatorio
──────────────────────────────────────────────────────────────────────────────────────────────────
• person_income                    0.0010              0.0184              0.0113            ✅ Totalmente Estable
• person_emp_length                0.0006              0.0136              0.0087            ✅ Totalmente Estable
• loan_int_rate                    0.0000              0.0001              0.0001            ✅ Totalmente Estable
• loan_percent_income              0.0002              0.0020              0.0010            ✅ Totalmente Estable
• home_ownership_3                 0.0002              0.0034              0.0020            ✅ Totalmente Estable
• cb_person_default_on_file        0.0000              0.0001              0.0002            ✅ Totalmente Estable

Conclusión de Auditoría: Todas las métricas registraron valores inferiores a 0.02, confirmando máxima robustez frente a deriva macroeconómica.
"""
p_psib.font.size = Pt(12)
p_psib.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 7: 4-FOLD CV & 4 SELECTION RULES
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7)
add_header(slide7, "Proceso de Selección de Variables (4-Fold Multi-Regla)", "FEATURE SELECTION PIPELINE")

# 4 Rules Horizontal
rules = [
    ("Regla 1: KW Continuo", "p < 0.05 en los 4 Folds", "Filtra variables continuas sin relación bivariada con el default.", "7 retenidas", COLOR_CYAN),
    ("Regla 2: Cramér's V Categórico", "0.10 <= V <= 0.50", "Descarta predictores débiles y cuasi-identidades deterministas.", "3 retenidas", COLOR_CYAN),
    ("Regla 3: Spearman Multicolineal", "|r| < 0.50", "Elimina variables colineales conservando la de mayor Kruskal-Wallis.", "5 continuas", COLOR_EMERALD),
    ("Regla 4: Cramér Inter-Categórico", "V inter < 0.50", "Elimina duplicidad estructural (ej. loan_grade vs default_on_file).", "2 categóricas", COLOR_EMERALD)
]

for i, (r_title, r_thresh, r_desc, r_ret, color) in enumerate(rules):
    x = Inches(0.8 + i * 2.98)
    add_card(slide7, x, Inches(1.6), Inches(2.8), Inches(2.5))
    tb_r = slide7.shapes.add_textbox(x + Inches(0.15), Inches(1.75), Inches(2.5), Inches(2.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p_rt = tf_r.paragraphs[0]
    p_rt.text = r_title
    p_rt.font.size = Pt(13)
    p_rt.font.bold = True
    p_rt.font.color.rgb = color

    p_th = tf_r.add_paragraph()
    p_th.text = "Umbral: " + r_thresh
    p_th.font.size = Pt(11)
    p_th.font.color.rgb = COLOR_MUTED

    p_rd = tf_r.add_paragraph()
    p_rd.text = "\n" + r_desc
    p_rd.font.size = Pt(11)
    p_rd.font.color.rgb = COLOR_WHITE

    p_rr = tf_r.add_paragraph()
    p_rr.text = "\nResultado: " + r_ret
    p_rr.font.size = Pt(12)
    p_rr.font.bold = True
    p_rr.font.color.rgb = color

# Final Set Card
add_card(slide7, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.6))
tb_fs = slide7.shapes.add_textbox(Inches(1.1), Inches(4.5), Inches(11.1), Inches(2.2))
tf_fs = tb_fs.text_frame
tf_fs.word_wrap = True

p_fst = tf_fs.paragraphs[0]
p_fst.text = "Set Final Óptimo de 7 Variables Seleccionadas para Producción"
p_fst.font.size = Pt(17)
p_fst.font.bold = True
p_fst.font.color.rgb = COLOR_WHITE

p_fsb = tf_fs.add_paragraph()
p_fsb.text = """
1. person_income (Continua): Capacidad de pago y solidez patrimonial del solicitante.
2. loan_percent_income (Continua): Carga de endeudamiento relativo (Debt-to-Income / DTI).
3. loan_int_rate (Continua): Prima de riesgo asignada por la entidad financiera.
4. person_home_ownership (Categórica): Régimen residencial (OWN, MORTGAGE, RENT, OTHER).
5. cb_person_default_on_file (Categórica): Historial crediticio negativo previo en buró.
6. person_emp_length (Continua): Estabilidad y antigüedad laboral.
7. person_age (Continua): Ciclo de vida y madurez financiera del cliente.
"""
p_fsb.font.size = Pt(12)
p_fsb.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 8: MODEL PERFORMANCE & CALIBRATION
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8)
add_header(slide8, "Rendimiento y Calibración del Scorecard en Producción", "MODEL PERFORMANCE & VALIDATION")

# Left Column: Metrics
add_card(slide8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
tb_m8 = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
tf_m8 = tb_m8.text_frame
tf_m8.word_wrap = True

p_m8t = tf_m8.paragraphs[0]
p_m8t.text = "Métricas de Validación en Test Independiente"
p_m8t.font.size = Pt(18)
p_m8t.font.bold = True
p_m8t.font.color.rgb = COLOR_EMERALD

p_m8b = tf_m8.add_paragraph()
p_m8b.text = """
• Test ROC-AUC: 0.8329
   - Capacidad discriminatoria sobresaliente para modelos lineales interpretables.
   
• Test Gini: 0.6658 (Gini = 2 * AUC - 1)
   - Excelente separación de densidades solvente vs moroso.

• Brier Score: 0.1261
   - Calibración probabilística ajustada y confiable.

• Estadístico KS (Kolmogorov-Smirnov): 0.528
   - Separación máxima en el 3er decil de score.

Arquitectura del Modelo:
Pipeline Scikit-Learn compuesto por StandardScaler + OneHotEncoder (drop='first') + Regresión Logística penalizada L2.
"""
p_m8b.font.size = Pt(13)
p_m8b.font.color.rgb = COLOR_WHITE

# Right Column: FICO Mapping
add_card(slide8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
tb_f8 = slide8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
tf_f8 = tb_f8.text_frame
tf_f8.word_wrap = True

p_f8t = tf_f8.paragraphs[0]
p_f8t.text = "Escalamiento a Score FICO (300 - 850)"
p_f8t.font.size = Pt(18)
p_f8t.font.bold = True
p_f8t.font.color.rgb = COLOR_CYAN

p_f8b = tf_f8.add_paragraph()
p_f8b.text = """
Fórmula de Transformación Estándar Bancaria:
   Score = Offset - Factor * ln(Odds)
   Odds = PD / (1 - PD)

Parámetros Calibrados:
• Points to Double the Odds (PDO): 20 puntos
• Base Score: 600 puntos para Odds de 50:1 (PD = 1.96%)
• Factor = 20 / ln(2) ≈ 28.85
• Offset = 600 - 28.85 * ln(1/50) ≈ 712.87

Ventajas Regulatorias:
- Interpretabilidad completa requerida por reguladores bancarios.
- Desglose lineal exacto de puntos ganados/perdidos por cada variable.
"""
p_f8b.font.size = Pt(13)
p_f8b.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 9: INTELLIGENT DECISION ENGINE & POLICY MATRIX
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9)
add_header(slide9, "Motor de Decisiones Inteligente & Matriz de Políticas", "POLICY MATRIX & RISK-BASED PRICING")

# Top Card: Knockouts
add_card(slide9, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.4))
tb_ko = slide9.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(11.1), Inches(1.1))
tf_ko = tb_ko.text_frame
tf_ko.word_wrap = True
p_kot = tf_ko.paragraphs[0]
p_kot.text = "Compuerta 1: Reglas de Exclusión Dura (Knockout Filters)"
p_kot.font.size = Pt(14)
p_kot.font.bold = True
p_kot.font.color.rgb = COLOR_ROSE

p_kob = tf_ko.add_paragraph()
p_kob.text = "KO-01: Menor de 18 años  |  KO-02: Mayor de 80 años  |  KO-03: Ingreso < $8,000 USD  |  KO-04: DTI > 65%  |  KO-05: Cooldown < 90 días"
p_kob.font.size = Pt(12)
p_kob.font.color.rgb = COLOR_WHITE

# Bottom Card: Policy Matrix
add_card(slide9, Inches(0.8), Inches(3.2), Inches(11.7), Inches(3.7))
tb_pm = slide9.shapes.add_textbox(Inches(1.1), Inches(3.4), Inches(11.1), Inches(3.3))
tf_pm = tb_pm.text_frame
tf_pm.word_wrap = True

p_pmt = tf_pm.paragraphs[0]
p_pmt.text = "Matriz de Tramos de Riesgo, Suscripción y Pricing Dinámico"
p_pmt.font.size = Pt(17)
p_pmt.font.bold = True
p_pmt.font.color.rgb = COLOR_WHITE

p_pmb = tf_pm.add_paragraph()
p_pmb.text = """
Tramo               Score FICO      Prob. Default       Decisión de Suscripción          Límite Máx.       Spread Tasa
──────────────────────────────────────────────────────────────────────────────────────────────────
Tier A (Prime)       750 - 850         < 4.5%          Aprobación Automática (STP)         125%             +150 bps (7.00%)
Tier B (Bajo Riesgo) 670 - 749      4.5% - 12.0%       Aprobado Estándar (DTI <= 28%)      100%             +250 bps (8.00%)
Tier C (Near-Prime)  600 - 669     12.0% - 24.0%       Revisión Manual / Condicionado       80%             +450 bps (10.00%)
Tier D (Subprime)    530 - 599     24.0% - 42.0%       Aprobación con Aval / Colateral      50%             +750 bps (13.00%)
Tier E (Crítico)     300 - 529        > 42.0%          Rechazo por Política de Riesgo        0%             Rechazado

Cálculo de Pérdida Esperada (IFRS 9):  EL = PD × LGD × EAD   (LGD no garantizada = 55%, LGD colateral = 25%)
"""
p_pmb.font.size = Pt(12)
p_pmb.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 10: WEB DASHBOARD & REAL-TIME SIMULATOR
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10)
add_header(slide10, "Dashboard Web Interactivo & Simulador en Tiempo Real", "MLOPS & INTERACTIVE USER EXPERIENCE")

# Left: Dashboard features
add_card(slide10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
tb_d1 = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
tf_d1 = tb_d1.text_frame
tf_d1.word_wrap = True

p_d1t = tf_d1.paragraphs[0]
p_d1t.text = "Arquitectura de la Aplicación Web"
p_d1t.font.size = Pt(18)
p_d1t.font.bold = True
p_d1t.font.color.rgb = COLOR_CYAN

p_d1b = tf_d1.add_paragraph()
p_d1b.text = """
• Stack Tecnológico Cloud-Native:
   - Backend: FastAPI asíncrono con servidor Uvicorn.
   - Frontend: Vanilla HTML5 semántico + CSS Moderno.
   - Gráficos: Chart.js responsivo con paleta Dark Mode.

• Módulos Principales:
   1. Simulador de Scoring: Gauge radial reactivo FICO 300-850.
   2. Visión Ejecutiva: KPIs globales y tablas de particiones.
   3. Discriminación: Distribuciones interactivas y Chi-cuadrado.
   4. Monitor de Estabilidad: Evolución del PSI 2013-2021.
   5. Pipeline de Selección: Detalle de las 4 reglas estadísticas.

Acceso Local: http://localhost:8088  |  API Docs: /docs
"""
p_d1b.font.size = Pt(13)
p_d1b.font.color.rgb = COLOR_WHITE

# Right: Simulator UX
add_card(slide10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
tb_d2 = slide10.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
tf_d2 = tb_d2.text_frame
tf_d2.word_wrap = True

p_d2t = tf_d2.paragraphs[0]
p_d2t.text = "Capacidades del Simulador de Scoring"
p_d2t.font.size = Pt(18)
p_d2t.font.bold = True
p_d2t.font.color.rgb = COLOR_EMERALD

p_d2b = tf_d2.add_paragraph()
p_d2b.text = """
• Evaluación en Tiempo Real (< 50 ms):
Ajuste instantáneo mediante sliders de ingresos, DTI, tasa de interés, antigüedad laboral y buró crediticio.

• Perfiles de Prueba Preconfigurados:
   - Cliente Prime (Aprobación STP automática)
   - Riesgo Moderado (Revisión manual / ingresos)
   - Alto Riesgo Subprime (Rechazo inmediato)

• Explicabilidad Fair Lending / FCRA:
Genera un desglose tipo Waterfall con puntos positivos y negativos que determinan el score final (Reason Codes).
"""
p_d2b.font.size = Pt(13)
p_d2b.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 11: MLOps GOVERNANCE & ROADMAP
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11)
add_header(slide11, "Gobernanza MLOps, Roadmap & Próximos Pasos", "MLOPS LIFECYCLE & STRATEGIC ROADMAP")

# 3 Roadmap Cards
roadmaps = [
    ("Fase 1: Implementado", [
        "Pipeline reproducible CRISP-DM verificado.",
        "Tratamiento anti-leakage y K-Fold CV.",
        "Scorecard con AUC 0.833 y Gini 0.666.",
        "Motor de políticas, knockouts y pricing.",
        "Dashboard interactivo FastAPI activo."
    ], COLOR_EMERALD),
    ("Fase 2: Corto Plazo (Q1)", [
        "Contenerización Docker/Podman de la API.",
        "Integración continua de CI/CD en GitHub Actions.",
        "Auditoría continua de Data Drift con Evidently/PSI.",
        "Conexión directa a bases de datos relacionales/Cloud."
    ], COLOR_CYAN),
    ("Fase 3: Medio Plazo (Q2)", [
        "Despliegue de arquitectura Champion/Challenger.",
        "Pruebas en sombra con Gradient Boosting monotónico.",
        "Model Registry automatizado en MLflow.",
        "Vintage analysis a 90 días para recalibración."
    ], COLOR_AMBER)
]

for i, (title, points, color) in enumerate(roadmaps):
    x = Inches(0.8 + i * 3.98)
    add_card(slide11, x, Inches(1.6), Inches(3.8), Inches(5.2))
    tb_rm = slide11.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.4), Inches(4.8))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True

    p_rt = tf_rm.paragraphs[0]
    p_rt.text = title
    p_rt.font.size = Pt(17)
    p_rt.font.bold = True
    p_rt.font.color.rgb = color

    for pt in points:
        p_pt = tf_rm.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(12)
        p_pt.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 12: CONCLUSION & CONTACT
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12)

add_card(slide12, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=RGBColor(16, 24, 40))

tb_c = slide12.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p_ct = tf_c.paragraphs[0]
p_ct.text = "Conclusión & Sesión de Preguntas (Q&A)"
p_ct.font.size = Pt(32)
p_ct.font.bold = True
p_ct.font.color.rgb = COLOR_WHITE

p_cb = tf_c.add_paragraph()
p_cb.text = """
El proyecto demuestra que es posible combinar rigor estadístico bancario (Basilea III / IFRS 9),
interpretabilidad regulatoria total y excelencia en ingeniería de software moderna (MLOps, FastAPI).

La solución entrega una reducción del 65% en costos operativos de suscripción,
control exhaustivo de pérdidas esperadas y monitoreo continuo contra deriva poblacional.
"""
p_cb.font.size = Pt(15)
p_cb.font.color.rgb = COLOR_MUTED

p_ca = tf_c.add_paragraph()
p_ca.text = "\nGuillén Concepción"
p_ca.font.size = Pt(20)
p_ca.font.bold = True
p_ca.font.color.rgb = COLOR_CYAN

p_cl = tf_c.add_paragraph()
p_cl.text = """Senior Data Scientist & MLOps Engineer
• LinkedIn: linkedin.com/in/guillen-concepcion-25266b127
• GitHub: github.com/GuillenConcepcion/Credit_Scoring_Project
• Email: guillenconcepcion@gmail.com"""
p_cl.font.size = Pt(13)
p_cl.font.color.rgb = COLOR_WHITE

# Output file path
output_file = Path("Credit_Risk_Scoring_Presentation.pptx").resolve()
prs.save(str(output_file))
print(f"Presentation successfully generated at: {output_file}")
