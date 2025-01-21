# requirements: icalendar, selenium
import argparse
import icalendar
import selenium
from datetime import datetime as dt
from icalendar import Calendar, Event
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser("python calendario-mitec.py")
parser.add_argument('outfile', nargs='?', const='arg_was_not_given', help='output file, in ics format [default: calendario.ics]', default="calendario.ics")
parser.add_argument('--driver', help='driver to be used', metavar='[gecko (default), chrome]', default='gecko')
parser.add_argument('--binary-location', help='path to browser (e.g. librewolf)', metavar='VALUE', default='')
parser.add_argument('--service-executable', help='path to gecko/chrome (requires --binary-location for gecko)', metavar='VALUE', default='')
args = parser.parse_args()

def convert_abrev_dias(dias):
    final = dias
    guia = ({"Lu": "Mo", 
             "Ma": "Tu", 
             "Mi": "We", 
             "Ju": "Th",
             "Vi": "Fr",
             "Do": "Su", 
             "-": " " })

    for esp, eng in guia.items():
       final = final.replace(esp, eng)

    return final.split()

cal = Calendar()

if args.driver == "gecko":
    # Firefox/Librewolf
    try:
        options = webdriver.FirefoxOptions()
        service = webdriver.FirefoxService()
        if args.binary_location != "":
            options.binary_location = args.binary_location
        if args.service_executable != "":
            service = webdriver.FirefoxService(args.service_executable)
        driver = webdriver.Firefox(options=options, service=service)
    except selenium.common.exceptions.NoSuchDriverException:
        args.driver = "chrome"
        args.binary_location = ""
        args.service_executable = ""
        print("Failed to open gecko-based browser, trying chrome with no options...")

if args.driver == "chrome":
    # Chromium/Chrome
    options = Options()
    service = Service()
    if args.binary_location != "":
        options.binary_location = args.binary_location
    if args.service_executable != "":
        service = Service(executable_path=args.service_executable)
    driver = webdriver.Chrome(service=service, options=options)


driver.get("https://mitec.itesm.mx/")
sidebar_items = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='menu-title']")))
driver.get("https://mitec.itesm.mx/Paginas/mitec/index.aspx#/horario")

detalles_btn = WebDriverWait(
        driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "label[class='btn tab ml-3 btn-calendar']")))
detalles_btn.click()

materias = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='info-container row']"))
)

for materia in materias:
    materia.find_element(By.CSS_SELECTOR, "div[class='fecha_Inicio d-flex']")
    texto = materia.text.split("\n")
    nombre = texto[3]

    if "Proyecto solidario" in nombre:
        continue

    fecha_inicio = texto[0]
    fecha_final = texto[2]
    salon = texto[4]
    profe = texto[5]

    if "Co-Titular" in texto[6]:
        profe += "\n" + texto[6]
        dias = texto[7]
        lista_dias = convert_abrev_dias(dias)
        hora_inicial, hora_final = texto[8].replace("a", "").replace(" hrs", "").split()
    else:
        dias = texto[6]
        lista_dias = convert_abrev_dias(dias)
        hora_inicial, hora_final = texto[7].replace("a", "").replace(" hrs", "").split()

    descripcion = profe + "\n" + \
                  f"Salón: {salon}\n" + \
                  f"Horario: {hora_inicial} - {hora_final}\n" + \
                  f"Días: {dias}\n"

    ev = Event()
    ev.name = "VEVENT"
    ev.add('summary', nombre)
    ev.add('dtstart', dt.strptime(fecha_inicio + " " + hora_inicial, '%d-%m-%Y %H:%M'))
    ev.add('dtend', dt.strptime(fecha_inicio + " " + hora_final, '%d-%m-%Y %H:%M'))
    ev.add('class', 'public')
    # https://calget.com/tools/rrule-generator
    ev.add('rrule', {'freq': 'weekly', 
                 'interval': '1',
                 'until': dt.strptime(fecha_final + " " + hora_final,'%d-%m-%Y %H:%M'),
                 'byday': lista_dias })
    ev.add('location', salon)
    ev.add('description', descripcion)
    cal.add_component(ev)

driver.quit()

with open(args.outfile, "wb") as f:
    f.write(cal.to_ical())

print(f"Saved to {args.outfile}")
