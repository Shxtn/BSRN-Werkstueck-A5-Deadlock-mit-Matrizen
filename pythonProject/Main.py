
import numpy as np  # Importiert das NumPy-Modul, das für numerische Operationen und die Arbeit mit Arrays verwendet wird.
import random
import logging      # importiert das Modul logging, mit dem wir ein Verlaufsprotokoll über die Aktivitäten des Simulators erstellen können
import argparse     # importiert das Modul argparse, wird benötigt um die Kommandozeilenargumente der Main zu analysieren und interpretieren
from rich.prompt import Prompt, IntPrompt 
from rich.console import Console
from rich.table import Table

console = Console()

def input_Ressourcenvektor():
    #Wenn der Benutzer selbst den Ressourcenvektor eingeben will, muss gefragt werden wie viele Klassen der Benutzer haben will
    anzahl = IntPrompt.ask("Wie viele Ressourcenklassen haben sie: ")  # Fragt den Benutzer nach der Anzahl der Ressourcenklassen.
    ressourcenvektor = []  # Erstellt eine leere Liste für den Ressourcenvektor.

    # Eingabe der Menge der jeweiligen Ressourcenklassen
    for i in range(anzahl):  # Iteriert über die Anzahl der Ressourcenklassen.
        ressource = IntPrompt.ask(f"Geben sie nun die Menge der Ressourcenklasse {i+1}: ")  # Fragt nach der Menge der aktuellen Ressourcenklasse.
        ressourcenvektor.append(ressource)  # Fügt die Menge der aktuellen Ressourcenklasse zur Liste hinzu.

    return ressourcenvektor  # Gibt den Ressourcenvektor zurück.

def input_Belegungsmatrix(anzahl):
    # Abfrage wie viele Prozesse der Benutzer haben will
    prozesse = IntPrompt.ask("Geben sie die Anzahl der Prozesse an: ")  # Fragt den Benutzer nach der Anzahl der Prozesse.
    belegungsmatrix = np.zeros((prozesse, anzahl), dtype=int)  # Erstellt eine Matrix aus Nullen mit der Größe (Prozesse, anzahl).

    for i in range(prozesse):  # Iteriert über die Anzahl der Prozesse.
        prozessanzahl = i + 1  # Zählt die Prozessnummer.

        # Erstellung einer leeren Liste
        belegung = []  # Erstellt eine leere Liste für die Belegung des aktuellen Prozesses.

        # Abfrage wie viel die jeweiligen Prozesse von den oben angegebenen Ressourcenklassen benötigen
        for j in range(anzahl):  # Iteriert über die Anzahl der Ressourcenklassen.
            vektor = IntPrompt.ask(f"Geben sie an wie viele Ressourcen der Prozess {prozessanzahl} von der Ressourcenklasse {j+1}:")  # Fragt nach der benötigten Menge der aktuellen Ressourcenklasse für den aktuellen Prozess.

            # Hinzufügen des Vektors zur Liste
            belegung.append(vektor)  # Fügt die Menge der aktuellen Ressourcenklasse zur Liste hinzu.

        belegungsmatrix[i] = belegung  # Setzt die Belegung des aktuellen Prozesses in die Belegungsmatrix.
    return np.array(belegungsmatrix)  # Gibt die Belegungsmatrix als NumPy-Array zurück.

# Die Funktion dient der Eingabe der Anforderungsmatrix
def input_Anforderungsmatrix(Prozesse, anzahl):
    # Erstellt eine leere Anforderungsmatrix mit der angegebenen Anzahl von Prozessen und Ressourcenklassen, initialisiert mit Nullen
    anforderungsmatrix = np.zeros((Prozesse, anzahl), dtype=int)

    # Schleife über jeden Prozess
    for i in range(Prozesse):
        # Setzt die Prozessnummer fest (1-basierter Index)
        prozessanzahl = i + 1

        # Erstellt eine leere Liste zur Speicherung der Anforderungen für den aktuellen Prozess
        anforderung = []

        # Schleife über jede Ressourcenklasse
        for l in range(anzahl):
            # Fragt den Benutzer, wie viele Ressourcen der aktuellen Klasse der aktuelle Prozess benötigt
            vektor = IntPrompt.ask(f"Geben sie an wie viele Ressourcen der Prozess {Prozessanzahl} von der Ressourcenklasse {l + 1} benötigt:")

            # Fügt die Benutzerangabe zur Liste der Anforderungen hinzu
            anforderung.append(vektor) # Das Objekt 'Vektor' wird an das Ende der Liste 'Anforderung' angehängt
            numpy_Anforderung = np.array(anforderung)  # Konvertiert die Liste in ein NumPy-Array (wird hier aber nicht verwendet)

        # Setzt die Zeile der Anforderungsmatrix für den aktuellen Prozess auf die gesammelten Anforderungen
        anforderungsmatrix[i] = anforderung

