import pandas as pd
import os

def clean_trainer_files():
    # Ruta de la carpeta entrenador
    trainer_path = 'Database/entrenador'
    
    # Procesar archivos en carpeta entrenador
    for file in os.listdir(trainer_path):
        if file.endswith('.csv'):
            file_path = os.path.join(trainer_path, file)
            df = pd.read_csv(file_path)
            df = df.drop(['at', 'to'], axis=1)
            df.to_csv(file_path, index=False)
            print(f"Limpiado: {file_path}")

if __name__ == "__main__":
    print("Iniciando limpieza de columnas en carpeta entrenador...")
    clean_trainer_files()
    print("\n¡Proceso de limpieza completado!")
