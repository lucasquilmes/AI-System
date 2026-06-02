


Lucas Alejo Dening Céspedes

Avaluació de Models de Llenguatge Locals per a l'Adaptació Automàtica a Lectura Fàcil


TREBALL DE FI DE GRAU
dirigit per Antonio Moreno Ribas

Grau en Enginyeria de Sistemes i Serveis de Telecomunicacions



Universitat Rovira i Virgili
Tarragona
2025
 
1. Introducció
1.1. Motivació
Les persones amb dificultats de comprensió lectora —ja sigui per discapacitat intel·lectual, baixa alfabetització o per ser parlants no natives— s'enfronten cada dia a barreres cognitives en textos que les envolten: documents oficials, prospectes mèdics, contractes de serveis, etiquetes de productes o notícies de premsa. Aquesta dificultat genera exclusió social i limita l'autonomia personal.
Per mitigar aquest problema existeix l'estàndard de Lectura Fàcil (UNE 153101:2018), un conjunt de pautes de disseny i redacció destinat a garantir l'accessibilitat cognitiva de qualsevol tipus de text. Tanmateix, l'adaptació manual de documents a aquest estàndard per part de professionals especialitzats és un procés lent i costós en recursos. Aquesta limitació justifica la necessitat d'investigar l'automatització de la simplificació de textos mitjançant l'ús de Models de Llenguatge de Gran Escala (LLMs), avaluant si són capaços de preservar la fidelitat del contingut original mentre milloren significativament la seva accessibilitat lingüística.
1.2. INSERLAB i el Plantejament de la Idea
Aquest projecte, anomenat Explain-Up, neix en el context de l'ecosistema de recerca i transferència de la Universitat Rovira i Virgili, alineat amb els principis d'inclusió social promoguts per iniciatives com INSERLAB. La idea central d'Explain-Up és desenvolupar una plataforma tecnològica assistida per intel·ligència artificial que faciliti i acceleri el procés d'adaptació de textos a Lectura Fàcil. El projecte compta amb la col·laboració de la Dra. Teresa Torres i el seu equip, experts en accessibilitat cognitiva i Lectura Fàcil, que han aportat el coneixement especialitzat i els materials de referència necessaris per orientar i validar el desenvolupament de l'estudi.
Per aconseguir un desenvolupament rigorós, el projecte es fonamenta en la col·laboració amb entorns de validació humana. L'obtenció de textos reals adaptats manualment per especialistes proporciona el ground truth o veritat fonamental, una peça indispensable per poder calibrar, comparar i avaluar de manera quantitativa el rendiment real dels models de llenguatge locals enfront dels estàndards de qualitat humans.
1.3. Objectius i Qüestions de Recerca
L'objectiu principal d'aquest treball és dissenyar, implementar i validar un framework automatitzat per avaluar la capacitat de diferents models de llenguatge —executats en un entorn local— en la tasca de simplificar textos a l'estàndard de Lectura Fàcil.
Per assolir aquesta fita, es defineixen els objectius específics següents:
•	Desenvolupar una eina de programari modular en Python que integri el motor Ollama i la biblioteca LangChain per executar inferències amb models de codi obert, garantint la privacitat de les dades processades.
•	Analitzar de manera sistemàtica l'impacte de diferents metodologies de disseny d'instruccions (prompting) en la qualitat de l'adaptació generada.
•	Dissenyar un entorn d'avaluació quantitativa multidimensional que combini mètriques avançades de simplificació, similitud semàntica, complexitat lèxica i llegibilitat per mesurar amb rigor el rendiment de cada model i tècnica.

Qüestions de Recerca
A partir d'aquests objectius, es formulen les qüestions de recerca que guiaran el treball:
•	QR1: Hi ha diferències significatives en la qualitat de l'adaptació a Lectura Fàcil entre els diferents models de llenguatge locals avaluats?
•	QR2: Quina influència té la tècnica de prompting en la qualitat dels resultats, i existeix una tècnica universalment superior o el rendiment depèn del domini textual?
•	QR3: Quines mètriques automàtiques presenten major poder discriminatiu per avaluar la qualitat de les adaptacions generades?
•	QR4: Com afecta la temperatura de generació a la qualitat i l'estabilitat dels outputs produïts pels models?

