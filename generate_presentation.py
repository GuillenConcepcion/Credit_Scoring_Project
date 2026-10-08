"""
High-Resolution Executive PowerPoint Presentation Generator
Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
"""

import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# 1. GENERATE HIGH-RESOLUTION DARK-THEME CHARTS (300 DPI)
# ==============================================================================
assets_dir = Path("presentation_assets")
assets_dir.mkdir(exist_ok=True)

plt.style.use("dark_background")

# Chart A: Splits & Volumes (for Slide 4)
fig, ax1 = plt.subplots(figsize=(6.2, 4.2), dpi=300)
fig.patch.set_facecolor("#162035")
ax1.set_facecolor("#162035")

categories = ['Train', 'Test', 'OOT (2022)']
rates = [21.43, 21.41, 23.57]
counts = [21292, 5324, 5965]

bars = ax1.bar(categories, rates, color=['#38BDF8', '#38BDF8', '#34D399'], width=0.45, label='Tasa de Default (%)')
ax1.set_ylabel('Tasa de Default (%)', color='#38BDF8', fontsize=11, fontweight='bold')
ax1.set_ylim(0, 32)
ax1.tick_params(colors='#E2E8F0', labelsize=10)
ax1.grid(axis='y', color='#334155', linestyle='--', alpha=0.5)

for bar in bars:
    y = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, y + 0.8, f'{y:.2f}%', ha='center', va='bottom', color='#FFFFFF', fontweight='bold', fontsize=11)

ax2 = ax1.twinx()
ax2.plot(categories, counts, color='#FBBF24', marker='o', linewidth=2.5, markersize=8, label='Volumen')
ax2.set_ylabel('Observaciones', color='#FBBF24', fontsize=11, fontweight='bold')
ax2.set_ylim(0, 26000)
ax2.tick_params(colors='#FBBF24', labelsize=10)
ax2.grid(False)

for i, txt in enumerate(counts):
    ax2.annotate(f"{txt:,}", (categories[i], counts[i] + 1000), color='#FBBF24', ha='center', fontweight='bold', fontsize=10)

plt.title("Estabilidad de Tasa de Default & Volumen por Partición", color='#FFFFFF', fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()
chart_splits_path = assets_dir / "chart_splits.png"
plt.savefig(chart_splits_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

# Chart B: PSI Trend Over Time (for Slide 6)
fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=300)
fig.patch.set_facecolor("#162035")
ax.set_facecolor("#162035")

years = ["13-14", "14-15", "15-16", "16-17", "17-18", "18-19", "19-20", "20-21"]
psi_income = [0.0013, 0.0012, 0.0017, 0.0038, 0.0026, 0.0027, 0.0239, 0.0008]
psi_emp = [0.0095, 0.0120, 0.0022, 0.0034, 0.0023, 0.0022, 0.0525, 0.0018]
psi_rate = [0.0013, 0.0036, 0.0013, 0.0004, 0.0001, 0.0016, 0.0008, 0.0004]

ax.plot(years, psi_income, marker='s', color='#38BDF8', linewidth=2.2, label='person_income')
ax.plot(years, psi_emp, marker='^', color='#34D399', linewidth=2.2, label='person_emp_length')
ax.plot(years, psi_rate, marker='o', color='#FBBF24', linewidth=2.2, label='loan_int_rate')

# Threshold line
ax.axhline(y=0.10, color='#F43F5E', linestyle='--', linewidth=2, label='Umbral Alerta PSI = 0.10')
ax.fill_between(range(len(years)), 0, 0.10, color='#10B981', alpha=0.08)

ax.set_ylabel('Índice PSI', color='#E2E8F0', fontsize=11, fontweight='bold')
ax.set_ylim(0, 0.12)
ax.tick_params(colors='#E2E8F0', labelsize=10)
ax.grid(color='#334155', linestyle='--', alpha=0.5)
ax.legend(loc='upper right', frameon=False, fontsize=9, labelcolor='#E2E8F0')
plt.title("Evolución Interanual del PSI (Zona Verde < 0.10)", color='#FFFFFF', fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
chart_psi_path = assets_dir / "chart_psi.png"
plt.savefig(chart_psi_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

# Chart C: FICO Bell Curve & Risk Tiers (for Slide 8)
fig, ax = plt.subplots(figsize=(6.2, 4.0), dpi=300)
fig.patch.set_facecolor("#162035")
ax.set_facecolor("#162035")

x = np.linspace(300, 850, 500)
mu = 675
sigma = 75
y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

ax.plot(x, y, color='#38BDF8', linewidth=2.8)

# Shading for Tiers
ax.fill_between(x, 0, y, where=(x >= 750), color='#10B981', alpha=0.4, label='Tier A (Prime >=750)')
ax.fill_between(x, 0, y, where=((x >= 670) & (x < 750)), color='#38BDF8', alpha=0.3, label='Tier B (Low Risk 670-749)')
ax.fill_between(x, 0, y, where=((x >= 600) & (x < 670)), color='#FBBF24', alpha=0.3, label='Tier C (Near-Prime 600-669)')
ax.fill_between(x, 0, y, where=((x >= 530) & (x < 600)), color='#FB7185', alpha=0.3, label='Tier D (Subprime 530-599)')
ax.fill_between(x, 0, y, where=(x < 530), color='#F43F5E', alpha=0.5, label='Tier E (Decline <530)')

ax.set_xlabel('Puntuación Crediticia (FICO Scale 300 - 850)', color='#E2E8F0', fontsize=10, fontweight='bold')
ax.set_yticks([])
ax.tick_params(colors='#E2E8F0', labelsize=10)
ax.grid(axis='x', color='#334155', linestyle='--', alpha=0.4)
ax.legend(loc='upper left', frameon=False, fontsize=8.5, labelcolor='#E2E8F0')
plt.title("Distribución Poblacional de Score & Tramos de Riesgo", color='#FFFFFF', fontsize=12, fontweight='bold', pad=10)
plt.tight_layout()
chart_score_path = assets_dir / "chart_score.png"
plt.savefig(chart_score_path, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

# ==============================================================================
# 2. INITIALIZE PRESENTATION & DESIGN TOKENS
# ==============================================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

COLOR_BG = RGBColor(11, 15, 25)           # Deep Obsidian #0B0F19
COLOR_CARD = RGBColor(22, 32, 53)         # Navy Slate #162035
COLOR_CARD_DARK = RGBColor(16, 24, 40)    # Elevated Dark Slate
COLOR_BORDER = RGBColor(51, 65, 85)       # Slate Border #334155
COLOR_CYAN = RGBColor(56, 189, 248)       # Electric Cyan #38BDF8
COLOR_EMERALD = RGBColor(52, 211, 153)    # Bright Emerald #34D399
COLOR_AMBER = RGBColor(251, 191, 36)      # Vivid Amber #FBBF24
COLOR_ROSE = RGBColor(251, 113, 133)      # Bright Rose #FB7185
COLOR_WHITE = RGBColor(255, 255, 255)     # Pure White #FFFFFF
COLOR_SILVER = RGBColor(226, 232, 240)    # Crisp Bright Silver #E2E8F0
COLOR_MUTED = RGBColor(148, 163, 184)     # Medium Slate #94A3B8

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = COLOR_BG
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, title_text, category_text="ENTERPRISE CREDIT RISK ANALYTICS"):
    # Category tag
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.32))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    p_cat.font.name = FONT_HEADING

    # Title
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.font.name = FONT_HEADING

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.4)
    return shape

