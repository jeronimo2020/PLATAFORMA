import os
import re

def analyze_checkpoints():
    checkpoint_path = 'Database/checkpoints_mihijo'
    checkpoints = os.listdir(checkpoint_path)
    
    # Extraer valores de loss de los nombres de archivo
    losses = []
    for checkpoint in checkpoints:
        match = re.search(r'val_loss_(\d+\.\d+)', checkpoint)
        if match:
            losses.append(float(match.group(1)))
    
    if losses:
        initial_loss = max(losses)
        final_loss = min(losses)
        improvement = ((initial_loss - final_loss) / initial_loss) * 100
        
        print(f"Análisis de Aprendizaje:")
        print(f"Loss inicial: {initial_loss:.4f}")
        print(f"Mejor loss: {final_loss:.4f}")
        print(f"Mejora total: {improvement:.2f}%")
        print(f"Total checkpoints: {len(losses)}")

if __name__ == "__main__":
    analyze_checkpoints()
