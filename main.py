import pygame,enum,sqlite3
import win32cred
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
    editid =enum.auto()
    edtname = enum.auto()
    Tmode = enum.auto()
    Tmenu = enum.auto()
    TAUTH = enum.auto()

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
    def Sprint(self, screen, text):
        text_bitmap = self.font.render(f"{text}", True, "black","white")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    def dprint(self, screen, text):
        text_bitmap = self.font.render(text.center(14), True, "red")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
    def Dprint(self, screen, text):
        text_bitmap = self.font.render(f">{text.center(12)}<", True, "red")
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
#cmd = mode.swap
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
    menuitem("Move",mode.Tmode),
    menuitem("Reset",mode.reset),
    menuitem("Get Logs",mode.fetch_DB),
    menuitem("Here",mode.hered),
    menuitem("Swap class",mode.swap),
    menuitem("Config",mode.TAUTH),
    
]
Tmenu = [
    menuitem("Edit",mode.editid),
    menuitem("Save",mode.save),
]
conn = sqlite3.connect("AATEND.DB")
conn.execute(f"""CREATE TABLE if not exists tbl (
	key INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	time TEXT NOT NULL,
	dir TEXT NOT NULL
);""")
cur = conn.cursor()
clsselN = "9-2"
ccls = ()
cclen = 0
def swap(clas):
    global clsz,hnh,clsselN,ccls,cclen
    clsz = classz[clas]
    ccls = tuple(clsz.keys())
    cclen = len(ccls)
    hnh = {}
    clsselN = clas
    for k,v in clsz.items():
        hnh[k] = False
