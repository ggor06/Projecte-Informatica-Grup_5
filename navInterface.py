import tkinter as tk
from tkinter import messagebox, filedialog
from navGraph import createGraph, Plot, PlotNode, ReadNavPoints, ReadNavSegments, SaveNavPoints, SaveNavSegments, FindShortestPath, RemoveNavPoint, AddSegment, LecturaNavPoints, LecturaNavSegments, AddNavPoint, AddNavPoint
from navPoint import navPoint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from functools import partial
from path import Path, PlotPath
import matplotlib.backends.backend_tkagg as tkagg

G = createGraph()


def loadGraphFiles():
    pts_file= filedialog.askopenfilename(title="Selecciona el NAV Points arxiu", filetypes=[("Text Files", "*    .txt"), ("All Files", "*.*")])
    if not pts_file:
        return
    seg_file = filedialog.askopenfilename(title="Selecciona el NAV Segments arxiu", filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not seg_file:
        return
    ReadNavPoints(G, pts_file)
    ReadNavSegments(G, seg_file)

    ax.clear()
    Plot(G,ax)
    canvas.draw()

click_enabled = False

def saveGraphFiles():
    
    pts_file = filedialog.asksaveasfilename(
        title="Guardar NAV Points com",
        defaultextension=".txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not pts_file:
        return

    seg_file = filedialog.asksaveasfilename(
        title="Guardar NAV Segments com",
        defaultextension=".txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not seg_file:
        return

    SaveNavPoints(G, pts_file)
    SaveNavSegments(G, seg_file)

    messagebox.showinfo("Save Graph", "Graph files saved successfully.")

navpoint_counter = 1
selected_node_code = None

def updateGraphNodes():
    ax.clear()
    Plot(G, ax)
    canvas.draw()

def updateGraphNeighbors():
    ax.clear()
    PlotNode(G, selected_node_code, ax)
    canvas.draw()

def updatePath():
    ax.clear()
    list = FindShortestPath(G, entryNodeOrigin.get(), entryNodeDest.get())
    if list:
        path = Path(list)
        PlotPath(G, path, ax)
    canvas.draw()

navpoint_counter = 1
def create_navPoint(lat, lon):
    global navpoint_counter
    code = str(navpoint_counter)  
    name = f"Node_{navpoint_counter}"     
    navpoint_counter += 1
    p = navPoint()
    p.navPoint(code, name, lat, lon)
    return p

#Fet parcialment amb GPT, tutorials de YT i foros(reddit i Stackoverflow) --> És una funció molt complicada de pensar
def clickRatolí(event, ax, canvas):
    global selected_node_code, click_enabled

    x_click = event.xdata
    y_click = event.ydata
    if x_click is None or y_click is None:
        return

    # Primer: intentar seleccionar un node per veure veïns
    node_positions = {n.code: (n.lon, n.lat) for n in G.navPoints}
    clicked_code = None
    min_dist = float("inf")

    for code, (lon, lat) in node_positions.items():
        dist = math.hypot(lon - x_click, lat - y_click)
        if dist < 0.1 and dist < min_dist:
            min_dist = dist
            clicked_code = code

    if clicked_code is not None:
        selected_node_code = clicked_code
        updateGraphNeighbors()
        return

    # Només afegir si està activat
    if not click_enabled:
        return

    from navGraph import AddNavPoint, SaveNavPoints

    new_code = f"N{len(G.navPoints) + 1}"
    new_name = f"Node_{len(G.navPoints) + 1}"
    lat = round(y_click, 2)
    lon = round(x_click, 2)

    if AddNavPoint(G, new_code, new_name, lat, lon):
        SaveNavPoints(G, "navPoints.txt")
        updateGraphNodes()
    else:
        messagebox.showerror("Error", f"El node amb codi '{new_code}' ja existeix.")

def toggleClick():
    global click_enabled
    click_enabled = not click_enabled
    if click_enabled:
        button_toggle_click.config(text="Desactiva clic per afegir node", bg="lightgreen")
    else:
        button_toggle_click.config(text="Activa clic per afegir node", bg="SystemButtonFace")


def RemoveNodeUI():
    code = entryD.get().strip()  # Ara llegim el "code" del node
    if RemoveNavPoint(G, code):
        ax.clear()
        Plot(G, ax)
        canvas.draw()
    else:
        messagebox.showerror("Error", f"El node amb codi '{code}' no existeix.")

def AddSegmentUI():
    origin = entrySegOrigin.get().strip()
    dest = entrySegDest.get().strip()

    if AddSegment(G, origin, dest):
        SaveNavSegments(G, "navSegments.txt")
        ax.clear()
        Plot(G, ax)
        canvas.draw()
    else:
        messagebox.showerror("Error", "No s'ha pogut afegir el segment. Comprova els codis dels nodes.")

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
button_inputNode=tk.Button(button_inputNode_frame, text="Afegir node", command=lambda: LecturaNavPoints(G, entryN.get(), ax, canvas))
button_inputNode.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)

button_toggle_click = tk.Button(button_inputNode_frame, text="Activa clic per afegir node", command=toggleClick)
button_toggle_click.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_inputNode_frame.rowconfigure(2, weight=1)


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
charge_frame = tk.LabelFrame(root, text="Load / Save Graph")
charge_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
charge_frame.columnconfigure(0, weight=1)
charge_frame.rowconfigure([0,1], weight=1)

btn_load = tk.Button(charge_frame, text="Load Graph", command=loadGraphFiles)
btn_load.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

btn_save = tk.Button(charge_frame, text="Save Graph", command=saveGraphFiles)
btn_save.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")


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

#Frame para poner el zoom
toolbar_frame = tk.Frame(graph_frame)
toolbar_frame.grid(row=1, column=0, sticky="ew")
#Zoom
toolbar = tkagg.NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)


root.mainloop()

