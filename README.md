# Requirements

- Python
- Linux (Andere OS is mogelijk maar hiervoor is geen onderstaande documentatie niet volledig bruikbaar.)
- Maak een venv aan waar je de python scripts zal uitvoeren. Installeer daarin de requirements uit requirements.txt
  ```sh
  python -m venv ENV_DIR/vlimpers_venv
  pip install -r requirement.txt
  ```

# Aanvragen PTOW dagen

## Maak een CSV bestand aan
Voer het script uit om een CSV bestand aan te maken met alle dagen die je als PTOW wenst in te voeren. Het script zal alle weekdagen opnemen vanaf jouw startdatum tot en met vandaag.

```sh
python maak_overzicht.py
```
- Bevestig dat je een eventueel bestaand data_invoer.csv bestand in de vlimpers repository wil overschrijven.
- Het script zal je vragen wat de eerste datum is die je wenst op te nemen en zal vervolgens alle werkdagen tot en met vandaag aanvullen.
  Je hebt nu een CSV bestand `data_invoer.csv` aangemaakt. Alle dagen kregen als opname-code "d", wat wil zeggen dat je voor de volledige dag PTOW zal aanvragen.

## Open het CSV bestand en geef nu voor elke dag op welke actie is vereist. 
Je kan PTOW aanvragen voor een volledige dag, een voormiddag, een namiddag of je kan de rij laten overslaan

- Kies "vm" of "nm" om respectievelijke voormiddag of namiddag te kiezen in plaats van een volledige dag.

- Schrap de dagen waar je geen PTOW wil voor aanvragen. Het is voldoende om de opname-code leeg te maken. Dus de waarde "d" vervangen door een lege waarde. Je kan ook de volledige rijen wissen maar dat is niet nodig.

  - Open je NMBS app. Alle Brussel-dagen kunnen daaruit worden afgeleid.
  - Verwijder de feestdagen uit die periode.
  - Verwijder je vakantiedagen uit die periode (Let op dat je in het Vlimpers overzicht niet ziet of je een volledige dag of een halve dag verlof hebt genomen.)
  - Verwijder andere niet telewerkdagen (dienstreizen, teamdag, ...)

- Je CSV bestand bevat nu enkel nog opname-codes voor de dagen waar je PTOW wil voor aanvragen. De dagen zonder opname-codes zullen worden genegeerd.

## Open een browser op een specifieke poort die Selenium later kan aanspreken
- Start een Google venster op een poort die we vanuit Selenium kunnen bevragen
  ```sh
  which google-chrome-stable
  /usr/bin/google-chrome-stable --remote-debugging-port=9222 --user-data-dir=".config/google-chrome/Default" "https://vlimpers.vlaanderen.be/"
  ```

- Meld je aan
- Ga naar formulier om verlof aan te vragen zodat "Soort verlof", "Naam afwezigheid" en de knop "Indienen" zichtbaar zijn.
- Sluit de andere tabbladen. Enkel het tabblad met het formulier mag open blijven staan.

## Just sit back, relax and enjoy the party
```sh
python aanvragen_ptow.py
```
Dit script zal alle datums met een opname-code behandelen die in de CSV zijn opgenomen.
