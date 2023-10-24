Sia data una rete ad albero su cui si muovono k flussi, ciascuno dalla propria origine o k verso la propria destinazione d k . Supponendo di conoscere le lunghezze l ij degli archi (ij), che i veicoli partano tutti con carica completa e abbiano autonomia L, si posizionino il numero minimo di colonnine sui nodi della rete per permettere a tutti di raggiungere la propria destinazione, anche con + rifornimenti. Si supponga anche che ad ogni ricarica la batteria venga completamente ricaricata, qualunque sia il livello precedente.

# ChargingStations
LibreriaUtile: NetworkX per Python

## 1) MODELLO MATEMATICO
  Una volta fatto, chiedere subito un ricevimento alla Nonato che aiuta a far partire e lo corregge. È utile per continuare il progetto.

## 2) IMPLEMENTAZIONE DI UNA PRIMA GREEDY
  La prima greedy dà una prima soluzione, che sarà da ottimizzare.

## 3) ALTRE RICERCHE LOCALI
  Che usano la soluzione di partenza e la ottimizzano.



# Una greedy possibile
Un'euristica greedy che potrebbe essere utilizzata per risolvere questo problema potrebbe essere la seguente:

1. Iniziamo con un insieme vuoto di stazioni di ricarica.
2. Per ogni flusso da origine a destinazione, seguiamo il percorso dell'albero. Partiamo con una carica completa (cioè, l'autonomia è L).
3. Mentre percorriamo il percorso, diminuiamo l'autonomia del veicolo della lunghezza dell'arco corrente.
4. Quando l'autonomia del veicolo sta per scendere a zero (o meno), dobbiamo posizionare una stazione di ricarica. La posizioniamo sul nodo più vicino che non supera l'autonomia del veicolo (cioè, scegliamo il nodo più lontano possibile lungo il percorso che può ancora essere raggiunto con la carica rimanente). Aggiungiamo questo nodo all'insieme delle stazioni di ricarica.
5. Ripetiamo i passaggi 3-4 fino a quando tutti i veicoli hanno raggiunto le loro destinazioni.

Questa euristica cerca di minimizzare il numero di stazioni di ricarica posizionando ogni stazione il più lontano possibile lungo ogni percorso, dato che ogni veicolo parte con la carica completa e ogni stazione di ricarica ricarica completamente la batteria del veicolo.

Tuttavia, è importante notare che questa euristica potrebbe non fornire sempre la soluzione ottimale. Ad esempio, potrebbe essere possibile risparmiare stazioni di ricarica considerando come i percorsi dei diversi flussi si intersecano e si sovrappongono. Per problemi più complessi o per ottenere soluzioni più ottimali, potrebbe essere necessario utilizzare tecniche più avanzate o algoritmi di ottimizzazione globale.

# una greedy migliore
Certamente, considerando le intersezioni tra i percorsi dei flussi, possiamo modificare l'euristica precedente nel seguente modo:

1. Iniziamo con un insieme vuoto di stazioni di ricarica.
2. Per ogni flusso da origine a destinazione, seguiamo il percorso dell'albero. Partiamo con una carica completa (cioè, l'autonomia è L).
3. Mentre percorriamo il percorso, diminuiamo l'autonomia del veicolo della lunghezza dell'arco corrente.
4. Se l'autonomia del veicolo sta per scendere a zero (o meno) con il prossimo arco, dobbiamo posizionare una stazione di ricarica. Invece di posizionare la stazione sul nodo più vicino lungo il percorso, consideriamo i nodi di intersezione con altri percorsi. Se esiste un nodo di intersezione entro l'autonomia del veicolo, posizioniamo la stazione di ricarica su quel nodo. Altrimenti, posizioniamo la stazione sul nodo più lontano possibile lungo il percorso che può ancora essere raggiunto con la carica rimanente. Aggiungiamo questo nodo all'insieme delle stazioni di ricarica.
5. Ripetiamo i passaggi 3-4 fino a quando tutti i veicoli hanno raggiunto le loro destinazioni.

Grazie per avermi fatto notare l'errore! Spero che questa versione corretta dell'euristica sia utile.

