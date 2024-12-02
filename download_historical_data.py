from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import pandas as pd
import time
import os

def get_historical_data(iq, instrument, interval, start_date, end_date):
    data = []
    current_timestamp = end_date
    last_timestamp = None
    
    print(f"\nDescargando datos para {instrument}")
    print(f"Desde: {start_date}")
    print(f"Hasta: {end_date}")
    
    while current_timestamp > start_date:
        candles = iq.get_candles(instrument, interval, 1000, int(current_timestamp.timestamp()))
        
        if not candles or (last_timestamp and last_timestamp == candles[0]['from']):
            break
            
        data.extend(candles)
        last_timestamp = candles[0]['from']
        current_timestamp = datetime.fromtimestamp(last_timestamp)
        print(f"Procesando... Fecha actual: {current_timestamp}")
        time.sleep(1)
    
    df = pd.DataFrame(data)
    df['from'] = pd.to_datetime(df['from'], unit='s')
    df = df.drop_duplicates(subset=['from'])
    df = df.sort_values('from')
    
    mask = (df['from'] >= start_date) & (df['from'] <= end_date)
    df = df.loc[mask]
    
    return df

# El resto del código permanece igual...


def download_all_instruments():
    EMAIL = "jeronimo.trade2023@gmail.com"
    PASSWORD = "5452589"
    
    forex_instruments = [
        'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD',
        'USDCAD', 'NZDUSD', 'USDCHF', 'EURGBP',
        'EURJPY', 'GBPJPY', 'AUDJPY', 'USDMXN'
    ]
    
    iq = IQ_Option(EMAIL, PASSWORD)
    check, reason = iq.connect()
    
    if check:
        print("¡Conexión exitosa!")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        for instrument in forex_instruments:
            try:
                # Obtener datos en velas de 30 segundos
                historical_data = get_historical_data(iq, instrument, 30, start_date, end_date)
                
                # Crear nombre de archivo con timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{instrument}_{timestamp}.csv"
                filepath = os.path.join('Database', 'forex', instrument, filename)
                
                # Guardar datos
                historical_data.to_csv(filepath, index=False)
                print(f"\nDatos guardados en {filepath}")
                print(f"Total de velas para {instrument}: {len(historical_data)}")
                
            except Exception as e:
                print(f"Error al procesar {instrument}: {str(e)}")
                continue
            
    else:
        print(f"Error de conexión: {reason}")

if __name__ == "__main__":
    download_all_instruments()
    print("\n¡Descarga completa!")
