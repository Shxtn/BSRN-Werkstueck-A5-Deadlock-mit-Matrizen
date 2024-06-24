
import numpy as np  # Importiert das NumPy-Modul, das für numerische Operationen und die Arbeit mit Arrays verwendet wird.
import random
import logging      # importiert das Modul logging, mit dem wir ein Verlaufsprotokoll über die Aktivitäten des Simulators erstellen können
import argparse     # importiert das Modul argparse, wird benötigt um die Kommandozeilenargumente der Main zu analysieren und interpretieren

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


def simulate_processes(Ressourcenvektor, Belegungs_Matrix, AnforderungsMatrix, noninteractive, logger):
    # Eintrag in das Verlaufsprotokoll über den Start der Prozesssimulation; die folgenden "logger.info"-Zeilen der Methode
    # funktionieren analog und sollten über den entsprechenden Eintrag selbsterklärend sein. Daher werden diese nicht
    # erneut kommentiert
    logger.info("Prozesssimulation gestartet")

    # Bestimmen der Anzahl der Prozesse aus der Anforderungsmatrix
    anzahl_prozesse = AnforderungsMatrix.shape[0]

    # Erstellen einer Liste, um den Abschlussstatus jedes Prozesses zu verfolgen
    finished = [False] * anzahl_prozesse

    logger.info("Abschlussstatus aller Prozesse auf \"Nicht abgeschlossen\" gesetzt")

    # Berechnen des initialen Ressourcenrestvektors
    # Dies erfolgt durch Subtrahieren der summierten Belegung von den verfügbaren Ressourcen
    ressourcenrestvektor = Ressourcenvektor - np.sum(Belegungs_Matrix, axis=0)
    print(f"Initialer Ressourcenrestvektor: {ressourcenrestvektor}")

    logger.info(f"Berechnung und Ausgabe initialer Restressourcenvektor: {ressourcenrestvektor}")

    # Fortsetzung der Simulation, bis alle Prozesse abgeschlossen sind
    while not all(finished):
        # Liste der Prozesse, die ausgeführt werden können
        ausführbare_prozesse = []

        # Überprüfung jedes Prozesses, um festzustellen, ob er ausgeführt werden kann
        for i in range(anzahl_prozesse):
            # Überprüfung, ob der Prozess noch nicht abgeschlossen ist und ob seine Anforderungen erfüllbar sind
            if not finished[i] and all((AnforderungsMatrix[i] <= ressourcenrestvektor)):
                # Prozess zur Liste der ausführbaren Prozesse hinzufügen
                ausführbare_prozesse.append(i)

                logger.info(f"Prüfung aller ausführbaren Prozesse, Ergebnis: {ausführbare_prozesse}")

        # Wenn keine ausführbaren Prozesse vorhanden sind, liegt ein Deadlock vor
        if not ausführbare_prozesse:
            print("Deadlock: Kein Prozess kann ausgeführt werden.")

            logger.info("Kein Prozess ausführbar, Deadlock!")
            break

        # Wenn die Simulation im non-interactive Modus ist, wähle zufällig einen ausführbaren Prozess
        if noninteractive:
            nächster_prozess = random.choice(ausführbare_prozesse)

            logger.info(f"Benutzer hat \"noninteractive\" gewählt, zufällige Wahl eines ausführbaren Prozesses getroffen: {nächster_prozess}")

        # WICHTIG: Die Simulation endet hier, da der nächste Prozess im interactive Modus
        # nicht ausgewählt wird. Der Code muss erweitert werden, um die Ausführung fortzusetzen.

        else:  # Dieser Block wird ausgeführt, wenn der vorhergehende if-Block nicht zutrifft
            while True:  # Beginne eine unendliche Schleife, die solange läuft, bis sie manuell unterbrochen wird
                print(f"Ausführbare Prozesse: {ausführbare_prozesse}")  # Drucke die Liste der ausführbaren Prozesse
                try:  # Versuche den folgenden Block auszuführen, um potenzielle Fehler abzufangen
                    nächster_prozess = int(input( "Welcher Prozess soll als nächstes ausgeführt werden? "))  # Frage den Benutzer nach der nächsten Prozessnummer und konvertiere die Eingabe in einen Integer

                    logger.info(f"Auszuführender Prozess durch Benutzer gewählt: {nächster_prozess}")


                    if nächster_prozess in ausführbare_prozesse:  # Überprüfe, ob der eingegebene Prozess in der Liste der ausführbaren Prozesse ist

                        logger.info(f"Gewählter Prozess {nächster_prozess} ist ausführbar")
                        break  # Wenn ja, verlasse die Schleife
                    else:  # Wenn nein
                        print(f"Prozess {nächster_prozess} kann nicht ausgeführt werden. Bitte wählen Sie einen anderen Prozess.")  # Informiere den Benutzer, dass dieser Prozess nicht ausgeführt werden kann

                        logger.info(f"Gewählter Prozess {nächster_prozess} ist nicht ausführbar")

                except ValueError:  # Fange den Fehler ab, wenn die Eingabe keine gültige Zahl ist
                    print("Ungültige Eingabe. Bitte eine gültige Prozessnummer eingeben.")  # Informiere den Benutzer über die ungültige Eingabe

                    # Fehlermeldung im Verlaufsprotokoll über eine ungültige Nutzereingabe bei der Wahl des nächsten auszuführenden Prozesses;
                    # die folgenden "logger.error"-Zeilen der Methode funktionieren analog und sollten über den entsprechenden Eintrag
                    # selbsterklärend sein. Daher werden diese nicht erneut kommentiert
                    logger.error(f"Fehler: Eingabe {nächster_prozess} des Benutzers ist ungültig")

        # Aktualisiere den Ressourcenrestvektor mit den freigegebenen Ressourcen des ausgeführten Prozesses
        neue_ressourcenrestvektor = (ressourcenrestvektor + Belegungs_Matrix[nächster_prozess])

        # Überprüfen, ob negative Werte im neuen Ressourcenrestvektor vorhanden sind
        if any(neue_ressourcenrestvektor < 0):  # Wenn irgendein Wert im neuen Vektor negativ ist
            print(f"Fehler: Negative Werte im Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}.")  # Fehlerausgabe
            logger.error(f"Fehler: Negative Werte im Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}")
            print(f"Aktueller Ressourcenrestvektor: {ressourcenrestvektor}")  # Drucke den aktuellen Ressourcenrestvektor
            logger.error(f"Aktueller Ressourcenrestvektor: {ressourcenrestvektor}")
            print(f"Anforderungen von Prozess {nächster_prozess}: {AnforderungsMatrix[nächster_prozess]}")  # Drucke die Anforderungen des Prozesses
            logger.error(f"Anforderungen von Prozess {nächster_prozess}: {AnforderungsMatrix[nächster_prozess]}")
            print(f"Belegte Ressourcen von Prozess {nächster_prozess}: {Belegungs_Matrix[nächster_prozess]}")  # Drucke die belegten Ressourcen des Prozesses
            logger.error(f"Belegte Ressourcen von Prozess {nächster_prozess}: {Belegungs_Matrix[nächster_prozess]}")
            break  # Beende die Schleife

        print(f"Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}: {ressourcenrestvektor}")  # Drucke den Ressourcenrestvektor nach der Ausführung des Prozesses
        logger.info(f"Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}: {ressourcenrestvektor}")

        # Aktualisiere den Ressourcenrestvektor
        ressourcenrestvektor = neue_ressourcenrestvektor

        # Markiere den Prozess als abgeschlossen
        finished[nächster_prozess] = True
        print(f"Prozess {nächster_prozess} ist abgeschlossen. Ressourcenrestvektor: {ressourcenrestvektor}")  # Informiere über den Abschluss des Prozesses und drucke den aktuellen Ressourcenrestvektor
        logger.info(f"Prozess {nächster_prozess} abgeschlossen, Ressourcenrestvektor: {ressourcenrestvektor}")

        print("Simulation abgeschlossen. Alle ausführbaren Prozesse wurden bearbeitet oder ein Deadlock ist aufgetreten")  # Drucke eine Abschlussmeldung der Simulation
        logger.info("Simulation abgeschlossen, alle ausführbaren Prozesse bearbeitet oder Deadlock")