Tasques i Contribucions Esperades
Per assolir els objectius, es preveuen les tasques següents: (1) disseny i implementació del pipeline d'avaluació automatitzat; (2) selecció i configuració dels models i les tècniques de prompting; (3) execució de les avaluacions i recollida de resultats; (4) anàlisi estadística i comparativa dels resultats; i (5) validació amb usuaris finals. Les contribucions esperades del treball inclouen un framework reutilitzable per a l'avaluació de simplificació textual, un conjunt de dades d'avaluació amb referències humanes, i evidència empírica sobre quines configuracions de model i prompt són més adequades per a la tasca de Lectura Fàcil en llengua castellana.

1.4. Estructura del Document
El present document s'organitza de la manera següent. El Capítol 2 presenta el context teòric del treball: la normativa de Lectura Fàcil, les tècniques de prompting avaluades i les mètriques d'avaluació utilitzades. El Capítol 3 descriu el disseny del sistema, incloent l'arquitectura de l'aplicació i la del pipeline d'estudi. El Capítol 4 recull les proves realitzades i els resultats obtinguts en cada fase d'avaluació. El Capítol 5 conté la discussió dels resultats. El Capítol 6 exposa les limitacions del treball. El Capítol 7 presenta les conclusions i el treball futur. Finalment, els annexos inclouen la normativa UNE completa, els prompts utilitzats i els datasets de l'estudi.
2. Context del Treball
2.1. Accessibilitat Cognitiva i Lectura Fàcil
L'accessibilitat cognitiva és el dret que tenen totes les persones a comprendre la informació que les envolta, un factor indispensable per garantir l'autonomia personal i la participació ciutadana plena. En l'àmbit de l'administració pública, la barrera lingüística generada per la documentació formal, burocràtica i jurídica suposa un factor d'exclusió social de gran rellevància. Per donar resposta a aquesta necessitat, sorgeix el moviment de la Lectura Fàcil, estandarditzat a Espanya sota les directrius de la norma UNE 153101:2018.
Aquest estàndard estableix un conjunt rigorós de pautes de redacció i disseny ortotipogràfic orientades a simplificar el missatge sense alterar-ne el significat. La Taula 1 recull els dotze aspectes principals de la norma.

[TAULA 1: Principals aspectes de la norma UNE 153101:2018]
| Aspecte | Prescripció |
|---|---|
| Longitud de les oracions | Màxim 15 paraules per oració |
| Estructura sintàctica | Ordre directe: subjecte + verb + complement. Evitar subordinades |
| Vocabulari | Paraules comunes i quotidianes. Evitar tecnicismes |
| Idea per frase | Una única idea principal per oració |
| Veu verbal | Preferentment veu activa |
| Temps verbal | Temps simples: present, passat simple |
| Nombres | Xifres aràbigues per a tots els nombres |
| Abreviatures i sigles | Evitar o explicar sempre en la primera aparició |
| Paràgrafs | Curts, d'una a tres oracions |
| Disseny tipogràfic | Lletra gran (mínim 14 pt), interlineat ampli, marges generosos |
| Il·lustracions | Acompanyar el text amb imatges que reforçin el missatge |
| Validació | Revisió per persones del públic objectiu abans de publicar |

