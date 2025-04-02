# Macera Oyunu

from random import randint
from time import sleep
import curses
import tkinter as tk
import threading
import json
import os


### Classlar ###

class Oyuncu:
    """ Oyuncunun sınıfı.
        100 can, 10 atak gücü (Sopa), %15 şans ile başlanır.
        Envanter dict türündedir. Sopa ile başlanır
    """

    def __init__(self, isim):
        self.isim = isim
        self.bolum = 1
        self.envanter = dict()
        self.can = 100
        self.atak = 10
        self.sans = 15

        self.envantere_ekle(Sopa())

        self.gorevler = list()  # Oyuncunun görevlerini tutan bir list
    
    @property
    def data(self) -> dict:
        depo = self.envanter.copy()
        return {"isim": self.isim,
                "bolum": self.bolum,
                "silah": depo.pop("Silah", None).__str__(),
                "envanter": depo,
                "can": self.can,
                "atak": self.atak,
                "sans": self.sans,
                }
    
    def save(self):
        """ Oyuncunun isminde bir json dosyası oyuncunun bilgileri ile dizine yazdırılır
            Her bölüm sonunda çağırılmalı.
        """
        with open(f"{self.isim}.json", 'w') as fff:
            json.dump(oyuncu.data, fff, indent= 4)

    def save_sil(self):
        try: os.remove(f"{self.isim}.json")
        except: pass

    def save_yukle(self, data):
        self.bolum = data["bolum"]
        self.envanter = data["envanter"]
        self.can = data["can"]
        self.atak = data["atak"]
        self.sans = data["sans"]
        if data["Silah"] == "Sopa":
            self.envantere_ekle(Sopa())




    
    def envantere_ekle(self, esya):
        if issubclass(type(esya), Silah):
            self.envanter["Silah"] = esya
            self.atak = esya.atakguc

        elif esya in self.envanter:
            self.envanter[esya] += 1

        else:
            self.envanter[esya] = 1
    
    def kullan(self, esya):
        if esya in self.envanter:
            self.envanter[esya] -= 1
            if not self.envanter[esya]:
                del self.envanter[esya]
        else:
            raise KeyError
        
    def saldiri(self, hedef):
        hedef.can -= self.atak + (self.atak + randint(0, int(self.atak * self.sans / 100)))
        return f"{self.isim}  {hedef}"

    def __call__(self):
        return oyuncu.isim
    def __str__(self):
        return oyuncu.isim



class Dusman:
    """ Düşmanlar için ortak sınıf.
    """
    def __init__(self, can):
        self.can = can


class Bucur(Dusman):
    """ Bücür isimli düşmanın sınıfı. Nesneler "Bücür" ismine döner.
        20 canları vardır.
    """
    def __init__(self):
        self.isim = "Bücür"
        super().__init__(20)
    
    def __str__(self):
        return self.isim
    


class Silah:
    def __init__(self, isim, atakguc):
        self.isim = isim
        self.atakguc = atakguc
    
    def __str__(self):
        return self.isim

class Sopa(Silah):
    def __init__(self):
        super().__init__("Sopa", 10)
    








### Fonksiyolar ###



def pencere():
    """ Oyuncunun menüdeki bilgilerinin yenilenmesini sağlar
        Menüdeki bilgiler her değiştiğinde çağırılmalı.
    """
    global win_isim, win_can, win_sans, win_envanter, win_env
    try:
        win_isim.destroy()
        win_can.destroy()
        win_sans.destroy()
        win_envanter.destroy()
        win_env.destroy()
    except:
        pass
    win_isim = tk.Label(win, text= oyuncu.isim, bg= "slategrey", fg="blue")
    win_can = tk.Label(win, text= f"Can: {oyuncu.can}", bg= "slategrey", fg= "#ddd310")
    win_atak = tk.Label(win, text= f"Atak Gücü: {oyuncu.atak}", bg= "slategrey", fg= "#ddd310")
    win_sans = tk.Label(win, text= f"Şans: {oyuncu.sans}", bg= "slategrey", fg= "#ddd310")
    win_envanter = tk.Label(canvas, text= "Envanter:", bg= "#add8e6")

    win_envanterdekiler = ""
    for i, j in oyuncu.envanter.items():
        win_envanterdekiler += f"{i}: {j}\n"
    win_env = tk.Label(canvas, text= win_envanterdekiler, bg= "#add8e6")

    win_isim.pack()
    win_can.pack()
    win_atak.pack()
    win_sans.pack()

    win_envanter.place(relx= .5, rely= .1, anchor= tk.CENTER)
    win_env.place(relx=0.5, rely=0.5, anchor= tk.CENTER)
    












