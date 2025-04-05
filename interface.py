import tkinter as tk
from tkinter import messagebox
from graph import Plot, PlotNode, CreateGraph_1
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

G = CreateGraph_1()

#Ventana principal
root = tk.Tk()
root.geometry("1200x600")
root.title("Grafo de nodos y de vecinos")

#Config de la ventana(3 filas 2 columnas)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

#Casilla de los grafos
button_graph_frame = tk.LabelFrame(root, text="Grafos")
button_graph_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla
button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)

#Botones de dentro de la casilla de grafos
button_nodes=tk.Button(button_graph_frame, text="Grafo de nodos", command=lambda: updateGraphNodes())
button_nodes.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_neighbors=tk.Button(button_graph_frame, text="Grafo de vecinos", command=lambda: updateGraphNeigbors())
button_neighbors.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

#Casilla para input
button_input_frame = tk.LabelFrame(root, text="Input")
button_input_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla
button_input_frame.rowconfigure(0, weight=1)
button_input_frame.rowconfigure(1, weight=1)
button_input_frame.columnconfigure(0, weight=1)

#Botones de dentro de la casilla de input
button_input=tk.Button(button_input_frame, text="Input")
button_input.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
entry=tk.Entry(button_input_frame)
entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

#Frame para los grafos
graph_frame=tk.LabelFrame(root, text="Grafos")
graph_frame.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky="nsew")
graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)

#Creación de la figura
fig=Figure(figsize=(5, 4), dpi=100)
ax=fig.add_subplot(111)
canvas=FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

#Actualización de los grafos
def updateGraphNodes():
    ax.clear()
    Plot(G)
    canvas.draw()

def updateGraphNeigbors():
    ax.clear()
    PlotNode(G, "C")
    canvas.draw()

root.mainloop()