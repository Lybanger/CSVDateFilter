from datetime import datetime, timedelta
import pandas as pd
import re


def filtro_rango_fecha(pat, dias_a_filtrar):
    # Generar fecha y hora actual
    fecha_actual = datetime.now()

    # Calcular la fecha del día anterior
    fecha_filtrar_desde = fecha_actual - timedelta(days=dias_a_filtrar)

    # Formatear la fecha de inicio del rango
    fecha_inicio_str = fecha_filtrar_desde.strftime("%b %d, %Y")

    # Leer el archivo CSV
    df = pd.read_csv(pat)

    # Filtrar filas dentro del rango de fechas
    filtro = df[''] >= fecha_inicio_str
    df = df[filtro]

    # Guardar el DataFrame resultante en el mismo archivo CSV
    df.to_csv(pat, index=False, encoding='utf-8-sig')


def filtro_dia_anterior(pat):
    # Generar fecha y hora actual
    fecha_actual = datetime.now()

    fecha_ayer = fecha_actual - timedelta(days=1)

    dia = fecha_ayer.day

    if dia < 10:
        dia = f"0{dia}"
    dia = str(dia)

    if fecha_ayer.month == 1:
        mes = "Jan"
    elif fecha_ayer.month == 2:
        mes = "Feb"
    elif fecha_ayer.month == 3:
        mes = "Mar"
    elif fecha_ayer.month == 4:
        mes = "Apr"
    elif fecha_ayer.month == 5:
        mes = "May"
    elif fecha_ayer.month == 6:
        mes = "Jun"
    elif fecha_ayer.month == 7:
        mes = "Jul"
    elif fecha_ayer.month == 8:
        mes = "Aug"
    elif fecha_ayer.month == 9:
        mes = "Sep"
    elif fecha_ayer.month == 10:
        mes = "Oct"
    elif fecha_ayer.month == 11:
        mes = "Nov"
    else:
        mes = "Dec"
    print(f"{mes} {dia}, {fecha_ayer.year}")
    fil = str(mes) + " " + str(dia) + ", " + str(fecha_ayer.year)
    # filtrado de días para su elimination alv
    df = pd.read_csv(pat)
    filtro = df['Date'].str.contains(fil)
    df = df[~filtro]
    df.to_csv(pat, index=False, encoding='utf-8-sig')


def filtro_fecha(pat):
    df = pd.read_csv(pat)

    df['fecha_hora'] = pd.to_datetime(df['Date'])

    # Extraer la fecha y la hora en columnas separadas
    df['Fecha'] = df['fecha_hora'].dt.date
    df['Hora'] = df['fecha_hora'].dt.time

    def hr_fecha(row):
        fecha = row["Fecha"]
        hora = row["Hora"]
        if pd.isna(fecha) and pd.isna(hora):
            return ""
        return str(fecha) + ',' + str(hora)

    df["fecha_hora"] = df.apply(hr_fecha, axis=1)

    gg = {
        "-": ",",
        ":": ","
    }
    pattern = "|".join(gg.keys())

    def apply_re_sub(x):
        if pd.notnull(x):
            return re.sub(pattern, lambda m: gg[m.group(0)], x)
        else:
            return x

    df["fecha_hora"] = df["fecha_hora"].apply(apply_re_sub)

    def formula(fecha):
        try:
            if pd.notnull(fecha):
                d = int(fecha[8:10])
                m = int(fecha[5:7])
                y = int(fecha[0:4])
                h = int(fecha[11:13])
                mm = int(fecha[14:16])
                s = int(fecha[17:19])

                # return str(left) + "." + str(concat)
                fecha_objeto = datetime(y, m, d, h, mm, s)

                # Calcular el número de serie de la fecha
                fecha_base = datetime(1900, 1, 1, 0, 0, 0)
                diferencia = fecha_objeto - fecha_base
                dias_extra = diferencia.days + 2

                # Extraer los valores de horas y minutos
                valor2 = fecha_objeto.hour
                valor3 = fecha_objeto.minute
                valor4 = fecha_objeto.second

                # Sumar los valores numéricos obtenidos
                resultado1 = valor2 / 24 + valor3 / 1440 + valor4 / 86400
                resultado1 = resultado1 % 1
                resultado1 = str(resultado1)
                resultado = str(dias_extra) + "." + str(resultado1[2:])
                return resultado
            else:
                return fecha
        except ValueError:
            print("")

    df["Date"] = df["fecha_hora"].apply(formula)

    columnas_a_borrar = ['fecha_hora', 'Fecha', 'Hora']
    df.drop(columnas_a_borrar, axis=1, inplace=True)

    # Guardar el archivo con la nueva columna
    df.to_csv(pat, index=False, encoding='utf-8-sig')


def filtro_fecha2(pat):
    df = pd.read_csv(pat)

    df['fecha_hora'] = pd.to_datetime(df['Date'])

    # Extraer la fecha y la hora en columnas separadas
    df['Fecha'] = df['fecha_hora'].dt.date
    df['Hora'] = df['fecha_hora'].dt.time

    def hr_fecha(row):
        fecha = row["Fecha"]
        hora = row["Hora"]
        if pd.isna(fecha) and pd.isna(hora):
            return ""
        return str(fecha) + ',' + str(hora)

    df["fecha_hora"] = df.apply(hr_fecha, axis=1)

    gg = {
        "-": ",",
        ":": ","
    }
    pattern = "|".join(gg.keys())

    def apply_re_sub(x):
        if pd.notnull(x):
            return re.sub(pattern, lambda m: gg[m.group(0)], x)
        else:
            return x

    df["fecha_hora"] = df["fecha_hora"].apply(apply_re_sub)

    def formula(fecha):
        try:
            if pd.notnull(fecha):
                d = int(fecha[8:10])
                m = int(fecha[5:7])
                y = int(fecha[0:4])
                h = int(fecha[11:13])
                mm = int(fecha[14:16])
                s = int(fecha[17:19])

                # return str(left) + "." + str(concat)
                fecha = datetime(y, m, d, h, mm, s)
                fecha_objeto = fecha + timedelta(hours=6)

                # Calcular el número de serie de la fecha
                fecha_base = datetime(1900, 1, 1, 0, 0, 0)
                diferencia = fecha_objeto - fecha_base
                dias_extra = diferencia.days + 2

                # Extraer los valores de horas y minutos
                valor2 = fecha_objeto.hour
                valor3 = fecha_objeto.minute
                valor4 = fecha_objeto.second

                # Sumar los valores numéricos obtenidos
                resultado1 = valor2 / 24 + valor3 / 1440 + valor4 / 86400
                resultado1 = resultado1 % 1
                resultado1 = str(resultado1)
                resultado = str(dias_extra) + "." + str(resultado1[2:])
                return resultado
            else:
                return fecha
        except ValueError:
            print("")

    df["Date (UTC)"] = df["fecha_hora"].apply(formula)

    columnas_a_borrar = ['fecha_hora', 'Fecha', 'Hora']
    df.drop(columnas_a_borrar, axis=1, inplace=True)

    # Guardar el archivo con la nueva columna
    df.to_csv(pat, index=False, encoding='utf-8-sig')