# auch in der main-Methode erfolgt keine erneute Kommentierung zu "logger.info"- und "logger.error"-Zeilen
def main():
    # ArgumentParser-Obkjekt (Funktion s. Kommentar bei Import-Zeile oben) wird erstellt
    parser = argparse.ArgumentParser(description='Ressourcen- und Prozessmatrix-Eingabe')
    # Pflichtargument für Kommandozeileneingabe, die den Eingabemodus des Benutzers für den Simulator festlegt
    parser.add_argument('-mode', choices=['s', 'd'], required=True,
                        help="Eingabemodus: 's' für manuelle Eingabe, 'd' für Datei")
    # optionale Argumente für die Dateinamen des Ressourcenvektors, der Belegungs- und der Anforderungsmatrix im Datei-Modus
    parser.add_argument('-rv', '--ressourcenvektor', type=str, help="Dateiname für den Ressourcenvektor")
    parser.add_argument('-bm', '--belegungsmatrix', type=str, help="Dateiname für die Belegungsmatrix")
    parser.add_argument('-am', '--anforderungsmatrix', type=str, help="Dateiname für die Anforderungsmatrix")
    # optionales Argument um den "noninteractive"-Modus nutzen zu können
    parser.add_argument('-noninteractive', action='store_true', help="Automatische Auswahl des nächsten Prozesses")
    # optionales Argument um den Namen der Logdatei für das Verlaufsprotokoll zu ändern, standardmäßig "simulator.log"
    parser.add_argument('-l', '--logfile', type=str, default='simulator.log', help="Logdatei")
    # Kommandozeilenargumente werden geparst und in der Variablen "args" gespeichert
    args = parser.parse_args()

    # konfiguriert die Einstellungen für das Verlaufsprotokoll des Programms, also den Namen der Logdatei, den Schreibmodus,
    # das Format der Einträge, das Datums- und Zeitformat sowie das Level (also Info oder Error) der Einträge
    logging.basicConfig(
        filename=args.logfile,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )

    # Logger-Objekt wird erstellt
    logger = logging.getLogger()

    logger.info("Programm startet")

    # überprüft, ob der mauelle Modus gewählt wurde
    if args.mode == 's':

        logger.info("Benutzer wählt manuelle Eingabe")

        # manuelle Eingabe und anschließende Ausgabe des Ressourcenvektors
        ressourcenvektor = input_Ressourcenvektor()
        print("Ressourcenvektor", ressourcenvektor)
        logger.info(f"Eingegebener Ressourcenvektor: {ressourcenvektor}")

        # Anzahl der Ressourcen wird bestimmt und in der Variablen "anzahl" gespeichert
        anzahl = len(ressourcenvektor)

        # manuelle Eingabe und anschließende Ausgabe der Belegungsmatrixx mit Übergabe der Anzahl der Ressourcen
        belegungsmatrix = input_Belegungsmatrix(anzahl)
        print("Belegungsmatrix\n", belegungsmatrix)
        logger.info(f"Eingegebene Belegungsmatrix:\n {belegungsmatrix}")

        # Anzahl der Prozesse wird bestimmt und in der Variablen "prozesse" gespeichert
        prozesse = len(belegungsmatrix)
        logger.info(f"Prozesse: {prozesse}")

        # manuelle Eingabe und anschließende Ausgabe der Anforderungsmatrix mit Übergabe der Anzahl der Prozesse und Ressourcen
        anforderungsmatrix = input_Anforderungsmatrix(prozesse, anzahl)
        print("Anforderungsmatrix\n", anforderungsmatrix)
        logger.info(f"Eingegebene Anforderungsmatrix:\n {anforderungsmatrix}")

        # Ausführung der "simulate_processes"-Methode mit anschließender Ausgabe des Ergebnisses
        simulate_processes(ressourcenvektor, belegungsmatrix, anforderungsmatrix, args.noninteractive, logger)
        print(simulate_processes)
        logger.info(f"Simulation zur Überprüfung auf Deadlock gestartet: {simulate_processes}")

    # überprüft, ob der Modus zum Einlesen von Dateien gewählt wurde
    elif args.mode == 'd':

        logger.info("Benutzer wählt Eingabe durch Einlesen einer Datei")

        # Überprüfung, ob die Dateinamen korrekt in die Kommandozeile eingegeben wurden und gibt Fehlermeldung aus, falls nicht
        if not (args.ressourcenvektor and args.belegungsmatrix and args.anforderungsmatrix):
            print(
                "Fehler: Wenn der Modus 'd' gewählt wird, müssen die Namen der Dateien für den Ressourcenvektor, die Belegungsmatrix und die Anforderungsmatrix eingegeben werden ")
            logger.error(
                "Fehler: Kein Dateiname für Einlesen des Ressourcenvektors, der Belegungsmatrix oder der Anforderungsmatrix eingegeben")
            return

        # Main-Methode durchläuft die gleichen Schritte wie im manuellen Modeus, nur dass die Daten durch das Auslesen der Dateien
        # und nicht mehr durch manuelle Eingabe eingespeist werden
        ressourcenvektor = read_from_file(args.ressourcenvektor)
        print("Ressourcenvektor:", ressourcenvektor)
        logger.info(f"Eingelesener Ressourcenvektor: {ressourcenvektor}")

        anzahl = len(ressourcenvektor)

        # die ".reshape"-Methode mit den übergebenen Parametern sorgt dafür, dass aus den Daten der eingelesenen Datei
        # eine zweidimensionale Matrix mit "anzahl" Spalten  und einer errechneten Anzahl von Zeilen erzeugt wird
        belegungsmatrix = read_from_file(args.belegungsmatrix).reshape(-1, anzahl)
        print("Belegungsmatrix:\n", belegungsmatrix)
        logger.info(f"Eingelesene Belegungsmatrix:\n {belegungsmatrix}")

        anforderungsmatrix = read_from_file(args.anforderungsmatrix).reshape(-1, anzahl)
        print("Anforderungsmatrix:\n", anforderungsmatrix)
        logger.info(f"Eingelesene Anforderungsmatrix:\n {anforderungsmatrix}")

        simulate_processes(ressourcenvektor, belegungsmatrix, anforderungsmatrix, args.noninteractive, logger)
        print(simulate_processes)
        logger.info(f"Simulation zur Überprüfung auf Deadlock gestartet: {simulate_processes}")


# Ausführung der Main, bei direkter Ausführung des Skripts
if __name__ == "__main__":
    main()