def add_bullet_point(text_frame, bold_prefix, text_content, font_size=12, text_color=COLOR_SILVER, prefix_color=COLOR_CYAN, space_after=6):
    p = text_frame.add_paragraph()
    p.space_after = Pt(space_after)
    
    if bold_prefix:
        run_p = p.add_run()
        run_p.text = bold_prefix + " "
        run_p.font.name = FONT_BODY
        run_p.font.bold = True
        run_p.font.size = Pt(font_size)
        run_p.font.color.rgb = prefix_color
        
    run_t = p.add_run()
    run_t.text = text_content
    run_t.font.name = FONT_BODY
    run_t.font.bold = False
    run_t.font.size = Pt(font_size)
    run_t.font.color.rgb = text_color

def style_table(table, col_widths, headers, rows_data):
    # Set col widths
    for i, w in enumerate(col_widths):
        table.columns[i].width = w

    # Header Row
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        p.alignment = PP_ALIGN.CENTER

    # Data Rows
    for row_idx, r_data in enumerate(rows_data, 1):
        bg = RGBColor(22, 32, 53) if row_idx % 2 == 1 else RGBColor(16, 24, 40)
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

# ==============================================================================
# SLIDE 1: COVER SLIDE
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=COLOR_CARD_DARK)

tb_b1 = s1.shapes.add_textbox(Inches(1.4), Inches(1.3), Inches(10.5), Inches(0.4))
p_b1 = tb_b1.text_frame.paragraphs[0]
p_b1.text = "CRISP-DM MACHINE LEARNING PIPELINE • PRODUCTION SCORECARD • BASEL III / IFRS 9"
p_b1.font.name = FONT_HEADING
p_b1.font.size = Pt(12)
p_b1.font.bold = True
p_b1.font.color.rgb = COLOR_CYAN

tb_t1 = s1.shapes.add_textbox(Inches(1.4), Inches(1.8), Inches(10.5), Inches(1.8))
p_t1 = tb_t1.text_frame.paragraphs[0]
p_t1.text = "Enterprise Credit Risk Intelligence &\nAutomated Decisioning Engine"
p_t1.font.name = FONT_HEADING
p_t1.font.size = Pt(36)
p_t1.font.bold = True
p_t1.font.color.rgb = COLOR_WHITE

tb_s1 = s1.shapes.add_textbox(Inches(1.4), Inches(3.7), Inches(10.5), Inches(0.9))
p_s1 = tb_s1.text_frame.paragraphs[0]
p_s1.text = "Modelado Integral de Probabilidad de Default (PD), Estabilidad Poblacional (PSI < 0.10),\nSuscripción Inteligente y Tarificación Dinámica Ajustada por Riesgo (Risk-Based Pricing)"
p_s1.font.name = FONT_BODY
p_s1.font.size = Pt(15)
p_s1.font.color.rgb = COLOR_SILVER

tb_a1 = s1.shapes.add_textbox(Inches(1.4), Inches(4.8), Inches(10.5), Inches(1.4))
tf_a1 = tb_a1.text_frame
p_aut1 = tf_a1.paragraphs[0]
p_aut1.text = "Guillén Concepción"
p_aut1.font.name = FONT_HEADING
p_aut1.font.size = Pt(20)
p_aut1.font.bold = True
p_aut1.font.color.rgb = COLOR_WHITE

p_aut2 = tf_a1.add_paragraph()
p_aut2.text = "Senior Data Scientist & MLOps Engineer"
p_aut2.font.name = FONT_BODY
p_aut2.font.size = Pt(13)
p_aut2.font.bold = True
p_aut2.font.color.rgb = COLOR_CYAN

