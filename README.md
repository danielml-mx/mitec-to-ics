# mitec-to-ics.py
Herramienta *web-scraper* para exportar tu horario como aparece en MiTec a un archivo iCal (para ser utilizado en calcurse, Google Calendar, iCloud Calendar, etc.) 

![image](https://github.com/user-attachments/assets/38ee6965-3c64-4a51-a160-477215ecd11b)

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
                              [--preguntar-por-periodo]
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
  --preguntar-por-periodo
                        pregunta por periodo a exportar en lugar de exportar el más reciente
```

### Ejemplos
```
python mitec-to-ics.py calendario-fj25.ics 
python mitec-to-ics.py --driver chrome calendario-fj25.ics
python mitec-to-ics.py --driver chrome --binary-location=/usr/bin/chromium calendario-fj25.ics
```

## Fun fact
Además, puedes añadir tu calendario de Canvas a tu calendario personal. Ve al calendario y a la derecha debe aparecer 'Calendar Feed'. Descarga el archivo o bien usa la liga e impórtalo en tu cliente de calendario preferido.
