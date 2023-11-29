# ChargingStations

Sia data una rete ad albero su cui si muovono k flussi, ciascuno dalla propria origine o k verso la propria destinazione d k . Supponendo di conoscere le lunghezze l ij degli archi (ij), che i veicoli partano tutti con carica completa e abbiano autonomia L, si posizionino il numero minimo di colonnine sui nodi della rete per permettere a tutti di raggiungere la propria destinazione, anche con + rifornimenti. Si supponga anche che ad ogni ricarica la batteria venga completamente ricaricata, qualunque sia il livello precedente.

## 1) IMPLEMENTAZIONE DI UNA PRIMA GREEDY

  Prima euristica greedy "naive":

  1. Iniziamo con un insieme vuoto di stazioni di ricarica.
  2. Per ogni flusso da origine a destinazione, seguiamo il percorso dell'albero. Ogni veicolo (flusso) parte con autonomia L.
  3. Mentre percorriamo il percorso, diminuiamo l'autonomia del veicolo della lunghezza dell'arco che si percorre.
  4. Se l'autonommia non è sufficiente per percorrere il prossimo arco del percorso, quindi percorrendolo scenderebbe a zero o meno, posizioniamo una colonnina di ricarica sul nodo corrente.
  5. Ripetiamo i passaggi 3-4 fino a quando tutti i veicoli hanno raggiunto le loro destinazioni.

Questa euristica cerca di minimizzare il numero di stazioni di ricarica posizionando ogni stazione il più lontano possibile lungo ogni percorso.
Il nodo più "promettente" su cui posizionare la colonnina di ricarica è quello più lontano dalla sorgente per ogni flusso.
L'ammissibilità è garantita dall'implementazione intrinseca dell'algoritmo.

## 2) UN ALTRO ALGORITMO COSTRUTTIVO

1. Iniziamo con un insieme di stazioni di ricarica riempito randomicamente.
2. Per ogni flusso da origine a destinazione, seguiamo il percorso dell'albero. Ogni veicolo (flusso) parte con autonomia L.
3. Controlliamo se la soluzione creata inizialmente in maniera randomica è ammissibile, ossia se tutti i veicoli riescono a raggiungere la propria destinazione con le colonnine posizionate.
4. Se quanto detto al punto 3 è vero, allora si è trovata la soluzione.

## 3) ALTRE RICERCHE LOCALI
  Che usano la soluzione di partenza e la ottimizzano.

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