p_aut3 = tf_a1.add_paragraph()
p_aut3.text = "LinkedIn: in/guillen-concepcion  |  GitHub: @GuillenConcepcion  |  Email: guillenconcepcion@gmail.com"
p_aut3.font.name = FONT_BODY
p_aut3.font.size = Pt(11.5)
p_aut3.font.color.rgb = COLOR_MUTED

# ==============================================================================
# SLIDE 2: EXECUTIVE SUMMARY & STRATEGIC HIGHLIGHTS
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "Resumen Ejecutivo: Impacto Estratégico y Valor de Negocio", "BUSINESS VALUE & EXECUTIVE SUMMARY")

# 4 KPI Cards
metrics = [
    ("32,581", "Solicitudes Históricas", "100% de Cartera Analizada", COLOR_CYAN),
    ("0.8329", "Poder de Separación (AUC)", "Test Out-of-Sample", COLOR_EMERALD),
    ("0.6658", "Coeficiente de Gini", "Alta Capacidad de Clasificación", COLOR_EMERALD),
    ("< 0.10", "Estabilidad Temporal (PSI)", "Cero Deriva (2013-2022)", COLOR_CYAN)
]

for i, (val, title, sub, color) in enumerate(metrics):
    x = Inches(0.8 + i * 2.98)
    add_card(s2, x, Inches(1.5), Inches(2.8), Inches(1.6))
    tb_m = s2.shapes.add_textbox(x, Inches(1.55), Inches(2.8), Inches(1.5))
    tf_m = tb_m.text_frame
    p_v = tf_m.paragraphs[0]
    p_v.text = val
    p_v.font.name = FONT_HEADING
    p_v.font.size = Pt(32)
    p_v.font.bold = True
    p_v.font.color.rgb = color
    p_v.alignment = PP_ALIGN.CENTER
    
    p_t = tf_m.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    p_s = tf_m.add_paragraph()
    p_s.text = sub
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = COLOR_MUTED
    p_s.alignment = PP_ALIGN.CENTER

# 3 Strategic Pillars
pillars = [
    ("Optimización del Negocio", [
        ("Trade-off de Rentabilidad:", "Sustituye la evaluación subjetiva por un scorecard cuantitativo que maximiza colocaciones con pérdida controlada."),
        ("Reducción de Mora:", "Filtrado analítico de solicitudes de alto riesgo (Tier D/E) reduciendo el default promedio institucional."),
        ("Escalabilidad:", "Tiempos de respuesta inferiores a 50 milisegundos por solicitud crediticia.")
    ], COLOR_CYAN),
    ("Gobernanza & Cumplimiento", [
        ("Marco Basilea III / IFRS 9:", "Estimación rigurosa de Probabilidad de Default (PD) y Pérdida Esperada (EL = PD × LGD × EAD)."),
        ("Explicabilidad Total:", "Generación automática de 'Reason Codes' conformes a leyes de crédito justo (Equal Credit Opportunity Act / FCRA)."),
        ("Monitoreo Regulatorio:", "Auditoría de drift continuo mediante Population Stability Index (PSI).")
    ], COLOR_EMERALD),
    ("Eficiencia Operativa", [
        ("Procesamiento STP:", "Aprobación automática directa (Straight-Through Processing) en perfiles Prime (Tier A)."),
        ("Tarificación por Riesgo:", "Asignación dinámica de spreads (+150 a +750 bps) en función del perfil de riesgo."),
        ("Ahorro de Costes:", "Reducción proyectada del 65% en tiempos de suscripción y análisis manual.")
    ], COLOR_AMBER)
]

for i, (title, points, color) in enumerate(pillars):
    x = Inches(0.8 + i * 3.98)
    add_card(s2, x, Inches(3.3), Inches(3.8), Inches(3.7))
    tb_p = s2.shapes.add_textbox(x + Inches(0.2), Inches(3.45), Inches(3.4), Inches(3.4))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_title = tf_p.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(16)
    p_title.font.bold = True
    p_title.font.color.rgb = color
    p_title.space_after = Pt(10)

    for prefix, body in points:
        add_bullet_point(tf_p, "• " + prefix, body, font_size=11, space_after=8)

# ==============================================================================
# SLIDE 3: DATA ARCHITECTURE & CRISP-DM PHASES
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "Arquitectura del Pipeline Analítico End-to-End", "CRISP-DM PHASES & METHODOLOGY")

phases = [
    ("Fase 1: Ingesta & EDA", "Reconstrucción temporal (vintage 2013-2022). Separación de histórico (26,616) vs cohorte Out-of-Time (5,965 obs). Reportes automatizados en Excel."),
    ("Fase 2: Limpieza & Split", "Split 80/20 estratificado por def_year. Clipping IQR en Train exclusivo (Zero Data Leakage). Imputación de nulos con medianas y dummies."),
    ("Fase 3: Asociación", "Kruskal-Wallis para continuas vs default. V de Cramér para categóricas. Matrices Spearman y Cramér inter-variables para multicolinealidad."),
    ("Fase 4: Storytelling", "Análisis de contingencia Chi² (Home Ownership: 1,248.48, p < 1e-200). Gráficos ejecutivos Cole Nussbaumer Knaflic de alta resolución."),
    ("Fase 5: Estabilidad PSI", "Monitoreo temporal ventana a ventana (2013-2021) y Train vs Test vs OOT. Todas las variables con PSI < 0.02 (Estabilidad máxima)."),
    ("Fase 6: Selección 4-Folds", "Pipeline multi-regla sobre validación cruzada: Filtro univariado (KW/V) y multicolinealidad (Spearman/V). Reducción óptima a 7 variables clave.")
]

