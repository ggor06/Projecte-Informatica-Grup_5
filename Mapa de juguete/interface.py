import tkinter as tk
from tkinter import messagebox
from graph import Graph, Plot, PlotNode, CreateGraph_1, LecturaNodos, RemoveNode, ReadGraphData, AddSegment, ReadGraphData, SaveGraphToFile, FindShortestPath
import matplotlib.pyplot as plt
from node import Node
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from functools import partial
from path import Path, PlotPath

G = CreateGraph_1()
ReadGraphData(G, "Graph_data_sample.txt")
#Aportació de GPT per a que no es repeteixin noms de Nodes genèrics
node_counter = max(
    [int(n.name[1:]) for n in G.nodes if n.name.startswith("N") and n.name[1:].isdigit()],default=0) + 1

#Actualización de los grafos
def updateGraphNodes():
    ax.clear()
    Plot(G, ax)
    canvas.draw()

def updateGraphNeighbors():
    ax.clear()
    PlotNode(G, clickRatolí, ax)
    canvas.draw()

def updatePath():
    ax.clear()
    list=FindShortestPath(G, entryNodeOrigin.get(), entryNodeDest.get())
    path = Path(list)
    PlotPath(G, path, ax)
    canvas.draw()

node_counter = 1

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
    if not clickedNode:
        global node_counter
        name = f"N{node_counter}"
        node_counter += 1
        node = Node(name, round(x_click,2), round(y_click,2))
        G.nodes.append(node)
        ax.clear()
        Plot(G, ax)  
        canvas.draw()
        
def RemoveNodeUI():
    name = entryD.get().strip()
    if RemoveNode(G, name):
        ax.clear()
        Plot(G, ax)
        canvas.draw()
    else:
        messagebox.showerror("Error", f"El node '{name}' no existeix.")
    
def AddSegmentUI():
    name = entrySegName.get().strip()
    origin = entrySegOrigin.get().strip()
    dest = entrySegDest.get().strip()

    if AddSegment(G, origin, dest, name):
        ax.clear()
        Plot(G, ax)
        canvas.draw()
    else:
        messagebox.showerror("Error", "No s'ha pogut afegir el segment. Comprova els noms dels nodes.")



#Ventana principal
root = tk.Tk()
root.geometry("1400x800")
root.title("Gràfic de nodes i veïns")

#Config de la ventana(3 filas 2 columnas)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=8)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

#Casilla de los grafos
button_graph_frame = tk.LabelFrame(root, text="Gràfics")
button_graph_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla
button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de grafos
button_nodes=tk.Button(button_graph_frame, text="Gràfic de nodes", command=lambda: updateGraphNodes())
button_nodes.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_neighbors=tk.Button(button_graph_frame, text="Gràfic de veïns", command=lambda: updateGraphNeighbors())
button_neighbors.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

#Casilla para inputNode
button_inputNode_frame = tk.LabelFrame(root, text="Afegir node")
button_inputNode_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla de inputNode
button_inputNode_frame.rowconfigure(0, weight=1)
button_inputNode_frame.rowconfigure(1, weight=1)
button_inputNode_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de inputNode
entryN=tk.Entry(button_inputNode_frame)
entryN.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputNode=tk.Button(button_inputNode_frame, text="Afegir node", command=lambda: LecturaNodos(G, entryN.get(), ax, canvas))
button_inputNode.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

# Frame to add a segment with a custom name
button_customSegment_frame = tk.LabelFrame(root, text="Afegir segment")
button_customSegment_frame.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_customSegment_frame.rowconfigure([0, 1, 2, 3], weight=1)
button_customSegment_frame.columnconfigure(0, weight=1)

entrySegName = tk.Entry(button_customSegment_frame)
entrySegName.insert(0, "Nom del segment")
entrySegName.grid(row=0, column=0, padx=5, pady=2, sticky="ew")