# Gibt die ausgefüllte Anforderungsmatrix zurück
    return anforderungsmatrix

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


def simulate_processes(ressourcenvektor, belegungsmatrix, anforderungsmatrix, noninteractive, logger):
    # Eintrag in das Verlaufsprotokoll über den Start der Prozesssimulation; die folgenden "logger.info"-Zeilen der Methode
    # funktionieren analog und sollten über den entsprechenden Eintrag selbsterklärend sein. Daher werden diese nicht
    # erneut kommentiert
    logger.info("Prozesssimulation gestartet")

    # Bestimmen der Anzahl der Prozesse aus der Anforderungsmatrix
    anzahl_prozesse = anforderungsmatrix.shape[0]

    # Erstellen einer Liste, um den Abschlussstatus jedes Prozesses zu verfolgen
    finished = [False] * anzahl_prozesse

    logger.info("Abschlussstatus aller Prozesse auf \"Nicht abgeschlossen\" gesetzt")

    # Berechnen des initialen Ressourcenrestvektors
    # Dies erfolgt durch Subtrahieren der summierten Belegung von den verfügbaren Ressourcen
    ressourcenrestvektor = ressourcenvektor - np.sum(belegungsmatrix, axis=0)
    console.print(f"Initialer Ressourcenrestvektor: {ressourcenrestvektor}")

    logger.info(f"Berechnung und Ausgabe initialer Restressourcenvektor: {ressourcenrestvektor}")

    # Fortsetzung der Simulation, bis alle Prozesse abgeschlossen sind
    while not all(finished):
        # Liste der Prozesse, die ausgeführt werden können
        ausführbare_prozesse = []

        # Überprüfung jedes Prozesses, um festzustellen, ob er ausgeführt werden kann
        for i in range(anzahl_prozesse):
            # Überprüfung, ob der Prozess noch nicht abgeschlossen ist und ob seine Anforderungen erfüllbar sind
            if not finished[i] and all((anforderungsmatrix[i] <= ressourcenrestvektor)):
                # Prozess zur Liste der ausführbaren Prozesse hinzufügen
                ausführbare_prozesse.append(i)

                logger.info(f"Prüfung aller ausführbaren Prozesse, Ergebnis: {ausführbare_prozesse}")

        # Wenn keine ausführbaren Prozesse vorhanden sind, liegt ein Deadlock vor
        if not ausführbare_prozesse:
            console.print("Deadlock: Kein Prozess kann ausgeführt werden.")

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
                console.print(f"Ausführbare Prozesse: {ausführbare_prozesse}")  # Drucke die Liste der ausführbaren Prozesse
                try:  # Versuche den folgenden Block auszuführen, um potenzielle Fehler abzufangen
                    nächster_prozess = IntPrompt.ask( "Welcher Prozess soll als nächstes ausgeführt werden? ")  # Frage den Benutzer nach der nächsten Prozessnummer und konvertiere die Eingabe in einen Integer

                    logger.info(f"Auszuführender Prozess durch Benutzer gewählt: {nächster_prozess}")


                    if nächster_prozess in ausführbare_prozesse:  # Überprüfe, ob der eingegebene Prozess in der Liste der ausführbaren Prozesse ist

                        logger.info(f"Gewählter Prozess {nächster_prozess} ist ausführbar")
                        break  # Wenn ja, verlasse die Schleife
                    else:  # Wenn nein
                        console.print(f"Prozess {nächster_prozess} kann nicht ausgeführt werden. Bitte wählen Sie einen anderen Prozess.")  # Informiere den Benutzer, dass dieser Prozess nicht ausgeführt werden kann

                        logger.info(f"Gewählter Prozess {nächster_prozess} ist nicht ausführbar")

                except ValueError:  # Fange den Fehler ab, wenn die Eingabe keine gültige Zahl ist
                    console.print("Ungültige Eingabe. Bitte eine gültige Prozessnummer eingeben.")  # Informiere den Benutzer über die ungültige Eingabe

                    # Fehlermeldung im Verlaufsprotokoll über eine ungültige Nutzereingabe bei der Wahl des nächsten auszuführenden Prozesses;
                    # die folgenden "logger.error"-Zeilen der Methode funktionieren analog und sollten über den entsprechenden Eintrag
                    # selbsterklärend sein. Daher werden diese nicht erneut kommentiert
                    logger.error(f"Fehler: Eingabe {nächster_prozess} des Benutzers ist ungültig")

        # Aktualisiere den Ressourcenrestvektor mit den freigegebenen Ressourcen des ausgeführten Prozesses
        neue_ressourcenrestvektor = (ressourcenrestvektor + belegungsmatrix[nächster_prozess])

        # Überprüfen, ob negative Werte im neuen Ressourcenrestvektor vorhanden sind
        if any(neue_ressourcenrestvektor < 0):  # Wenn irgendein Wert im neuen Vektor negativ ist
            console.print(f"Fehler: Negative Werte im Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}.")  # Fehlerausgabe
            logger.error(f"Fehler: Negative Werte im Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}")
            console.print(f"Aktueller Ressourcenrestvektor: {ressourcenrestvektor}")  # Drucke den aktuellen Ressourcenrestvektor
            logger.error(f"Aktueller Ressourcenrestvektor: {ressourcenrestvektor}")
            console.print(f"Anforderungen von Prozess {nächster_prozess}: {anforderungsmatrix[nächster_prozess]}")  # Drucke die Anforderungen des Prozesses
            logger.error(f"Anforderungen von Prozess {nächster_prozess}: {anforderungsmatrix[nächster_prozess]}")
            console.print(f"Belegte Ressourcen von Prozess {nächster_prozess}: {belegungsmatrix[nächster_prozess]}")  # Drucke die belegten Ressourcen des Prozesses
            logger.error(f"Belegte Ressourcen von Prozess {nächster_prozess}: {belegungsmatrix[nächster_prozess]}")
            break  # Beende die Schleife

        console.print(f"Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}: {ressourcenrestvektor}")  # Drucke den Ressourcenrestvektor nach der Ausführung des Prozesses
        logger.info(f"Ressourcenrestvektor nach Ausführung von Prozess {nächster_prozess}: {ressourcenrestvektor}")

        # Aktualisiere den Ressourcenrestvektor
        ressourcenrestvektor = neue_ressourcenrestvektor

        # Markiere den Prozess als abgeschlossen
        finished[nächster_prozess] = True
        console.print(f"Prozess {nächster_prozess} ist abgeschlossen. Ressourcenrestvektor: {ressourcenrestvektor}")  # Informiere über den Abschluss des Prozesses und drucke den aktuellen Ressourcenrestvektor
        logger.info(f"Prozess {nächster_prozess} abgeschlossen, Ressourcenrestvektor: {ressourcenrestvektor}")

        console.print("Simulation abgeschlossen. Alle ausführbaren Prozesse wurden bearbeitet oder ein Deadlock ist aufgetreten")  # Drucke eine Abschlussmeldung der Simulation
        logger.info("Simulation abgeschlossen, alle ausführbaren Prozesse bearbeitet oder Deadlock")