# un altro algoritmo greedy
Un altro possibile algoritmo che tiene conto del fatto che non c'è bisogno di minimizzare il numero di nodi da attraversare potrebbe essere il seguente:

1. Iniziamo con un insieme vuoto di stazioni di ricarica.
2. Per ogni flusso da origine a destinazione, seguiamo il percorso dell'albero. Partiamo con una carica completa (cioè, l'autonomia è L).
3. Mentre percorriamo il percorso, diminuiamo l'autonomia del veicolo della lunghezza dell'arco corrente.
4. Se l'autonomia del veicolo sta per scendere a zero (o quasi) con il prossimo arco, dobbiamo posizionare una stazione di ricarica. Invece di posizionare la stazione sul nodo più vicino lungo il percorso, consideriamo i nodi di intersezione con altri percorsi. Se esiste un nodo di intersezione entro l'autonomia del veicolo, posizioniamo la stazione di ricarica su quel nodo. Altrimenti, posizioniamo la stazione sul nodo corrente. Aggiungiamo questo nodo all'insieme delle stazioni di ricarica.
5. Ripetiamo i passaggi 3-4 fino a quando tutti i veicoli hanno raggiunto le loro destinazioni.

In questo algoritmo, non stiamo cercando di minimizzare il numero di nodi attraversati. Invece, stiamo cercando di massimizzare l'uso delle intersezioni tra i percorsi per ridurre il numero totale di stazioni di ricarica necessarie.

Tuttavia, come sempre, questa euristica potrebbe non fornire sempre la soluzione ottimale. Per problemi più complessi o per ottenere soluzioni più ottimali, potrebbe essere necessario utilizzare tecniche più avanzate o algoritmi di ottimizzazione globale.

# Algoritmo di Prim
L'algoritmo di Prim è un algoritmo di ricerca dell'albero di copertura minimo per grafi pesati. L'algoritmo mantiene una lista di nodi visitati e una lista di nodi da visitare. Inizialmente, tutti i nodi sono nella lista dei nodi da visitare. L'algoritmo seleziona il nodo con il costo più basso dalla lista dei nodi da visitare e lo aggiunge alla lista dei nodi visitati. Quindi, per ogni nodo adiacente al nodo appena visitato, l'algoritmo calcola il costo del percorso dal nodo iniziale al nodo adiacente attraverso il nodo appena visitato. Se il costo del percorso è inferiore al costo del percorso corrente dal nodo iniziale al nodo adiacente, l'algoritmo aggiorna il costo del percorso e il nodo precedente del nodo adiacente. L'algoritmo continua a selezionare il nodo con il costo più basso dalla lista dei nodi da visitare e ad aggiornare i costi dei percorsi e i nodi precedenti dei nodi adiacenti finché tutti i nodi non sono stati visitati.


# Algoritmo di Dijkstra
L'algoritmo di Dijkstra è un algoritmo di ricerca del percorso più breve per grafi pesati. L'algoritmo mantiene una lista di nodi visitati e una lista di nodi da visitare. Inizialmente, tutti i nodi sono nella lista dei nodi da visitare. L'algoritmo seleziona il nodo con il costo più basso dalla lista dei nodi da visitare e lo aggiunge alla lista dei nodi visitati. Quindi, per ogni nodo adiacente al nodo appena visitato, l'algoritmo calcola il costo del percorso dal nodo iniziale al nodo adiacente attraverso il nodo appena visitato. Se il costo del percorso è inferiore al costo del percorso corrente dal nodo iniziale al nodo adiacente, l'algoritmo aggiorna il costo del percorso e il nodo precedente del nodo adiacente. L'algoritmo continua a selezionare il nodo con il costo più basso dalla lista dei nodi da visitare e ad aggiornare i costi dei percorsi e i nodi precedenti dei nodi adiacenti finché tutti i nodi non sono stati visitati.

Si potrebbe utilizzare un mix tra i due algoritmi per poter trovare la soluzione ottima. Per questo si potrebbe decidere dove posizionare le colonnine e assegnare un peso più basso e utilizzare l'algoritmo di Dijkstra per trovare il percorso più breve tra due nodi. In questo modo si potrebbe trovare la soluzione ottima.