entrySegOrigin = tk.Entry(button_customSegment_frame)
entrySegOrigin.insert(0, "Node origen")
entrySegOrigin.grid(row=1, column=0, padx=5, pady=2, sticky="ew")

entrySegDest = tk.Entry(button_customSegment_frame)
entrySegDest.insert(0, "Node destí")
entrySegDest.grid(row=2, column=0, padx=5, pady=2, sticky="ew")

button_customSegment = tk.Button(button_customSegment_frame, text="Afegir Segment", command=lambda: AddSegmentUI())
button_customSegment.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

#Frame para DeleteNode_Segments
button_inputDeleteNode_Segments_frame = tk.LabelFrame(root, text="Eliminar node i segments")
button_inputDeleteNode_Segments_frame.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Celdas dentro de la casilla de DeleteNode_Segments
button_inputDeleteNode_Segments_frame.rowconfigure(0, weight=1)
button_inputDeleteNode_Segments_frame.rowconfigure(1, weight=1)
button_inputDeleteNode_Segments_frame.columnconfigure(0, weight=1)
#Botones de dentro de la casilla de DeleteNode&Segments
entryD=tk.Entry(button_inputDeleteNode_Segments_frame)
entryD.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputDeleteNode_Segments=tk.Button(button_inputDeleteNode_Segments_frame, text="Eliminar", command=RemoveNodeUI)
button_inputDeleteNode_Segments.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
#Frame para los grafos
graph_frame=tk.LabelFrame(root, text="Gràfic")
graph_frame.grid(row=0, column=1, rowspan=4, padx=5, pady=5, sticky="nsew")
graph_frame.columnconfigure(0, weight=1)
graph_frame.rowconfigure(0, weight=1)
#Frame para cargar y aguardar grafos
charge_frame=tk.LabelFrame(root, text="Guardar y carregar gràfic")
charge_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
charge_frame.rowconfigure(0, weight=1)
charge_frame.rowconfigure(1, weight=1)
charge_frame.rowconfigure(2, weight=1)
charge_frame.rowconfigure(3, weight=1)
charge_frame.columnconfigure(0, weight=1)
#Botones para cargar y guardar grafos
entrysaveName = tk.Entry(charge_frame)
entrysaveName.insert(0, "Nom del fitxer")
entrysaveName.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
saveGraph=tk.Button(charge_frame, text="Guardar gràfic", command=lambda: SaveGraphToFile(G, entrysaveName.get()))
saveGraph.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
entrychargeName=tk.Entry(charge_frame)
entrychargeName.insert(0, "Nom del fitxer")
entrychargeName.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
chargeGraph=tk.Button(charge_frame, text="Carregar gràfic", command=lambda: ReadGraphData(G, entrychargeName.get()))
chargeGraph.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
#Frame para poner nodos para path
path_frame=tk.LabelFrame(root, text="Camí a seguir")
path_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
path_frame.rowconfigure(0, weight=1)
path_frame.rowconfigure(1, weight=1)
path_frame.rowconfigure(2, weight=1)
path_frame.columnconfigure(0, weight=1)
#Botones para poner nodos de inicio y final
entryNodeOrigin = tk.Entry(path_frame)
entryNodeOrigin.insert(0, "Node origen")
entryNodeOrigin.grid(row=0, column=0, padx=5, pady=2, sticky="ew")
entryNodeDest = tk.Entry(path_frame)
entryNodeDest.insert(0, "Node destí")
entryNodeDest.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
button_path = tk.Button(path_frame, text="Afegir Camí", command=lambda: updatePath())
button_path.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

#Creación de la figura(para poner los grafos)
fig=Figure(figsize=(5, 4), dpi=100)
ax=fig.add_subplot(111)
canvas=FigureCanvasTkAgg(fig, master=graph_frame)
#Manera de cridar a la funció clickRatolí i que funcioni
canvas.mpl_connect("button_press_event", partial(clickRatolí, ax=ax, canvas=canvas))
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")



root.mainloop()