def yazc(stdscr, metin:str, y:int= None, x:int= None, stil= curses.COLOR_WHITE) -> None:
    """ Verilen metinin her harfi çok bir kısa süre beklenerek yazılır.
        Yer belirtilmez ise terminalin ortasına yazdırılır.
        "@" karakterinin olduğu yere oyuncunun ismi yazılır.
    """
    y = maxy//2 if y==None else y
    x = maxx//2 - len(metin)//2 if x==None else x 
    if m:= metin.count("@"):
        x -= m*(len(oyuncu()) -1)
    for i in metin:
        if i == "@":
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            yazc(stdscr, oyuncu(), y, x, stil= curses.color_pair(1))
            x += len(oyuncu())
            continue
        stdscr.addstr(y, x, i, stil)
        stdscr.refresh()
        x += 1
        sleep(.04)


def yazci(stdscr, sure=1, *args, y=None, x=None, stil= curses.COLOR_WHITE, clear=True) -> None:
    """ Verilen parametreler hepsinin sonunda süre beklenecek şekilde yazdırılır.
        Varsayılan olarak terminalin ortasına yazdırılır.
        İlk parametre curses'in objesi için, ikinci parametre (sure) aralarda ve sonda beklenecek süre (saniye)
        Sonraki isimsiz parametreler yazılacak metinler.
        stil parametresi curses color pairleri için.
        clear True ise kendisinden önceki yazılar silinir.
        yazci(stdscr, süre, "metinler", stil= white, clear=True)
    """
    if clear: stdscr.clear()
    uzunluklar = list()
    for metin in args:
        uzunluklar.append(len(metin))
    orta = sum(uzunluklar)
    y = maxy//2 if not y else y
    x = maxx//2 - orta//2 if not x else x
    for i, uzunluk in enumerate(uzunluklar):
        yazc(stdscr, args[i], y, x, stil=stil)
        x += uzunluk
        sleep(sure)
    stdscr.addstr(chr(187))
    return stdscr.getch()







### Hazırlık ###

# Pencere oluşturulur
win = tk.Tk()
win.config(bg= "slategrey")
win.geometry("250x400")
win.maxsize(250, 720)
win.minsize(250, 400)
win.title("Menü")
canvas = tk.Canvas(width= 230, height= 250)
canvas.config(bg= "#add8e6")
canvas.place(anchor= tk.CENTER, relx= 0.5, rely= 0.55)

kapat = tk.Button(win, text= "Kapat", command= lambda: win.protocol("WM_DELETE_WINDOW") and win.destroy())
kapat.place(relx=.75, rely=.9)



odalar = ("Başlangıç", "Koca Mağara")










### Başlangıç ###

def Oyna(stdscr):
    global oyuncu, maxy, maxx
    maxy, maxx = stdscr.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Oyuncu ismi rengi
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Kırmızı yazı
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Yeşil yazı




    ### Oyun başlar ###

    yazci(stdscr, 1, "Hey", ", sen.", " Sonunda uyandın.")

    while True:
        stdscr.clear()  # Terminal temizlenir.
        curses.echo()   # Kullanıcının cevabının ekranda görünmesi
        soru = "Senin adın nedir? : "
        yazc(stdscr, soru, y= maxy//2, x=0)
        ad = stdscr.getstr(maxy//2, len(soru), 22).decode('utf-8').strip()  # maksimum 22 karakterlik isim alınır
        karaliste = ["/", "\\", ",", "@", ":", "*", ">", "<", "?", "\"", "|"]

        if not ad or any(i in ad for i in karaliste) or ad.isnumeric():
            yazci(stdscr, 0.5, "Benimle dalga mı geçiyorsun!", " Doğru düzgün söyle.", stil= curses.color_pair(2))
            continue
        break



    oyuncu = Oyuncu(ad) # Oyuncu oluşturuldu
    pencere()   # Oyuncu bilgilerinin menüde gösterilmesi
    

    if f"{ad}.json" in os.listdir():
        curses.noecho()
        cevap = yazci(stdscr, 0.1, "Save dosyası bulundu. Yüklemek ister misin(1) yoksa sıfırdan mı devam(2) edersin?",stil=curses.color_pair(3))
        while cevap != ord("1") and cevap != ord("2"):
            cevap = stdscr.getch()
        if cevap == ord("1"):
            try:
                with open(f"{oyuncu}.json", 'r') as fff:
                    data = json.load(fff)
                oyuncu.save_yukle(data)
            except:
                yazci(stdscr, 1.25, "Save dosyası yüklenemedi.", stil= curses.color_pair(2))
    oyuncu.save()





    while True:
        ### 1. Bölüm ###
        
        if oyuncu.bolum == 1:
            yazci(stdscr, 1, "Herkes senin uyanmanı bekliyordu @.")
            stdscr.clear()

            oyuncu.save()


        elif oyuncu.bolum == 2:
            pass

            oyuncu.save()
        
        elif oyuncu.bolum == 3:
            pass

            oyuncu.save()

        else:
            yazci(stdscr, 2, "Sanırım", " ... ", " kayboldun.")


        stdscr.getch()
        oyuncu.save_sil()
        win.destroy()








oyna = threading.Thread(target= lambda: curses.wrapper(Oyna), daemon= True)
oyna.start()

win.mainloop()
