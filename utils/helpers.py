from datetime import datetime

def format_date(date_str):
    """Formatea fechas en español"""
    months = {
        1: "Enero", 2: "Febrero", 3: "Marzo",
        4: "Abril", 5: "Mayo", 6: "Junio",
        # ... completar meses
    }
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    return f"{date_obj.day} de {months[date_obj.month]} de {date_obj.year}"