import csv
import logging
from datetime import datetime
from time import sleep

from datatest import validate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

LOG = logging.getLogger(__name__)
ptow_data = list()
ptow_dagen = list()

chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(chrome_options)
driver.maximize_window()


def strftime_format(format):
    def func(value):
        try:
            datetime.strptime(value, format)
        except ValueError:
            return False
        return True

    func.__doc__ = f'should use date format {format}'
    return func


def vraag_ptow_aan(f_datum, f_opname):
    try:
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        # Wait for the element to be present and clickable
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Afwezigheid aanvragen']"))
        )
        # Click the element
        element.click()
        sleep(2)  # geef tijd om extra velden te laden

        LOG.info(f"Vraag Ptow aan op {f_datum} ({f_opname}")

        naam_afwezigheid = Select(driver.find_element(By.ID, "DERIVED_ABS_SS_PIN_TAKE_NUM"))  # Dropdown
        naam_afwezigheid.select_by_visible_text("Telewerken - PTOW")
        sleep(2)  # geef tijd om extra velden te laden

        periode_text = {
            "d": "Volledige dag",
            "nm": "Namiddag",
            "vm": "Voormiddag"
        }
        periode = Select(driver.find_element(By.ID, "DERIVED_ABS_SS_VO_DURATION"))
        periode.select_by_visible_text(periode_text[f_opname])

        if f_opname != 'd':
            sleep(1)  # nodig indien duration wordt aangepast

        begindatum = driver.find_element(By.ID, "DERIVED_ABS_SS_BGN_DT")
        begindatum.clear()
        begindatum.send_keys(f_datum)
        einddatum = driver.find_element(By.ID, "DERIVED_ABS_SS_END_DT")
        einddatum.clear()
        einddatum.send_keys(f_datum)

        driver.find_element(By.ID, 'DERIVED_ABS_SS_SUBMIT_BTN').click()  # Indienen

        sleep(2)  # Geef het iframe waarin om bevestiging wordt gevraagd tijd om te laden
        # Wacht tot het iframe beschikbaar is
        # iframe = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//iframe[starts-with(@id, 'ptModFrame_')]")))  # werkt niet
        iframe = driver.find_element(By.TAG_NAME, 'iframe')
        # Schakel over naar het iframe
        driver.switch_to.frame(iframe)

        # Wait for the element to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'DERIVED_ABS_SS_YES'))
        )
        # Click the element
        element.click()

        # Schakel terug naar de hoofdinhoud
        driver.switch_to.default_content()
        sleep(2)
        LOG.info(f"PTOW succesvol aangevraagd op {f_datum} ({f_opname}")

    except Exception as e:
        LOG.exception(e)


with open('data_invoer.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        dagnaam = row[0]  # maandag tot vrijdag. Informatief, functioneel niet nodig
        datum = row[1]  # formaat "%d-%m-%Y"
        opname = row[2]  # d: volledige dag. vm voormiddag, nm namiddag

        if not opname:  # rijen zonder opname-code slaan we over.
            continue
        if opname in ["d", "vm", "nm"]:
            ptow_data.append((dagnaam, datum, opname))
            ptow_dagen.append(datum)
        else:
            LOG.error(f"Ongekende opname-code '{opname}' voor {datum}. Deze rij zal niet worden behandeld.")
            continue

    # valideer dagen. Indien er ongeldige datum(s) aanwezig zijn in de CSV wordt het script afgebroken
    validate(ptow_dagen, strftime_format("%d-%m-%Y"))

    for tnaam, tdatum, topname in ptow_data:
        vraag_ptow_aan(tdatum, topname)
