import os

def create_database_structure():
    # Lista de instrumentos forex
    forex_instruments = [
        'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD',
        'USDCAD', 'NZDUSD', 'USDCHF', 'EURGBP',
        'EURJPY', 'GBPJPY', 'AUDJPY', 'USDMXN'
    ]
    
    # Crear directorio principal
    base_path = 'Database'
    os.makedirs(base_path, exist_ok=True)
    
    # Crear directorio forex
    forex_path = os.path.join(base_path, 'forex')
    os.makedirs(forex_path, exist_ok=True)
    
    # Crear directorios para cada instrumento
    for instrument in forex_instruments:
        instrument_path = os.path.join(forex_path, instrument)
        os.makedirs(instrument_path, exist_ok=True)
        print(f"Creado directorio para: {instrument}")

if __name__ == "__main__":
    create_database_structure()
    print("\n¡Estructura de directorios creada exitosamente!")
