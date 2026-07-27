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