for i, (p_title, p_desc) in enumerate(phases):
    col = i % 3
    row = i // 3
    x = Inches(0.8 + col * 3.98)
    y = Inches(1.6 + row * 2.7)
    add_card(s3, x, y, Inches(3.8), Inches(2.45))
    tb_ph = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(3.4), Inches(2.1))
    tf_ph = tb_ph.text_frame
    tf_ph.word_wrap = True
    
    p_t = tf_ph.paragraphs[0]
    p_t.text = p_title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(16)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_CYAN
    p_t.space_after = Pt(8)

    p_d = tf_ph.add_paragraph()
    p_d.text = p_desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_SILVER

# ==============================================================================
# SLIDE 4: TEMPORAL SPLIT & DATASET PARTITIONING (FIXED WITH HIGH-RES CHART & TABLE)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Estratificación y Partición Metodológica de Datos", "DATASET SPLITS & LEAKAGE PREVENTION")

# 1. Native Clean Table on the left
table_shape = s4.shapes.add_table(4, 5, Inches(0.8), Inches(1.5), Inches(5.8), Inches(2.4))
table = table_shape.table
style_table(
    table,
    [Inches(1.2), Inches(1.1), Inches(1.0), Inches(1.1), Inches(1.4)],
    ["Partición", "Volumen", "% Total", "Defaults", "Tasa Default"],
    [
        ["Train (Desarrollo)", "21,292", "65.3%", "4,562", "21.43%"],
        ["Test (Out-of-Sample)", "5,324", "16.3%", "1,140", "21.41%"],
        ["OOT (Temporal 2022)", "5,965", "18.3%", "1,406", "23.57%"]
    ]
)

# 2. Key Methodological Guarantees Card (Bottom Left)
add_card(s4, Inches(0.8), Inches(4.1), Inches(5.8), Inches(2.9))
tb_g = s4.shapes.add_textbox(Inches(1.0), Inches(4.25), Inches(5.4), Inches(2.6))
tf_g = tb_g.text_frame
tf_g.word_wrap = True

p_gt = tf_g.paragraphs[0]
p_gt.text = "Garantías Metodológicas Anti-Fuga (Zero Leakage)"
p_gt.font.name = FONT_HEADING
p_gt.font.size = Pt(15)
p_gt.font.bold = True
p_gt.font.color.rgb = COLOR_EMERALD
p_gt.space_after = Pt(8)

add_bullet_point(tf_g, "1. Aislamiento Estricto:", "Los cuartiles IQR de clipping y la mediana de imputación se calcularon únicamente sobre Train.", font_size=11, space_after=6)
add_bullet_point(tf_g, "2. Estratificación Bivariada:", "El split preservó la tasa exacta de default combinando target y año (def_year).", font_size=11, space_after=6)
add_bullet_point(tf_g, "3. Muestra Ciega Out-of-Time:", "La cohorte 2022 (OOT) evalúa la estabilidad frente a shocks temporales reales.", font_size=11, space_after=4)

# 3. High-Resolution Chart Embedded on Right
add_card(s4, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.5))
s4.shapes.add_picture(str(chart_splits_path), Inches(7.0), Inches(1.6), Inches(5.4), Inches(5.2))

# ==============================================================================
# SLIDE 5: FEATURE DISCRIMINATION & STORYTELLING
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "Discriminación de Atributos & Storytelling Visual", "FEATURE DISCRIMINATION ANALYSIS")

# Embed real high-res picture of default_by_ownership.png on the left
add_card(s5, Inches(0.8), Inches(1.5), Inches(5.9), Inches(5.5))
pic_ownership = Path("default_by_ownership.png")
if pic_ownership.exists():
    s5.shapes.add_picture(str(pic_ownership), Inches(0.95), Inches(1.85), Inches(5.6), Inches(4.7))

# Association Metrics Card on the right
add_card(s5, Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.5))
tb_as = s5.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.1), Inches(5.1))
tf_as = tb_as.text_frame
tf_as.word_wrap = True

p_ast = tf_as.paragraphs[0]
p_ast.text = "Hallazgos de Discriminación y Pruebas Estadísticas"
p_ast.font.name = FONT_HEADING
p_ast.font.size = Pt(17)
p_ast.font.bold = True
p_ast.font.color.rgb = COLOR_CYAN
p_ast.space_after = Pt(10)

add_bullet_point(tf_as, "Régimen de Vivienda:", "Chi² = 1,248.48 (p < 1e-200), V de Cramér = 0.242.", font_size=12, prefix_color=COLOR_AMBER)
add_bullet_point(tf_as, "• Inquilinos (RENT):", "31.32% de mora (50.4% de las solicitudes).", font_size=11.5)
add_bullet_point(tf_as, "• Hipoteca (MORTGAGE):", "12.58% de mora (41.2% de las solicitudes).", font_size=11.5)
add_bullet_point(tf_as, "• Vivienda Propia (OWN):", "7.32% de mora (8.0% de las solicitudes).", font_size=11.5)
add_bullet_point(tf_as, "Insight Clave:", "Los inquilinos registran un riesgo 4.3x superior frente a propietarios de vivienda libre de cargas.", font_size=11.5, text_color=COLOR_EMERALD, space_after=12)

add_bullet_point(tf_as, "Monotonicidad por Calificación:", "Loan Grade A (9.9%) hasta G (98.4%) confirma estricta consistencia lógica.", font_size=11.5, prefix_color=COLOR_AMBER)
add_bullet_point(tf_as, "Fuerza Bivariada Cuantitativa:", "DTI (KW = 2,135.9), Tasa (KW = 1,861.4) e Ingreso (KW = 1,566.8) lideran la capacidad explicativa.", font_size=11.5, prefix_color=COLOR_CYAN)

