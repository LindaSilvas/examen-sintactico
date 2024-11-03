from flask import Flask, render_template, request
import re
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def validar_curp():
    mensaje_sintactico = ""
    tabla_lexico = []
    token_count = {"Letras": 0, "Números": 0, "Otros": 0}
    curp = ""  # Inicializa la variable curp

    if request.method == "POST":
        curp = request.form["curp"].strip().upper()

        # Validación de formato general de CURP usando una expresión regular
        regex_curp = r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$"
        
        if len(curp) != 18:
            mensaje_sintactico = "Error: La CURP debe contener exactamente 18 caracteres."
        elif not re.match(regex_curp, curp):
            mensaje_sintactico = "Error: El formato de la CURP es incorrecto."
        else:
            # Desglose de la CURP en campos específicos para el análisis léxico
            tabla_lexico = [
                ("Apellido Paterno", curp[0:2]),
                ("Apellido Materno", curp[2]),
                ("Inicial del Nombre", curp[3]),
                ("Año de Nacimiento", curp[4:6]),
                ("Mes de Nacimiento", curp[6:8]),
                ("Día de Nacimiento", curp[8:10]),
                ("Género", curp[10]),  # Solo H o M
                ("Entidad de Nacimiento", curp[11:13]),
                ("Consonante Primer Apellido", curp[13]),
                ("Consonante Segundo Apellido", curp[14]),
                ("Consonante Primer Nombre", curp[15]),
                ("Renapo", curp[16:18])
            ]

            # Validación de fecha de nacimiento en CURP (día, mes y año)
            try:
                year = int(curp[4:6])
                month = int(curp[6:8])
                day = int(curp[8:10])
                full_year = 2000 + year if year <= datetime.now().year % 100 else 1900 + year

                # Chequear si el año es bisiesto
                is_leap_year = (full_year % 4 == 0 and (full_year % 100 != 0 or full_year % 400 == 0))
                days_in_month = {
                    1: 31, 2: 29 if is_leap_year else 28, 3: 31, 4: 30, 5: 31,
                    6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
                }

                if month < 1 or month > 12 or day < 1 or day > days_in_month[month]:
                    mensaje_sintactico = "Error: La CURP contiene una fecha inválida o coincide solo en años bisiestos."
                else:
                    mensaje_sintactico = "CURP Valida."

            except ValueError:
                mensaje_sintactico = "Error: La fecha de nacimiento en la CURP no es válida."

            # Contar tipos de tokens
            token_count["Letras"] = len(re.findall(r"[A-Z]", curp))
            token_count["Números"] = len(re.findall(r"[0-9]", curp))
            token_count["Otros"] = len(re.findall(r"[^A-Z0-9]", curp))

    return render_template("index.html",
                           mensaje_sintactico=mensaje_sintactico,
                           tabla_lexico=tabla_lexico,
                           token_count=token_count,
                           curp=curp)

if __name__ == "__main__":
    app.run(debug=True)
