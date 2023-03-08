import pygame,enum,sqlite3
import json, sys, datetime
import colorama
from termcolor import colored 
import configparser
import logging
import csv
import coloredlogs
import verboselogs

pygame.init()

scr = pygame.display.set_mode((1360,768),pygame.FULLSCREEN)

class mode(enum.Enum):
    scan = enum.auto()
    menu = enum.auto()
    save = enum.auto()
    reset = enum.auto()
    fetch_DB = enum.auto()
    hered = enum.auto()
    swap = enum.auto()

class TextPrint:
    def __init__(self,orgn=(10,10)):
        self.orgn = orgn
        self.reset()
        self.font = pygame.font.SysFont(("Fixedsys","SysFixed","Courier New"), 20,True)
        #self.fontpygame.font.SysFont("Marlett",25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, "white")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    def mprint(self, screen, text):
        text_bitmap = self.font.render(text.center(14), True, "white")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    def Mprint(self, screen, text):
        text_bitmap = self.font.render(f">{text.center(12)}<", True, "white")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = self.orgn[0]
        self.y = self.orgn[1]
        self.line_height = 17

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10
typed = TextPrint()
HERE = TextPrint((10,40))
NOTHERE = TextPrint(((1360/2)+10,40))
verboselogs.install()
logging.basicConfig()
coloredlogs.install(level=5,fmt="%(asctime)s [%(levelname)s]: %(message)s")
f = open("usrs.json")
classz = json.load(f)
clsz = classz["9-2"]
hnh = {}
typd = ""
cmd = mode.scan
menusel = 0
class menuitem:
    def __init__(self,txt,code) -> None:
        self.txt = txt
        self.code = code
for k,v in clsz.items():
    hnh[k] = False
menu = [
    menuitem("Scan",mode.scan),
    menuitem("Reset",mode.reset),
    menuitem("Fetch DB",mode.fetch_DB),
    menuitem("Here",mode.hered),
    menuitem("Save",mode.save),
    menuitem("Swap class",mode.swap),
]
conn = sqlite3.connect("AATEND.DB")
conn.execute(f"""CREATE TABLE if not exists tbl (
	key INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	time TEXT NOT NULL,
	dir TEXT NOT NULL
);""")
cur = conn.cursor()

def swap(clas):
    global clsz,hnh
    clsz = classz[clas]
    hnh = {}
    for k,v in clsz.items():
        hnh[k] = False
classez = tuple(classz.keys())
clssel = 0
while True:
    if cmd == mode.reset:
        menusel =0
        cmd = mode.scan
        now = datetime.datetime.now()
        cur.execute("""INSERT INTO tbl(name,time,dir)
              VALUES(?,?,?)""",("*",now.strftime("%d/%m/%Y %H:%M"),"RESET"))
        conn.commit()
        for k,v in clsz.items():
            hnh[k] =False
    elif cmd == mode.hered:
        menusel =0
        cmd = mode.scan
        now = datetime.datetime.now()
        cur.execute("""INSERT INTO tbl(name,time,dir)
              VALUES(?,?,?)""",("*",now.strftime("%d/%m/%Y %H:%M"),"HERED"))
        conn.commit()
        for k,v in clsz.items():
            hnh[k] =True
    elif cmd == mode.save:
        with open('export.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='§',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["IDX","name","time","direction"])
            sqlite_select_query = """SELECT * from tbl"""
            cur.execute(sqlite_select_query)
            records = cur.fetchall()
            for i,n,t,d in records:
                spamwriter.writerow([i,n,t,d])
        cmd = mode.scan

    scr.fill((0,0,0))
    HERE.reset()
    typed.reset()
    pygame.draw.line(scr,"white",(0,35),(1360,35))
    NOTHERE.reset()
    typed.tprint(scr,f"{'Auto Atendance 2.0-BETA'.ljust(27)}   |{typd.center(15)}|")
    if cmd == mode.scan:
        for k,v in clsz.items():
            if hnh[k]:
                HERE.tprint(scr,v)
            else:
                NOTHERE.tprint(scr,v)
    elif cmd == mode.menu:
        I = 0
        for i in menu:
            if I == menusel:
                HERE.Mprint(scr,i.txt)
            else:
                HERE.mprint(scr,i.txt)
            I += 1
    elif cmd == mode.swap:
        I = 0
        for k in classez:
            if I == clssel:
                HERE.Mprint(scr,k) 
            else:
                HERE.mprint(scr,k)
            I += 1
    elif cmd == mode.fetch_DB:
        HERE.tprint(scr,"IDX  first/last name   time: D/M/Y H:M  direction")
        HERE.tprint(scr,"--- ----------------- ----------------- ---------")
        sqlite_select_query = """SELECT * from tbl"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        for i,n,t,d in records:
            HERE.tprint(scr,f"{str(i).center(3)} {n.center(17)} {t.center(17)} {d.center(9)}")
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_F12:
                cmd = mode.menu
            elif e.key == pygame.K_ESCAPE:
                sys.exit()
            elif cmd == mode.scan:
                
                if e.key == pygame.K_RETURN:
                    try:
                        now = datetime.datetime.now()
                        hnh[typd] = not hnh[typd]
                        if hnh[typd]: direc = "in"
                        else: direc = "out"
                        cur.execute("""INSERT INTO tbl(name,time,dir)
              VALUES(?,?,?)""",(clsz[typd],now.strftime("%d/%m/%Y %H:%M"),direc))
                        conn.commit()
                    except:
                        logging.log(15,"Invalid code:"+typd)
                    typd = ""
                elif e.key == pygame.K_BACKSPACE:
                    typd = typd[0:-1]
                else:
                    typd += e.unicode
            elif cmd == mode.menu:
                if e.key == pygame.K_UP:
                    menusel -= 1
                elif e.key == pygame.K_DOWN:
                    menusel += 1
                elif e.key == pygame.K_RETURN:
                    cmd = menu[menusel].code
            elif cmd == mode.swap:
                if e.key == pygame.K_UP:
                    clssel -= 1
                elif e.key == pygame.K_DOWN:
                    clssel += 1
                elif e.key == pygame.K_RETURN:
                    swap(classez[clssel])
                    cmd = mode.scan
                    menusel =0
        