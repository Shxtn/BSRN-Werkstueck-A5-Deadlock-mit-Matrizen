import numpy as np  # Importiert das NumPy-Modul, das für numerische Operationen und die Arbeit mit Arrays verwendet wird.

def input_Ressourcenvektor():
    #Wenn der Benutzer selbst den Ressourcenvektor eingeben will, muss gefragt werden wie viele Klassen der Benutzer haben will
    anzahl = int(input("Wie viele Ressourcenklassen haben sie: "))  # Fragt den Benutzer nach der Anzahl der Ressourcenklassen.
    Ressourcenvektor = []  # Erstellt eine leere Liste für den Ressourcenvektor.

    # Eingabe der Menge der jeweiligen Ressourcenklassen
    for i in range(anzahl):  # Iteriert über die Anzahl der Ressourcenklassen.
        ressource = int(input(f"Geben sie nun die Menge der Ressourcenklasse {i+1}: "))  # Fragt nach der Menge der aktuellen Ressourcenklasse.
        Ressourcenvektor.append(ressource)  # Fügt die Menge der aktuellen Ressourcenklasse zur Liste hinzu.

    return Ressourcenvektor  # Gibt den Ressourcenvektor zurück.

def input_Belegungsmatrix(anzahl):
    # Abfrage wie viele Prozesse der Benutzer haben will
    Prozesse = int(input("Geben sie die Anzahl der Prozesse an: "))  # Fragt den Benutzer nach der Anzahl der Prozesse.
    Belegungs_Matrix = np.zeros((Prozesse, anzahl), dtype=int)  # Erstellt eine Matrix aus Nullen mit der Größe (Prozesse, anzahl).

    for i in range(Prozesse):  # Iteriert über die Anzahl der Prozesse.
        Prozessanzahl = i + 1  # Zählt die Prozessnummer.

        # Erstellung einer leeren Liste
        Belegung = []  # Erstellt eine leere Liste für die Belegung des aktuellen Prozesses.

        # Abfrage wie viel die jeweiligen Prozesse von den oben angegebenen Ressourcenklassen benötigen
        for j in range(anzahl):  # Iteriert über die Anzahl der Ressourcenklassen.
            Vektor = int(input(f"Geben sie an wie viele Ressourcen der Prozess {Prozessanzahl} von der Ressourcenklasse {j+1}:"))  # Fragt nach der benötigten Menge der aktuellen Ressourcenklasse für den aktuellen Prozess.

            # Hinzufügen des Vektors zur Liste
            Belegung.append(Vektor)  # Fügt die Menge der aktuellen Ressourcenklasse zur Liste hinzu.

        Belegungs_Matrix[i] = Belegung  # Setzt die Belegung des aktuellen Prozesses in die Belegungsmatrix.
    return np.array(Belegungs_Matrix)  # Gibt die Belegungsmatrix als NumPy-Array zurück.

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
                vektor.append(int(ressourcen)) # Das Objekt 'ressourcen' wird an das Ende der Liste 'vektor' angehängt

    # Wandelt die Liste in ein NumPy-Array um und gibt es zurück
    return np.array(vektor)


