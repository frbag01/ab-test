-- 1.Controllo del Sample Ratio Mismatch (SRM):
-- Domanda: Conta quanti utenti sono stati assegnati al Gruppo A e quanti al Gruppo B.'

SELECT group_test, COUNT(*) AS numerosità
FROM ab
GROUP BY group_test

-- 2.Calcolo del Tasso di Conversione (Baseline vs Test):

-- Domanda: Scrivi una query che calcoli il numero di conversioni e il Conversion Rate (CR%) per ogni gruppo 

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

-- 3.Engagement per Dispositivo:

-- Domanda: Calcola la media di Page Views e Time Spent per gruppo, segmentando per Device. Il nuovo design (B) ha migliorato il tempo speso su Mobile?


SELECT group_test,AVG(page_views) AS paginemed,AVG(time_spent) AS tempmed
FROM ab
WHERE device='Mobile'
GROUP BY group_test
ORDER BY tempmed DESC



-- 4.Top Performing Locations:

-- Domanda: Trova le 2 Location con il conversion rate più alto nel Gruppo B. Dove ha funzionato meglio il cambiamento?

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


-- 5. Analisi degli utenti "Power Users":

-- Domanda: Seleziona gli utenti che hanno superato la media nazionale di Time Spent ma non hanno convertito. Quanti di questi sono nel Gruppo B? (Potenziale frizione nel funnel).


WITH NOCONVB AS(
SELECT user_id, time_spent, 
       (SELECT AVG(time_spent) FROM ab) AS media_nazionale
FROM ab
WHERE conv = 'No'
  AND group_test='B'	
  AND time_spent > (SELECT AVG(time_spent) FROM ab)
)

SELECT COUNT(*) FROM NOCONVB