Tradicionalment, l'adaptació de textos a aquest estàndard requereix la intervenció de professionals especialitzats i processos de validació manual, la qual cosa encareix i alenteix la democratització de l'accés a la informació institucional. Aquest capítol presenta el marc teòric del treball: la secció 2.2 descriu les tècniques de prompting avaluades i la secció 2.3 les mètriques d'avaluació emprades.
2.2. Models de Llenguatge de Gran Escala (LLMs) Locals i Tècniques de Prompting
L'evolució de la intel·ligència artificial generativa ha introduït els Models de Llenguatge de Gran Escala (LLMs) com a eines viables per abordar tasques de processament i transformació del llenguatge natural. En el marc del projecte Explain-Up, l'ús de LLMs de codi obert executats de manera local —mitjançant motors d'inferència com Ollama i orquestradors de flux com LangChain— constitueix una decisió tècnica fonamental per garantir la privacitat i la seguretat de les dades, un requisit crític quan es processen textos de qualsevol tipus, des de documents oficials fins a continguts d'ús quotidià.
La hipòtesi principal de l'estudi és que la qualitat de les adaptacions depèn tant del model emprat com de la tècnica d'instrucció (prompting) utilitzada. A continuació es descriuen les tècniques avaluades, agrupades per categoria.
Tècniques d'Estructura Bàsica
•	Zero-Shot Prompting: Instrucció directa sense exemples previs, confiant plenament en el coneixement preentrenat del model.
•	Few-Shot Prompting: Inclusió de parells d'exemples (text original i adaptació) dins el prompt per calibrar el to i el patró de sortida esperat.
•	Role Prompting: Assignació d'una identitat especialitzada al model —com ara expert en accessibilitat cognitiva— abans de processar el text.
Tècniques de Raonament i Lògica
•	Chain of Thought (CoT): Facilitació d'exemples on el raonament intermedi es desglossa pas a pas, obligant el model a articular la seva lògica abans d'emetre una resposta.
•	Zero-Shot Chain of Thought: Variant que afegeix la instrucció de "pensar pas a pas" al final del prompt, activant el raonament seqüencial sense necessitat d'exemples.
•	Tree of Thoughts (ToT): Evolució avançada en la qual el model genera i avalua múltiples branques de raonament en paral·lel, descartant les vies menys prometedores.
•	Self-Consistency: Generació de diverses respostes per a una mateixa instrucció, seleccionant la més freqüent com a sortida definitiva.
Tècniques de Refinament, Conjunt i Coneixement
•	Self-Refinement (Autorefinament): Procés iteratiu en el qual el model genera un esborrany, el critica respecte a les pautes de Lectura Fàcil i en produeix una versió millorada.
•	Expert Ensemble (Conjunt d'Experts): Simulació d'un panell virtual d'agents especialitzats que analitzen el text des de perspectives diferents i consensuen una resposta unificada.
•	Meta-Prompting: Ús del propi model per dissenyar o millorar les instruccions que s'aportaran en una segona crida.

Tècniques Combinades i Versions Iteratives (V0–V8)
A més de les tècniques estàndard descrites anteriorment, el projecte ha desenvolupat una sèrie de nou prompts propis (V0 a V8) que combinen i adapten els enfocaments anteriors a les especificitats de la Lectura Fàcil i la normativa UNE 153101:2018. Cada versió incorpora ajustos progressius en la instrucció, l'estructura de l'exemple i el nivell de detall de les pautes, partint d'una instrucció bàsica (V0) fins a una tècnica d'imitació progressiva (V8) en la qual el model ancora la seva sortida a l'estil concret de l'anotador humà. Aquestes versions constitueixen la contribució tècnica principal de l'estudi i han obtingut els millors resultats globals en les avaluacions automàtiques. Els prompts complets de cadascuna de les tècniques avaluades es poden consultar a l'Annex 2.

La secció 2.3 presenta les mètriques automàtiques emprades per quantificar la qualitat de les adaptacions generades per cadascuna d'aquestes tècniques.
2.3. Mètriques d'Avaluació
Per quantificar l'èxit de les adaptacions generades és imprescindible disposar d'un entorn d'avaluació automàtic robust. Donada la naturalesa de la Lectura Fàcil, l'avaluació ha de cobrir simultàniament dues dimensions inseparables: l'accessibilitat lingüística i la fidelitat semàntica respecte al text original.
Mètriques de Qualitat de Simplificació i Llegibilitat
•	SARI (System Output Against References and Input): Mètrica de referència proposada per Xu et al. (2016) que avalua la qualitat comparant tres operacions d'edició sobre el text: addició de paraules útils, conservació de paraules de l'original i eliminació d'elements innecessaris. Una puntuació superior a 40 indica un rendiment competitiu en l'estat de l'art [6].
•	Flesch Reading Ease: Basada en la fórmula clàssica de Flesch (1948) adaptada al castellà. Mesura la complexitat de lectura analitzant la longitud mitjana de les oracions i el nombre de síl·labes per paraula. Per complir els criteris mínims d'accessibilitat cognitiva el text ha de superar els 65 punts, sent òptim superar els 80 [2].
•	Fórmula de Comprensibilitat de Gutiérrez de Polini: Índex dissenyat específicament per a la llengua castellana. Valors superiors a 60 són necessaris per certificar una Lectura Fàcil profunda.
Mètriques de Fidelitat i Significat
•	BERTScore F1: Proposada per Zhang et al. (2020), calcula la similitud semàntica mitjançant embeddings contextuals basats en BERT. Detecta equivalències de significat encara que les paraules siguin diferents, resultant útil per identificar al·lucinacions del model. Es persegueixen valors superiors a 0,80 [7].
•	ROUGE-L: Desenvolupada per Lin (2004), mesura el solapament lèxic utilitzant la subsequència comuna més llarga (LCS). El rang esperat per a una adaptació exitosa se situa entre 0,35 i 0,45 [4].
•	BLEU (Bilingual Evaluation Understudy): Dissenyada per Papineni et al. (2002), avalua la precisió de n-grames de la sortida respecte a la referència humana. En tasques de simplificació severa són habituals puntuacions entre 15 i 25 [5].
Mètriques de Diagnòstic Estructural i Lèxic
•	Ràtio de Compressió Relatiu (CR ratio): En lloc de comparar directament el text generat amb l'original, s'utilitza un ràtio relatiu que mesura en quina mesura la compressió del model s'assembla a la que va realitzar l'anotador humà en la referència. Es calcula com (longitud_generat / longitud_original) / (longitud_referència / longitud_original), de manera que un valor de 1,0 indica que el model ha comprimit el text en la mateixa proporció que l'expert. Valors superiors a 1,0 indiquen que el model genera textos més llargs que la referència; valors inferiors, més curts. L'objectiu és aproximar-se a 1,0.
•	Longitud Mitjana de l'Oració (LMO): Mitjana de paraules per oració. La norma UNE 153101:2018 requereix una mitjana estrictament inferior a 15 paraules.
•	Type-Token Ratio (TTR): Diversitat lèxica calculada com a quocient entre mots únics i total de paraules. En textos de Lectura Fàcil es busquen ràtios baixos (0,30–0,45) que reflecteixin la repetició de termes clars.
•	Índex de Paraules Complexes: Percentatge de paraules polisil·làbiques sobre el total. No ha de superar el 10–15 % del text.
•	Densitat d'Entitats Nominals (NER Density): Percentatge de noms propis, organitzacions o dates detectats mitjançant eines com spaCy. Una densitat inferior al 5 % certifica que el model ha reduït l'excés burocràtic.
•	Levenshtein Normalitzada: Similitud d'edició a nivell de paraula entre el text generat i la referència humana, calculada com 1 − (distància_Levenshtein / màxim_longitud). Valors superiors a 0,30 indiquen una proximitat estilística notable amb l'adaptació humana; valors propers a 1,0 representen una coincidència gairebé literal.

La Taula 2 resumeix el conjunt de mètriques amb el rang esperat per a cada una en el context de la Lectura Fàcil.

[TAULA 2: Resum de mètriques, fórmules i rangs esperats]
| Mètrica | Fórmula simplificada | Rang esperat (Lectura Fàcil) |
|---|---|---|
| SARI | Mitjana(F1_add, F1_keep, F1_del) | > 40 (competitiu), > 55 (excel·lent) |
| Flesch RE | 206,835 − 1,015·(paraules/oracions) − 84,6·(síl·labes/paraula) | > 65 (accessible), > 80 (òptim) |
| BERTScore F1 | Similitud cosinus entre embeddings BERT | > 0,80 |
| ROUGE-L | LCS(generat, referència) / longitud_referència | 0,35 – 0,45 |
| BLEU | Precisió geomètrica de n-grames (n=1..4) | 15 – 25 |
| CR ratio | (long_gen/long_orig) / (long_ref/long_orig) | ≈ 1,0 |
| LMO | Σ paraules / nombre_oracions | < 15 paraules/oració |
| TTR ratio | TTR_generat / TTR_referència | ≈ 1,0 |
| CWR ratio | CWR_generat / CWR_referència | ≈ 1,0 |
| NER Density | Entitats_NER / total_paraules | < 5 % |
| Levenshtein sim. | 1 − dist_Lev / màx(long_gen, long_ref) | > 0,30 |

Les set mètriques amb major poder discriminatiu en aquest estudi —SARI, BERTScore, Levenshtein, Flesch ratio, CR ratio, TTR ratio i CWR ratio— es combinen en un score compost normalitzat [0–1] que s'utilitza com a mesura global de qualitat al llarg del treball. El Capítol 4 descriu com s'apliquen aquestes mètriques en les diferents fases de l'estudi.
3. Disseny del Sistema
3.1. Arquitectura de l'Aplicació
L'arquitectura de l'aplicació Explain-Up es centra en el flux d'interacció de l'usuari: el procés comença amb la captura fotogràfica d'un text mitjançant un dispositiu mòbil, l'extracció del contingut escrit mitjançant OCR (tecnologia que queda fora de l'abast d'aquest treball) i l'enviament al LLM local per obtenir l'adaptació i retornar-la a l'usuari.
3.2. Arquitectura de l'Estudi
El sistema desenvolupat per a l'estudi s'estructura com un pipeline de processament de dades automatitzat, combinant el flux d'informació per a l'avaluació amb l'arquitectura modular del programari. L'aplicació interactua programàticament amb el motor local Ollama mitjançant LangChain per injectar els prompts d'instrucció, i les respostes generades pels models es capturen i emmagatzemen per a la seva avaluació matemàtica posterior.
3.3. Implementació
El programari d'avaluació es va implementar amb una arquitectura modular en Python. Un script d'entrada principal delega el processament al mòdul avaluador, el qual coordina el flux de dades i importa mòduls auxiliars especialitzats per a la gestió d'arxius i el càlcul aïllat de les mètriques més complexes. Per garantir la reproduïbilitat dels resultats, tots els models s'han executat amb temperatura fixa T=0,0 i llavor fixa seed=42; amb aquests paràmetres, davant del mateix input el model produeix sempre el mateix output.
4. Proves
4.1. Fase 1 — Avaluació de Models i Tècniques de Prompting
La Fase 1 constitueix l'avaluació exhaustiva de l'espai de configuracions possibles. En total es van generar i avaluar 3.666 outputs automàtics, distribuïts en 1.908 avaluacions sobre el dataset test_poor i 1.758 sobre exemples_lectura_facil_formatted.
Models avaluats
Es van avaluar vuit models de llenguatge executats en local mitjançant Ollama, abastant diferents mides de paràmetres (des de 8B fins a 70B): llama3.1:8b, mistral-nemo (12B), command-r (35B), gemma2:27b, mixtral (47B, arquitectura Mixture-of-Experts), llama3.3 (70B), qwen2.5:32b i aya-expanse:32b. Els dos models més robustos van resultar ser llama3.3 i gemma2_27b, que es van mantenir al top-2 en els dos conjunts de dades.
Tècniques de prompting
Es van dissenyar i avaluar 20 tècniques de prompting organitzades en tres grups: nou versions pròpies d'elaboració progressiva (V0–V8, descrites a la secció 2.2), nou tècniques estàndard de la literatura (zero-shot, few-shot, role, CoT, zero-shot CoT, ToT, self-consistency, self-refinement i expert ensemble, més meta-prompting) i dos prompts de domini específic (MOTOR i AUDIT). La tècnica V8, basada en imitació progressiva de l'estil expert, va ser la més efectiva sobre el dataset de textos de complexitat alta (test_poor), obtenint el màxim SARI (0,557) i la major similitud Levenshtein (0,325) de l'estudi.
Conjunts de dades i avaluació
Es van utilitzar dos conjunts de dades: test_poor, amb 12 textos de alta complexitat lingüística i referències produïdes per anotadors humans; i exemples_lectura_facil_formatted, amb 11 textos de domini divers (salut, serveis i administració) amb referències certificades de Lectura Fàcil. Es van calcular 7 mètriques automàtiques, essent SARI i Levenshtein les de major poder discriminatiu.
Resultats clau
La troballa més rellevant de la Fase 1 és que el disseny del prompt té un impacte significativament major en la qualitat de l'adaptació (ΔSARI ≈ 0,15–0,20) que la mida del model (ΔSARI ≈ 0,03–0,06). A més, es va constatar que no existeix una tècnica universalment superior: els prompts optimitzats per a textos de molta compressió (V7, V8) perden efectivitat en textos de domini divers on les referències són més extenses, i viceversa. El principal factor que explica aquesta divergència és el Ràtio de Compressió (CR ratio), ja que les referències dels dos datasets tenen longituds molt diferents.
4.2. Avaluació de l'Efecte de la Temperatura
Com a extensió de l'avaluació principal, es va analitzar com la temperatura de generació afecta la qualitat i l'estabilitat dels resultats. S'empraren els models llama3.3 i gemma2:27b —els més robustos de la Fase 1— juntament amb els prompts V8 i CoT sobre els dos datasets, avaluant quatre nivells de temperatura (T=0,0; 0,3; 0,7; 1,0) amb llavor fixa (seed=42), per un total de 32 combinacions.
El resultat principal és que la temperatura no millora la qualitat mitjana de les adaptacions en cap dels dos datasets: SARI i BERTScore són màxims a T=0,0 en ambdós casos. A més, augmentar la temperatura amplifica l'especialització de domini, fent el model menys generalitzable entre datasets. La configuració globalment més robusta és llama3.3 + T=0,0 + V8, amb un score compost mitjà de 0,587 entre datasets.
4.3. Validació amb Usuaris Finals

Els resultats d'aquest capítol permeten respondre les qüestions de recerca formulades a la introducció i proporcionen una base sòlida per a les conclusions del treball, que es presenten al Capítol 7.
5. Discussió

6. Limitacions

7. Conclusions
7.1. Resum
Els resultats de la Fase 1 permeten extreure les conclusions principals següents:
•	Disseny del prompt vs. mida del model: El disseny del prompt va tenir un impacte significativament major en la qualitat de l'adaptació (ΔSARI ≈ 0,15–0,20) que la mida del model (ΔSARI ≈ 0,03–0,06).
•	Models més robustos: llama3.3 i gemma2_27b van demostrar ser els models més estables, mantenint-se al top-2 en els dos dominis avaluats.
•	Tècnica destacada: La tècnica V8 (imitació progressiva) va ser la més efectiva sobre el dataset de textos de complexitat alta, assolint SARI=0,557 i Levenshtein=0,325, màxims absoluts de l'estudi.
•	Divergència entre dominis: La diferència en el Ràtio de Compressió (CR ratio) va ser el principal factor que va provocar la divergència en el rendiment dels prompts entre datasets.
•	Mètriques més útils: Levenshtein i SARI van resultar ser les mètriques amb major poder discriminatiu, mentre que BERTScore va mostrar un rang efectiu massa estret per diferenciar correctament la qualitat dels outputs.
7.2. Resultats Tangibles

7.3. Treball Futur
Les línies de treball futur previstes inclouen: (1) l'anàlisi de l'estabilitat estocàstica del sistema variant la llavor de generació a temperatura no determinista, per obtenir resultats amb intervals de confiança; (2) l'ampliació de l'estudi a models multilingües i a textos en llengua catalana; (3) la integració del pipeline d'avaluació a la plataforma Explain-Up per permetre avaluació contínua en producció; i (4) la validació qualitativa amb un nombre major d'usuaris finals amb discapacitat intel·lectual per complementar les mètriques automàtiques.

Referències
[1] AENOR (2018). UNE 153101:2018 Lectura Fàcil. Pautes i recomanacions per a l'elaboració de documents. Asociación Española de Normalización.
[2] Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233.
[3] Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. Soviet Physics Doklady, 10(8), 707–710.
[4] Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. ACL Workshop on Text Summarization Branches Out.
[5] Papineni, K., Roukos, S., Ward, T., & Zhu, W.-J. (2002). BLEU: a method for automatic evaluation of machine translation. ACL 2002, 311–318.
[6] Xu, W., Napoles, C., Pavlick, E., Chen, Q., & Callison-Burch, C. (2016). Optimizing statistical machine translation for text simplification. Transactions of the Association for Computational Linguistics, 4, 401–415.
[7] Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating text generation with BERT. International Conference on Learning Representations (ICLR 2020).
8. Annexos

