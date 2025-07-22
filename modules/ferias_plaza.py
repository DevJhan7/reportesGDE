import pandas as pd
from pathlib import Path

MESES = [
    'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
    'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'
]

def cargar_datos_ferias_plaza(anio):
    archivo = Path(__file__).parent.parent / "data" / "ferias" / f"{anio}_ferias_manchay.csv"
    if not archivo.exists():
        return pd.DataFrame()

    df = pd.read_csv(archivo, sep=';', encoding='utf-8')
    registros = []

    for _, fila in df.iterrows():
        macro = str(fila.get('GIRO', 'OTROS')).strip().upper()
        for mes in MESES:
            monto = fila.get(mes)
            if pd.notna(monto):
                try:
                    monto = float(str(monto).replace(',', '.'))
                except:
                    continue
                fecha = pd.to_datetime(f"01-{mes}-{anio}", format="%d-%B-%Y", dayfirst=True, errors='coerce')
                registros.append({
                    'FERIA': f"Plaza Cívica {anio}",
                    'MACRO_CATEGORIA': macro,
                    'MONTO': monto,
                    'INGRESO': fecha
                })

    return pd.DataFrame(registros)
