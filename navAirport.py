from navGraph import ReadNavPoints
from navPoint import navPoint
from navGraph import AddNavPoint
class navAirport:
    def navAirport(self, name):
        self.name=name
        self.sid=[]
        self.star=[]

def ReadNavAirports(g, airports_file):
    g.navAirports = []
    with open(airports_file, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    for i in range(0, len(lines), 3):
        ap = navAirport(); ap.navAirport(lines[i])
        sid_code  = lines[i+1].split()[-1]
        star_code = lines[i+2].split()[-1]
        for pt in g.navPoints:
            if pt.name == sid_code:
                ap.sid.append(pt)
            if pt.name == star_code:
                ap.star.append(pt)
        g.navAirports.append(ap)
    return g.navAirports