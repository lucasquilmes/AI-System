"""
Genera l'informe complet de la Fase 2A en format Word.
Sortida: informe_fase2_report.docx
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "informe_fase2_report.docx"

C_BLUE_D = RGBColor(0, 70, 127)
C_BLUE_M = RGBColor(0, 114, 198)
C_GREY   = RGBColor(80, 80, 80)
C_GREEN  = RGBColor(0, 112, 0)
C_RED    = RGBColor(180, 20, 20)
C_ORANGE = RGBColor(200, 100, 0)
C_WHITE  = RGBColor(255, 255, 255)
C_GOLD   = RGBColor(180, 130, 0)

# ── Helpers ────────────────────────────────────────────────────────────────────
def shade(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)

def heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if level == 1 else 8)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.font.size  = Pt({1: 16, 2: 13, 3: 11}[level])
    run.font.bold  = True
    run.font.color.rgb = C_BLUE_D

def body(doc, text, size=11, italic=False, colour=None, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size   = Pt(size)
    run.font.italic = italic
    run.font.bold   = bold
    if colour:
        run.font.color.rgb = colour

def bullet(doc, text, size=11):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.size = Pt(size)

def caption(doc, text):
    body(doc, text, size=9, italic=True, colour=C_GREY)

def hdr_row(table, headers, bg="00467F", sizes=None):
    row = table.rows[0]
    for j, h in enumerate(headers):
        c = row.cells[j]
        shade(c, bg)
        c.text = h
        for par in c.paragraphs:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in par.runs:
                run.font.bold  = True
                run.font.size  = Pt(sizes[j] if sizes else 9)
                run.font.color.rgb = C_WHITE

def fmt_cell(cell, text, center=True, size=9, bold=False, colour=None):
    cell.text = text
    for par in cell.paragraphs:
        if center:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in par.runs:
            run.font.size = Pt(size)
            run.font.bold = bold
            if colour:
                run.font.color.rgb = colour

def highlight_max(table, row_idxs, col_idxs, bg="D5E8D4"):
    """Highlight the cell with highest float value among given positions."""
    best_val = -999
    best_pos = None
    for ri in row_idxs:
        for ci in col_idxs:
            try:
                v = float(table.rows[ri].cells[ci].text)
                if v > best_val:
                    best_val = v
                    best_pos = (ri, ci)
            except ValueError:
                pass
    if best_pos:
        shade(table.rows[best_pos[0]].cells[best_pos[1]], bg)
        for par in table.rows[best_pos[0]].cells[best_pos[1]].paragraphs:
            for run in par.runs:
                run.font.bold = True
                run.font.color.rgb = C_GREEN

def set_col_widths(table, widths):
    for row in table.rows:
        for j, w in enumerate(widths):
            row.cells[j].width = w

# ── Document setup ─────────────────────────────────────────────────────────────
doc = Document()
sec = doc.sections[0]
sec.top_margin = sec.bottom_margin = Cm(2.5)
sec.left_margin = sec.right_margin = Cm(3.0)
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(11)

# ══════════════════════════════════════════════════════════════════════════════
# PORTADA
# ══════════════════════════════════════════════════════════════════════════════
for _ in range(4):
    doc.add_paragraph()

for txt, sz in [
    ("INFORME DE LA FASE 2A", 22),
    ("EFECTE DE LA TEMPERATURA EN L'ADAPTACIÓ", 18),
    ("AUTOMÀTICA A LECTURA FÀCIL", 18),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(txt)
    r.font.size = Pt(sz)
    r.font.bold = True
    r.font.color.rgb = C_BLUE_D

doc.add_paragraph()
for txt, sz, col in [
    ("Projecte Explain-Up — Avaluació de LLMs locals per a Lectura Fàcil", 13, C_GREY),
    ("Juny 2026", 11, C_GREY),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(txt)
    r.font.size = Pt(sz)
    r.font.color.rgb = col

for _ in range(3):
    doc.add_paragraph()

for ln in [
    "Models avaluats: llama3.3 (70B) · gemma2:27b",
    "Prompts: V8 (imitació progressiva) · CoT (cadena de raonament)",
    "Temperatures: T=0.0 · T=0.3 · T=0.7 · T=1.0  —  Semilla fixa: seed=42",
    "Datasets: test_poor (12 textos) · exemples_lectura_facil_formatted (11 textos)",
    "Total combinacions: 32  ·  Mètrica principal: score compost normalitzat [0–1]",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(ln)
    r.font.size = Pt(10)
    r.font.color.rgb = C_GREY

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# 1. RESUM EXECUTIU
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "1. Resum Executiu")
body(doc, (
    "La Fase 2A analitza com la temperatura de mostreig afecta la qualitat de les adaptacions "
    "automàtiques a Lectura Fàcil generades per models de llenguatge locals. "
    "Partint dels resultats de la Fase 1, s'han seleccionat els dos models més robustos "
    "(llama3.3 i gemma2:27b), els dos prompts més efectius (V8 i CoT) "
    "i s'han avaluat quatre nivells de temperatura (T=0.0, 0.3, 0.7, 1.0) "
    "sobre els dos datasets de l'estudi, per un total de 32 combinacions."
))
body(doc, "Els cinc resultats principals de la fase són:")
bullet(doc, (
    "La temperatura no millora la qualitat de l'adaptació. SARI i BERTScore "
    "assoleixen el màxim a T=0.0 en els dos datasets sense excepció."
))
bullet(doc, (
    "llama3.3 supera gemma2:27b en el 75% de les combinacions temperatura×prompt "
    "i és el model globalment més robust."
))
bullet(doc, (
    "Augmentar la temperatura amplifica l'especialització de domini: "
    "el model funciona millor al dataset fàcil i pitjor al difícil. "
    "El gap inter-dataset de llama3.3+V8 creix de 0.157 (T=0.0) a 0.241 (T=1.0)."
))
bullet(doc, (
    "V8 i CoT s'intercanvien el lideratge entre datasets: V8 guanya +22pp a test_poor "
    "(textos administratius) però perd −5pp a exemples (domini divers). "
    "CoT generalitza millor entre dominis amb gaps de 0.005–0.038."
))
bullet(doc, (
    "La configuració globalment òptima és llama3.3 + T=0.0 + V8, "
    "amb score compost mitjà de 0.587 i gap inter-dataset de 0.314, "
    "el menor entre les configuracions d'alt rendiment."
))

# ══════════════════════════════════════════════════════════════════════════════
# 2. DISSENY EXPERIMENTAL
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "2. Disseny Experimental")
heading(doc, "2.1. Configuració", 2)
body(doc, (
    "La Fase 2A és una extensió directa de la Fase 1. Es mantenen fixos els models i "
    "prompts més eficients identificats i es varia sistemàticament la temperatura, "
    "l'únic hiperparàmetre que no es va explorar en la fase anterior."
))
doc.add_paragraph()

t = doc.add_table(rows=7, cols=2)
t.style = "Table Grid"
hdr_row(t, ["Paràmetre", "Valors"])
rows_data = [
    ("Models",       "llama3.3 (70B) · gemma2:27b (27B)"),
    ("Prompts",      "V8 — Imitació progressiva de l'anotador expert\nCoT — Cadena de raonament (Chain of Thought)"),
    ("Temperatures", "0.0 · 0.3 · 0.7 · 1.0"),
    ("Semilla",      "42 (fixa per a reproduïbilitat)"),
    ("Datasets",     "test_poor (12 textos, alta complexitat)\nexemples_lectura_facil_formatted (11 textos, domini divers)"),
    ("Total combin.","2 models × 2 prompts × 4 temperatures × 2 datasets = 32"),
]
for i, (k, v) in enumerate(rows_data):
    fmt_cell(t.rows[i+1].cells[0], k, center=False, size=10, bold=True)
    fmt_cell(t.rows[i+1].cells[1], v, center=False, size=10)
set_col_widths(t, [Cm(4), Cm(10)])
caption(doc, "Taula 1. Configuració experimental de la Fase 2A.")

heading(doc, "2.2. Hipòtesi de Treball", 2)
body(doc, (
    "La hipòtesi inicial plantejava que una temperatura moderada (T=0.3–0.7) podria "
    "millorar la diversitat lèxica de l'output acostant-lo a l'estil de l'anotador, "
    "mentre que T=1.0 podria generar incoherències que penalitzessin SARI i BERTScore. "
    "S'esperava també que V8 fos més sensible a la temperatura que CoT, "
    "al ser una tècnica d'imitació més estructurada."
))

heading(doc, "2.3. Mètrica d'Avaluació", 2)
body(doc, (
    "S'utilitza el mateix score compost de 7 mètriques que en la Fase 1, "
    "normalitzat globalment sobre totes les dades de la fase per permetre comparació directa. "
    "Les 7 mètriques i la seva direcció òptima són:"
))
doc.add_paragraph()

t2 = doc.add_table(rows=8, cols=3)
t2.style = "Table Grid"
hdr_row(t2, ["Mètrica", "Descripció", "Òptim"])
metrics = [
    ("SARI (÷100)", "Qualitat de simplificació: addició, conservació, eliminació de paraules", "↑ Màxim"),
    ("BERTScore F1", "Preservació semàntica via embeddings contextuals BERT", "↑ Màxim"),
    ("Levenshtein sim.", "Proximitat estilística a l'anotador humà", "↑ Màxim"),
    ("Flesch ratio", "Flesch_generat / Flesch_referència. Llegibilitat relativa", "≈ 1.0"),
    ("CR ratio", "Compressió_model / Compressió_humana. Proporció de compressió", "≈ 1.0"),
    ("TTR ratio", "Diversitat lèxica relativa respecte a la referència", "≈ 1.0"),
    ("CWR ratio", "Ràtio de paraules complexes respecte a la referència", "≈ 1.0"),
]
for i, (m, d, o) in enumerate(metrics):
    fmt_cell(t2.rows[i+1].cells[0], m, center=False, size=9, bold=True)
    fmt_cell(t2.rows[i+1].cells[1], d, center=False, size=9)
    fmt_cell(t2.rows[i+1].cells[2], o, center=True, size=9)
set_col_widths(t2, [Cm(3.0), Cm(8.5), Cm(2.0)])
caption(doc, "Taula 2. Mètriques del score compost i direcció òptima.")

# ══════════════════════════════════════════════════════════════════════════════
# 3. RESULTATS — test_poor
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "3. Resultats — Dataset test_poor")
body(doc, (
    "El dataset test_poor conté 12 textos de temàtica administrativa de complexitat alta, "
    "amb referències produïdes per anotadors humans. "
    "Els textos originals presenten estructures subordinades complexes, vocabulari tècnic-burocràtic "
    "i una longitud mitjana per oració superior a 20 paraules. "
    "Aquest dataset va ser el banc de proves principal de la Fase 1 "
    "i és on el sistema obté els seus millors resultats absoluts."
))

heading(doc, "3.1. Score Compost per Model i Temperatura", 2)
body(doc, (
    "La Taula 3 mostra el score compost mitjà (promig sobre V8 i CoT) per a cada combinació "
    "model × temperatura. La cel·la verda indica el màxim global."
))
doc.add_paragraph()

t3 = doc.add_table(rows=3, cols=5)
t3.style = "Table Grid"
hdr_row(t3, ["Model", "T=0.0", "T=0.3", "T=0.7", "T=1.0"])
data3 = [
    ("gemma2:27b", "0.5435", "0.5012", "0.5122", "0.4995"),
    ("llama3.3",   "0.6333", "0.6180", "0.6066", "0.5813"),
]
for i, (model, *vals) in enumerate(data3):
    fmt_cell(t3.rows[i+1].cells[0], model, center=False, size=10, bold=True)
    for j, v in enumerate(vals):
        fmt_cell(t3.rows[i+1].cells[j+1], v, size=10)
highlight_max(t3, [1, 2], [1, 2, 3, 4])
set_col_widths(t3, [Cm(3.5), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)])
caption(doc, "Taula 3. Score compost (mitjana V8+CoT) per model i temperatura — test_poor. Verd = màxim global.")

body(doc, (
    "llama3.3 supera gemma2:27b en totes les temperatures quan s'obté la mitjana entre prompts. "
    "La degradació de llama3.3 és monòtona: cada increment de temperatura redueix el score. "
    "gemma2:27b presenta un comportament no monòton (recupera lleugerament a T=0.7 respecte T=0.3), "
    "senyal d'una major sensibilitat al soroll estocàstic."
))

heading(doc, "3.2. Desglose per Prompt i Temperatura", 2)
body(doc, "La Taula 4 desglossa els resultats per prompt, revelant un comportament asimètric entre V8 i CoT.")
doc.add_paragraph()

t4 = doc.add_table(rows=5, cols=5)
t4.style = "Table Grid"
hdr_row(t4, ["Model / Prompt", "T=0.0", "T=0.3", "T=0.7", "T=1.0"])
data4 = [
    ("gemma2:27b — CoT", "0.3229", "0.3061", "0.2391", "0.3177"),
    ("gemma2:27b — V8",  "0.7641", "0.6964", "0.7854", "0.6812"),
    ("llama3.3 — CoT",   "0.5233", "0.4801", "0.4449", "0.4316"),
    ("llama3.3 — V8",    "0.7434", "0.7558", "0.7683", "0.7310"),
]
for i, (label, *vals) in enumerate(data4):
    fmt_cell(t4.rows[i+1].cells[0], label, center=False, size=10, bold=True)
    for j, v in enumerate(vals):
        fmt_cell(t4.rows[i+1].cells[j+1], v, size=10)
highlight_max(t4, [1, 2, 3, 4], [1, 2, 3, 4])
set_col_widths(t4, [Cm(4.0), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)])
caption(doc, "Taula 4. Score compost per model, prompt i temperatura — test_poor. Verd = màxim absolut.")

body(doc, (
    "V8 domina àmpliament sobre CoT en les dues configuracions de model, "
    "confirmant el resultat de la Fase 1. L'efecte de la temperatura sobre V8 és oposat entre models: "
    "llama3.3 assoleix el seu pic a T=0.3 (0.7558), mentre que gemma2:27b el assoleix a T=0.7 (0.7854). "
    "Tots els millors resultats de CoT es concentren a T=0.0, independentment del model."
))

heading(doc, "3.3. Mètriques Absolutes per Temperatura", 2)
body(doc, (
    "La Taula 5 mostra les mètriques individuals promitjades sobre totes les combinacions "
    "model×prompt per a cada temperatura, permetent identificar quines dimensions es degraden primer."
))
doc.add_paragraph()

t5 = doc.add_table(rows=5, cols=6)
t5.style = "Table Grid"
hdr_row(t5, ["T", "SARI", "BERTScore", "Levenshtein", "Flesch r", "CR r"])
data5 = [
    ("0.0", "48.08", "0.793", "0.258", "1.034", "1.055"),
    ("0.3", "47.39", "0.792", "0.244", "1.038", "1.064"),
    ("0.7", "46.53", "0.789", "0.252", "1.043", "1.020"),
    ("1.0", "47.15", "0.789", "0.244", "1.010", "1.073"),
]
for i, row_data in enumerate(data5):
    for j, v in enumerate(row_data):
        fmt_cell(t5.rows[i+1].cells[j], v, size=10)
for col in [1, 2, 3]:
    highlight_max(t5, [1, 2, 3, 4], [col])
set_col_widths(t5, [Cm(1.5), Cm(2.0), Cm(2.5), Cm(3.0), Cm(2.5), Cm(2.0)])
caption(doc, "Taula 5. Mètriques absolutes per temperatura (mitjana totes combinacions) — test_poor. Verd = màxim per columna.")

body(doc, (
    "SARI i BERTScore assoleixen el màxim a T=0.0 i decauen amb la temperatura. "
    "El Flesch ratio més proper a 1.0 s'obté a T=1.0 (1.010 vs 1.034 a T=0.0), "
    "la qual cosa suggereix que una major variabilitat pot acostar l'estil de llegibilitat "
    "a la referència, però a costa de penalitzar les mètriques de contingut."
))

heading(doc, "3.4. Top-5 Combinacions", 2)
body(doc, (
    "La Taula 6 recull les cinc millors combinacions absolutes a test_poor, "
    "incloent les mètriques individuals clau per entendre per què destaquen."
))
doc.add_paragraph()

t6 = doc.add_table(rows=6, cols=9)
t6.style = "Table Grid"
hdr_row(t6, ["#", "Model", "T", "Prompt", "Score", "SARI", "BERTScore", "Levenshtein", "CR r"])
top5_poor = [
    ("1", "gemma2:27b", "0.7", "V8",  "0.7854", "57.65", "0.835", "0.326", "1.187"),
    ("2", "llama3.3",   "0.7", "V8",  "0.7683", "56.67", "0.827", "0.367", "1.235"),
    ("3", "gemma2:27b", "0.0", "V8",  "0.7641", "58.95", "0.827", "0.362", "1.205"),
    ("4", "llama3.3",   "0.3", "V8",  "0.7558", "55.87", "0.828", "0.317", "1.208"),
    ("5", "llama3.3",   "0.0", "V8",  "0.7434", "57.56", "0.832", "0.346", "1.194"),
]
for i, row_data in enumerate(top5_poor):
    for j, v in enumerate(row_data):
        bold = (i == 0)
        fmt_cell(t6.rows[i+1].cells[j], v, size=9, bold=bold)
    shade(t6.rows[i+1].cells[0], "D5E8D4" if i == 0 else "FFFFFF")
set_col_widths(t6, [Cm(0.6), Cm(2.5), Cm(1.0), Cm(1.5), Cm(1.5), Cm(1.5), Cm(2.2), Cm(2.5), Cm(1.2)])
caption(doc, "Taula 6. Top-5 combinacions per score compost — test_poor. La fila verda és el màxim puntual.")

body(doc, (
    "La millor combinació puntual és gemma2:27b + T=0.7 + V8 (score=0.785). "
    "Tanmateix, la diferència amb el 3r classificat (gemma2:27b + T=0.0 + V8, score=0.764) "
    "és de tan sols 0.021 punts sobre N=12 textos, la qual cosa no permet establir "
    "significació estadística. Les cinc millors combinacions utilitzen exclusivament V8."
))

# ══════════════════════════════════════════════════════════════════════════════
# 4. RESULTATS — exemples
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "4. Resultats — Dataset exemples_lectura_facil_formatted")
body(doc, (
    "El dataset exemples_lectura_facil_formatted conté 11 textos de domini divers "
    "(salut, educació, cuina, telecomunicacions, economia, jocs) "
    "amb referències certificades de Lectura Fàcil. "
    "A diferència de test_poor, els textos de referència ja estan en format Lectura Fàcil, "
    "la qual cosa genera un CR ratio sistemàticament inferior a 1.0 (~0.63): "
    "les referències humanes són més concises que els outputs generats."
))

heading(doc, "4.1. Score Compost per Model i Temperatura", 2)
doc.add_paragraph()

t7 = doc.add_table(rows=3, cols=5)
t7.style = "Table Grid"
hdr_row(t7, ["Model", "T=0.0", "T=0.3", "T=0.7", "T=1.0"])
data7 = [
    ("gemma2:27b", "0.2886", "0.2967", "0.2583", "0.3654"),
    ("llama3.3",   "0.4575", "0.4059", "0.3297", "0.3119"),
]
for i, (model, *vals) in enumerate(data7):
    fmt_cell(t7.rows[i+1].cells[0], model, center=False, size=10, bold=True)
    for j, v in enumerate(vals):
        fmt_cell(t7.rows[i+1].cells[j+1], v, size=10)
highlight_max(t7, [1, 2], [1, 2, 3, 4])
set_col_widths(t7, [Cm(3.5), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)])
caption(doc, "Taula 7. Score compost (mitjana V8+CoT) per model i temperatura — exemples.")

body(doc, (
    "llama3.3 domina de forma contundent (+58% sobre gemma2:27b a T=0.0). "
    "Els comportaments de temperatura són qualitativament oposats entre models: "
    "llama3.3 es degrada monòtonament, mentre que gemma2:27b millora en augmentar la temperatura, "
    "assolint el màxim a T=1.0. "
    "Aquest patró invers apunta a diferències fonamentals en com cada model gestiona l'aleatorietat "
    "davant textos de referència de Lectura Fàcil."
))

heading(doc, "4.2. Desglose per Prompt i Temperatura — Inversió V8/CoT", 2)
body(doc, (
    "La Taula 8 revela el hallazgo més important de la fase: "
    "en aquest dataset, CoT supera V8 per a llama3.3, just al contrari que a test_poor."
))
doc.add_paragraph()

t8 = doc.add_table(rows=5, cols=5)
t8.style = "Table Grid"
hdr_row(t8, ["Model / Prompt", "T=0.0", "T=0.3", "T=0.7", "T=1.0"])
data8 = [
    ("gemma2:27b — CoT", "0.2710", "0.2725", "0.2246", "0.3159"),
    ("gemma2:27b — V8",  "0.3063", "0.3210", "0.2919", "0.4149"),
    ("llama3.3 — CoT",   "0.4851", "0.4746", "0.3668", "0.3754"),
    ("llama3.3 — V8",    "0.4298", "0.3371", "0.2925", "0.2484"),
]
for i, (label, *vals) in enumerate(data8):
    fmt_cell(t8.rows[i+1].cells[0], label, center=False, size=10, bold=True)
    for j, v in enumerate(vals):
        fmt_cell(t8.rows[i+1].cells[j+1], v, size=10)
highlight_max(t8, [1, 2, 3, 4], [1, 2, 3, 4])
set_col_widths(t8, [Cm(4.0), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)])
caption(doc, "Taula 8. Score compost per model, prompt i temperatura — exemples. Verd = màxim absolut.")

body(doc, (
    "Per a llama3.3, CoT (0.485) supera V8 (0.430) a T=0.0. "
    "V8 es degrada dràsticament amb la temperatura (0.430 → 0.248), "
    "mentre que CoT es manté relativament estable (0.485 → 0.375). "
    "La hipòtesi explicativa: V8 ancora el seu output a exemples concrets de l'anotador administratiu; "
    "quan els textos de referència ja segueixen un altre estil de Lectura Fàcil, "
    "V8 introdueix un biaix de domini que CoT evita raonant des de principis generals."
))

heading(doc, "4.3. Mètriques Absolutes per Temperatura", 2)
doc.add_paragraph()

t9 = doc.add_table(rows=5, cols=6)
t9.style = "Table Grid"
hdr_row(t9, ["T", "SARI", "BERTScore", "Levenshtein", "Flesch r", "CR r"])
data9 = [
    ("0.0", "48.45", "0.764", "0.188", "1.082", "0.628"),
    ("0.3", "47.30", "0.762", "0.197", "1.060", "0.632"),
    ("0.7", "47.16", "0.759", "0.186", "1.073", "0.614"),
    ("1.0", "47.16", "0.762", "0.189", "1.086", "0.616"),
]
for i, row_data in enumerate(data9):
    for j, v in enumerate(row_data):
        fmt_cell(t9.rows[i+1].cells[j], v, size=10)
for col in [1, 2, 3]:
    highlight_max(t9, [1, 2, 3, 4], [col])
set_col_widths(t9, [Cm(1.5), Cm(2.0), Cm(2.5), Cm(3.0), Cm(2.5), Cm(2.0)])
caption(doc, "Taula 9. Mètriques absolutes per temperatura — exemples. CR ratio <1.0 = el model genera textos més llargs que la referència.")

body(doc, (
    "El CR ratio és sistemàticament inferior a 1.0 (~0.63) en tots els casos, "
    "confirmant la inversió ja identificada a la Fase 1: "
    "els textos de referència de Lectura Fàcil d'aquest dataset "
    "són més concrets i concisos que els outputs generats pel model. "
    "El model tendeix a generar adaptacions massa llargues respecte a l'estil de l'anotador."
))

heading(doc, "4.4. Top-5 Combinacions", 2)
doc.add_paragraph()

t10 = doc.add_table(rows=6, cols=9)
t10.style = "Table Grid"
hdr_row(t10, ["#", "Model", "T", "Prompt", "Score", "SARI", "BERTScore", "Levenshtein", "CR r"])
top5_ex = [
    ("1", "llama3.3",   "0.0", "CoT", "0.4851", "50.07", "0.768", "0.192", "0.654"),
    ("2", "llama3.3",   "0.3", "CoT", "0.4746", "47.14", "0.759", "0.186", "0.652"),
    ("3", "llama3.3",   "0.0", "V8",  "0.4298", "48.42", "0.759", "0.190", "0.634"),
    ("4", "gemma2:27b", "1.0", "V8",  "0.4149", "47.72", "0.766", "0.203", "0.650"),
    ("5", "llama3.3",   "1.0", "CoT", "0.3754", "49.21", "0.765", "0.187", "0.627"),
]
for i, row_data in enumerate(top5_ex):
    for j, v in enumerate(row_data):
        fmt_cell(t10.rows[i+1].cells[j], v, size=9, bold=(i == 0))
    shade(t10.rows[i+1].cells[0], "D5E8D4" if i == 0 else "FFFFFF")
set_col_widths(t10, [Cm(0.6), Cm(2.5), Cm(1.0), Cm(1.5), Cm(1.5), Cm(1.5), Cm(2.2), Cm(2.5), Cm(1.2)])
caption(doc, "Taula 10. Top-5 combinacions per score compost — exemples.")

body(doc, (
    "CoT domina el top-5 d'aquest dataset, al contrari de test_poor on V8 ocupava les cinc primeres posicions. "
    "La millor combinació (llama3.3 + T=0.0 + CoT, score=0.485) és significativament inferior "
    "al millor de test_poor (0.785), cosa que reflecteix la major dificultat d'aquest dataset "
    "per al sistema actual."
))

# ══════════════════════════════════════════════════════════════════════════════
# 5. ANÀLISI COMPARATIVA ENTRE DATASETS
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "5. Anàlisi Comparativa entre Datasets")
heading(doc, "5.1. Estabilitat Cross-Dataset per Configuració", 2)
body(doc, (
    "La mètrica més rellevant per seleccionar la configuració definitiva és el "
    "gap inter-dataset (diferència de score entre test_poor i exemples): "
    "un gap alt indica que la configuració s'especialitza en un domini i falla en l'altre. "
    "La Taula 11 compara les principals configuracions."
))
doc.add_paragraph()

t11 = doc.add_table(rows=8, cols=7)
t11.style = "Table Grid"
hdr_row(t11, ["Model", "T", "Prompt", "test_poor", "exemples", "Mitjana", "Gap"])
stability = [
    ("llama3.3",   "0.3", "CoT", "0.4801", "0.4746", "0.477", "0.005"),
    ("llama3.3",   "0.0", "CoT", "0.5233", "0.4851", "0.504", "0.038"),
    ("gemma2:27b", "1.0", "CoT", "0.3177", "0.3159", "0.317", "0.002"),
    ("gemma2:27b", "0.7", "CoT", "0.2391", "0.2246", "0.232", "0.014"),
    ("llama3.3",   "0.0", "V8",  "0.7434", "0.4298", "0.587", "0.314"),
    ("llama3.3",   "0.7", "V8",  "0.7683", "0.2925", "0.530", "0.476"),
    ("gemma2:27b", "0.7", "V8",  "0.7854", "0.2919", "0.539", "0.494"),
]
for i, (model, temp, prompt, tp, ex, avg, gap) in enumerate(stability):
    is_recommended = (model == "llama3.3" and temp == "0.0" and prompt == "V8")
    is_best_peak   = (model == "gemma2:27b" and temp == "0.7" and prompt == "V8")
    bg = "D5E8D4" if is_recommended else ("FFF2CC" if is_best_peak else "FFFFFF")
    row = t11.rows[i+1]
    for j, v in enumerate([model, temp, prompt, tp, ex, avg, gap]):
        fmt_cell(row.cells[j], v, size=9, bold=is_recommended)
        shade(row.cells[j], bg)
    # Color gap: low=green, high=red
    try:
        gval = float(gap)
        col = C_GREEN if gval < 0.05 else (C_ORANGE if gval < 0.2 else C_RED)
        for par in row.cells[6].paragraphs:
            for run in par.runs:
                run.font.color.rgb = col
                run.font.bold = True
    except:
        pass
set_col_widths(t11, [Cm(2.8), Cm(1.0), Cm(1.8), Cm(2.0), Cm(2.0), Cm(1.8), Cm(1.8)])
caption(doc, (
    "Taula 11. Estabilitat cross-dataset. Verd = configuració recomanada (llama3.3+T=0.0+V8); "
    "groc = millor puntual (gemma2:27b+T=0.7+V8). Gap en vermell = alta especialització de domini."
))

body(doc, (
    "Les configuracions amb CoT presenten gaps molt reduïts (0.002–0.038), "
    "mentre que totes les configuracions amb V8 presenten gaps elevats (0.265–0.494). "
    "Això confirma que CoT generalitza entre dominis i V8 s'especialitza en text administratiu. "
    "La configuració llama3.3+T=0.0+V8 (fila verda) combina el màxim de rendiment "
    "en el dataset administratiu amb el menor gap entre les opcions d'alt rendiment."
))

heading(doc, "5.2. Efecte de la Temperatura sobre l'Estabilitat", 2)
body(doc, (
    "La Taula 12 mostra com la desviació estàndard del score entre datasets "
    "creix de forma contínua amb la temperatura per a llama3.3+V8, "
    "el cas amb l'efecte de temperatura més marcat."
))
doc.add_paragraph()

t12 = doc.add_table(rows=5, cols=5)
t12.style = "Table Grid"
hdr_row(t12, ["T", "test_poor", "exemples", "Diferència", "Std entre datasets"])
temp_stability = [
    ("0.0", "0.7434", "0.4298", "0.313", "0.157"),
    ("0.3", "0.7558", "0.3371", "0.419", "0.209"),
    ("0.7", "0.7683", "0.2925", "0.476", "0.238"),
    ("1.0", "0.7310", "0.2484", "0.483", "0.241"),
]
for i, row_data in enumerate(temp_stability):
    for j, v in enumerate(row_data):
        fmt_cell(t12.rows[i+1].cells[j], v, size=10)
    try:
        std = float(temp_stability[i][4])
        col = C_GREEN if std < 0.17 else (C_ORANGE if std < 0.22 else C_RED)
        for par in t12.rows[i+1].cells[4].paragraphs:
            for run in par.runs:
                run.font.color.rgb = col
                run.font.bold = True
    except:
        pass
set_col_widths(t12, [Cm(1.5), Cm(2.5), Cm(2.5), Cm(2.5), Cm(3.5)])
caption(doc, "Taula 12. Efecte de la temperatura sobre l'estabilitat cross-dataset (llama3.3+V8).")

body(doc, (
    "La desviació estàndard entre datasets creix de 0.157 a T=0.0 fins a 0.241 a T=1.0 (+54%). "
    "Augmentar la temperatura no tan sols degrada el rendiment mitjà, "
    "sinó que amplifica l'especialització de domini, fent el model menys generalitzable."
))

heading(doc, "5.3. Inversió del Rendiment Relatiu V8 vs. CoT", 2)
body(doc, (
    "La Taula 13 resumeix la inversió completa del rànquing de prompts entre datasets, "
    "el finding més destacat de la Fase 2A."
))
doc.add_paragraph()

t13 = doc.add_table(rows=3, cols=4)
t13.style = "Table Grid"
hdr_row(t13, ["Dataset", "Millor prompt (llama3.3, T=0.0)", "Score", "Diferència vs. l'altre"])
inv_data = [
    ("test_poor", "V8", "0.7434", "+0.220 respecte CoT (0.5233)"),
    ("exemples",  "CoT","0.4851", "+0.055 respecte V8 (0.4298)"),
]
for i, row_data in enumerate(inv_data):
    for j, v in enumerate(row_data):
        fmt_cell(t13.rows[i+1].cells[j], v, center=(j > 0), size=10)
set_col_widths(t13, [Cm(3.0), Cm(3.5), Cm(1.8), Cm(5.0)])
caption(doc, (
    "Taula 13. Inversió del prompt dominant entre datasets "
    "(llama3.3, T=0.0). V8 guanya clarament a test_poor; CoT guanya a exemples."
))

body(doc, (
    "La hipòtesi explicativa: V8 és una tècnica d'imitació que ancora l'estil de l'output "
    "als exemples de l'anotador administratiu presents en el prompt. "
    "A test_poor, on els textos d'origen també són administratius, "
    "aquest anclatge és un avantatge (+22 punts). "
    "A exemples, on les referències ja estan en format Lectura Fàcil "
    "amb un estil diferent del que copia V8, el biaix de domini perjudica el rendiment. "
    "CoT, en raona des de principis generals de simplificació, "
    "s'adapta millor a qualsevol domini textual."
))

# ══════════════════════════════════════════════════════════════════════════════
# 6. DISCUSSIÓ
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "6. Discussió")

heading(doc, "6.1. La Temperatura no Millora la Simplificació a Lectura Fàcil", 2)
body(doc, (
    "Contràriament a la hipòtesi inicial, incrementar la temperatura no produeix millores "
    "sistemàtiques en cap dels dos datasets. SARI, la mètrica primària per a simplificació "
    "de text, és màxima a T=0.0 en ambdós datasets (48.08 i 48.45 respectivament). "
    "BERTScore segueix el mateix patró."
))
body(doc, (
    "Això suggereix que la tasca de simplificació a Lectura Fàcil no es beneficia "
    "de l'exploració estocàstica addicional: els models ja contenen el coneixement "
    "necessari en la seva distribució modal, i allunyar-se'n introdueix soroll. "
    "Aquest resultat és coherent amb la literatura: Wang et al. (2023) van demostrar "
    "que la consistència de les respostes disminueix amb la temperatura fins i tot "
    "quan la qualitat mitjana es manté estable, i Holtzman et al. (2020) van mostrar "
    "que el mostreig amb temperatura alta pot generar outputs que s'allunyen "
    "de la distribució de referència en tasques de generació condicionada."
))

heading(doc, "6.2. Comportaments Asimètrics entre Models", 2)
body(doc, (
    "El comportament oposat de gemma2:27b (millora amb temperatura a exemples) "
    "respecte a llama3.3 (es degrada amb temperatura) suggereix diferències "
    "arquitectòniques en com cada model gestiona l'aleatorietat. "
    "gemma2:27b a exemples parteix d'un baseline tan baix (0.289 a T=0.0) "
    "que qualsevol variació pot produir outputs accidentalment millors. "
    "Aquest efecte de 'soroll beneficiós' en models amb baix rendiment base "
    "no ha d'interpretar-se com una virtut de la temperatura, "
    "sinó com a artefacte estadístic sobre N=11 textos."
))

heading(doc, "6.3. La Generalització com a Criteri de Selecció", 2)
body(doc, (
    "L'elecció de la configuració definitiva no pot basar-se únicament en el màxim puntual. "
    "gemma2:27b+T=0.7+V8 obté el score més alt a test_poor (0.785), "
    "però col·lapsa a exemples (0.292), amb una mitjana de 0.539. "
    "llama3.3+T=0.0+V8 obté 0.743 a test_poor i 0.430 a exemples, "
    "amb una mitjana de 0.587 i un gap de 0.314. "
    "Des de la perspectiva d'un sistema desplegat en producció "
    "que ha de processar textos de múltiples dominis, "
    "la robustesa cross-domain és més valuosa que el màxim en un sol domini."
))

heading(doc, "6.4. Reproduïbilitat com a Requisit Científic", 2)
body(doc, (
    "T=0.0 és determinista: donat el mateix input i el mateix model, "
    "l'output és idèntic en totes les execucions. "
    "Això satisfà un requisit fonamental de reproduïbilitat científica "
    "que T>0 no pot garantir sense múltiples execucions i anàlisi de variança. "
    "Per a un sistema en producció, la predictibilitat de l'output "
    "és una propietat operacional crítica que reforça l'elecció de T=0.0."
))

# ══════════════════════════════════════════════════════════════════════════════
# 7. CONCLUSIONS
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "7. Conclusions")
body(doc, "Es presenten les set conclusions de la Fase 2A en ordre de rellevància:")

concls = [
    ("C1", "La temperatura no millora l'adaptació a Lectura Fàcil",
     "SARI i BERTScore assoleixen el màxim a T=0.0 en els dos datasets sense excepció. "
     "La hipòtesi que una temperatura moderada milloraria la diversitat lèxica "
     "i l'aproximació a l'estil de l'anotador no es confirma."),
    ("C2", "llama3.3 és el model més robust entre dominis",
     "Supera gemma2:27b en el 75% de les combinacions temperatura×prompt "
     "i lidera de forma contundent a exemples (+58% a T=0.0), el dataset més exigent."),
    ("C3", "Temperatura més alta amplifica l'especialització de domini",
     "La desviació estàndard de llama3.3+V8 entre datasets creix de 0.157 (T=0.0) "
     "a 0.241 (T=1.0). Augmentar la temperatura fa el model "
     "més expert en el domini fàcil i pitjor en el difícil."),
    ("C4", "V8 s'especialitza en text administratiu; CoT generalitza entre dominis",
     "La inversió completa del rànquing de prompts entre datasets "
     "(V8 guanya +22pp a test_poor, perd −5pp a exemples per a llama3.3) "
     "és el finding més rellevant de la fase. "
     "En sistemes multi-domini, CoT ofereix estabilitat amb gaps de 0.005–0.038 "
     "front els 0.265–0.494 de V8."),
    ("C5", "La configuració globalment òptima és llama3.3 + T=0.0 + V8",
     "Maximitza la mitjana cross-dataset (0.587) amb el menor gap "
     "entre configuracions d'alt rendiment (0.314). "
     "Ofereix a més reproduïbilitat determinista. "
     "Recomanada per a desplegament en dominis administratius."),
    ("C6", "El pic de gemma2:27b+T=0.7+V8 a test_poor no és generalitzable",
     "Amb N=12 textos, la diferència de 0.021 punts respecte a llama3.3+T=0.0+V8 "
     "no és estadísticament significativa, i el model presenta comportament no monòton "
     "respecte a la temperatura, senyal d'alta sensibilitat al soroll mostral."),
    ("C7", "L'avaluació automàtica sobre N petit té limitacions",
     "Amb 11–12 textos per dataset, els resultats són orientatius "
     "però no permeten inferències estadístiques sòlides. "
     "La validació humana confirma les tendències principals "
     "però és necessari un corpus de validació més gran per a conclusions definitives."),
]
for num, tit, txt in concls:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.3)
    p.paragraph_format.space_before = Pt(6)
    r1 = p.add_run(f"{num} — {tit}: ")
    r1.font.bold = True; r1.font.size = Pt(11); r1.font.color.rgb = C_BLUE_D
    r2 = p.add_run(txt)
    r2.font.size = Pt(11)

# ══════════════════════════════════════════════════════════════════════════════
# 8. CONFIGURACIÓ RECOMANADA PER A PRODUCCIÓ
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "8. Configuració Recomanada per a Producció")
body(doc, (
    "Basant-se en l'anàlisi de robustesa cross-dataset, reproduïbilitat i rendiment absolut, "
    "la Taula 14 recull les configuracions recomanades per a dos escenaris d'ús."
))
doc.add_paragraph()

t14 = doc.add_table(rows=5, cols=3)
t14.style = "Table Grid"
hdr_row(t14, ["Paràmetre", "Domini administratiu (especialitzat)", "Multi-domini (general)"])
prod = [
    ("Model",       "llama3.3 (70B)", "llama3.3 (70B)"),
    ("Temperatura", "0.0 — determinista", "0.0 — determinista"),
    ("Prompt",      "V8 — imitació progressiva", "CoT — cadena de raonament"),
    ("Justificació","Score 0.743 a test_poor\n+22pp sobre CoT en text administratiu",
                    "Gap inter-dataset 0.038 (vs 0.314 de V8)\nEstable en qualsevol domini"),
]
for i, (param, v1, v2) in enumerate(prod):
    fmt_cell(t14.rows[i+1].cells[0], param, center=False, size=10, bold=True)
    fmt_cell(t14.rows[i+1].cells[1], v1, center=False, size=10)
    fmt_cell(t14.rows[i+1].cells[2], v2, center=False, size=10)
for j in range(3):
    shade(t14.rows[4].cells[j], "EAF4EA")
set_col_widths(t14, [Cm(3.0), Cm(6.0), Cm(5.0)])
caption(doc, "Taula 14. Configuració recomanada per a producció en funció de l'escenari d'ús.")

# ══════════════════════════════════════════════════════════════════════════════
# 9. PRÒXIMS PASSOS — FASE 2B
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "9. Pròxims Passos — Fase 2B")
body(doc, (
    "Els resultats de la Fase 2A confirmen T=0.0 com a temperatura òptima, "
    "però descarten la Fase 2B de variabilitat de llavor sobre aquesta temperatura "
    "al ser determinista (seed diferent no canvia el resultat a T=0.0). "
    "Si es vol estudiar l'estabilitat estocàstica del sistema, "
    "la temperatura candidata és T=0.3, la millor temperatura no-determinista:"
))
bullet(doc, "test_poor: llama3.3 + T=0.3 + V8 = 0.756 (2n millor absolut)")
bullet(doc, "exemples: llama3.3 + T=0.3 + CoT = 0.475 (2n millor absolut)")
body(doc, (
    "La Fase 2B amb T=0.3 respondria: quant varia l'output entre execucions "
    "amb la mateixa configuració i llavors distintes? "
    "Això mesuraria l'estabilitat estocàstica intrínseca del model "
    "i permetria reportar resultats amb intervals de confiança."
))

# ══════════════════════════════════════════════════════════════════════════════
# 10. LIMITACIONS
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "10. Limitacions de l'Estudi")
for lim in [
    ("N reduït per dataset",
     "Amb 11–12 textos per dataset, les diferències de 0.01–0.02 en score compost "
     "no assoleixen significació estadística. Es requereix un corpus d'almenys 50 textos "
     "per confirmar les tendències amb p<0.05."),
    ("Semilla única",
     "Tots els experiments s'han executat amb seed=42. "
     "Per a T>0.0, una sola semilla no captura la variabilitat intrínseca del mostreig. "
     "La Fase 2B hauria d'abordar aquesta limitació."),
    ("Dos models i dos prompts",
     "L'espai explorat és una subselecció de la Fase 1 (8 models, 20 prompts). "
     "Models intermedis (qwen2.5:32b, command-r) podrien respondre diferent a la temperatura."),
    ("Sense validació estadística formal",
     "No s'han aplicat tests de significació (t-test, ANOVA) per la mida de la mostra. "
     "Les comparacions es basen en diferències absolutes de score compost normalitzat."),
    ("Mètriques automàtiques vs. qualitat humana",
     "Com s'ha confirmat a l'estudi amb usuaris finals, les mètriques automàtiques "
     "no detecten tots els fenòmens rellevants (e.g., regressió lèxica). "
     "La Fase 2A s'hauria de complementar amb avaluació humana per a conclusions definitives."),
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent  = Cm(0.3)
    p.paragraph_format.space_before = Pt(4)
    r1 = p.add_run(f"• {lim[0]}: ")
    r1.font.bold = True; r1.font.size = Pt(11)
    r2 = p.add_run(lim[1])
    r2.font.size = Pt(11)

# ══════════════════════════════════════════════════════════════════════════════
# REFERÈNCIES
# ══════════════════════════════════════════════════════════════════════════════
heading(doc, "Referències")
for ref in [
    "Holtzman, A., Buys, J., Du, L., Forbes, M., & Choi, Y. (2020). "
    "The curious case of neural text degeneration. Proceedings of ICLR 2020.",
    "Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., ... & Zhou, D. (2023). "
    "Self-consistency improves chain of thought reasoning in language models. Proceedings of ICLR 2023.",
    "Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F., Chi, E., ... & Zhou, D. (2022). "
    "Chain-of-thought prompting elicits reasoning in large language models. NeurIPS, 35, 24824–24837.",
    "Xu, W., Napoles, C., Pavlick, E., Chen, Q., & Callison-Burch, C. (2016). "
    "Optimizing statistical machine translation for text simplification. "
    "Transactions of the Association for Computational Linguistics, 4, 401–415.",
    "Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). "
    "BERTScore: Evaluating text generation with BERT. Proceedings of ICLR 2020.",
]:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent   = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.space_after   = Pt(3)
    r = p.add_run(ref)
    r.font.size = Pt(10)

# ── GUARDAR ───────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f"Guardat: {OUT}")
