# Macera Oyunu

from random import randint
from colorama import init, Fore, Back, Style    # Renkli yazılar için
from time import sleep
import tkinter as tk
import threading


class Oyuncu:
    """ Oyuncunun sınıfı.
        100 can, 10 atak gücü (sopa), %15 şans ile başlanır.
        Envanter dict türündedir. Sopa ile başlanır
    """

    def __init__(self, isim):
        self.isim = isim
        self.envanter = dict()
        self.can = 100
        self.atak = 10
        self.sans = 15

        self.silah = Sopa()
        self.envanter["Silah"] = self.silah
    
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
 
    def __str__(self):
        return Style.BRIGHT + Fore.CYAN + self.isim + Style.RESET_ALL



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
    


















def yaz(yazi, /,  *, stil=None, end="\n"):
    """ Parametre olarak string girilir ve her karakter 0.05 saniye aralıklarla yazılır
        '@' karakterinin yerine oyuncu adı yazılır.
        stil parametresine Fore.RED gibi renk özellikleri girilebilir.

    """
    for i in yazi:
        if i == "@":
            yaz(oyuncu.isim, stil=Style.BRIGHT + Fore.CYAN, end="")
            continue    
        print(i if not stil else stil + i, end="")
        sleep(.05)
    print(end=end)




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
    win_isim = tk.Label(win, text= oyuncu.isim, bg= "slategrey")
    win_can = tk.Label(win, text= f"Can: {oyuncu.can}", bg= "slategrey")
    win_atak = tk.Label(win, text= f"Atak Gücü: {oyuncu.atak}", bg= "slategrey")
    win_sans = tk.Label(win, text= f"Şans: {oyuncu.sans}", bg= "slategrey")
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
    











### Hazırlık ###
init(autoreset=True)  # Colorama modülümüzün init fonksiyonu

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
















### Başlangıç ###
yaz("Hoşgeldin!", stil=Style.BRIGHT)

def Oyna():
    global oyuncu
    while True:
        # Karakter isim belirlemesi
        yaz("Karakterin için bir isim gir: ", end="")
        ad = input().strip()
        karaliste = ["/", "\\", ",", "@"]
        if not ad or any(i in ad for i in karaliste) or ad.isnumeric():
            yaz("Adam gibi isim gir >:(", stil= Fore.RED + Style.DIM)
            continue
        elif len(ad) > 20:
            yaz("20 Karakterden fazla isim giremezsin :(", stil= Fore.RED + Style.DIM)
            continue

        oyuncu = Oyuncu(ad) # Oyuncu oluşturuldu

        # Oyuncu bilgilerinin menüde gösterilmesi
        pencere()

        yaz("Merhaba, @!", stil=Style.BRIGHT)

        # yaz("Eyvah, @ 10 hasar aldı!", stil= Fore.RED)




        
        
        input("Bitir.")
        win.destroy()
        break










oyna = threading.Thread(target= Oyna, daemon= True)
oyna.start()

win.mainloop()
