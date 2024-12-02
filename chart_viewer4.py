import os
import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser
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
        
        # Estilo inicial
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
        self.chart_bg_color = '#212529'
        self.font_size = 10
        self.y_interval = 5
        self.volume_position = 'below'  # Opciones: 'below', 'inline', 'hidden'
        
        self.setup_gui()
        
    def setup_gui(self):
        # Barra de menú
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        config_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Configuraciones", menu=config_menu)
        config_menu.add_command(label="Cambiar color de fondo", command=self.change_bg_color)
        config_menu.add_command(label="Ajustar posiciones y fuentes", command=self.configure_positions_fonts)
        config_menu.add_separator()
        config_menu.add_command(label="Salir", command=self.on_closing)
        
        # Marco principal
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
        
        # Gráficos
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.update_chart_styles()
        
    def update_chart_styles(self):
        self.fig.patch.set_facecolor(self.chart_bg_color)
        self.ax1.set_facecolor(self.chart_bg_color)
        self.ax2.set_facecolor(self.chart_bg_color)
        
        self.ax1.yaxis.tick_right()  # Valores del eje Y dentro del gráfico
        self.ax1.tick_params(axis='y', labelsize=self.font_size, pad=-45)  # Tamaño y posición de las etiquetas
        self.ax1.set_yticks(self.ax1.get_yticks()[::self.y_interval])  # Ajustar intervalos del eje Y
        
        self.ax1.grid(which='major', color='#495057', linestyle='--', linewidth=0.5)
        self.ax2.grid(which='major', color='#495057', linestyle='--', linewidth=0.5)
        
        if self.volume_position == 'hidden':
            self.ax2.set_visible(False)
        elif self.volume_position == 'inline':
            self.ax2.set_position(self.ax1.get_position())
        else:  # 'below'
            pass  # No necesita ajustes, ya es por defecto debajo

    def configure_positions_fonts(self):
        # Cambiar tamaño de la fuente
        new_font_size = simpledialog.askinteger("Tamaño de Fuente", "Ingrese tamaño de la fuente:", initialvalue=self.font_size)
        if new_font_size:
            self.font_size = new_font_size
        
        # Cambiar intervalos del eje Y
        new_interval = simpledialog.askinteger("Intervalo del Eje Y", "Ingrese el intervalo de las marcas:", initialvalue=self.y_interval)
        if new_interval:
            self.y_interval = new_interval
        
        # Cambiar posición del volumen
        volume_position = simpledialog.askstring("Posición del Volumen", "Ingrese posición (below/inline/hidden):", initialvalue=self.volume_position)
        if volume_position in ['below', 'inline', 'hidden']:
            self.volume_position = volume_position
        
        self.update_chart_styles()
        self.canvas.draw()
    
    def change_bg_color(self):
        color_code = colorchooser.askcolor(title="Seleccionar color de fondo")[1]
        if color_code:
            self.chart_bg_color = color_code
            self.update_chart_styles()
            self.canvas.draw()
        
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
        
        mpf.plot(df.tail(60), 
                 type='candle', 
                 style=self.style, 
                 ax=self.ax1, 
                 volume=self.ax2, 
                 show_nontrading=False)
        
        self.update_chart_styles()
        self.canvas.draw()
        
    def on_closing(self):
        plt.close('all')
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = ttkb.Window(themename="darkly")
    app = ForexChartViewer(root)
    root.mainloop()
