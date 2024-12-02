import os
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys

class ForexChartViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Forex Chart Viewer")
        self.root.geometry("1200x800")
        
        self.style = mpf.make_mpf_style(
            base_mpf_style='charles',
            gridstyle=':',  # Cuadrícula fina
            rc={'figure.facecolor': '#212529',
                'axes.facecolor': '#212529',
                'axes.edgecolor': '#495057',
                'axes.labelcolor': '#f8f9fa',
                'xtick.color': '#f8f9fa',
                'ytick.color': '#f8f9fa'}
        )
        self.setup_gui()
        
    def setup_gui(self):
        self.main_frame = ttkb.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files = [f for f in os.listdir('Database/entrenador') if f.endswith('.csv')]
        self.selected_file = tk.StringVar(value=self.files[0] if self.files else "")
        
        top_frame = ttkb.Frame(self.main_frame)
        top_frame.pack(side=TOP, fill=X, pady=10)
        
        ttkb.Label(top_frame, text="Seleccione un archivo:", bootstyle=INFO).pack(side=LEFT, padx=5)
        self.file_dropdown = ttkb.Combobox(top_frame, textvariable=self.selected_file, values=self.files, bootstyle=INFO)
        self.file_dropdown.pack(side=LEFT, padx=5)
        
        self.load_button = ttkb.Button(top_frame, text="Cargar Datos", bootstyle=SUCCESS, command=self.load_data)
        self.load_button.pack(side=LEFT, padx=5)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        self.fig.patch.set_facecolor('#212529')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def load_data(self):
        file_path = os.path.join('Database/entrenador', self.selected_file.get())
        df = pd.read_csv(file_path)
        
        df = df.rename(columns={
            'open': 'Open',
            'max': 'High',
            'min': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        df['date_time'] = pd.to_datetime(df['date_time'])
        df.set_index('date_time', inplace=True)
        
        self.ax1.clear()
        self.ax2.clear()
        
        # Configurar cuadrículas y escalas
        self.ax1.grid(which='major', color='#495057', linestyle='--', linewidth=0.5)
        self.ax2.grid(which='major', color='#495057', linestyle='--', linewidth=0.5)
        
        # Formatear el eje X
        self.ax1.tick_params(axis='x', rotation=45)
        self.ax2.tick_params(axis='x', rotation=45)
        
        # Dibujar el gráfico de velas
        mpf.plot(df.tail(60), 
                 type='candle', 
                 style=self.style, 
                 ax=self.ax1, 
                 volume=self.ax2, 
                 show_nontrading=False)
        
        # Ajustar la barra de escalado del eje Y automáticamente
        self.ax1.relim()
        self.ax1.autoscale_view()
        
        self.ax2.relim()
        self.ax2.autoscale_view()
        
        self.canvas.draw()

if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = ForexChartViewer(root)
    root.mainloop()
