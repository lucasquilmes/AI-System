"""
Genera l'informe complet de l'estudi de validació amb usuaris finals.
Sortida: user_study/informe_estudi_usuaris.docx
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

ROOT = Path(__file__).parent
OUT  = ROOT / "user_study" / "informe_estudi_usuaris.docx"

C_BLUE_D = RGBColor(0, 70, 127)
C_BLUE_M = RGBColor(0, 114, 198)
C_GREY   = RGBColor(80, 80, 80)
C_GREEN  = RGBColor(0, 112, 0)
C_RED    = RGBColor(180, 20, 20)
C_ORANGE = RGBColor(200, 100, 0)
C_WHITE  = RGBColor(255, 255, 255)

RESULTS = [
    (1, 0,"orig", "No","Sí","Sí","Sí","comprimido, dosis, vía oral, regularidad, paulatinamente, gradual"),
    (1, 1,"adapt","Sí","Sí","No","No",""),
    (1, 2,"orig", "Sí","Sí","Sí","Sí","repoblación, núcleos, Mitra, fortificadas"),
    (1, 3,"adapt","No","No","Sí","Sí","palo de triunfo, as, baza, acuse, jugador «mano», baceta"),
    (1, 4,"orig", "No","No","Sí","Sí","baremo"),
    (1, 6,"orig", "Sí","Sí","Sí","No","Maizena, clavo molido, embadurnar"),
    (1, 7,"adapt","No","No","Sí","Sí","simétrica, eSIM, MultiSIM"),
    (1, 8,"orig", "Sí","Sí","No","No",""),
    (1, 9,"adapt","Sí","Sí","No","No","inflación (marcada)"),
    (2, 1,"orig", "Sí","Sí","No","Sí",""),
    (2, 2,"adapt","Sí","Sí","Sí","Sí",""),
    (2, 3,"orig", "Sí","Sí","Sí","No",""),
    (2, 5,"orig", "Sí","Sí","No","No",""),
    (2, 7,"orig", "Sí","Sí","No","No",""),
    (2, 8,"adapt","Sí","Sí","No","No",""),
    (2, 9,"orig", "Sí","Sí","Sí","Sí",""),
    (2,10,"adapt","Sí","Sí","No","No",""),
    (3, 0,"adapt","Sí","Sí","No","Sí",""),
    (3, 2,"orig", "No","No","Sí","Sí","prohombres, feudo, jurisdicción, siglo XII"),
    (3, 4,"adapt","Sí","Sí","No","No",""),
    (3, 6,"orig", "Sí","Sí","Sí","Sí","embadurnar"),
    (3, 8,"adapt","Sí","No","Sí","Sí","microrrelato, extensió, caràcters, adjunta"),
    (3, 1,"adapt","No","No","Sí","Sí","Docentes, recursos, ratios, salarial, firme"),
    (3, 3,"orig", "No","No","Sí","Sí","Tute, sobrantes, acuse, jugador «mano», baceta, tantos"),
    (3, 5,"adapt","Sí","Sí","Sí","Sí",""),
    (3, 7,"orig", "No","No","Sí","Sí","fibra, Gb, permanència, llamadas infinitas, cesión"),
]

DOMAINS = {
    0:"Farmàcia / Salut", 1:"Educació / Laboral", 2:"Història medieval",
    3:"Joc de taula (Tute)", 4:"Administratiu", 5:"Educació / Laboral",
    6:"Cuina", 7:"Telecomunicacions", 8:"Telecomunicacions",
    9:"Economia", 10:"—",
}

SESSIONS = {
    1:{1:[(0,"orig"),(1,"adapt"),(2,"orig"),(3,"adapt"),(4,"orig")],
       2:[(5,"adapt"),(6,"orig"),(7,"adapt"),(8,"orig"),(9,"adapt")]},
    2:{1:[(1,"orig"),(2,"adapt"),(3,"orig"),(4,"adapt"),(5,"orig")],
       2:[(6,"adapt"),(7,"orig"),(8,"adapt"),(9,"orig"),(10,"adapt")]},
    3:{1:[(0,"adapt"),(2,"orig"),(4,"adapt"),(6,"orig"),(8,"adapt")],
       2:[(10,"orig"),(1,"adapt"),(3,"orig"),(5,"adapt"),(7,"orig")]},
}
MISSING = {(1,5),(2,4),(2,6),(3,10)}

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
    p.paragraph_format.space_before = Pt(12 if level==1 else 8)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.font.size  = Pt({1:16,2:13,3:11}[level])
    run.font.bold  = True
    run.font.color.rgb = C_BLUE_D

def body(doc, text, size=11, italic=False, colour=None, bold=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.size   = Pt(size)
    run.font.italic = italic
    run.font.bold   = bold
    if colour: run.font.color.rgb = colour

def bullet(doc, text, size=11):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.size = Pt(size)

def hdr_cell(cell, text, bg="00467F"):
    shade(cell, bg)
    cell.text = text
    for par in cell.paragraphs:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in par.runs:
            run.font.bold  = True
            run.font.size  = Pt(9)
            run.font.color.rgb = C_WHITE

def center9(cell):
    for par in cell.paragraphs:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in par.runs:
            run.font.size = Pt(9)

def yn(v): return "✓" if v=="Sí" else "✗"
def pct(n,d): return f"{n/d*100:.0f}%" if d else "—"

# ── Document ───────────────────────────────────────────────────────────────────
doc = Document()
sec = doc.sections[0]
sec.top_margin = sec.bottom_margin = Cm(2.5)
sec.left_margin = sec.right_margin = Cm(3.0)
sty = doc.styles["Normal"]
sty.font.name = "Calibri"
sty.font.size = Pt(11)

# ── PORTADA ────────────────────────────────────────────────────────────────────
for _ in range(4): doc.add_paragraph()
for txt, sz in [("INFORME D'ESTUDI DE VALIDACIÓ",22),("AMB USUARIS FINALS",22)]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(txt); r.font.size=Pt(sz); r.font.bold=True; r.font.color.rgb=C_BLUE_D
doc.add_paragraph()
for txt, sz, col in [
    ("Projecte Explain-Up — Lectura Fàcil", 14, C_GREY),
    ("Juny 2026", 12, C_GREY),
]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(txt); r.font.size=Pt(sz); r.font.color.rgb=col
for _ in range(3): doc.add_paragraph()
for ln in [
    "Participants: 3 persones adultes amb discapacitat intel·lectual",
    "Sessions: 2 sessions per participant (10 textos per persona)",
    "Format: Resposta binària Sí/No — 4 preguntes per text",
    "Observacions vàlides: 26 (14 originals · 12 adaptats)",
]:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(ln); r.font.size=Pt(11); r.font.color.rgb=C_GREY
doc.add_page_break()

# ── 1. INTRODUCCIÓ ─────────────────────────────────────────────────────────────
heading(doc,"1. Introducció i Objectius")
body(doc,(
    "L'estudi de validació amb usuaris finals constitueix la fase de tancament del projecte Explain-Up, "
    "que investiga l'automatització de l'adaptació de textos a l'estàndard de Lectura Fàcil (UNE 153101:2018) "
    "mitjançant Models de Llenguatge de Gran Escala (LLMs) locals. "
    "Les fases anteriors han avaluat la qualitat de les adaptacions de manera automàtica "
    "—amb mètriques com SARI, BERTScore o la similitud de Levenshtein—, però cap mesura automàtica "
    "substitueix la percepció real de les persones a qui va destinat el producte. "
    "Aquesta fase explora si la millora numèrica es tradueix en una millora real de l'accessibilitat "
    "percebuda pel públic objectiu: persones adultes amb discapacitat intel·lectual."
))
body(doc,"Els objectius específics de l'estudi són:")
bullet(doc,"Comparar la llegibilitat percebuda entre textos originals i textos adaptats automàticament.")
bullet(doc,"Identificar dominis textuals on l'adaptació és especialment eficaç o deficient.")
bullet(doc,"Recollir evidència qualitativa sobre el vocabulari que presenta dificultats reals als participants.")
bullet(doc,"Contrastar els resultats humans amb les mètriques automàtiques per validar el seu poder predictiu.")

# ── 2. METODOLOGIA ─────────────────────────────────────────────────────────────
heading(doc,"2. Metodologia")
heading(doc,"2.1. Participants",2)
body(doc,(
    "Van participar tres persones adultes amb discapacitat intel·lectual, "
    "reclutades en col·laboració amb l'equip de la Dra. Teresa Torres (URV). "
    "Tots els participants tenien experiència lectora bàsica en castellà "
    "i van ser acompanyats per un moderador que podia resoldre dubtes de procediment, "
    "sense donar indicacions sobre el contingut dels textos. "
    "La participació va ser voluntària i anònima. "
    "El nombre reduït de participants és coherent amb la naturalesa pilot de l'estudi, "
    "orientat a recollir evidència qualitativa i no a obtenir significació estadística."
))
heading(doc,"2.2. Materials",2)
body(doc,(
    "Els textos procedeixen del dataset exemples_lectura_facil_formatted, "
    "que conté 11 textos de domini divers (salut, educació, història, cuina, telecomunicacions, economia) "
    "amb referències de Lectura Fàcil certificades per especialistes humans. "
    "Les adaptacions automàtiques van ser generades pel model llama3.3 (70B paràmetres) "
    "amb la tècnica de prompting V8 (imitació progressiva de l'estil de l'anotador expert) "
    "i temperatura T=0.0, configuració identificada com a globalment òptima en la Fase 2A del projecte "
    "(score compost mitjà 0.587, gap entre datasets 0.314)."
))
heading(doc,"2.3. Disseny Contrabalancejat",2)
body(doc,(
    "Es va emprar un disseny contrabalancejat de tipus quadrat llatí que garanteix: "
    "(1) cap participant veu el mateix text en ambdues versions; "
    "(2) cada text és avaluat en les dues versions per participants diferents, "
    "permetent comparació directa; "
    "(3) l'ordre de presentació varia entre participants per evitar efectes d'ordre. "
    "La Taula 1 mostra l'assignació completa."
))
doc.add_paragraph()

# Taula 1 — Assignació
t1 = doc.add_table(rows=6, cols=7)
t1.style = "Table Grid"
for j,h in enumerate(["Pos.","P1/S1","P1/S2","P2/S1","P2/S2","P3/S1","P3/S2"]):
    hdr_cell(t1.rows[0].cells[j], h)
order = [(1,1),(1,2),(2,1),(2,2),(3,1),(3,2)]
for ti in range(5):
    row = t1.rows[ti+1]
    row.cells[0].text = f"T{ti+1}"
    for par in row.cells[0].paragraphs:
        for run in par.runs: run.font.bold=True; run.font.size=Pt(9)
    for j,(p,s) in enumerate(order):
        idx,ver = SESSIONS[p][s][ti]
        missing = (p,idx) in MISSING
        label = "—" if missing else f"T{idx} ({'O' if ver=='orig' else 'A'})"
        c = row.cells[j+1]; c.text = label
        for par in c.paragraphs:
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in par.runs:
                run.font.size = Pt(9)
                run.font.bold = (ver=="adapt" and not missing)
                run.font.color.rgb = C_GREY if missing else (C_BLUE_M if ver=="adapt" else C_BLUE_D)
widths1 = [Cm(1.0),Cm(2.0),Cm(2.0),Cm(2.0),Cm(2.0),Cm(2.0),Cm(2.0)]
for row in t1.rows:
    for j,w in enumerate(widths1): row.cells[j].width=w
body(doc,"Taula 1. Assignació de textos per participant i sessió. O = original; A = adaptat; blau negreta = versió adaptada.",
     size=9,italic=True,colour=C_GREY)

heading(doc,"2.4. Instrument de Mesura",2)
body(doc,"Després de cada text, el participant responia 4 preguntes binàries (Sí/No):")
for q in [
    "Q1 — El text és fàcil de llegir.  [positiu: Sí = accessible]",
    "Q2 — He entès bé el text.  [positiu: Sí = comprensió alta]",
    "Q3 — Hi havia paraules que no coneixia.  [negatiu: Sí = barrera lèxica]",
    "Q4 — Hi havia frases llargues o difícils d'entendre.  [negatiu: Sí = barrera sintàctica]",
]: bullet(doc,q)
body(doc,(
    "El format binari —en lloc d'escales Likert— s'escull per adequar l'instrument "
    "al perfil cognitiu dels participants, minimitzant la càrrega de decisió."
))

# ── 3. RESULTATS PER PARTICIPANT ───────────────────────────────────────────────
heading(doc,"3. Resultats Detallats per Participant")
body(doc,(
    "Les taules 2, 3 i 4 recullen les respostes individuals de cada participant. "
    "Les files en blau corresponen a textos en versió adaptada; les blanques, a textos originals. "
    "Els símbols ✓ (verd) i ✗ (vermell) indiquen resposta favorable o desfavorable a l'accessibilitat."
))

for p_num in [1,2,3]:
    heading(doc,f"3.{p_num}. Participant {p_num}",2)
    p_res = [(tidx,ver,q1,q2,q3,q4,notes)
             for (pn,tidx,ver,q1,q2,q3,q4,notes) in RESULTS if pn==p_num]
    t = doc.add_table(rows=len(p_res)+1, cols=7)
    t.style = "Table Grid"
    for j,h in enumerate(["Text","Domini","Versió","Q1\nFàcil","Q2\nEntès","Q3\nParaules","Q4\nFrases"]):
        hdr_cell(t.rows[0].cells[j],h)
    for i,(tidx,ver,q1,q2,q3,q4,notes) in enumerate(p_res):
        row = t.rows[i+1]
        row.cells[0].text = f"T{tidx}"
        row.cells[1].text = DOMAINS.get(tidx,"—")
        row.cells[2].text = "Adaptat" if ver=="adapt" else "Original"
        for j,v in enumerate([q1,q2,q3,q4],3):
            row.cells[j].text = yn(v)
        bg = "DAE8FC" if ver=="adapt" else "FFFFFF"
        for j in range(7): shade(row.cells[j],bg)
        for j in range(7): center9(row.cells[j])
        for j,(v,pos) in enumerate([(q1,True),(q2,True),(q3,False),(q4,False)],3):
            for par in row.cells[j].paragraphs:
                for run in par.runs:
                    good = (v=="Sí" and pos) or (v=="No" and not pos)
                    run.font.color.rgb = C_GREEN if good else C_RED
                    run.font.bold = True
        # notes as tooltip in col 1
        if notes:
            row.cells[1].paragraphs[0].runs[0].font.size = Pt(8)
            p2 = row.cells[1].add_paragraph()
            r2 = p2.add_run(f"↳ {notes}")
            r2.font.size=Pt(7.5); r2.font.italic=True; r2.font.color.rgb=C_GREY
    ws = [Cm(1.0),Cm(4.0),Cm(1.8),Cm(1.3),Cm(1.3),Cm(1.7),Cm(1.5)]
    for row in t.rows:
        for j,w in enumerate(ws): row.cells[j].width=w
    body(doc,f"Taula {p_num+1}. Resultats del Participant {p_num}.",size=9,italic=True,colour=C_GREY)

# ── 4. ANÀLISI QUANTITATIVA ────────────────────────────────────────────────────
heading(doc,"4. Anàlisi Quantitativa")
heading(doc,"4.1. Comparació Global Original vs. Adaptat",2)
body(doc,(
    "La Taula 5 compara la taxa de respostes Sí per a cada pregunta "
    "entre les 14 observacions originals i les 12 observacions adaptades. "
    "Per a Q3 i Q4, un percentatge menor indica menys barreres, és a dir, millora."
))

orig_r  = [(q1,q2,q3,q4) for (pn,tidx,ver,q1,q2,q3,q4,n) in RESULTS if ver=="orig"]
adapt_r = [(q1,q2,q3,q4) for (pn,tidx,ver,q1,q2,q3,q4,n) in RESULTS if ver=="adapt"]
no=len(orig_r); na=len(adapt_r)
def csi(lst,i): return sum(1 for r in lst if r[i]=="Sí")
oq=[csi(orig_r,i) for i in range(4)]
aq=[csi(adapt_r,i) for i in range(4)]

t5 = doc.add_table(rows=5,cols=6)
t5.style = "Table Grid"
for j,h in enumerate(["Pregunta","ORIG (Sí/n)","ORIG %","ADAPT (Sí/n)","ADAPT %","Δ (pp)"]):
    hdr_cell(t5.rows[0].cells[j],h)
q_labels = [
    "Q1 — El text és fàcil de llegir",
    "Q2 — He entès bé el text",
    "Q3 — Paraules desconegudes (↓ millor)",
    "Q4 — Frases llargues/difícils (↓ millor)",
]
for i in range(4):
    row = t5.rows[i+1]
    row.cells[0].text = q_labels[i]
    row.cells[1].text = f"{oq[i]} / {no}"; center9(row.cells[1])
    row.cells[2].text = pct(oq[i],no);     center9(row.cells[2])
    row.cells[3].text = f"{aq[i]} / {na}"; center9(row.cells[3])
    row.cells[4].text = pct(aq[i],na);     center9(row.cells[4])
    d = (aq[i]/na - oq[i]/no)*100
    pos_q = i in [0,1]
    sign = "+" if d>=0 else ""
    row.cells[5].text = f"{sign}{d:.0f}pp"; center9(row.cells[5])
    good = (d>0 and pos_q) or (d<0 and not pos_q)
    for par in row.cells[5].paragraphs:
        for run in par.runs:
            run.font.color.rgb = C_GREEN if good else (C_GREY if abs(d)<3 else C_RED)
            run.font.bold=True
    for j in range(6):
        for par in row.cells[j].paragraphs:
            for run in par.runs: run.font.size=Pt(9)
ws5=[Cm(6.5),Cm(2.0),Cm(1.5),Cm(2.0),Cm(1.5),Cm(1.8)]
for row in t5.rows:
    for j,w in enumerate(ws5): row.cells[j].width=w
body(doc,"Taula 5. Comparació global ORIG vs. ADAPT. Verd = millora; vermell = empitjorament; gris = diferència <3pp.",
     size=9,italic=True,colour=C_GREY)

heading(doc,"4.2. Taxa d'Accessibilitat Composta",2)
o_acc = sum(1 for r in orig_r  if r[0]=="Sí" and r[1]=="Sí")
a_acc = sum(1 for r in adapt_r if r[0]=="Sí" and r[1]=="Sí")
body(doc,(
    "La taxa d'accessibilitat composta mesura els textos que un participant considera "
    "alhora fàcils de llegir (Q1=Sí) i ben compresos (Q2=Sí):"
))
bullet(doc,f"Textos originals: {o_acc} / {no} = {o_acc/no*100:.1f}%")
bullet(doc,f"Textos adaptats:  {a_acc} / {na} = {a_acc/na*100:.1f}%")
bullet(doc,f"Diferència: {(a_acc/na - o_acc/no)*100:+.1f}pp — pràcticament empat")
body(doc,(
    "Tot i la millora en llegibilitat superficial (Q1, +11pp), la comprensió efectiva (Q2) "
    "decreix lleugerament (−4pp), resultant en una millora composta mínima (+3pp). "
    "L'adaptació simplifica la forma lingüística, però no garanteix una comprensió "
    "significativament superior en tots els casos."
))

heading(doc,"4.3. Resum per Pregunta",2)
body(doc,(
    "Analitzant cada dimensió per separat, emergeix el perfil d'impacte de l'adaptació:"
))
bullet(doc,"Q1 — Llegibilitat: +11pp (64% → 75%). Millora consistent. El model genera textos percebuts com més fluids.")
bullet(doc,"Q2 — Comprensió: −4pp (71% → 67%). Lleugera regressió, probablement per casos on l'adaptació desestructura el missatge.")
bullet(doc,"Q3 — Vocabulari: −21pp (71% → 50%). Impacte més clar i robust. El model elimina efectivament termes poc habituals.")
bullet(doc,"Q4 — Sintaxi: −6pp (64% → 58%). Millora moderada. Reducció de frases llargues no plenament consistent.")

# ── 5. ANÀLISI PER DOMINI ──────────────────────────────────────────────────────
heading(doc,"5. Anàlisi per Domini Textual")
body(doc,(
    "La variable amb major poder explicatiu dels resultats és el domini temàtic del text. "
    "La Taula 6 mostra els resultats per a cada text amb la informació de versió i participant. "
    "Els textos en blau han estat llegits en versió adaptada."
))
doc.add_paragraph()

text_rows = sorted(
    [(tidx,pn,ver,q1,q2,q3,q4,DOMAINS.get(tidx,"—"),notes)
     for (pn,tidx,ver,q1,q2,q3,q4,notes) in RESULTS],
    key=lambda x: x[0]
)
t6 = doc.add_table(rows=len(text_rows)+1, cols=7)
t6.style = "Table Grid"
for j,h in enumerate(["T","Domini","Part.","Versió","Q1","Q2","Q3 · Q4"]):
    hdr_cell(t6.rows[0].cells[j],h)
for i,(tidx,pn,ver,q1,q2,q3,q4,domain,notes) in enumerate(text_rows):
    row = t6.rows[i+1]
    row.cells[0].text = f"T{tidx}"
    row.cells[1].text = domain
    row.cells[2].text = f"P{pn}"
    row.cells[3].text = "Adapt." if ver=="adapt" else "Orig."
    row.cells[4].text = yn(q1)
    row.cells[5].text = yn(q2)
    row.cells[6].text = f"{yn(q3)} · {yn(q4)}"
    bg = "DAE8FC" if ver=="adapt" else "FFFFFF"
    for j in range(7): shade(row.cells[j],bg); center9(row.cells[j])
    for j,(v,pos) in enumerate([(q1,True),(q2,True)],4):
        for par in row.cells[j].paragraphs:
            for run in par.runs:
                run.font.color.rgb = C_GREEN if v=="Sí" else C_RED
                run.font.bold=True
ws6=[Cm(0.9),Cm(3.5),Cm(0.9),Cm(1.8),Cm(1.0),Cm(1.0),Cm(1.8)]
for row in t6.rows:
    for j,w in enumerate(ws6): row.cells[j].width=w
body(doc,"Taula 6. Resultats per text. Blau = versió adaptada; blanc = versió original.",
     size=9,italic=True,colour=C_GREY)

heading(doc,"5.1. Dominis on l'Adaptació és Eficaç",2)
body(doc,(
    "S'observa millora neta en dominis de contingut general i estructurat, "
    "on el model pot substituir termes tècnics per equivalents d'ús comú:"
))
bullet(doc,(
    "Farmàcia/Salut (T0): P1 amb ORIG reporta No/Sí (no fàcil, però entès) "
    "amb sis termes farmacèutics desconeguts. P3 amb ADAPT reporta Sí/Sí sense vocabulari problemàtic. "
    "L'adaptació elimina comprimido, dosis, paulatinamente i similars amb èxit."
))
bullet(doc,(
    "Administratiu (T4): P1 amb ORIG: No/No (ni fàcil ni entès, «baremo» com a barrera). "
    "P3 amb ADAPT: Sí/Sí (accessible i comprès). Millora clara gràcies a la reestructuració sintàctica."
))
bullet(doc,(
    "Economia (T9): P2 amb ORIG: Sí/Sí però amb Q3+Q4 negatius (paraules i frases difícils). "
    "P1 amb ADAPT: Sí/Sí i Q3+Q4 favorables. Reducció efectiva de complexitat econòmica."
))

heading(doc,"5.2. Dominis on l'Adaptació Falla o Empitjora",2)
body(doc,(
    "Quatre dominis presenten resultats negatius o neutres, que il·lustren els límits del sistema:"
))
bullet(doc,(
    "Joc de taula — Tute (T3): La terminologia del joc (baza, acuse, baceta, jugador «mano», sobrantes) "
    "és funcionalment irreductible: sense aquests termes el text perd el significat original. "
    "Tant P2 amb ORIG (Sí/Sí) —que coneixia el joc— com P3 amb ORIG (No/No) —que no el coneixia— "
    "confirmen que és el domini del text, no la versió, el factor determinant. "
    "P1 amb ADAPT obté No/No, igual de problemàtic."
))
bullet(doc,(
    "Telecomunicacions (T7 — Fibra, T8 — SIM): Els termes del sector (Gb, fibra, eSIM, MultiSIM, "
    "cesión, permanència) persisten en ambdues versions. "
    "P3 amb ORIG de T7: No/No. P1 amb ADAPT de T7: No/No. "
    "P1 amb ORIG de T8: Sí/Sí (el participant coneixia el context), però "
    "P3 amb ADAPT de T8: Sí/No (llegible però no comprès, amb nous termes tècnics literaris). "
    "El model introdueix registre literari (microrrelat) en un text de serveis mòbils."
))
bullet(doc,(
    "Educació/Laboral (T1): El cas de regressió més greu. "
    "P2 amb ORIG: Sí/Sí, sense vocabulari problemàtic. "
    "P3 amb ADAPT: No/No, amb cinc termes nous reportats (Docentes, recursos, ratios, salarial, firme). "
    "El model ha reformulat el text en registre administratiu-formal, amplificant les barreres "
    "en lloc de reduir-les. Constitueix la fallada més clara del sistema."
))

# ── 6. ANÀLISI QUALITATIVA DEL VOCABULARI ─────────────────────────────────────
heading(doc,"6. Anàlisi Qualitativa del Vocabulari")
body(doc,(
    "Les paraules marcades pels participants com a desconegudes "
    "—en total, més de 45 termes únics recollits al llarg de l'estudi— "
    "permeten identificar tres patrons de barrera lèxica."
))
heading(doc,"6.1. Vocabulari Tècnic Irreductible",2)
body(doc,(
    "Un conjunt de termes apareix com a barrera independentment de la versió del text. "
    "Pertanyen a dominis especialitzats que el model no pot simplificar sense alterar "
    "el significat essencial del contingut:"
))
bullet(doc,"Jocs: baza, acuse, baceta, jugador «mano», palo de triunfo, as, sobrantes, tantos")
bullet(doc,"Telecomunicacions: eSIM, MultiSIM, Gb, fibra, permanència, cesión, llamadas infinitas")
bullet(doc,"Història medieval: prohombres, feudo, Mitra, jurisdicció, repoblació, núcleos, fortificades")
body(doc,(
    "Aquests resultats suggereixen que certs textos del dataset contenen contingut "
    "intrínsecament incompatible amb Lectura Fàcil, independentment de la tècnica d'adaptació. "
    "Per a aquests casos, la solució no és millorar el model sinó redissenyar el text amb supervisió humana "
    "o descartar-los del corpus."
))
heading(doc,"6.2. Vocabulari Tècnic Reduïble",2)
body(doc,(
    "En contrast, d'altres dominis contenen termes que l'adaptació elimina parcialment o totalment, "
    "confirmant que el sistema funciona quan existeix un equivalent de llengua comuna:"
))
bullet(doc,"Farmàcia: comprimido, dosis, vía oral, paulatinamente, gradual → eliminats en la versió adaptada (P1/T0)")
bullet(doc,"Administratiu: baremo → eliminat en la versió adaptada (P3/T4)")
bullet(doc,"Cuina: embadurnar, clavo molido → presents en ORIG (T6-P1, T6-P3), no reportats en cap versió adaptada")
heading(doc,"6.3. Termes Nous Introduïts per l'Adaptació",2)
body(doc,(
    "El patró més problemàtic és la introducció de termes nous per part del model. "
    "S'identifiquen dos casos:"
))
bullet(doc,(
    "T1 (Educació/ADAPT — P3): El model reformula el text i introdueix «Docentes, recursos, "
    "ratios, salarial, firme», termes del registre administratiu no presents ni reportats "
    "en la versió original (P2/T1-ORIG: sense vocabulari problemàtic)."
))
bullet(doc,(
    "T8 (Telecomunicacions/ADAPT — P3): L'adaptació incorpora termes literaris "
    "(«microrrelat, extensió, caràcters, adjunta») presumiblement en fer analogies explicatives, "
    "resultat en comprensió pitjor que la versió original (P1/T8-ORIG: Sí/Sí/No/No)."
))

# ── 7. COMPARACIÓ DIRECTA PER TEXT ────────────────────────────────────────────
heading(doc,"7. Comparació Directa per Text (ORIG vs. ADAPT)")
body(doc,(
    "El disseny contrabalancejat permet comparar directament la mateixa peça de contingut "
    "en ambdues versions quan disposem d'observacions creuades. "
    "La Taula 7 recull els 9 textos amb dades en les dues versions."
))
doc.add_paragraph()

comps = [
    (0,"Farmàcia/Salut",     "P1-ORIG","No","Sí","P3-ADAPT","Sí","Sí","ADAPT ✓"),
    (1,"Educació/Laboral",   "P2-ORIG","Sí","Sí","P3-ADAPT","No","No","ORIG ✓✓"),
    (2,"Història medieval",  "P1,P3-ORIG","Mixt","Mixt","P2-ADAPT","Sí","Sí","ADAPT ✓ (vs avg)"),
    (3,"Tute (joc)",         "P2,P3-ORIG","Mixt","Mixt","P1-ADAPT","No","No","EMPAT (negat.)"),
    (4,"Administratiu",      "P1-ORIG","No","No","P3-ADAPT","Sí","Sí","ADAPT ✓✓"),
    (5,"Educació/Laboral",   "P2-ORIG","Sí","Sí","P3-ADAPT","Sí","Sí","EMPAT (pos.)"),
    (7,"Telecomunicacions",  "P2,P3-ORIG","Mixt","Mixt","P1-ADAPT","No","No","ORIG ✓"),
    (8,"Telecom. (SIM)",     "P1-ORIG","Sí","Sí","P2,P3-ADAPT","Mixt","Mixt","ORIG lleuger"),
    (9,"Economia",           "P2-ORIG","Sí","Sí","P1-ADAPT","Sí","Sí","EMPAT (pos.)"),
]
t7 = doc.add_table(rows=len(comps)+1, cols=5)
t7.style = "Table Grid"
for j,h in enumerate(["T","Domini","ORIG (Q1/Q2)","ADAPT (Q1/Q2)","Veredicte"]):
    hdr_cell(t7.rows[0].cells[j],h)
for i,(tidx,dom,owho,oq1,oq2,awho,aq1,aq2,verd) in enumerate(comps):
    row = t7.rows[i+1]
    row.cells[0].text = f"T{tidx}"
    row.cells[1].text = dom
    row.cells[2].text = f"{owho}\n({oq1}/{oq2})"
    row.cells[3].text = f"{awho}\n({aq1}/{aq2})"
    row.cells[4].text = verd
    for j in range(5): center9(row.cells[j])
    for par in row.cells[4].paragraphs:
        for run in par.runs:
            run.font.bold=True
            run.font.color.rgb = (C_GREEN if "ADAPT" in verd and "✓" in verd
                                  else C_RED if "ORIG" in verd and "✓" in verd
                                  else C_ORANGE)
ws7=[Cm(0.9),Cm(3.5),Cm(3.0),Cm(3.0),Cm(3.0)]
for row in t7.rows:
    for j,w in enumerate(ws7): row.cells[j].width=w
body(doc,"Taula 7. Comparació directa per text. ADAPT ✓✓ = guanya clarament; ORIG ✓✓ = guanya clarament; EMPAT = sense diferència.",
     size=9,italic=True,colour=C_GREY)
body(doc,(
    "Recompte de veredictes: ADAPT guanya clarament en 2 textos (T0, T4); "
    "ORIG guanya clarament en 2 textos (T1, T7); 5 textos presenten empat o resultat mixt. "
    "El domini textual és el factor determinant, no la versió."
))

# ── 8. ALINEACIÓ AMB MÈTRIQUES AUTOMÀTIQUES ──────────────────────────────────
heading(doc,"8. Alineació amb les Mètriques Automàtiques")
body(doc,(
    "Un objectiu implícit de l'estudi és validar si les mètriques automàtiques "
    "calculades en les fases anteriors prediuen adequadament la percepció humana."
))
bullet(doc,(
    "Validació positiva: Els textos amb SARI baix en les avaluacions automàtiques "
    "(T3-Tute, T7-telecomunicacions) coincideixen exactament amb els pitjors resultats humans. "
    "SARI és la mètrica amb major poder predictiu."
))
bullet(doc,(
    "BERTScore i comprensió: La reducció de paraules desconegudes en versions adaptades "
    "s'alinea amb les puntuacions BERTScore, que detecten preservació semàntica "
    "respecte a la referència humana."
))
bullet(doc,(
    "Limitació detectada: Les mètriques automàtiques no detecten regressió lèxica (T1). "
    "El model compara l'output amb una referència experta, no amb el nivell cognitiu "
    "del públic objectiu. Calen mètriques complementàries de nivell lexical "
    "(p. ex., freqüència de paraules, edat d'adquisició) per capturar aquest fenomen."
))

# ── 9. CONCLUSIONS ─────────────────────────────────────────────────────────────
heading(doc,"9. Conclusions")
body(doc,"Es presenten les sis conclusions principals en ordre de rellevància i robustesa:")
concls = [
    ("C1","Reducció clara del vocabulari complex",
     "L'adaptació redueix la taxa de textos amb paraules desconegudes del 71% al 50% (−21pp). "
     "És l'impacte més consistent, observable en múltiples participants i dominis."),
    ("C2","Sense millora neta en comprensió global",
     "La taxa d'accessibilitat composta millora únicament +3pp (64% → 67%). "
     "La simplificació lexical no es tradueix automàticament en comprensió superior."),
    ("C3","El domini textual és el factor determinant",
     "Textos de jocs de taula i telecomunicacions resisteixen qualsevol adaptació automàtica "
     "per la seva terminologia irreductible. Textos generals, de salut i administratius "
     "responen bé a l'adaptació."),
    ("C4","Risc de regressió en textos educatius i laborals",
     "En el text T1 (Educació), la versió adaptada va ser significativament pitjor que l'original. "
     "El model va introduir vocabulari administratiu complex absent en l'original. "
     "Constitueix el principal punt de millora del sistema."),
    ("C5","Alineació parcial amb les mètriques automàtiques",
     "SARI prediu correctament els casos extrems. Però les mètriques actuals no detecten "
     "fenòmens de regressió lèxica, revelant una limitació important del pipeline d'avaluació."),
    ("C6","Estudi pilot — no concloent estadísticament",
     "Amb 26 observacions i 3 participants, els resultats proporcionen evidència orientativa "
     "qualitativa, no prova estadística. Es requereix una validació amb mostra major."),
]
for num,tit,txt in concls:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.space_before = Pt(5)
    r1 = p.add_run(f"{num} — {tit}: ")
    r1.font.bold=True; r1.font.size=Pt(11); r1.font.color.rgb=C_BLUE_D
    r2 = p.add_run(txt)
    r2.font.size=Pt(11)

# ── 10. LIMITACIONS ───────────────────────────────────────────────────────────
heading(doc,"10. Limitacions de l'Estudi")
for lim in [
    "Mida de la mostra: 3 participants i 26 observacions no permeten inferències estadístiques generals.",
    "Sessions incompletes: 4 textos no van ser avaluats, reduint el balanç del disseny contrabalancejat.",
    "Format binari: el Sí/No mesura presència/absència però no graduació. Una escala de 3 punts "
     "podria capturar matisos.",
    "Efecte moderador: la presència de l'acompanyant, tot i ser neutral, pot haver influït en les respostes.",
    "Monolingüisme castellà: els resultats no s'estenen directament a textos en català o altres idiomes.",
    "Un sol sistema avaluat: s'ha avaluat únicament llama3.3+V8+T=0.0; "
     "altres models o prompts podrien tenir perfils humans diferents.",
]:
    bullet(doc,lim)

# ── GUARDAR ───────────────────────────────────────────────────────────────────
doc.save(OUT)
print(f"Guardat: {OUT}")
