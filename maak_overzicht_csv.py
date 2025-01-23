import csv
from datetime import datetime
from datetime import timedelta
import locale

locale.setlocale(locale.LC_TIME, "nl_BE.utf8")  # Nederlandstalige dagnamen
use_user_input = False


def main():
    overschrijf_warning = input("Dit script overschrijft data_invoer.csv. Ben je zeker dat je wil doorgaan? (j)")
    if overschrijf_warning not in ("j", ""):
        exit("Script afgebroken. Je moet akkoord gaan om het bestaande CSV te overschrijven.")
    # Vraag om begindag
    start_date_input = input("Geef een begindag op (bv 1-1-2025): ")

    try:
        start_date = datetime.strptime(start_date_input, "%d-%m-%Y")
    except ValueError:
        print("Ongeldige datumindeling. Gebruik DD-MM-YYYY.")
        return

    today = datetime.now()
    included_days = []

    current_date = start_date

    while current_date <= today:
        # Controleer of de dag een weekdag is (maandag=0, zondag=6)
        if current_date.weekday() < 5:  # Weekdagen zijn 0 t/m 4
            day_name = current_date.strftime("%A")
            day_formatted = current_date.strftime("%d-%m-%Y")
            if use_user_input:
                msg = (f"{day_name} {day_formatted}. Druk op Enter of type 'd' om de volledige dag op te nemen "
                       f"als PTOW , 'n' om over te slaan: ")
                response = (input(msg) or "d".strip().lower())
                if response not in ["n", "d"]:
                    print("OPGELET! Ongeldig antwoord: " + response + ", de datum wordt niet opgenomen in de CSV")
                    response = "n"

                if response != "n":
                    included_days.append([day_name, day_formatted, response])
            else:
                included_days.append([day_name, day_formatted, "d"])

        # Ga naar de volgende dag
        current_date += timedelta(days=1)

    # Schrijf de opgenomen dagen naar een CSV-bestand
    with open("data_invoer.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(included_days)

    print("De dagen zijn opgeslagen in 'data_invoer.csv'.")


if __name__ == "__main__":
    main()
