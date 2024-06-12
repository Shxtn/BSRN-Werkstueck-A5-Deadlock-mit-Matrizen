import numpy as np  # Importiert das NumPy-Modul, das für numerische Operationen und die Arbeit mit Arrays verwendet wird.

def input_Ressourcenvektor():
    "Wenn der Benutzer selbst den Ressourcenvektor eingeben will, muss gefragt werden wie viele Klassen der Benutzer haben will"
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


