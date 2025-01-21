# mitec-to-ics.py
Herramienta web-scraper para exportar tu horario como aparece en MiTec a un archivo iCal (para ser utilizado en calcurse, Google Calendar, iCloud Calendar, etc.) 

## Sobre este proyecto
Consiste en un script de Python que recopila la información de todas las materias actualmente inscritas en MiTec para depositarlas en un archivo .ics. Por predeterminado, utiliza el navegador Firefox con geckodriver para viajar a MiTec y lo guarda en un archivo llamado 'calendario.ics'. Estas tres variables pueden ser modificadas, y también por predeterminado el script intentará utilizar Chrome si no detecta a Firefox. 

Cabe destacar que este script necesita intervención de usuario para ingresar las credenciales para aceder a MiTec. Una vez que el sito haya sido cargado, el navegador esperará hasta que las credenciales (usuario, contraseña y código OTP) sean ingresadas y que MiTec sea propiamiente accesado.

## Instalación
```
git clone https://github.com/danielml-mx/mitec-to-ics.git
cd mitec-to-ics/
pip install -r requirements.txt # o en Arch, yay -S python-selenium python-icalendar
```

## Uso
```
usage: python mitec-to-ics.py [-h] [--driver [gecko (default), chrome]] [--binary-location VALUE] [--service-executable VALUE]
                                  [outfile]

positional arguments:
  outfile               output file, in ics format [default: calendario.ics]

options:
  -h, --help            show this help message and exit
  --driver [gecko (default), chrome]
                        driver to be used
  --binary-location VALUE
                        path to browser (e.g. librewolf)
  --service-executable VALUE
                        path to gecko/chrome (requires --binary-location for gecko)
```

### Ejemplo
```
python mitec-to-ics.py calendario-fj25.ics 
python mitec-to-ics.py --driver chrome calendario-fj25.ics
python mitec-to-ics.py --driver chrome --binary-location=/usr/bin/brave calendario-fj25.ics
```