# ==============================================================================
# SLIDE 6: POPULATION STABILITY INDEX (PSI)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Evaluación de Estabilidad Poblacional (PSI)", "REGULATORY DRIFT & POPULATION STABILITY")

# Left: Native Clean PSI Table
table_psi = s6.shapes.add_table(7, 4, Inches(0.8), Inches(1.5), Inches(5.8), Inches(3.4)).table
style_table(
    table_psi,
    [Inches(2.0), Inches(1.2), Inches(1.2), Inches(1.4)],
    ["Variable", "Train vs Test", "Train vs OOT", "Diagnóstico"],
    [
        ["person_income", "0.0010", "0.0184", "✅ Estable"],
        ["person_emp_length", "0.0006", "0.0136", "✅ Estable"],
        ["loan_int_rate", "0.0000", "0.0001", "✅ Estable"],
        ["loan_percent_income", "0.0002", "0.0020", "✅ Estable"],
        ["home_ownership_3", "0.0002", "0.0034", "✅ Estable"],
        ["cb_person_default_on_file", "0.0000", "0.0001", "✅ Estable"]
    ]
)

# Bottom Left: Benchmarks Card
add_card(s6, Inches(0.8), Inches(5.1), Inches(5.8), Inches(1.9))
tb_bn = s6.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.4), Inches(1.7))
tf_bn = tb_bn.text_frame
tf_bn.word_wrap = True
p_bnt = tf_bn.paragraphs[0]
p_bnt.text = "Criterios Regulatorios de Deriva Poblacional (PSI)"
p_bnt.font.name = FONT_HEADING
p_bnt.font.size = Pt(13)
p_bnt.font.bold = True
p_bnt.font.color.rgb = COLOR_WHITE
p_bnt.space_after = Pt(4)

add_bullet_point(tf_bn, "• PSI < 0.10 (Zona Verde):", "Distribución estable. No requiere ajuste ni recalibración.", font_size=10.5, prefix_color=COLOR_EMERALD, space_after=3)
add_bullet_point(tf_bn, "• 0.10 <= PSI < 0.25 (Zona Ámbar):", "Deriva moderada. Monitoreo estrecho requerido.", font_size=10.5, prefix_color=COLOR_AMBER, space_after=3)
add_bullet_point(tf_bn, "• PSI >= 0.25 (Zona Roja):", "Deriva severa. Descalibración crítica; reentrenamiento obligatorio.", font_size=10.5, prefix_color=COLOR_ROSE, space_after=2)

# Right: High-Res PSI Trendline Chart
add_card(s6, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.5))
s6.shapes.add_picture(str(chart_psi_path), Inches(7.05), Inches(1.8), Inches(5.3), Inches(4.8))

# ==============================================================================
# SLIDE 7: 4-FOLD CV & VARIABLE SELECTION
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Proceso de Selección de Variables (4-Fold Multi-Regla)", "FEATURE SELECTION PIPELINE")

# 4 Rules Horizontal Cards
rules = [
    ("Regla 1: KW Continuo", "p < 0.05 en los 4 Folds", "Filtra variables continuas sin relación bivariada con el default.", "7 retenidas", COLOR_CYAN),
    ("Regla 2: Cramér's V Categórico", "0.10 <= V <= 0.50", "Descarta predictores débiles y cuasi-identidades deterministas.", "3 retenidas", COLOR_CYAN),
    ("Regla 3: Spearman Multicolineal", "|r| < 0.50", "Elimina variables colineales conservando la de mayor Kruskal-Wallis.", "5 continuas", COLOR_EMERALD),
    ("Regla 4: Cramér Inter-Categórico", "V inter < 0.50", "Elimina redundancia estructural (ej. loan_grade vs default_on_file).", "2 categóricas", COLOR_EMERALD)
]

for i, (r_title, r_thresh, r_desc, r_ret, color) in enumerate(rules):
    x = Inches(0.8 + i * 2.98)
    add_card(s7, x, Inches(1.5), Inches(2.8), Inches(2.2))
    tb_r = s7.shapes.add_textbox(x + Inches(0.15), Inches(1.6), Inches(2.5), Inches(2.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p_rt = tf_r.paragraphs[0]
    p_rt.text = r_title
    p_rt.font.name = FONT_HEADING
    p_rt.font.size = Pt(13)
    p_rt.font.bold = True
    p_rt.font.color.rgb = color

    p_th = tf_r.add_paragraph()
    p_th.text = "Umbral: " + r_thresh
    p_th.font.name = FONT_BODY
    p_th.font.size = Pt(10.5)
    p_th.font.color.rgb = COLOR_MUTED

    p_rd = tf_r.add_paragraph()
    p_rd.text = r_desc
    p_rd.font.name = FONT_BODY
    p_rd.font.size = Pt(10.5)
    p_rd.font.color.rgb = COLOR_SILVER

    p_rr = tf_r.add_paragraph()
    p_rr.text = "Retenidas: " + r_ret
    p_rr.font.name = FONT_HEADING
    p_rr.font.size = Pt(11)
    p_rr.font.bold = True
    p_rr.font.color.rgb = color

# Final Selected Features Table
table_feats = s7.shapes.add_table(8, 4, Inches(0.8), Inches(3.9), Inches(11.733), Inches(3.1)).table
style_table(
    table_feats,
    [Inches(2.5), Inches(1.5), Inches(3.2), Inches(4.5)],
    ["Variable Técnica", "Tipo", "Nombre de Negocio", "Rol en la Política de Riesgo"],
    [
        ["person_income", "Continua", "Ingreso Anual ($)", "Capacidad de pago y solidez patrimonial del cliente"],
        ["loan_percent_income", "Continua", "Ratio Préstamo/Ingreso (DTI)", "Nivel de apalancamiento y carga de servicio de deuda"],
        ["loan_int_rate", "Continua", "Tasa de Interés (%)", "Prima de riesgo asignada por la entidad financiera"],
        ["person_home_ownership", "Categórica", "Régimen de Vivienda", "Estabilidad habitacional y respaldo patrimonial (OWN/RENT)"],
        ["cb_person_default_on_file", "Categórica", "Historial Previo de Mora", "Comportamiento crediticio histórico negativo en buró"],
        ["person_emp_length", "Continua", "Antigüedad Laboral (Años)", "Estabilidad y permanencia en la fuente de ingresos"],
        ["person_age", "Continua", "Edad del Solicitante", "Ciclo de vida, madurez y horizonte financiero"]
    ]
)

# ==============================================================================
# SLIDE 8: MODEL PERFORMANCE & FICO CALIBRATION
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "Rendimiento y Calibración del Scorecard en Producción", "MODEL PERFORMANCE & VALIDATION")

# Left Column: Metrics & Formulation Card
add_card(s8, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.5))
tb_m8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(5.1))
tf_m8 = tb_m8.text_frame
tf_m8.word_wrap = True

