from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import pandas as pd
import time

def get_complete_historical_data(iq, instrument, interval, start_date, end_date):
    data = []
    current_timestamp = end_date
    
    print(f"Iniciando descarga de datos para {instrument}")
    print(f"Desde: {start_date}")
    print(f"Hasta: {end_date}")
    
    while current_timestamp > start_date:
        candles = iq.get_candles(instrument, interval, 1000, int(current_timestamp.timestamp()))
        
        if not candles:
            break
            
        data.extend(candles)
        current_timestamp = datetime.fromtimestamp(candles[0]['from'])
        print(f"Descargando datos... Fecha actual: {current_timestamp}")
        time.sleep(0.5)
    
    df = pd.DataFrame(data)
    df['from'] = pd.to_datetime(df['from'], unit='s')
    df = df.drop_duplicates(subset=['from'])
    df = df.sort_values('from')
    
    mask = (df['from'] >= start_date) & (df['from'] <= end_date)
    df = df.loc[mask]
    
    return df

EMAIL = "jeronimo.trade2023@gmail.com"
PASSWORD = "5452589"

iq = IQ_Option(EMAIL, PASSWORD)
check, reason = iq.connect()

if check:
    print("Conexión exitosa!")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    instrument = "EURUSD"
    interval = 60
    
    historical_data = get_complete_historical_data(iq, instrument, interval, start_date, end_date)
    print(f"\nTotal de velas obtenidas: {len(historical_data)}")
    
    # Guardar los datos en un CSV
    csv_filename = f"{instrument}_historical_data.csv"
    historical_data.to_csv(csv_filename, index=False)
    print(f"\nDatos guardados en {csv_filename}")
else:
    print(f"Error de conexión: {reason}")
