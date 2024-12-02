import pandas as pd
import os

def standardize_forex_data():
    trainer_path = 'Database/entrenador'
    
    for file in os.listdir(trainer_path):
        if file.endswith('.csv'):
            file_path = os.path.join(trainer_path, file)
            df = pd.read_csv(file_path)
            
            # Eliminar columna id
            if 'id' in df.columns:
                df = df.drop('id', axis=1)
            
            # Renombrar from a date_time
            if 'from' in df.columns:
                df = df.rename(columns={'from': 'date_time'})
            
            # Guardar el archivo limpio
            df.to_csv(file_path, index=False)
            print(f"Archivo limpiado: {file}")

if __name__ == "__main__":
    print("Iniciando limpieza de datos...")
    standardize_forex_data()
    print("Limpieza completada!")