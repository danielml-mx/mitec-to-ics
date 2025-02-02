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

parser = argparse.ArgumentParser("python mitec-to-ics.py")
parser.add_argument('outfile', nargs='?', const='arg_was_not_given', help='output file, en formato ics [default: calendario.ics]', default="calendario.ics")
parser.add_argument('--driver', help='driver a utilizar', metavar='[gecko (default), chrome]', default='gecko')
parser.add_argument('--binary-location', help='path a un navegador (e.g. librewolf)', metavar='VALUE', default='')
parser.add_argument('--service-executable', help='path a gecko/chrome (requiere --binary-location con gecko)', metavar='VALUE', default='')
parser.add_argument('--preguntar-por-periodo', help='pregunta por periodo a exportar en lugar de exportar el más reciente', action='store_true')
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
        print("Inicializando gecko...")
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
        print("No se pudo abrir un navegador basado en gecko, intentando chrome sin opciones...")

if args.driver == "chrome":
    # Chromium/Chrome
    print("Inicializando chrome...")
    options = Options()
    service = Service()
    if args.binary_location != "":
        options.binary_location = args.binary_location
    if args.service_executable != "":
        service = Service(executable_path=args.service_executable)
    driver = webdriver.Chrome(service=service, options=options)


#driver.fullscreen()
driver.get("https://mitec.itesm.mx/")
print("Esperando a que se inicie sesión...")
sidebar_items = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='menu-title']")))
print("Listo.")
driver.get("https://mitec.itesm.mx/Paginas/mitec/index.aspx#/horario")


periodos_menu = WebDriverWait(
        driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[class='dropdown-toggle btn btn-color']")))
periodos_menu.click()

periodos = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[id='arrow']"))
)

if args.preguntar_por_periodo:
    index_periodo = 1
    print("\nSelecciona el periodo a exportar:")
    for periodo in periodos:
        print(f"{index_periodo}) {periodo.text}")
        index_periodo += 1
    index_periodo = int(input()) - 1
else:
    index_periodo = 0

periodos[index_periodo].click()


detalles_btn = WebDriverWait(
        driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "label[class='btn tab ml-3 btn-calendar']")))
detalles_btn.click()

driver.fullscreen_window()
materias = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='info-container row']"))
)

# Todo esto fue experimentación para evitar tener que
# maximizar el navegador (no toda la información
# de las materias está disponible si no es así).
# Lo dejo porque lo podría retomar en el futuro.

#ver_mas_btns = driver.find_elements(By.CSS_SELECTOR, "div[class='see-More animated fadeIn']")
#ver_mas_btns = WebDriverWait(driver, 1000000).until(EC.elements_to_be_clickable((By.CSS_SELECTOR, "div[class='see-More animated fadeIn']"))).click()
#ver_mas_btns = WebDriverWait(driver, 10).until(
#    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class='see-More animated fadeIn']"))
#)
#
#scroll = 500
#for btn in ver_mas_btns:
#    try:
#        btn.click()
#    except:
#        scroll += 500
#        driver.execute_script(f"window.scrollTo(0, {scroll})")
#        btn.click()


for materia in materias:
    materia.find_element(By.CSS_SELECTOR, "div[class='fecha_Inicio d-flex']")
    texto = materia.text.split("\n")
    nombre = texto[3]

    if "Proyecto solidario" in nombre:
        continue

    print(texto)
    fecha_inicio = texto[0]
    fecha_final = texto[2]
    profe = texto[5]

    if "Co-Titular" in texto[6]:
        profe += "\n" + texto[6]
        dias = texto[7]
        lista_dias = convert_abrev_dias(dias)
        hora_inicial, hora_final = texto[8].replace("a", "").replace(" hrs", "").split()
        salon = (texto[9] + " " + texto[10]).replace("Edificio", "").replace("Salón", "")
    else:
        dias = texto[6]
        lista_dias = convert_abrev_dias(dias)
        hora_inicial, hora_final = texto[7].replace("a", "").replace(" hrs", "").split()
        salon = (texto[8] + " " + texto[9]).replace("Edificio", "").replace("Salón", "")

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

    if "Mo" not in lista_dias:
        ev.add('exdate', dt.strptime(fecha_inicio + " " + hora_inicial, '%d-%m-%Y %H:%M'))

    cal.add_component(ev)

driver.quit()

with open(args.outfile, "wb") as f:
    f.write(cal.to_ical())

print(f"Saved to {args.outfile}")
