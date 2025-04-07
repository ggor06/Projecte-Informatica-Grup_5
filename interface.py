import tkinter as tk
from tkinter import messagebox
from graph import Graph, Plot, PlotNode, CreateGraph_1, LecturaNodos, LecturaSegmentos, RemoveNode, LoadSavedNodes, LoadSavedSegments
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from functools import partial


G = CreateGraph_1()
LoadSavedNodes(G, "saved_nodes.txt")
LoadSavedSegments(G, "saved_segments.txt")

#Actualización de los grafos
def updateGraphNodes():
    ax.clear()
    Plot(G, ax)
    canvas.draw()

def updateGraphNeigbors():
    ax.clear()
    PlotNode(G, clickRatolí, ax)
    canvas.draw()

#Fet parcialment amb GPT, tutorials de YT i foros(reddit i Stackoverflow) --> És una funció molt complicada de pensar
def clickRatolí(event, ax, canvas):
    #Diccionari de posicions
    node_positions = {node.name: (node.x, node.y) for node in G.nodes}
    x_click=event.xdata
    y_click=event.ydata
    clickedNode = None
    min_distance = float('inf')
    print(f"Clic detectat a ({x_click:.2f}, {y_click:.2f})")
    #Recorrer el diccionari
    for name, (x,y) in node_positions.items():
        xdistance = x - x_click
        ydistance = y - y_click
        distance = math.sqrt(xdistance**2 + ydistance**2)
        if distance < 0.5 and distance < min_distance:
            min_distance=distance
            clickedNode = name
    if clickedNode:
        ax.clear()
        PlotNode(G, clickedNode, ax)
        canvas.draw()
        
def RemoveNodeUI():
    name = entryD.get().strip()
    if RemoveNode(G, name):
        ax.clear()
        Plot(G, ax)
        canvas.draw()
    else:
        messagebox.showerror("Error", f"El node '{name}' no existeix.")

#Ventana principal
root = tk.Tk()
root.geometry("1400x700")
root.title("Grafo de nodos y de vecinos")

#Config de la ventana(3 filas 2 columnas)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

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

#Casilla para inputNode
button_inputNode_frame = tk.LabelFrame(root, text="AÑADIR NODO")
button_inputNode_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla de inputNode
button_inputNode_frame.rowconfigure(0, weight=1)
button_inputNode_frame.rowconfigure(1, weight=1)
button_inputNode_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de inputNode
entryN=tk.Entry(button_inputNode_frame)
entryN.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputNode=tk.Button(button_inputNode_frame, text="Input", command=lambda: LecturaNodos(G, entryN.get(), ax, canvas))
button_inputNode.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

#Frame para inputSegment
button_inputSegment_frame = tk.LabelFrame(root, text="AÑADIR SEGMENTO")
button_inputSegment_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla de inputSegment
button_inputSegment_frame.rowconfigure(0, weight=1)
button_inputSegment_frame.rowconfigure(1, weight=1)
button_inputSegment_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de inputSegment
entryS=tk.Entry(button_inputSegment_frame)
entryS.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputSegment=tk.Button(button_inputSegment_frame, text="Input", command=lambda:LecturaSegmentos(G, entryS.get(), ax, canvas))
button_inputSegment.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)


#Frame para DeleteNode_Segments
button_inputDeleteNode_Segments_frame = tk.LabelFrame(root, text="ELIMINAR NODO Y SEGMENTOS")
button_inputDeleteNode_Segments_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla de DeleteNode_Segments
button_inputDeleteNode_Segments_frame.rowconfigure(0, weight=1)
button_inputDeleteNode_Segments_frame.rowconfigure(1, weight=1)
button_inputDeleteNode_Segments_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de DeleteNode&Segments
entryD=tk.Entry(button_inputDeleteNode_Segments_frame)
entryD.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputDeleteNode_Segments=tk.Button(button_inputDeleteNode_Segments_frame, text="Input", command=RemoveNodeUI)
button_inputDeleteNode_Segments.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)


#Frame para los grafos
graph_frame=tk.LabelFrame(root, text="Grafos")
graph_frame.grid(row=0, column=1, rowspan=4, padx=5, pady=5, sticky="nsew")
graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)

#Creación de la figura(para poner los grafos)
fig=Figure(figsize=(5, 4), dpi=100)
ax=fig.add_subplot(111)
canvas=FigureCanvasTkAgg(fig, master=graph_frame)
#Manera de cridar a la funció clickRatolí i que funcioni
canvas.mpl_connect("button_press_event", partial(clickRatolí, ax=ax, canvas=canvas))
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

root.mainloop()