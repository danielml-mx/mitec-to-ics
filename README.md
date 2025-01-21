# mitec-to-ics.py
Herramienta *web-scraper* para exportar tu horario como aparece en MiTec a un archivo iCal (para ser utilizado en calcurse, Google Calendar, iCloud Calendar, etc.) 

## Sobre este proyecto
Consiste en un *script* de Python que recopila la información de todas las materias actualmente inscritas en MiTec para depositarlas en un archivo .ics. Por predeterminado se utiliza el navegador Firefox con geckodriver y se exporta la información a un archivo llamado 'calendario.ics'. Estas tres variables pueden ser modificadas, y también por predeterminado el *script* intentará utilizar Chrome si no detecta a Firefox. 

Cabe destacar que este *script* necesita de intervención de usuario para ingresar las credenciales para acceder a MiTec. Una vez que el sito haya sido cargado, el navegador esperará hasta que las credenciales (usuario, contraseña y código OTP) sean ingresadas y que MiTec sea propiamiente accesado.

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
  outfile               output file, en formato ics [default: calendario.ics]

options:
  -h, --help            show this help message and exit
  --driver [gecko (default), chrome]
                        driver a utilizar
  --binary-location VALUE
                        path a un navegador (e.g. librewolf)
  --service-executable VALUE
                        path a gecko/chrome (requiere --binary-location con gecko)
```

### Ejemplos
```
python mitec-to-ics.py calendario-fj25.ics 
python mitec-to-ics.py --driver chrome calendario-fj25.ics
python mitec-to-ics.py --driver chrome --binary-location=/usr/bin/chromium calendario-fj25.ics
```
