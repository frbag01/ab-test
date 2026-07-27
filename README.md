# Introduzione
Il dataset utilizzato in questo progetto appartiene alla categoria dei dataset di A/B Testing per l’analisi del comportamento degli utenti su piattaforme digitali, nel contesto di un A/B test, gli utenti vengono assegnati casualmente a due gruppi:
- Gruppo A (Control Group): rappresenta la versione originale del prodotto o della pagina.
- Gruppo B (Treatment Group): rappresenta la nuova versione o modifica introdotta.

L'obiettivo è misurare se la variazione introdotta produce un miglioramento significativo in una metrica chiave, come ad esempio il tasso di conversione
# Background
## Metadati principali del dataset
Il dataset include diverse variabili che descrivono il comportamento degli utenti durante l’esperimento:
- User ID – identificatore univoco dell’utente
- Group – gruppo di assegnazione dell’utente (A o B)
- Device – tipologia di dispositivo utilizzato (Desktop, Mobile, Tablet)
- Location – area geografica dell’utente
- Page Views – numero di pagine visitate durante la sessione
- Time Spent – tempo trascorso sulla pagina o sul sito
- Conversion – variabile binaria che indica se l’utente ha completato l’azione desiderata (1 = sì, 0 = no)

Queste variabili permettono di analizzare sia il comportamento degli utenti che le performance delle diverse varianti del test.


# Domande di Analisi