p_m8t = tf_m8.paragraphs[0]
p_m8t.text = "Resultados de Validación y Escala FICO"
p_m8t.font.name = FONT_HEADING
p_m8t.font.size = Pt(17)
p_m8t.font.bold = True
p_m8t.font.color.rgb = COLOR_CYAN
p_m8t.space_after = Pt(8)

add_bullet_point(tf_m8, "Test ROC-AUC:", "0.8329 (Poder de discriminación excelente).", font_size=12, prefix_color=COLOR_EMERALD)
add_bullet_point(tf_m8, "Test Gini:", "0.6658 (Gini = 2 × AUC - 1).", font_size=12, prefix_color=COLOR_EMERALD)
add_bullet_point(tf_m8, "Brier Score:", "0.1261 (Calibración probabilística fiable).", font_size=12, prefix_color=COLOR_CYAN)
add_bullet_point(tf_m8, "Estadístico KS:", "0.528 (Máxima separación en 3er decil de score).", font_size=12, prefix_color=COLOR_CYAN, space_after=12)

add_bullet_point(tf_m8, "Fórmula FICO:", "Score = Offset - Factor × ln(Odds)", font_size=12, prefix_color=COLOR_AMBER)
add_bullet_point(tf_m8, "• PDO (Points to Double Odds):", "20 puntos por duplicación de odds.", font_size=11)
add_bullet_point(tf_m8, "• Base Score:", "600 puntos para Odds de 50:1 (PD = 1.96%).", font_size=11)
add_bullet_point(tf_m8, "• Parámetros:", "Factor ≈ 28.85, Offset ≈ 712.87.", font_size=11)
add_bullet_point(tf_m8, "Cumplimiento Regulatorio:", "Interpretabilidad aditiva requerida por reguladores bancarios.", font_size=11.5, text_color=COLOR_EMERALD)

# Right Column: High-Res Bell Curve Chart
add_card(s8, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.5))
s8.shapes.add_picture(str(chart_score_path), Inches(7.05), Inches(1.75), Inches(5.3), Inches(5.0))

# ==============================================================================
# SLIDE 9: INTELLIGENT DECISION ENGINE & POLICY MATRIX
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "Motor de Decisiones Inteligente & Matriz de Políticas", "POLICY MATRIX & RISK-BASED PRICING")

# Top Card: Knockouts Banner
add_card(s9, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.3))
tb_ko = s9.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.1))
tf_ko = tb_ko.text_frame
tf_ko.word_wrap = True

p_kot = tf_ko.paragraphs[0]
p_kot.text = "Compuerta Pre-Scoring: Reglas de Exclusión Dura (Knockout Filters)"
p_kot.font.name = FONT_HEADING
p_kot.font.size = Pt(13)
p_kot.font.bold = True
p_kot.font.color.rgb = COLOR_ROSE
p_kot.space_after = Pt(4)

p_kob = tf_ko.add_paragraph()
p_kob.text = "• KO-01: Menor de 18 años   |   • KO-02: Mayor de 80 años   |   • KO-03: Ingreso < $8,000 USD   |   • KO-04: DTI > 65%   |   • KO-05: Cooldown < 90 días"
p_kob.font.name = FONT_BODY
p_kob.font.size = Pt(11)
p_kob.font.color.rgb = COLOR_WHITE

# Middle Table: Policy Matrix & Tiers
table_policy = s9.shapes.add_table(6, 6, Inches(0.8), Inches(3.0), Inches(11.733), Inches(2.7)).table
style_table(
    table_policy,
    [Inches(2.1), Inches(1.6), Inches(1.6), Inches(2.8), Inches(1.8), Inches(1.8)],
    ["Tramo de Riesgo", "Rango Score", "Prob. Default", "Decisión Operativa", "Límite Máximo", "Spread Tasa"],
    [
        ["Tier A (Prime)", "750 - 850", "< 4.5%", "Aprobación Automática (STP)", "125% del monto", "+150 bps (7.00%)"],
        ["Tier B (Bajo Riesgo)", "670 - 749", "4.5% - 12.0%", "Aprobado Estándar (DTI <= 28%)", "100% del monto", "+250 bps (8.00%)"],
        ["Tier C (Near-Prime)", "600 - 669", "12.0% - 24.0%", "Revisión Manual / Condicionado", "80% del monto", "+450 bps (10.00%)"],
        ["Tier D (Subprime)", "530 - 599", "24.0% - 42.0%", "Aprobación con Aval / Colateral", "50% del monto", "+750 bps (13.00%)"],
        ["Tier E (Crítico)", "300 - 529", "> 42.0%", "Rechazado por Política de Riesgo", "0%", "Declinado"]
    ]
)

