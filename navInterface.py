import tkinter as tk
from tkinter import messagebox, filedialog
from navGraph import (createGraph, Plot, PlotNode, ReadNavPoints, ReadNavSegments, SaveNavPoints, SaveNavSegments, FindShortestPath, RemoveNavPoint, AddSegment, LecturaNavPoints, AddNavPoint, FindAirport, FindNavPoint, FindShortestPathBetweenAirports, FindShortestPathByName)
from navPoint import navPoint
from navAirport import ReadNavAirports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math
from functools import partial
from path import Path, PlotPath, txtGen
import matplotlib.backends.backend_tkagg as tkagg
import sys, subprocess, os

G = createGraph()

path=None

def loadGraphFiles():
    pts_file= filedialog.askopenfilename(title="Selecciona el NAV Points arxiu", filetypes=[("Text Files", "*    .txt"), ("All Files", "*.*")])
    if not pts_file:
        return
    seg_file = filedialog.askopenfilename(title="Selecciona el NAV Segments arxiu", filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not seg_file:
        return
    aer_file=filedialog.askopenfilename(title="Selecciona el NAV Aer arxiu", filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not aer_file:
        return
    
    G.pts_file = pts_file
    G.seg_file = seg_file
    G.aer_file = aer_file
    ReadNavPoints(G, pts_file)
    ReadNavSegments(G, seg_file)
    ReadNavAirports(G, aer_file)

    ax.clear()
    Plot(G,ax)
    canvas.draw()

click_enabled = False

def saveGraphFiles():
    
    pts_file = filedialog.asksaveasfilename(title="Guardar NAV Points com", defaultextension=".txt", filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not pts_file:
        return

    seg_file = filedialog.asksaveasfilename(title="Guardar NAV Segments com", defaultextension=".txt", filetypes=[("Text Files","*.txt"),("All Files","*.*")])
    if not seg_file:
        return

    SaveNavPoints(G, pts_file)
    SaveNavSegments(G, seg_file)

    messagebox.showinfo("Save Graph", "Graph files saved successfully.")

navpoint_counter = 1
selected_node_code = None

def updateGraphNodes():
    global tree_value_var
    ax.clear()
    Plot(G, ax)
    canvas.draw()

def updateGraphNeighbors():
    ax.clear()
    PlotNode(G, selected_node_code, ax)
    canvas.draw()

def updatePath():
    ax.clear()
    global path
    if not getattr(G, 'pts_file', None) or not getattr(G, 'seg_file', None) or not getattr(G, 'aer_file', None):
        messagebox.showerror("Sense dades", "Introdueixi les dades")
        return

    ReadNavPoints(G, G.pts_file)
    ReadNavSegments(G, G.seg_file)
    ReadNavAirports(G, G.aer_file)

    #Rebuild bidirectional neighbors
    from navPoint import AddNeighbor
    for seg in G.navSegments:
        o = next((n for n in G.navPoints if n.code == seg.originNumber), None)
        d = next((n for n in G.navPoints if n.code == seg.destinationNumber), None)
        if o and d:
            AddNeighbor(d, o)
            AddNeighbor(o, d)

    origin = entryNodeOrigin.get().strip()
    dest   = entryNodeDest.get().strip()

    try:
        is_airport = lambda txt: any(ap.name.lower() == txt.lower() for ap in G.navAirports)

        if is_airport(origin) and is_airport(dest):
            route_nodes = FindShortestPathBetweenAirports(G, origin, dest)
        else:
            route_nodes = FindShortestPathByName(G, origin, dest)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        canvas.draw()
        return

    if route_nodes:
        path=Path(route_nodes)
        PlotPath(G, path, ax)
        #Funcionalitat extra 1
        co2_value_var.set(f"{path.co2:.2f} kg")
        TREE_CO2_PER_YEAR = 22.0
        num_trees = math.ceil(path.co2 / TREE_CO2_PER_YEAR)
        tree_value_var.set(f"{num_trees} arbres")

    else:
        messagebox.showerror("Error", f"No hi ha ruta entre '{origin}' i '{dest}'")
        canvas.draw()
        return

    # KML
    header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Mapa amb ruta</name>
    <Style id="navpoint"><IconStyle><scale>0.5</scale>
      <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>
    </IconStyle></Style>
    <Style id="sid"><IconStyle><scale>0.8</scale>
      <Icon><href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href></Icon>
    </IconStyle></Style>
    <Style id="star"><IconStyle><scale>0.8</scale>
      <Icon><href>http://maps.google.com/mapfiles/kml/shapes/target.png</href></Icon>
    </IconStyle></Style>
    <Style id="airway"><LineStyle><color>7f00ffff</color><width>1</width></LineStyle></Style>
    <Style id="route"><LineStyle><color>ff0000ff</color><width>4</width></LineStyle></Style>
"""
    footer = """  </Document>
</kml>
"""
    kml_filename = "ruta.kml"
    with open(kml_filename, "w", encoding="utf-8") as f:
        f.write(header)

        for pt in G.navPoints:
            f.write(f"""    <Placemark>
      <name>{pt.code}</name>
      <styleUrl>#navpoint</styleUrl>
      <Point><coordinates>{pt.lon},{pt.lat}</coordinates></Point>
    </Placemark>
""")
        for ap in G.navAirports:
            for sid in ap.sid:
                f.write(f"""    <Placemark>
      <name>{ap.name}_SID</name>
      <styleUrl>#sid</styleUrl>
      <Point><coordinates>{sid.lon},{sid.lat}</coordinates></Point>
    </Placemark>
""")
            for star in ap.star:
                f.write(f"""    <Placemark>
      <name>{ap.name}_STAR</name>
      <styleUrl>#star</styleUrl>
      <Point><coordinates>{star.lon},{star.lat}</coordinates></Point>
    </Placemark>
""")
        for seg in G.navSegments:
            o = next((n for n in G.navPoints if n.code == seg.originNumber), None)
            d = next((n for n in G.navPoints if n.code == seg.destinationNumber), None)
            if o and d:
                f.write(f"""    <Placemark>
      <styleUrl>#airway</styleUrl>
      <LineString><tessellate>1</tessellate>
        <coordinates>{o.lon},{o.lat} {d.lon},{d.lat}</coordinates>
      </LineString>
    </Placemark>
""")
        if route_nodes:
            coords = " ".join(f"{n.lon},{n.lat}" for n in route_nodes)
            f.write(f"""    <Placemark>
      <name>Camí Seleccionat</name>
      <styleUrl>#route</styleUrl>
      <LineString><tessellate>1</tessellate>
        <coordinates>{coords}</coordinates>
      </LineString>
    </Placemark>
""")
        f.write(footer)

    if sys.platform.startswith("darwin"):
        subprocess.call(["open", kml_filename])
    elif os.name == "nt":
        os.startfile(kml_filename)
    else:
        subprocess.call(["xdg-open", kml_filename])

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
    code = entryD.get().strip()
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

def calc_co2(path):
    return path.co2

def on_generate(path):
    if not globals().get('path', None) or not getattr(path, "_co2_computed", False):
        messagebox.showerror("Sense camí plotat", "Primer fes un camí")
        return
    txtGen(path, filename="Resultat.txt")

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
#Activar nodos
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
button_path = tk.Button(path_frame, text="Afegir Camí i generar KML", command=lambda: updatePath())
button_path.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

#Frame para poner emisiones de CO2
co2_frame=tk.LabelFrame(root, text="Càlcul de les emisions de CO2")
co2_frame.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
co2_frame.rowconfigure(0, weight=1)
co2_frame.rowconfigure(1, weight=1)
co2_frame.rowconfigure(2, weight=1)
co2_frame.columnconfigure(0, weight=1)
co2_value_var = tk.StringVar(value="0.00 kg")
lbl_desc = tk.Label(co2_frame,text="Emissions totals:", font=("Helvetica", 10), bg=co2_frame.cget("bg"), fg="#333333")
lbl_desc.grid(row=0, column=0, sticky="w", padx=10, pady=(10,2))
lbl_value = tk.Label(co2_frame, textvariable=co2_value_var, font=("Helvetica", 16, "bold"), bg=co2_frame.cget("bg"),fg="#2E8B57")
lbl_value.grid(row=1, column=0, sticky="w", padx=10, pady=(0,10))
tree_value_var = tk.StringVar(value="0 arbres")
lbl_trees = tk.Label(co2_frame, text="Arbres necessaris:", font=("Helvetica", 12))
lbl_trees.grid(row=2, column=0, sticky="w", padx=10, pady=(5,0))
lbl_tree_value = tk.Label(co2_frame, textvariable=tree_value_var, font=("Helvetica", 12), fg="#228B22")
lbl_tree_value.grid(row=2, column=1, sticky="w", padx=10, pady=(5,10))

#Frame de creación de txt
txt_frame=tk.LabelFrame(root, text="Creació de navPoints del camí creat", padx=5, pady=5)
txt_frame.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
txt_frame.rowconfigure(0, weight=1)
txt_frame.columnconfigure(0, weight=1)
#Botón de creación de txt
txt_button=tk.Button(txt_frame, text="Generar arxiu .txt dels nodes i CO2", command=lambda: on_generate(path))
txt_button.grid(row=0, column =0, padx=5, pady=5, sticky="nsew")

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

