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
        Sopa silahı ile başlanır
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
                "Silah": depo.pop("Silah", None).__str__(),
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
        self.sans = data["sans"]
        if data["Silah"] == "Sopa":
            self.envantere_ekle(Sopa())
        pencere()


    
    def envantere_ekle(self, esya) -> None:
        """ Eşya envantere 1 tane eklenir
            Eğer eklenecek eşya silah türünde ise var olan silah ile değiştirilir \
            ve oyuncunun atak gücü değiştirilir.
        """
        if issubclass(type(esya), Silah):
            self.envanter["Silah"] = esya
            self.atak = esya.atakguc

        elif esya in self.envanter:
            self.envanter[esya] += 1

        else:
            self.envanter[esya] = 1
        try: pencere()
        except NameError: pass # oyuncu ilk oluşturulduğunda hata almamak için
    
    def kullan(self, esya) -> None | int:
        """ Eşya envanterde varsa sayısı bir azaltılır
            Sayısı 0 olursa silinir
            Eğer eşya envanterde yoksa KeyError hatası verilir
        """
        rtrn = None
        if esya in self.envanter:
            self.envanter[esya] -= 1
            if self.envanter[esya] == 0:
                del self.envanter[esya]
        else:
            raise KeyError
        if esya == "Yüce Ağaç Meyvesi":
            b = oyuncu.sans - 15
            zar = randint(b, 101)
            if zar == 100:
                miktar = 35
            elif zar > 90:
                miktar = 30
            elif zar > 80:
                miktar = 25
            else:
                miktar = 20
            
            self.can += miktar

            if self.can > 100:
                self.can = 100
            rtrn = miktar
        pencere()
        return rtrn


    def saldiri(self, hedef) -> None:
        """ Hedefin canı düşürülür.
            Ekran temizlenmez.
            Verilen hasarın bilgisi yazdırılır.
        """
        hasar = self.atak + randint(0, self.atak * self.sans // 100)
        hedef.can -= hasar
        if hedef.can < 0:
            hedef.can = 0
        yenile()
        if hedef.can == 0:
            yazci(0.4, f"{hedef} {hasar} hasar aldı.", stil= curses.color_pair(4), getch= False, clear= False)
            yazci(0.4, f"{hedef} öldü.", y= maxy//2 + 1, stil= curses.color_pair(4), clear= False)
        else:
            yazci(0.4, f"{hedef} {hasar} hasar aldı.", stil= curses.color_pair(4), clear= False)


    def __call__(self):
        return oyuncu.isim
    def __str__(self):
        return oyuncu.isim





class Dusman:
    """ Düşmanlar için ortak sınıf.
    """
    def __init__(self, can, atak):
        self.can = can
        self.atak = atak

    def saldiri(self):
        hasar = self.atak + randint(0, self.atak * 15 // 100)
        oyuncu.can -= hasar
        if oyuncu.can < 0:
            oyuncu.can = 0
        yenile()
        pencere()
        if oyuncu.can == 0:
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.COLOR_RED, getch=False, clear= False)
            yazci(5, "ÖLDÜN", y= maxy//2 + 1, stil= curses.COLOR_RED, clear= False)
        else:
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.COLOR_RED, clear= False)


class Bucur(Dusman):
    """ Bücür isimli düşmanın sınıfı. Nesneler "Bücür" ismine döner.
        20 canları vardır.
    """
    def __init__(self):
        self.isim = "Bücür"
        super().__init__(can= 20, atak= 7)
    
    def __str__(self):
        return self.isim
    


class Silah:
    def __init__(self, isim, atakguc):
        self.isim = isim
        self.atakguc = atakguc
    
    def __str__(self):
        return self.isim

class Sopa(Silah):
    """ 10 Atak güçlü silah
    """
    def __init__(self):
        super().__init__("Sopa", 10)
    








### Fonksiyolar ###



def pencere():
    """ Oyuncunun menüdeki bilgilerinin yenilenmesini sağlar
        Menüdeki bilgiler her değiştiğinde çağırılmalı.
    """
    global win_isim, win_can, win_atak, win_sans, win_envanter, win_env
    try:
        win_isim.destroy()
        win_can.destroy()
        win_atak.destroy()
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
    










kalp = "❤ " # u\2764

def yazc(metin:str, y:int= None, x:int= None, stil= curses.COLOR_WHITE) -> None:
    """ Verilen metinin her harfi çok bir kısa süre beklenerek yazılır.
        Yer belirtilmez ise terminalin ortasına yazdırılır.
        "@" karakterinin olduğu yere oyuncunun ismi yazılır.
        "£" karakterinin olduğu yere ❤ karakteri konur
    """
    y = maxy//2 if y==None else y
    if x == None:
        x = maxx//2 - len(metin)//2
        if "@" in metin:  # Eğer x belirtilmemişse oyuncu ismi uzunluğu hesaba katılarak orta bulunur
            x -= metin.count("@") * (len(oyuncu()) -1)

    metin = metin.replace("£", kalp)

    for i in metin:
        if i == "@":
            yazc(oyuncu(), y, x, stil= curses.color_pair(1))
            x += len(oyuncu())
            continue
        stdscr.addstr(y, x, i, stil)
        stdscr.refresh()
        x += 1
        sleep(.04)


def yazci(sure=1, *args, y=None, x=None, stil= curses.COLOR_WHITE, clear=True, getch=True) -> None | str:
    """ Verilen parametreler hepsinin sonunda süre beklenecek şekilde yazdırılır.
        Varsayılan olarak terminalin ortasına yazdırılır.
        İlk parametre curses'in objesi için, ikinci parametre (sure) aralarda ve sonda beklenecek süre (saniye)
        Sonraki isimsiz parametreler yazılacak metinler.
        stil parametresi curses color pairleri için.
        clear True ise kendisinden önceki yazılar silinir.
        getch True metinler yazıldıktan sonra herhangi bir karakter girilmesini beklenip beklenmemesini ifade eder
    """
    if clear: stdscr.clear() # terminali temizle

    uzunluklar = list()
    for metin in args:  # girilen metinlerin uzunluklarını toplam metnin ortasını bulmak için al
        uzunluk = len(metin)
        if "@" in metin:
            uzunluk += metin.count("@") * (len(oyuncu()) - 1)
        uzunluklar.append(uzunluk)

    orta = sum(uzunluklar)
    # y ve x belirlenmediyse terminalin ortası olarak al
    y = maxy//2 if y == None else y
    x = maxx//2 - orta//2 if x == None else x

    for i, uzunluk in enumerate(uzunluklar): # girilen her metnin sonunda 'sure' kadar beklenecek şekilde yaz
        yazc(args[i], y, x, stil=stil)
        x += uzunluk
        sleep(sure)
    if getch:
        stdscr.addstr(chr(187))
        return stdscr.getch()
    else:
        return None


def diyalog(*metinler):
    stdscr.clear()
    for i, metin in enumerate(metinler):
        yazci(.5, metin, y= maxy//2+i, stil= diy, getch= False, clear= False)
    stdscr.addstr(chr(187))
    stdscr.getch()



def sor(soru: str, secenekler: tuple, stil= curses.COLOR_WHITE, clear= True) -> str:
    """ Soru string olarak verilir
        Seçenekler string olarak bir tuple içinde verilir, seçenekler tek bir karakterden oluşmalı ("1", "2") gibi
        Seçeneklerden birisi seçilene kadar bir şey yapılmaz
        Seçeneklerden birisi seçildiğinde (Enter'a basılmasına gerek yoktur) fonksiyon cevaba döner
    """
    curses.noecho()
    cevap = yazci(0.1, soru, stil= stil, clear= clear)
    while all([cevap != ord(i) for i in secenekler]): # seçeneklerden birisi seçildiğinde sonlanan döngü
        cevap = stdscr.getch()
    return chr(cevap)




def yenile(ilk=False):
    """ Savaş sırasında ekran temizlenip oyuncunun ve düşmanların canları gösterilir
        Düşmanın canı 0 ise canı gösterilmez ve mevcut savaş için düşman listesinden çıkarılır
    """
    stdscr.clear()

    savasanlar = f":{kalp}{oyuncu.can}" # bundan hemen önce oyuncu ismi yazdırılacak

    for sira, dusman in enumerate(dusmanlar):
        # enumerate kullandığımızdan ötürü for döngüsü içinde liste uzunluğu değişimi bizi etkilemedi
        if dusman.can == 0:
            del dusmanlar[sira]
            continue
        savasanlar += f"  {dusman}:{kalp}{dusman.can}"

    if ilk:
        yazci(.04, "@" + savasanlar, y= 4, x= 0, clear= False, getch= False)
    else:
        stdscr.addstr(4, 0, oyuncu(), curses.color_pair(1))
        stdscr.addstr(4, len(oyuncu())+1, savasanlar)


dusmanlar = list()
def savas(*_dusmanlar):
    """ Oyuncu savaşa girdiğinde çağrılacak fonksiyon
    """
    global dusmanlar
    savasanlar = ""
    dusmanlar = list(_dusmanlar)

    yenile(ilk=True) # yazım animasyonu için

    while oyuncu.can and any([dusman.can for dusman in dusmanlar]):
        yenile()
        sec = sor("Saldır(1)  Yüce Ağaç Meyvesi Ye(2)", ("1", "2"), clear= False)
        
        if sec == "1":
            if len(dusmanlar) > 1: # Düşmanlar 1'den fazla ise hedef seç
                hedefler = ""
                for sira, dusman in enumerate(dusmanlar, 1):
                    hedefler += f"  {dusman}({sira})"
                yenile()
                indx = sor("Saldır:" + hedefler, (str(i) for i in range(1, len(dusmanlar)+1)), clear= False)
                hedef = dusmanlar[int(indx) - 1]
            else:
                hedef = dusmanlar[0]
            
            oyuncu.saldiri(hedef)
            yenile()
            
            for dusman in dusmanlar:
                dusman.saldiri()
                yenile()


        elif sec == "2":
            yenile()
            try:
                yenilenen = oyuncu.kullan("Yüce Ağaç Meyvesi")
                yazci(0, f"@ canını {yenilenen} kadar yeniledi. ", stil= curses.color_pair(3), clear= False)
            except KeyError:
                yazci(0, "Yüce Ağaç Meyven kalmamış.", stil= curses.color_pair(2), clear= False)
    if oyuncu.can == 0:
        return "lose"
    else:
        return "win"

        
        












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

def Oyna(_stdscr):
    global oyuncu, maxy, maxx, stdscr, diy
    stdscr = _stdscr # global olarak tanımladık ki dışarıdaki fonksiyonları tanımlarken kullanabilelim
    maxy, maxx = stdscr.getmaxyx()  # terminalin o anki max en, boy büyüklüğünü alır
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)      # Oyuncu ismi rengi
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)       # Kırmızı yazı      olumsuz bir şey olduğunda
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)     # Yeşil yazı        genelde yararlı şeylerde
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Mor yazı          hasar verdiğinde
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # Sarı yazı         diyaloglarda
    diy = curses.color_pair(5)      # bunu değişkene aldık çünkü çok kullanabiliriz




    ### Oyun başlar ###

    yazci(1, "Hey", ", sen.", " Sonunda uyandın.", stil= diy)

    while True:
        stdscr.clear()  # Terminal temizlenir.
        curses.echo()   # Kullanıcının cevabının ekranda görünmesi
        soru = "Senin adın nedir? : "
        yazc(soru, y= maxy//2, x=0)
        ad = stdscr.getstr(maxy//2, len(soru), 22).decode('utf-8').strip()  # maksimum 22 karakterlik isim alınır
        karaliste = ["/", "\\", ",", "@", "£", ":", "*", ">", "<", "?", "\"", "|"]

        if not ad or any(i in ad for i in karaliste) or ad.isnumeric():
            yazci(0.5, "Benimle dalga mı geçiyorsun!", " Doğru düzgün söyle.", stil= curses.color_pair(2))
            continue
        break



    oyuncu = Oyuncu(ad) # Oyuncu oluşturuldu
    pencere()   # Oyuncu bilgilerinin menüde gösterilmesi
    

    if f"{ad}.json" in os.listdir():
        cevap = sor("Save dosyası bulundu. Yüklemek ister misin(1) yoksa sıfırdan mı devam(2) edersin?", ("1", "2"), stil= curses.color_pair(3))
        if cevap == "1":
            try:
                with open(f"{oyuncu}.json", 'r') as fff:
                    data = json.load(fff)
                oyuncu.save_yukle(data)
            except:
                yazci(1.25, "Save dosyası yüklenemedi.", stil= curses.color_pair(2))
    oyuncu.save()





    while True:
        ### 1. Bölüm ###
        yazci(2, "1. Bölüm", getch= False)
        
        if oyuncu.bolum == 1:
            yazci(1, "Herkes senin uyanmanı bekliyordu @.", stil= diy)
            stdscr.clear()

            d = sor("Neden?(1)  Neredeyim ben?(2)", ("1", "2"))
            if d == "1":
                diyalog("Bizi kendin ile beraber kurtarabilirsin de ondan.",\
                        "Bücürleri yenersen eğer biz de kurtulabiliriz.",\
                        "Sonuçta Bücürler seni de tutsak ettiler")
            else:
                diyalog("Kafana o taş düştükten sonra Bücürler seni mağaraya getirdiler.",\
                        "Eğer Bücürleri yenersen hepimiz kurtuluruz.")
            yazci(.5, "Etraf karanlık. Önünde bir tutsak topluluğu görüyorsun.")
            
            sor("Bücürler kim?(1)", ("1", ))

            yazci(.7, "Iıı...", " şu çirkin şeyler işte.", " İblislere çalışan.", stil=diy, getch= False)
            yazci(.5, "Onları bir sopayla ancak sen yenebilirsin.", y=maxy//2+1, stil= diy, clear= False)

            sor("Neden ben?(1)", ("1", ))


            diyalog("Çünkü sen kehanetteki elf soyundan gelen savaşçısın.")
            diyalog("Bir diğeri: Elf soyundan gelenlerin hepsinin öldüğünü sanıyordum.")
            diyalog("Evet hepimiz öyle düşünüyordük",\
                    "Fakat başka kim kafasına o büyüklükte bir taş düştükten sonra hayatta kalabilir?")
            diyalog("Ama görünüşe bakılırsa hafızanı kaybetmişsin.")
            diyalog("İblis soyundan gelenler elf soyundan gelenlerin hepsini katlettiler",\
                    "Ama kehanete göre Elf soyundan bir savaşçı hayatta kalacak",\
                    "ve iblislerin hepsini kesip hükümdarlıklarını sonlandıracak.")
            diyalog("Bücür: Abelovulobuleybubinaenaleyh")
            bucur1 = Bucur()
            bucur2 = Bucur()
            bucur3 = Bucur()
            diyalog("Sanırım Bücürlerle savaştığın kısma geldik.",\
                    "Bu Yüce Ağaç Meyvelerini al. İyileşmende yardımcı olacaklar.")
            oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
            oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
            yazci(1, "Yüce Ağaç Meyvesi aldın.", " Savaş sırasında saldırmadan hemen önce kullanabilirsin.")
            yazci(.5, "Görev: Bücürleri yen.")

            yazci(.5, "Bücürlerden biri takılıp düştü.", " 10 hasar aldı.")
            bucur3.can -= 10

            war = savas(bucur1, bucur2, bucur3)
            if war == "lose":
                continue

            yazci(.5, "Görevi tamamladın: Bücürleri yen.")
            oyuncu.sans += 2
            pencere()
            yazci(.5, "2 Şans puanı kazandın.")
            
            
            

            yazci(.5, "evet", stil= diy)




            oyuncu.save()


        elif oyuncu.bolum == 2:
            yazci(2, "2. Bölüm", getch= False)

            oyuncu.save()
        
        elif oyuncu.bolum == 3:
            pass

            oyuncu.save()

        else:
            yazci(2, "Sanırım", " ... ", " kayboldun.")


        oyuncu.save_sil()
        win.destroy()








oyna = threading.Thread(target= lambda: curses.wrapper(Oyna), daemon= True)
oyna.start()

win.mainloop()