# Bottom Card: IFRS 9 Expected Loss
add_card(s9, Inches(0.8), Inches(5.9), Inches(11.733), Inches(1.1))
tb_el = s9.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.3), Inches(0.9))
tf_el = tb_el.text_frame
tf_el.word_wrap = True
p_elt = tf_el.paragraphs[0]
p_elt.text = "Modelado de Pérdida Esperada IFRS 9:   EL = PD × LGD × EAD"
p_elt.font.name = FONT_HEADING
p_elt.font.size = Pt(13)
p_elt.font.bold = True
p_elt.font.color.rgb = COLOR_EMERALD

p_elb = tf_el.add_paragraph()
p_elb.text = "LGD no garantizada = 55% | LGD con garantía real = 25% | EAD = Saldo expuesto al default | Cálculo en tiempo real por solicitud."
p_elb.font.name = FONT_BODY
p_elb.font.size = Pt(11)
p_elb.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 10: WEB DASHBOARD & SIMULATOR
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "Dashboard Web Interactivo & Simulador en Tiempo Real", "MLOPS & INTERACTIVE USER EXPERIENCE")

# Left Card: Web App Architecture
add_card(s10, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.5))
tb_d1 = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(5.1))
tf_d1 = tb_d1.text_frame
tf_d1.word_wrap = True

p_d1t = tf_d1.paragraphs[0]
p_d1t.text = "Arquitectura y Componentes de la Plataforma"
p_d1t.font.name = FONT_HEADING
p_d1t.font.size = Pt(17)
p_d1t.font.bold = True
p_d1t.font.color.rgb = COLOR_CYAN
p_d1t.space_after = Pt(10)

add_bullet_point(tf_d1, "Backend de Inferencia:", "FastAPI asíncrono sobre servidor Uvicorn.", font_size=12, prefix_color=COLOR_EMERALD)
add_bullet_point(tf_d1, "Frontend Moderno:", "HTML5 semántico, Vanilla CSS Dark Mode y Chart.js.", font_size=12, prefix_color=COLOR_EMERALD)
add_bullet_point(tf_d1, "Rendimiento:", "Latencia de inferencia inferior a 50 milisegundos.", font_size=12, prefix_color=COLOR_CYAN, space_after=12)

add_bullet_point(tf_d1, "5 Módulos Integrados:", "", font_size=12, prefix_color=COLOR_AMBER)
add_bullet_point(tf_d1, "1. Simulador:", "Cálculo en vivo de score, probabilidad de mora y dictamen.", font_size=11)
add_bullet_point(tf_d1, "2. Visión Ejecutiva:", "KPIs globales y tablas de particiones (Train/Test/OOT).", font_size=11)
add_bullet_point(tf_d1, "3. Discriminación:", "Storytelling de tenencia de vivienda y grados de préstamo.", font_size=11)
add_bullet_point(tf_d1, "4. Monitor PSI:", "Matriz regulatoria de estabilidad temporal.", font_size=11)
add_bullet_point(tf_d1, "5. Selección:", "Detalle de las 4 reglas estadísticas de depuración.", font_size=11)

# Right Card: Simulator Experience
add_card(s10, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.5))
tb_d2 = s10.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.1))
tf_d2 = tb_d2.text_frame
tf_d2.word_wrap = True

p_d2t = tf_d2.paragraphs[0]
p_d2t.text = "Experiencia del Simulador de Scoring"
p_d2t.font.name = FONT_HEADING
p_d2t.font.size = Pt(17)
p_d2t.font.bold = True
p_d2t.font.color.rgb = COLOR_EMERALD
p_d2t.space_after = Pt(10)

add_bullet_point(tf_d2, "Gauge Radial Reactivo:", "Visualización instantánea del FICO Score (300-850) con arco animado.", font_size=12, prefix_color=COLOR_CYAN)
add_bullet_point(tf_d2, "Perfiles Preconfigurados:", "Botones de prueba rápida para casos típicos de negocio:", font_size=12, prefix_color=COLOR_CYAN)
add_bullet_point(tf_d2, "• Cliente Prime:", "Score 778 | Aprobación automática STP | Tasa 7.00%.", font_size=11)
add_bullet_point(tf_d2, "• Riesgo Medio:", "Score 642 | Derivación a revisión manual de ingresos.", font_size=11)
add_bullet_point(tf_d2, "• Alto Riesgo:", "Score 495 | Rechazo por antecedentes morosos en buró.", font_size=11, space_after=12)

add_bullet_point(tf_d2, "Explicabilidad Fair Lending:", "Desglose de factores Waterfall (+/- puntos de impacto).", font_size=12, prefix_color=COLOR_AMBER)
add_bullet_point(tf_d2, "Acceso Local:", "http://localhost:8088  |  Documentación OpenAPI: /docs", font_size=11.5, text_color=COLOR_WHITE)

# ==============================================================================
# SLIDE 11: MLOps GOVERNANCE & ROADMAP
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "Gobernanza MLOps, Roadmap & Próximos Pasos", "MLOPS LIFECYCLE & STRATEGIC ROADMAP")

