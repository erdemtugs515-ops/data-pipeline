import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PriceChart:
    def __init__(self, root):
        self.root = root
        self.root.title("NY Housing Chart")

        self.data = None

        tk.Button(root, text="Load CSV", command=self.load_csv).pack()
        tk.Button(root, text="Show Charts", command=self.show_charts).pack()
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.data.columns = self.data.columns.str.strip().str.lower()
            self.data = self.data[['price', 'latitude', 'longitude']].dropna()
            print("Loaded:", self.data.shape)
    def show_charts(self):
        if self.data is None:
            return

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        prices = self.data['price'].to_numpy()
        lat = self.data['latitude'].to_numpy()
        lon = self.data['longitude'].to_numpy()

        bins = np.linspace(prices.min(), prices.max(), 6)
        categories = np.digitize(prices, bins) - 1

        fig = plt.figure(figsize=(12, 8))
        gs = fig.add_gridspec(2, 2)

        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax3 = fig.add_subplot(gs[1, :])
        #long vs rpice
        ax1.scatter(lon, prices, c=prices, cmap='viridis', s=5)
        ax1.set_title("Longitude vs Price")
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Price")
        #lat vs price
        ax2.scatter(lat, prices, c=prices, cmap='viridis', s=5)
        ax2.set_title("Latitude vs Price")
        ax2.set_xlabel("Latitude")
        ax2.set_ylabel("Price")
        #map
        scatter = ax3.scatter(lon,lat,c=categories,cmap='viridis', s=8,alpha=0.8)
        ax3.set_title("NY Housing Map View")
        ax3.set_xlabel("Longitude")
        ax3.set_ylabel("Latitude")

        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label("Price Category")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root = tk.Tk()
app = PriceChart(root)
root.mainloop()


#i pray to the machine gods that this code works