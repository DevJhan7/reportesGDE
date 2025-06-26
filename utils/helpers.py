from datetime import datetime

SPANISH_MONTHS = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def get_spanish_month(month_number):
    """Devuelve el nombre del mes en español"""
    return SPANISH_MONTHS.get(month_number, "Mes inválido")

def format_date(date_str):
    """Formatea fecha a texto en español"""
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return f"{date_obj.day} de {SPANISH_MONTHS[date_obj.month]} de {date_obj.year}"
    except:
        return date_str