classez = tuple(classz.keys())
clssel = 0
edtn =""
edtid = ""
titel = 'Auto Atendance 2.0'.ljust(40)
#titel = 'Auto Atendance DEMO [PRESS F1] Scan Card'.ljust(40)
demo = False
lw,lh = typed.font.size("-")
print((768-40)/lh)
tmdsel = 0
swap("9-2")
Menusel = 0
auth = ("AutoAttendance\\dev",'dev',False)
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
    elif cmd == mode.TAUTH:
        try:
            if win32cred.CredUIPromptForCredentials("AutoAttendance") == auth:
                cmd = mode.Tmenu
                
            else:
                cmd = mode.menu
        except:
            cmd = mode.menu
    elif cmd == mode.hered:
        menusel =0
        cmd = mode.scan
        now = datetime.datetime.now()
        cur.execute("""INSERT INTO tbl(name,time,dir)
              VALUES(?,?,?)""",("*",now.strftime("%d/%m/%Y %H:%M"),"HERED"))
        conn.commit()
        for k,v in clsz.items():
            hnh[k] =True
    elif cmd == mode.save and not demo:
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
    elif cmd in (mode.editid,mode.swap,mode.save) and demo: cmd = mode.scan

    scr.fill((0,0,0))
    HERE.reset()
    typed.reset()
    pygame.draw.line(scr,"white",(0,35),(1360,35))
    NOTHERE.reset()
    #typed.tprint(scr,f"{titel}   |{typd.center(15)}|")
    if cmd == mode.scan:
        typed.tprint(scr,f"{titel}   |{typd.center(15)}|")
        for k,v in clsz.items():
            if hnh[k]:
                HERE.tprint(scr,v)
            else:
                NOTHERE.tprint(scr,v)
    elif cmd == mode.Tmenu:
        typed.tprint(scr,f"{titel}   |{'Config'.center(15)}|{'config: Do Not Scan'.rjust(30)}")
        I = 0
        for i in Tmenu:
            if i.code in (mode.editid,mode.swap,mode.save) and demo:
                if I == Menusel:
                    HERE.Dprint(scr,i.txt)
                else:
                    HERE.dprint(scr,i.txt)
            else:
                if I == Menusel:
                    HERE.Mprint(scr,i.txt)
                else:
                    HERE.mprint(scr,i.txt)
            I += 1
    elif cmd == mode.Tmode:
        typed.tprint(scr,f"{titel}   |{clsz[ccls[tmdsel]].center(15)}|{'T-Mode: Do Not Scan'.rjust(30)}")
        tmpsel = ccls[tmdsel]
        for k,v in clsz.items():
            if hnh[k]:
                if k == tmpsel:
                    HERE.Sprint(scr,v)
                else:
                    HERE.tprint(scr,v)
            else:
                if k == tmpsel:
                    NOTHERE.Sprint(scr,v)
                else:
                    NOTHERE.tprint(scr,v)

    elif cmd == mode.editid:
        typed.tprint(scr,f"{titel}   |{edtid.center(15)}|")
        NOTHERE.tprint(scr,f"Editing: {clsselN}")
        NOTHERE.tprint(scr,"Please enter id or scan card")
        for k,v in clsz.items():
            HERE.tprint(scr,f"{k.center(10)}: {v}")
    elif cmd == mode.edtname:
        typed.tprint(scr,f"{titel}   |{edtn.center(15)}|")
        NOTHERE.tprint(scr,f"Editing: {clsselN}")
        NOTHERE.tprint(scr,"Please enter name")
        NOTHERE.tprint(scr,f"Id: {edtid}")
        for k,v in clsz.items():
            HERE.tprint(scr,f"{k.center(10)}: {v}")
    elif cmd == mode.menu:
        typed.tprint(scr,f"{titel}   |{''.center(15)}|")
        HERE.mprint(scr,"AUTO ATTENDACE By Ben H")
        if demo:HERE.dprint(scr,"DEMO VESION")
        I = 0
        for i in menu:
            if i.code in (mode.editid,mode.swap,mode.save) and demo:
                if I == menusel:
                    HERE.Dprint(scr,i.txt)
                else:
                    HERE.dprint(scr,i.txt)
            else:
                if I == menusel:
                    HERE.Mprint(scr,i.txt)
                else:
                    HERE.mprint(scr,i.txt)
            I += 1
    elif cmd == mode.swap:
        typed.tprint(scr,f"{titel}   |{''.center(15)}|")
        I = 0
        for k in classez:
            if I == clssel:
                HERE.Mprint(scr,k) 
            else:
                HERE.mprint(scr,k)
            I += 1
    elif cmd == mode.fetch_DB:
        typed.tprint(scr,f"{titel}   |{''.center(15)}|")
        HERE.tprint(scr,"IDX  first/last name   time: D/M/Y H:M  direction")
        HERE.tprint(scr,"--- ----------------- ----------------- ---------")
        sqlite_select_query = """SELECT * from tbl"""
        cur.execute(sqlite_select_query)
        records = cur.fetchall()
        if len(records) > 31:
            records = records[len(records)%31:]
        for i,n,t,d in records:
            HERE.tprint(scr,f"{str(i).center(3)} {n.center(17)} {t.center(17)} {d.center(9)}")
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_F12  :
                cmd = mode.menu
            elif e.key == pygame.K_ESCAPE:
                sys.exit()
            elif cmd == mode.scan:
                
                if e.key == pygame.K_RETURN:
                    try:
                        typd = typd.removeprefix("978")
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
            elif cmd == mode.Tmenu:
                if e.key == pygame.K_UP:
                    Menusel -= 1
                elif e.key == pygame.K_DOWN:
                    Menusel += 1
                elif e.key == pygame.K_RETURN:
                    cmd = Tmenu[Menusel].code
            elif cmd == mode.swap:
                if e.key == pygame.K_UP:
                    clssel -= 1
                elif e.key == pygame.K_DOWN:
                    clssel += 1
                elif e.key == pygame.K_RETURN:
                    swap(classez[clssel])
                    cmd = mode.scan
                    menusel =0
            elif cmd == mode.editid:
                
                if e.key == pygame.K_RETURN:
                    hnh[edtid] = False
                    cmd = mode.edtname
                elif e.key == pygame.K_BACKSPACE:
                    edtid = edtid[0:-1]
                else:
                    edtid += e.unicode
            elif cmd == mode.edtname:
                
                if e.key == pygame.K_RETURN:
                    clsz[edtid] = edtn
                    classz[clsselN] =clsz
                    edtid = ""
                    edtn = ""
                    f = open("usrs.json","w")
                    json.dump(classz,f)
                    f.close()
                    cmd = mode.editid
                elif e.key == pygame.K_BACKSPACE:
                    edtn = edtn[0:-1]
                else:
                    edtn += e.unicode
            elif cmd == mode.Tmode:
                if e.key == pygame.K_UP:
                    tmdsel -= 1
                    if tmdsel < 0: tmdsel = cclen-1
                elif e.key == pygame.K_DOWN:
                    tmdsel += 1
                    if tmdsel > cclen-1: tmdsel = 0
                elif e.key == pygame.K_RETURN:
                    now = datetime.datetime.now()
                    hnh[ccls[tmdsel]] = not hnh[ccls[tmdsel]]
                    if hnh[ccls[tmdsel]]: direc = "in"
                    else: direc = "out"
                    cur.execute("""INSERT INTO tbl(name,time,dir)
              VALUES(?,?,?)""",(clsz[ccls[tmdsel]],now.strftime("%d/%m/%Y %H:%M"),direc))
                    conn.commit()
                elif e.key == pygame.K_F10 and not demo:
                    from barcode import EAN8,ISBN10
                    from barcode.writer import SVGWriter
                    for k,v in clsz.items():
                        with open(f"codes/{v}.svg", "wb") as f:
                            if len(k) == 8:
                                EAN8(k, writer=SVGWriter()).write(f)
                            elif len(k) == 10:
                                ISBN10(k, writer=SVGWriter()).write(f)
            elif cmd == mode.fetch_DB:
                if e.key == pygame.K_F10 and not demo:
                    with open("logs.txt","w") as f:
                        f.write("IDX  first/last name   time: D/M/Y H:M  direction\n")
                        f.write("--- ----------------- ----------------- ---------\n")
                        sqlite_select_query = """SELECT * from tbl"""
                        cur.execute(sqlite_select_query)
                        records = cur.fetchall()
                        cur.execute("DROP TABLE tbl")
                        conn.commit()
                        conn.execute(f"""CREATE TABLE if not exists tbl (
                            key INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            time TEXT NOT NULL,
                            dir TEXT NOT NULL
                        );""")
                        conn.commit()
                        for i,n,t,d in records:
                            f.write(f"{str(i).center(3)} {n.center(17)} {t.center(17)} {d.center(9)}\n")
                
        