# auch in der main-Methode erfolgt keine erneute Kommentierung zu "logger.info"- und "logger.error"-Zeilen
def main():
    # ArgumentParser-Obkjekt (Funktion s. Kommentar bei Import-Zeile oben) wird erstellt
    parser = argparse.ArgumentParser(description='Ressourcen- und Prozessmatrix-Eingabe')
    # Pflichtargument für Kommandozeileneingabe, die den Eingabemodus des Benutzers für den Simulator festlegt
    parser.add_argument('-mode', choices=['S','s', 'd','D'], required=True,
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
    mode = args.mode.lower()
    # überprüft, ob der mauelle Modus gewählt wurde
    if mode == 's':

        logger.info("Benutzer wählt manuelle Eingabe")

        # manuelle Eingabe und anschließende Ausgabe des Ressourcenvektors
        ressourcenvektor = input_Ressourcenvektor()
        console.print("Ressourcenvektor", ressourcenvektor)
        logger.info(f"Eingegebener Ressourcenvektor: {ressourcenvektor}")

        # Anzahl der Ressourcen wird bestimmt und in der Variablen "anzahl" gespeichert
        anzahl = len(ressourcenvektor)

        # manuelle Eingabe und anschließende Ausgabe der Belegungsmatrixx mit Übergabe der Anzahl der Ressourcen
        belegungsmatrix = input_Belegungsmatrix(anzahl)
        #KOMMENTIEREN
        table = Table(title="Belegungsmatrix")
        for col in range(belegungsmatrix.shape[1]):
            table.add_column(f"Ressourcenklasse {col + 1}", justify="right")
        for row in belegungsmatrix:
            table.add_row(*map(str, row))
        console.print(table)
        logger.info(f"Eingegebene Belegungsmatrix:\n {belegungsmatrix}")

        # Anzahl der Prozesse wird bestimmt und in der Variablen "prozesse" gespeichert
        prozesse = len(belegungsmatrix)
        logger.info(f"Prozesse: {prozesse}")

        # manuelle Eingabe und anschließende Ausgabe der Anforderungsmatrix mit Übergabe der Anzahl der Prozesse und Ressourcen
        anforderungsmatrix = input_Anforderungsmatrix(prozesse, anzahl)
        table = Table(title="Anforderungsmatrix")
        for col in range(anforderungsmatrix.shape[1]):
            table.add_column(f"Ressourcenklasse {col + 1}", justify="right")
        for row in anforderungsmatrix:
            table.add_row(*map(str, row))
        console.print(table)
        logger.info(f"Eingegebene Anforderungsmatrix:\n {anforderungsmatrix}")

        # Ausführung der "simulate_processes"-Methode mit anschließender Ausgabe des Ergebnisses
        simulate_processes(ressourcenvektor, belegungsmatrix, anforderungsmatrix, args.noninteractive, logger)
        console.print(simulate_processes)
        logger.info(f"Simulation zur Überprüfung auf Deadlock gestartet: {simulate_processes}")

    # überprüft, ob der Modus zum Einlesen von Dateien gewählt wurde
    elif mode == 'd':

        logger.info("Benutzer wählt Eingabe durch Einlesen einer Datei")

        # Überprüfung, ob die Dateinamen korrekt in die Kommandozeile eingegeben wurden und gibt Fehlermeldung aus, falls nicht
        if not (args.ressourcenvektor and args.belegungsmatrix and args.anforderungsmatrix):
            console.print(
                "Fehler: Wenn der Modus 'd' gewählt wird, müssen die Namen der Dateien für den Ressourcenvektor, die Belegungsmatrix und die Anforderungsmatrix eingegeben werden ")
            logger.error(
                "Fehler: Kein Dateiname für Einlesen des Ressourcenvektors, der Belegungsmatrix oder der Anforderungsmatrix eingegeben")
            return

        # Main-Methode durchläuft die gleichen Schritte wie im manuellen Modeus, nur dass die Daten durch das Auslesen der Dateien
        # und nicht mehr durch manuelle Eingabe eingespeist werden
        ressourcenvektor = read_from_file(args.ressourcenvektor)
        console.print("Ressourcenvektor:", ressourcenvektor)
        logger.info(f"Eingelesener Ressourcenvektor: {ressourcenvektor}")

        anzahl = len(ressourcenvektor)

        # die ".reshape"-Methode mit den übergebenen Parametern sorgt dafür, dass aus den Daten der eingelesenen Datei
        # eine zweidimensionale Matrix mit "anzahl" Spalten  und einer errechneten Anzahl von Zeilen erzeugt wird
        belegungsmatrix = read_from_file(args.belegungsmatrix).reshape(-1, anzahl)
        table = Table(title="Belegungsmatrix")
        for col in range(belegungsmatrix.shape[1]):
            table.add_column(f"Ressourcenklasse {col + 1}", justify="right")
        for row in belegungsmatrix:
            table.add_row(*map(str, row))
        console.print(table)
        logger.info(f"Eingelesene Belegungsmatrix:\n {belegungsmatrix}")

        anforderungsmatrix = read_from_file(args.anforderungsmatrix).reshape(-1, anzahl)
        table = Table(title="Anforderungsmatrix")
        for col in range(anforderungsmatrix.shape[1]):
            table.add_column(f"Ressourcenklasse {col + 1}", justify="right")
        for row in anforderungsmatrix:
            table.add_row(*map(str, row))
        console.print(table)       
        logger.info(f"Eingelesene Anforderungsmatrix:\n {anforderungsmatrix}")

        simulate_processes(ressourcenvektor, belegungsmatrix, anforderungsmatrix, args.noninteractive, logger)
        logger.info(f"Simulation zur Überprüfung auf Deadlock gestartet: {simulate_processes}")


# Ausführung der Main, bei direkter Ausführung des Skripts
if __name__ == "__main__":
    main()
