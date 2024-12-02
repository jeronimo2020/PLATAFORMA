from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import time
import pandas as pd

def get_historical_data(iq, instrument, interval, start_date, end_date):
    data = []
    
    # Convertir timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    # Obtener velas (candles)
    candles = iq.get_candles(instrument, interval, 1000, end_timestamp)
    
    # Convertir a DataFrame
    df = pd.DataFrame(candles)
    df['from'] = pd.to_datetime(df['from'], unit='s')
    
    return df

# Conexión
iq = IQ_Option("jeronimo.trade2023@gmail.com", "5452589")
iq.connect()

# Configurar fechas
end_date = datetime.now()
start_date = end_date - timedelta(days=180)  # 6 meses atrás

# Ejemplo para EURUSD con velas de 1 minuto
instrument = "EURUSD"
interval = 60  # 60 segundos = 1 minuto

historical_data = get_historical_data(iq, instrument, interval, start_date, end_date)
print(historical_data)
