import os
import shutil
from datetime import datetime

def copy_files_to_trainer():
    # Crear carpeta entrenador si no existe
    trainer_path = 'Database/entrenador'
    os.makedirs(trainer_path, exist_ok=True)
    
    # Ruta base de los archivos forex
    forex_path = 'Database/forex'
    
    # Obtener timestamp actual para el nombre de la copia
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Recorrer cada carpeta de instrumento
    for instrument in os.listdir(forex_path):
        instrument_path = os.path.join(forex_path, instrument)
        if os.path.isdir(instrument_path):
            # Buscar archivos CSV en la carpeta del instrumento
            for file in os.listdir(instrument_path):
                if file.endswith('.csv'):
                    # Crear nombre para la copia
                    source_file = os.path.join(instrument_path, file)
                    dest_file = os.path.join(trainer_path, f"{instrument}_{timestamp}.csv")
                    
                    # Copiar archivo
                    shutil.copy2(source_file, dest_file)
                    print(f"Copiado: {file} -> {dest_file}")

if __name__ == "__main__":
    print("Iniciando copia de archivos...")
    copy_files_to_trainer()
    print("\n¡Proceso de copia completado!")
