# Die Funktion dient der Eingabe der Anforderungsmatrix
def input_Anforderungsmatrix(Prozesse, anzahl):
    # Erstellt eine leere Anforderungsmatrix mit der angegebenen Anzahl von Prozessen und Ressourcenklassen, initialisiert mit Nullen
    AnforderungsMatrix = np.zeros((Prozesse, anzahl), dtype=int)

    # Schleife über jeden Prozess
    for i in range(Prozesse):
        # Setzt die Prozessnummer fest (1-basierter Index)
        Prozessanzahl = i + 1

        # Erstellt eine leere Liste zur Speicherung der Anforderungen für den aktuellen Prozess
        Anforderung = []

        # Schleife über jede Ressourcenklasse
        for l in range(anzahl):
            # Fragt den Benutzer, wie viele Ressourcen der aktuellen Klasse der aktuelle Prozess benötigt
            Vektor = int(input(f"Geben sie an wie viele Ressourcen der Prozess {Prozessanzahl} von der Ressourcenklasse {l + 1} benötigt:"))

            # Fügt die Benutzerangabe zur Liste der Anforderungen hinzu
            Anforderung.append(Vektor) # Das Objekt 'Vektor' wird an das Ende der Liste 'Anforderung' angehängt
            numpy_Anforderung = np.array(Anforderung)  # Konvertiert die Liste in ein NumPy-Array (wird hier aber nicht verwendet)

        # Setzt die Zeile der Anforderungsmatrix für den aktuellen Prozess auf die gesammelten Anforderungen
        AnforderungsMatrix[i] = Anforderung

# Gibt die ausgefüllte Anforderungsmatrix zurück
    return AnforderungsMatrix

# Definiert eine Funktion zum Lesen eines Vektors aus einer Datei
def read_from_file(filename):
    # Erstellt eine leere Liste zur Speicherung der Vektorelemente
    vektor = []

    # Öffnet die Datei im Lesemodus
    with open(filename, 'r') as file:
        # Liest jede Zeile der Datei
        for line in file:
            # Teilt jede Zeile in einzelne Ressourcen auf und fügt sie der Liste hinzu
            for ressourcen in line.split():
                vektor.append(ressourcen) # Das Objekt 'ressourcen' wird an das Ende der Liste 'vektor' angehängt

    # Wandelt die Liste in ein NumPy-Array um und gibt es zurück
    return np.array(vektor)