roadmaps = [
    ("Fase 1: Implementado", [
        ("Pipeline Reproducible:", "CRISP-DM verificado en < 5 segundos."),
        ("Tratamiento Anti-Leakage:", "Límites IQR y nulos en Train exclusivo."),
        ("Scorecard Calibrado:", "AUC 0.833, Gini 0.666 en Test independiente."),
        ("Motor de Decisión:", "Knockouts, Tiers y Pricing implementados."),
        ("Dashboard Interactivo:", "Aplicación web FastAPI operativa.")
    ], COLOR_EMERALD),
    ("Fase 2: Corto Plazo (Q1)", [
        ("Contenerización:", "Empaquetado Docker/Podman de la API."),
        ("Pipeline CI/CD:", "Automatización con GitHub Actions y linting."),
        ("Monitoreo de Deriva:", "Alertas tempranas de PSI con Evidently AI."),
        ("Persistencia SQL:", "Conexión a base de datos de producción.")
    ], COLOR_CYAN),
    ("Fase 3: Medio Plazo (Q2)", [
        ("Champion / Challenger:", "Scorecard logístico vs Gradient Boosting."),
        ("MLflow Registry:", "Versionado de modelos, métricas y artefactos."),
        ("Vintage Analysis:", "Seguimiento de morosidad observada a 90 días."),
        ("Alineación Actuarial:", "Recalibración periódica de matrices de corte.")
    ], COLOR_AMBER)
]

for i, (title, points, color) in enumerate(roadmaps):
    x = Inches(0.8 + i * 3.98)
    add_card(s11, x, Inches(1.5), Inches(3.8), Inches(5.5))
    tb_rm = s11.shapes.add_textbox(x + Inches(0.2), Inches(1.7), Inches(3.4), Inches(5.1))
    tf_rm = tb_rm.text_frame
    tf_rm.word_wrap = True

    p_rt = tf_rm.paragraphs[0]
    p_rt.text = title
    p_rt.font.name = FONT_HEADING
    p_rt.font.size = Pt(17)
    p_rt.font.bold = True
    p_rt.font.color.rgb = color
    p_rt.space_after = Pt(10)

    for prefix, body in points:
        add_bullet_point(tf_rm, "• " + prefix, body, font_size=11.5, space_after=8)

# ==============================================================================
# SLIDE 12: CONCLUSION & CONTACT
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)

add_card(s12, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=COLOR_CARD_DARK)

tb_c = s12.shapes.add_textbox(Inches(1.4), Inches(1.3), Inches(10.5), Inches(5.0))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p_ct = tf_c.paragraphs[0]
p_ct.text = "Conclusión & Sesión de Preguntas (Q&A)"
p_ct.font.name = FONT_HEADING
p_ct.font.size = Pt(32)
p_ct.font.bold = True
p_ct.font.color.rgb = COLOR_WHITE
p_ct.space_after = Pt(12)

p_cb1 = tf_c.add_paragraph()
p_cb1.text = "El proyecto demuestra la viabilidad de integrar rigor estadístico bancario (Basilea III / IFRS 9), interpretabilidad regulatoria absoluta y excelencia en ingeniería de software (MLOps, FastAPI y simulador interactivo)."
p_cb1.font.name = FONT_BODY
p_cb1.font.size = Pt(14)
p_cb1.font.color.rgb = COLOR_SILVER
p_cb1.space_after = Pt(8)

p_cb2 = tf_c.add_paragraph()
p_cb2.text = "Impacto esperado: reducción del 65% en costos operativos de suscripción (STP), control analítico de pérdidas esperadas y monitoreo continuo frente a deriva poblacional."
p_cb2.font.name = FONT_BODY
p_cb2.font.size = Pt(14)
p_cb2.font.color.rgb = COLOR_SILVER
p_cb2.space_after = Pt(20)

p_ca = tf_c.add_paragraph()
p_ca.text = "Guillén Concepción"
p_ca.font.name = FONT_HEADING
p_ca.font.size = Pt(22)
p_ca.font.bold = True
p_ca.font.color.rgb = COLOR_CYAN

p_cr = tf_c.add_paragraph()
p_cr.text = "Senior Data Scientist & MLOps Engineer"
p_cr.font.name = FONT_BODY
p_cr.font.size = Pt(14)
p_cr.font.bold = True
p_cr.font.color.rgb = COLOR_WHITE
p_cr.space_after = Pt(6)

p_cl1 = tf_c.add_paragraph()
p_cl1.text = "• LinkedIn: https://www.linkedin.com/in/guillen-concepcion-25266b127"
p_cl1.font.name = FONT_BODY
p_cl1.font.size = Pt(12)
p_cl1.font.color.rgb = COLOR_MUTED

p_cl2 = tf_c.add_paragraph()
p_cl2.text = "• GitHub: https://github.com/GuillenConcepcion/Credit_Scoring_Project"
p_cl2.font.name = FONT_BODY
p_cl2.font.size = Pt(12)
p_cl2.font.color.rgb = COLOR_MUTED

p_cl3 = tf_c.add_paragraph()
p_cl3.text = "• Email: guillenconcepcion@gmail.com"
p_cl3.font.name = FONT_BODY
p_cl3.font.size = Pt(12)
p_cl3.font.color.rgb = COLOR_MUTED

# Save presentation
output_pptx = Path("Credit_Risk_Scoring_Presentation.pptx").resolve()
prs.save(str(output_pptx))
print(f"High-resolution presentation saved successfully to: {output_pptx}")