1. Conversion Rate per gruppo
2. Il nuovo design (Gruppo B) ha migliorato il tempo medio trascorso sul sito per gli utenti Mobile?
3. In quali aree geografiche il nuovo design ha funzionato meglio?
4. Seleziona gli utenti che hanno superato la media nazionale di Time Spent ma non hanno convertito. Quanti di questi sono nel Gruppo B?
5. Valutare se la differenza tra i tassi di conversione dei due gruppi sia statisticamente significativa (Z-Test per proporzioni)
6. Intervalli di confidenza per i tassi di conversione dei due gruppi.
7. Il nuovo design ha aumentato il tempo medio speso sul sito oppure ha creato più utenti altamente coinvolti?
8. È possibile che il Gruppo B vinca complessivamente ma perda nel segmento Desktop? (Simpson's Paradox)
#### Dashboard Excel

La dashboard include una tabella riassuntiva con i principali KPI:
- Visitatori
- Conversioni
- Conversion Rate (CR%)
- Lift tra i gruppi

Per consentire un'esplorazione dinamica dei risultati, sono stati aggiunti Slicer interattivi per:
- Device
- Location


# Tools utilizzati
Durante lo sviluppo del progetto sono stati utilizzati diversi strumenti e tecnologie:

- Python per l’analisi dei dati e i test statistici
- SQL per interrogare e aggregare i dati
- Excel per la creazione di una dashboard riassuntiva e interattiva

Per supportare alcune fasi del processo analitico e migliorare l’efficienza nello sviluppo delle query e del codice, è stato utilizzato anche l’ausilio di strumenti di Intelligenza Artificiale.

Il progetto è stato inoltre ispirato ai progetti di data analysis realizzati da Luke Barousse, noto per i suoi contenuti educativi nel campo della data analytics e per i suoi esempi pratici di portfolio basati su SQL, Python e dashboard.

# Analisi
### 1. Conversion Rate per gruppo
Scrivi una query che calcoli il numero di conversioni e il Conversion Rate (CR%) per ogni gruppo
```sql
WITH CONVERSIONI AS(
	SELECT group_test,COUNT(*) AS conversioni 
	FROM ab
	WHERE conv='Yes'
	GROUP BY group_test
),
TOTALI AS(
SELECT group_test, COUNT(*) AS numerosità
FROM ab
GROUP BY group_test
)
SELECT TOTALI.group_test,CONVERSIONI.conversioni,ROUND((CONVERSIONI.conversioni*1.0)/TOTALI.numerosità,3) AS CR
FROM CONVERSIONI 
LEFT JOIN TOTALI ON TOTALI.group_test=CONVERSIONI.group_test
```

#### Risultati e Insights

dalla query emergono le seguenti metriche di performance per i due gruppi:

| Gruppo | Conversioni | Tasso di Conversione (CR) |
| :--- | :---: | :---: |
| **A (Controllo)** |  136 | **5,4%** |
| **B (Trattamento)** |  349 | **14,1%** |

#### Key Takeaways:
- **Aumento del Tasso di Conversione (Lift Relativo):** Il Gruppo B ha registrato un **incremento assoluto di +8,7 punti percentuali** nel Conversion Rate rispetto al gruppo di controllo A. In termini relativi, la nuova versione ha generato un **incremento delle conversioni del +161%**.
- **Sample Ratio Mismatch (SRM):** La numerosità dei due campioni (2.500 per A e 2.475 per B) risulta bilanciata (circa 50/50), indicando che il processo di randomizzazione e assegnazione degli utenti è avvenuto correttamente.
- **Conclusione preliminare:** Il nuovo design (Gruppo B) mostra un impatto nettamente positivo sulle conversioni rispetto alla versione originale.

### 2. Engagment per Mobile
Calcola la media di Page Views e Time Spent per gruppo, nei soli Mobile. 
```sql
SELECT group_test,ROUND(AVG(page_views),2) AS paginemed,ROUND(AVG(time_spent),2) AS tempmed
FROM ab
WHERE device='Mobile'
GROUP BY group_test
ORDER BY tempmed DESC
```
#### Risultati e Insights

| Gruppo | Page Views Medie | Time Spent Medio (sec) |
| :--- | :---: | :---: |
| **A (Controllo)** | 7,64 | 240,37 |
| **B (Trattamento)** | 7,44 | 243,38 |

#### Key Takeaways:
- **Tempo Trascorso (Time Spent):** Gli utenti del Gruppo B trascorrono in media **~3 secondi in più** sul sito (+1,25%) rispetto al Gruppo A (243,38 s vs 240,37 s).
- **Pagine Viste (Page Views):** Il Gruppo B registra un numero lievemente inferiore di pagine viste medie (7,44 vs 7,64).
- **Interpretazione:** Il **nuovo design (B) rende la navigazione più fluida e mirata nei dispositivi mobile**: gli utenti trovano ciò che cercano con meno passaggi e completano l'azione con maggior facilità.

### 3. Top Performing Locations
Trova le 2 nazioni con il conversion rate più alto nel Gruppo B. Dove ha funzionato meglio il cambiamento?
```sql
WITH CONVERSIONI AS(
	SELECT loc,COUNT(*) AS conversioni 
	FROM ab
	WHERE group_test='B' AND conv='Yes'
	GROUP BY loc
),
TOTALI AS(
	SELECT loc, COUNT(*) AS numerosità
	FROM ab
	WHERE group_test='B'
	GROUP BY loc
)
SELECT TOTALI.loc,ROUND((CONVERSIONI.conversioni*1.0)/TOTALI.numerosità,3) AS CR
FROM CONVERSIONI 
LEFT JOIN TOTALI ON TOTALI.loc=CONVERSIONI.loc
ORDER BY CR DESC
LIMIT 2
```
#### Risultati e Insights

| Area Geografica (Location) | Conversion Rate (CR%) |
| :--- | :---: |
| **Scotland (Scozia)** | **15,1%** |
| **Wales (Galles)** | **15,1%** |

#### Key Takeaways:
- **Performance D'Eccellenza:** **Scozia** e **Galles** rappresentano le due aree geografiche con il tasso di conversione più elevato all'interno del Gruppo B, registrando entrambe un **CR del 15,1%**.
- **Impatto del Nuovo Design:** Il cambio di layout ha mostrato la sua massima efficacia in queste due regioni, superando la media generale del Gruppo B (14,1%).

### 4. Analisi degli utenti "Power Users"
Seleziona quanti utenti che hanno superato la media nazionale di Time Spent ma non hanno convertito. Quanti di questi sono nel Gruppo B?
```sql
WITH NOCONVB AS(
SELECT user_id, time_spent, 
       (SELECT AVG(time_spent) FROM ab) AS media_nazionale
FROM ab
WHERE conv = 'No'
  AND group_test='B'	
  AND time_spent > (SELECT AVG(time_spent) FROM ab)
)

SELECT COUNT(*) FROM NOCONVB
```

#### Risultati e Insights

| **Utenti Non Convertiti con Time Spent > Media** | **1.076** |

#### Key Takeaways :
- **Elevato Coinvolgimento Senza Conversione:** Ben **1.076 utenti** del Gruppo B trascorrono sul sito più tempo della media (oltre 4 minuti e 2 secondi) senza però completare l'azione desiderata,esattamente **oltre la metà (50,5%) di tutti gli utenti non convertiti del Gruppo B**.


# PYTHON 

Puoi vedere il codice principale qui: [1] [Python Script](ab.py)

### 5.Test di Significatività Statistica (Z-Test)
Calcola il p-value per le conversioni tra A e B. Se il p-value è < 0.05, puoi rigettare l'ipotesi nulla?

Risultati del Test Chi-quadro
Statistica Chi2: 106.2281
p-value: 0.0000
Possiamo quindi **rifiutare con assoluta certezza l'ipotesi nulla ($H_0$)** di indipendenza tra i gruppi.
- **Impatto Reale della Variante:** La differenza tra il tasso di conversione del Gruppo A ($5,4\%$) e quello del Gruppo B ($14,1\%$) **non è frutto del caso o di una fluttuazione campionaria**, ma è direttamente attribuibile alla nuova versione (Gruppo B).

### 6.Intervalli di confidenza per i tassi di conversione dei due gruppi al 95%
Calcola e visualizza (con barre d'errore) gli intervalli di confidenza per i tassi di conversione di entrambi i gruppi. C'è un overlap?

Intervallo di Confidenza 95%: [7.04%, 10.30%]

Se ripetessimo questo A/B test 100 volte su campioni differenti, circa **95 volte su 100 l'intervallo calcolato conterrebbe la vera differenza** del tasso di conversione tra Gruppo B e Gruppo A nella popolazione generale (stimata tra il **+7,04%** e il **+10,30%**).
- **Assenza di Zero (Significatività Pratica):** Poiché l'intervallo si trova interamente sopra lo zero e non lo include, abbiamo un'ottima evidenza che il Gruppo B è superiore al Gruppo A.

### 7.Analisi della Distribuzione (Engagement)
Il nuovo design ha aumentato il tempo medio speso sul sito oppure ha creato più utenti altamente coinvolti?

![istogramma per confrontare la distribuzione di Time Spent tra i due gruppi](https://github.com/frbag01/ab-test/blob/main/hist.png?raw=true)

La variazione della media è trascurabile:

Media Gruppo A: 241.73

Media Gruppo B: 243.30

L'analisi visiva delle distribuzioni (istogrammi) e il confronto delle medie indicano che il nuovo design **non ha aumentato il tempo medio speso sul sito in modo rilevante** (+1,57 unità, pari a un incremento quasi impercettibile).
- **Omogeneità del Comportamento:** La sovrapposizione e la forma uniforme dei due istogrammi confermano che la variante B non sembrerbbe aver allungato la durata delle sessioni della media degli utenti in modo significativo.

### 8.Segmentazione e Simpson's Paradox
Crea un grafico a barre che mostri il Conversion Rate per Gruppo, ma suddiviso per Device. È possibile che B vinca globalmente ma perda su Desktop?

![Barplot per confrontare il CR per Gruppo](https://github.com/frbag01/ab-test/blob/main/barplot.png?raw=true)

Non è presente il Simpson's Paradox.**
- **Performance Coerente tra i Segmenti:** Il Gruppo B supera nettamente il Gruppo A in entrambi i dispositivi analizzati:
  - Su **Desktop**, il Conversion Rate sale dal **5,87%** al **13,91%** ($+8,04\%$ punti percentuali).
  - Su **Mobile**, il Conversion Rate sale dal **4,94%** al **14,24%** ($+9,30\%$ punti percentuali).
- **Conclusione:** Il successo del nuovo design (Gruppo B) non è un effetto distorto dall'aggregazione dei dati (come accadrebbe nel Paradosso di Simpson), ma è un **miglioramento solido e uniforme su tutti i dispositivi**, con un impatto particolarmente marcato sugli utenti Mobile.
