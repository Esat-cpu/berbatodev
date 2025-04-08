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
            json.dump(self.data, fff, indent= 4)

    def save_sil(self):
        try: os.remove(f"{self.isim}.json")
        except: pass

    def save_yukle(self):
        try:
            with open(f"{self()}.json", 'r') as fff:
                data = json.load(fff)
            self.bolum = data["bolum"]
            self.envanter = data["envanter"]
            self.can = data["can"]
            self.sans = data["sans"]
            if data["Silah"] == "Sopa":
                self.envantere_ekle(Sopa())
            elif data["Silah"] == "Paslı Kılıç":
                self.envantere_ekle(Pasli_Kilic())
            elif data["Silah"] == "Katana":
                self.envantere_ekle(Katana())
            elif data["Silah"] == "Rivers Of Blood":
                self.envantere_ekle(RiversOfBlood())
        except:
            yazci(1.25, "Save dosyası yüklenemedi.", stil= curses.color_pair(2))
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
            Eşya Yüce Ağaç Meyvesi ise can yeniler
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
            b = self.sans - 15
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
            yenile()
        pencere()
        return rtrn


    def saldiri(self, hedef) -> None:
        """ Hedefin canı düşürülür.
            Ekran temizlenmez.
            Verilen hasarın bilgisi yazdırılır.
        """
        ust_h = self.atak * self.sans // 100
        alt_h = self.atak * (self.sans - 45) // 100 # şans 45'ten fazla ise min ek hasar artar
        alt_h = 0 if alt_h < 0 else alt_h # ek hasar eksi çıkmaz.
        hasar = self.atak + randint(alt_h, ust_h)
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
        return self.isim
    def __str__(self):
        return self.isim




### Düşman Sınıfları ###
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
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.color_pair(2), getch=False, clear= False)
            yazci(5, "ÖLDÜN", y= maxy//2 + 1, stil= curses.color_pair(2), clear= False)
        else:
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.color_pair(2), clear= False)
        
    def __str__(self):
        return self.isim


class Bucur(Dusman):
    """ 20 canları, 7 atak güçleri vardır.
    """
    def __init__(self):
        self.isim = "Bücür"
        super().__init__(can= 20, atak= 7)
 
    
class Gardiyan(Dusman):
    """ 30 canları, 15 atak güçleri vardır.
    """
    def __init__(self):
        self.isim = "Gardiyan"
        super().__init__(can= 30, atak= 15)


class Belial(Dusman):
    """ 110 canı, 20 atak gücü vardır
    """
    def __init__(self):
        self.isim = "Belial"
        super().__init__(can= 110, atak= 20)


class M(Dusman):
    """ 50 canı, 16 atak gücü vardır
    """
    def __init__(self):
        self.isim = "M"
        super().__init__(can= 50, atak= 16)


class Shinobi(Dusman):
    """ 50 canı, 40 atak gücü vardır
    """
    def __init__(self):
        self.isim = "Shinobi"
        super().__init__(can= 50, atak= 40)


class Sparda(Dusman):
    """ 120 canı 40 atak gücü vardır
    """
    def __init__(self):
        self.isim = "Sparda"
        super().__init__(can= 120, atak= 40)


class Glorfindel(Oyuncu):
    """ Final Boss
    """
    def __init__(self):
        super().__init__("Glorfindel")
        self.sans = 100
    
    def save(): ...
    def save_sil(): ...
    def save_yukle(): ...
    def kullan(): ...

    def saldiri(self) -> None:
        """ Oyuncunun canı düşürülür.
            Ekran temizlenmez.
            Verilen hasarın bilgisi yazdırılır.
        """
        while self.can <= 60:
            try:
                self.can_yenile()
            except KeyError:
                break

        ust_h = self.atak * self.sans // 100
        alt_h = self.atak * (self.sans - 45) // 100 # şans 45'ten fazla ise min ek hasar artar
        alt_h = 0 if alt_h < 0 else alt_h # ek hasar eksi çıkmaz.
        hasar = self.atak + randint(alt_h, ust_h)
        oyuncu.can -= hasar
        if oyuncu.can < 0:
            oyuncu.can = 0
        yenile()
        if oyuncu.can == 0:
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.color_pair(2), getch= False, clear= False)
            yazci(0.4, "ÖLDÜN", y= maxy//2 + 1, stil= curses.color_pair(2), clear= False)
        else:
            yazci(0.4, f"@ {hasar} hasar aldı.", stil= curses.color_pair(2), clear= False)
        
    def can_yenile(self) -> None:
        """ Can yenileme için
        """
        esya = "Yüce Ağaç Meyvesi"
        if esya in self.envanter:
            self.envanter[esya] -= 1
            if self.envanter[esya] == 0:
                del self.envanter[esya]
        else:
            raise KeyError
        
        self.can += 40
        if self.can > 100:
            self.can = 100
        yenile()
        yazci(0, "Glorfindel canını 40 kadar yeniledi.", stil= curses.color_pair(2), clear= False)



### Silah Sınıfları ###
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

class Pasli_Kilic(Silah):
    """ 16 Atak güçlü silah
    """
    def __init__(self):
        super().__init__("Paslı Kılıç", 16)

class Katana(Silah):
    """ 20 atak güçlü silah
    """
    def __init__(self):
        super().__init__("Katana", 20)

class RiversOfBlood(Silah):
    """ 30 atak güçlü silah
    """
    def __init__(self):
        super().__init__("Rivers Of Blood", 30)














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
    win_sans = tk.Label(win, text= f"Şans: %{oyuncu.sans}", bg= "slategrey", fg= "#ddd310")
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
            x -= metin.count("@") * (len(oyuncu()) -1) // 2

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
        İlk parametre (sure): aralarda ve sonda beklenecek süre (saniye)
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
        stdscr.refresh()
        return stdscr.getch()
    else:
        return None


def diyalog(*metinler):
    stdscr.clear()
    for i, metin in enumerate(metinler):
        yazci(.5, metin, y= maxy//2+i, stil= diy, getch= False, clear= False)
    stdscr.addstr(chr(187))
    stdscr.refresh()
    stdscr.getch()

def hafiza():
    stdscr.clear()
    for i in range(maxy):
        stdscr.addstr(i, 0, "0"*(maxx-1))
    stdscr.refresh()



def sor(soru: str, secenekler: tuple, stil= curses.COLOR_WHITE, clear= True) -> str:
    """ Soru string olarak verilir
        Seçenekler string olarak bir tuple içinde verilir, seçenekler tek bir karakterden oluşmalı ("1", "2") gibi
        Seçeneklerden birisi seçilene kadar bir şey yapılmaz
        Seçeneklerden birisi seçildiğinde (Enter'a basılmasına gerek yoktur) fonksiyon cevaba döner
    """
    curses.noecho()
    cevap = yazci(0.07, soru, stil= stil, clear= clear)
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
        if dusman.can == 0:
            del dusmanlar[sira]
            continue
        savasanlar += f"  {dusman}:{kalp}{dusman.can}"

    if ilk:
        yazci(.04, "@" + savasanlar, y= 4, x= 0, clear= False, getch= False)
    else:
        stdscr.addstr(4, 0, oyuncu(), curses.color_pair(1))
        stdscr.addstr(4, len(oyuncu()), savasanlar)
        stdscr.refresh()


dusmanlar = list()
def savas(*_dusmanlar):
    """ Oyuncu savaşa girdiğinde çağrılacak fonksiyon
    """
    global dusmanlar
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
                yazci(0, f"@ canını {yenilenen} kadar yeniledi.", stil= curses.color_pair(3), clear= False)
            except KeyError:
                yazci(0, "Yüce Ağaç Meyven kalmamış.", stil= curses.color_pair(2), clear= False)
    if oyuncu.can == 0:
        oyuncu.save_yukle()
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
        soru = "Senin adın nedir? »: "
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
            oyuncu.save_yukle()
    oyuncu.save()























    while True:
        if oyuncu.bolum == 1:
            ### 1. Bölüm ###
            yazci(2, "1. Bölüm", getch= False)


            yazci(1, "Herkes senin uyanmanı bekliyordu @.", stil= diy)
            stdscr.clear()

            d = sor("'Neden?'(1)  'Neredeyim ben?'(2)", ("1", "2"))
            if d == "1":
                diyalog("Bizi kendin ile beraber kurtarabilirsin de ondan.",\
                        "Bücürleri yenersen eğer biz de kurtulabiliriz.",\
                        "Sonuçta Bücürler seni de tutsak ettiler")
            else:
                diyalog("Sen o uçurumdan düştükten sonra Bücürler seni mağaraya getirdiler.",\
                        "Eğer Bücürleri yenersen hepimiz kurtuluruz.")
            yazci(.5, "Etraf karanlık. Önünde bir tutsak topluluğu görüyorsun.")
            
            sor("'Bücürler kim?'(1)", ("1", ))

            yazci(.7, "Iıı...", " şu çirkin şeyler işte.", " İblislere çalışan.", stil=diy, getch= False)
            yazci(.5, "Onları bir sopayla ancak sen yenebilirsin.", y=maxy//2+1, stil= diy, clear= False)

            sor("'Neden ben?'(1)", ("1", ))


            diyalog("Çünkü sen kehanetteki elf soyundan gelen savaşçısın. Bir elf ")
            diyalog("Bir diğeri: Elf soyundan gelenlerin hepsinin öldüğünü sanıyordum.")
            diyalog("Evet hepimiz öyle düşünüyorduk",\
                    "Fakat başka kim o uçurumdan düştükten sonra hayatta kalabilir?",\
                    "Hem bakın, bir elf kolyesi takıyor.")
            diyalog("Ama görünüşe bakılırsa hafızanı kaybetmişsin.")
            diyalog("İblis soyundan gelenler elf soyundan gelenlerin hepsini katlettiler",\
                    "Ama kehanete göre Elf soyundan bir savaşçı hayatta kalacak",\
                    "ve iblisleri kesip hükümdarlıklarını sonlandıracak.")
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
            oyuncu.sans += 10
            pencere()
            yazci(.7, "Şansın %10 arttı.")
            
            diyalog("Gördünüz mü o olduğunu söylemiştim")

            sor("'Sanırım sana iki meyve borcum var.'(1)", ("1", ))
            diyalog("Yüce Ağaç Meyveleri insanları iyileştirmez.",\
                    "Sadece Elf soyundan gelenler için oldukça faydalıdır.",\
                    "O yüzden dert etme.",\
                    "Ama dikkat et iblis soyundan olanların eline geçmesin.",\
                    "Onlarda da Elfler kadar olmasa da işe yaradığını duymuştum.")

            diyalog("Biz şimdi kasabamıza geri dönüyoruz. Daha fazla Bücür gelmeden gitmeliyiz.")
            diyalog("Sen de Güney tarafına doğru ilerleyebilirsin.",\
                    "İblis soyundan gelen 3 savaşçıdan birinin kalesi ordadır.")

            sor("'Peki, ben o tarafa gidiyorum.'(1)", ("1", ))
            diyalog("Hoşçakal savaşçı! Umarım yine karşılaşırız.")
            yazci(.5, "Bir daha birbirinizi hiç görmediniz...")
            d = sor("Yola çık(1)  Bücürlerin cesetlerini ara(2)", ("1", "2"))
            
            if d == "2":
                oyuncu.envantere_ekle(Pasli_Kilic())
                yazci(.5, "Paslı Kılıç buldun.")
            yazci(.5, "İlk İblis Savaşçının Kalesine doğru yola çıktın.")

            oyuncu.bolum += 1
            oyuncu.save()
            yazci(.1, "Kaydediliyor...", getch= False)








        elif oyuncu.bolum == 2:
            ### 2. Bölüm ###
            stdscr.clear()
            stdscr.refresh()
            sleep(1.5)
            yazci(2, "2. Bölüm", getch= False)

            yazci(.5, "İblisleri kesmek üzere yola çıktın.")
            yazci(0, "Uyanalı 1 saat oldu.", getch=False)
            yazci(.5, "Hafızasını kaybetmiş birine göre biraz büyük bir amaç edindin.", y= maxy//2+1, clear= False)
            yazci(.5, "Elf kolyene bakıyorsun ve cesaretleniyorsun.")

            yazci(.5, "Önünde 3 iblisten ilkinin kalesi var. Biraz daha batıda bir kulübe var.", y= maxy//2-1)
            d = sor("Kaleye devam et(1)  Önce kulübeye git(2)", ("1", "2"), clear= False)

            if d == "1":
                pass
            elif d == "2":
                yazci(.5, "Kulübeye girdin. İçeride birisi var. Sana tanıdık geldi")
                diyalog("Hey, burada ne yapıyorsun")
                hafiza()
                sleep(.1)
                yazci(1, "Hatırlıyorsun.", getch= False)
                sor("'Marston?'(1)", ("1",))
                diyalog("Marston: @, Seni görmeyeli uzun zaman oldu.")
                sor("'Bu kaledeki İblisi kesmeye geldim.'(1)", ("1",))
                diyalog("Marston: Hmm...",\
                        "Soru sormayacağım, beni aşan bir işe benziyor",\
                        "Kaleye girmek için önce kapıdaki gardiyanları geçmen gerekiyor.")
                diyalog("Eğer benim için bir iyilik yapmayı kabul edersen,",\
                        "Sana gardiyanları geçmen için gerekli olan parolayı söylerim",\
                        "Onlarla savaşırım diyorsan sen bilirsin.")
                d = sor("Kabul et(1)  Reddet(2)", ("1", "2"))
                marston_gorev = 0
                marston_gorev_sonuc = 0
                
                if d == "1":
                    marston_gorev = 1
                    diyalog("Harika!",\
                            "Görevini açıklıyorum:")
                    diyalog("Kaleye girdiğinde bir beyaz bir kırımızı kapı göreceksin.",\
                            "Beyaz olanda benim arkadaşım var.",\
                            "Kırmızı olanda ise Yüce Ağaç Meyveleri.")
                    diyalog("Yüce Ağaç Meyvelerini alabilirsin fakat bir tanesini arkadaşıma ver.",\
                            "Orada ona yeterli yemek vermiyorlar.")
                    diyalog("Bu kadar.", "Parola Şafak")
                    yazci(.5, "Görev: Marston'un arkadaşına Yüce Ağaç Meyvesi ver.")
                else:
                    diyalog("Öyle olsun.",\
                            "Bol şans")
                    
                yazci(.5, "Kulübeden çıktın ve kaleye doğru ilerledin.")
            yazci(.4, "Gardiyanlar seni durdurdu")

            diyalog("Dur! Parola?")
            if marston_gorev:
                d = sor("'Bilmiyorum ama geçmem lazım.'(1)  'Şafak'(2)", ("1", "2"))
            else:
                d = sor("'Bilmiyorum ama geçmem lazım.'(1)", ("1",))
            
            gardiyan1 = Gardiyan()
            gardiyan2 = Gardiyan()

            if d == "1":
                diyalog("Geç bakalım geçebiliyorsan!")
                war = savas(gardiyan1, gardiyan2)
                if war == "lose":
                    continue

            elif d == "2":
                diyalog("Geç bakalım.")
            
            yazci(.5, "Kaleye girdin.")
            yazci(.5, "Önünde yukarı çıkan merdivenler,", getch= False)
            yazci(.5, "sağında beyaz bir kapı,", y= maxy//2+1, clear= False, getch= False)
            yazci(.5, "solunda kırmızı bir kapı var.", y= maxy//2+2, clear= False)

            meyve_alindi = 0
            while (d:= sor("Merdivenler(1)  Kırmızı Kapı(2)  Beyaz Kapı(3)", ("1", "2", "3"))) != "1":
                if d == "2":
                    if not meyve_alindi:
                        yazci(.5, "Önünde Yüce Ağaç Meyveleri var.")
                        d1 = sor("Geri dön(1)  Yüce Ağaç Meyvelerini al(2)", ("1", "2"))
                    else:
                        yazci(.5, "Oda boş.")
                        d1 = sor("Geri dön(1)", ("1", ))
                    
                    if d1 == "1":
                        continue
                    elif d1 == "2":
                        meyve_alindi = 1
                        for i in range(5):
                            oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
                        yazci(.5, "5 Yüce Ağaç Meyvesi aldın.")
                elif d == "3":
                    yazci(.5, "İçeride birisi var. Oturmuş bekliyor.")
                    
                    if meyve_alindi and not marston_gorev_sonuc:
                        d1 = sor("Geri dön(1)  Yüce Ağaç Meyvesini ver(2)", ("1", "2"))
                        if d1 == "1":
                            continue
                        elif d1 == "2":
                            marston_gorev_sonuc = 1
                            oyuncu.envanter["Yüce Ağaç Meyvesi"] -= 1
                            pencere()
                            yazci(.5, "Görevi Tamamladın: Marston'un arkadaşına Yüce Ağaç Meyvesi ver.")
                            oyuncu.sans += 20
                            pencere()
                            yazci(.7, "Şansın %20 arttı.")
                            continue
                    elif meyve_alindi and marston_gorev_sonuc:
                        yazci(.4, "O kişi hala orda duruyor.")
                    sor("Geri dön(1)", ("1", ))
            
            yazci(.5, "Merdivenlerden çıktın.")

            yazci(.5, "İblisi gördün.")
            hafiza()
            sleep(.1)
            yazci(.5, "Belial!", stil= curses.color_pair(2))
            belial = Belial()
            diyalog("Belial: Sen! Neden buradasın? Canına mı susadın!")
            d = sor("Seninkini almaya geldim(1)  Kilo mu aldın sen?(2)", ("1", "2"))

            if d == "1":
                diyalog("Bakalım kim kimin canını alıyor!")
            elif d == "2":
                diyalog("Seni yendikten sonra bir ziyafet daha çekeceğim")

            war = savas(belial)
            if war == "lose":
                continue
            
            yazci(.4, "Senin böyle olacağın belliydi...", stil= diy, getch= False)
            yazci(.4, "'Requiescat in pace.'")
            yazci(.4, "Bunu dedin ama ne demek olduğunu hatırlamıyorsun.")

            yazci(.4, "Bu tarafa bakan pencere çok yüksek değil, penereden indin.")
            
            if marston_gorev and not marston_gorev_sonuc:
                yazci(.4, "Marston'u gördün.")
                diyalog("Bana ihanet etmemeliydin @!")
                marston = M()
                marston.isim = "Marston"
                war = savas(marston)
                if war == "lose":
                    continue
            
            yazci(.4, "Sıradaki kaleye doğru yola çıktın.")

            oyuncu.bolum += 1
            oyuncu.save()
            yazci(.1, "Kaydediliyor...", getch= False)

















        elif oyuncu.bolum == 3:
            ### 3. Bölüm ###
            stdscr.clear()
            stdscr.refresh()
            sleep(1.5)
            yazci(2, "3. Bölüm", getch= False)

            yazci(.4, "İlk iblisini öldürdün.")
            yazci(.4, "Hafızanı kaybettikten sonra yani")
            yazci(.4, "Belki de önceden onlarcasını öldürmüşsündür.")
            yazci(.4, "Bilmiyorsun, sadece içinde bir huzursuzluk var.")
            yazci(.5, "Elf kolyene bakıyorsun ve cesaretleniyorsun.")

            
            yazci(.4, "Bir sandık buldun.", "Üstünde bir bilmece yazıyor.")
            d = sor("İblis? 111(1) 222(2) 333(3) 444(4) 555(5) 666(6) 777(7)", ("1", "2", "3", "4", "5", "6", "7"))
            if d == "6":
                yazci(.4, "Sandık açılıyor.")
                for i in range(5):
                    oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
                yazci(.4, "5 tane Yüce Ağaç Meyvesi aldın.")
            else:
                yazci(.4, "Bilemedin.")


            yazci(.4, "İkinci kale karşında duruyor.")
            yazci(.4, "Burayı koruyan bir kişi var sadece")
            yazci(.4, "İyi kılıç kullanan birine benziyor.")

            shinobi = Shinobi()

            war = savas(shinobi)

            if war == "lose":
                continue
            
            d = sor("Kaleye gir(1)  Shinobinin üstünü ara(2)", ("1", "2"))

            if d == "2":
                oyuncu.envantere_ekle(Katana())
                yazci(.4, "Katana buldun!")

            yazci(.4, "Kaleye girdin.")

            hizmetli_gorev = 0
            hizmetli_gorev_sonuc = 0
            hizmetli_item = 0

            yazci(.4, "Kalenin hizmetlisi kadın rafların tozunu alıyor.", getch= False)
            yazci(.4, "Sağında turuncu bir kapı, solunda siyah bir kapı var.", y= maxy//2+1, clear= False)

            turuncu_kapi = 0
            siyah_kapi = 0

            while True:
                if not hizmetli_gorev_sonuc:
                    d = sor("Siyah kapı(1)  Turuncu kapı(2)  Kadın ile konuş(3)", ("1", "2", "3"))
                else:
                    d = sor("Siyah kapı(1)  Turuncu kapı(2)", ("1", "2"))
                
                if d == "1":
                    if not siyah_kapi:
                        yazci(.4, "Kapıdan girdin ve merdivenlerin burada olduğunu gördün")
                        yazci(.4, "Fakat iki gardiyan burada bekliyor.")
                        gardiyan1 = Gardiyan()
                        gardiyan2 = Gardiyan()

                        war = savas(gardiyan1, gardiyan2)
                        if war == "lose":
                            break
                        
                        yazci(.4, "Gardiyanların birinden bir kalem düştü.")
                        oyuncu.envantere_ekle("Kalem")
                        hizmetli_item = 1
                        yazci(.4, "Kalemi aldın.")
                        siyah_kapi = 1

                    d2 = sor("Merdivenlere devam et(1)  Geri dön(2)", ("1", "2"))

                    if d2 == "1":
                        yazci(.4, "Kadın seni durdurdu.", "Sana neden bu kadar çabaladığını sordu.")
                        diyalog("Kadın: Evet öyle sordum.")
                        yazci(.3, "Hafızasını kaybetmiş birisi için bunu açıklamak zor.")
                        yazci(.7, "Düşünüyorsun")
                        hafiza()
                        sleep(.1)
                        yazci(.5, "Look", ", if you had", " one shot", " or one opportunity", getch= False)
                        yazci(.5, "to seize everything you ever wanted", " in one moment", " would you capture it", ", or just let it slip?", y= maxy//2+1, clear= False)

                        yazci(0, "Kadın: ... Dur bir dakika bu Eminem deği", getch=False, stil= diy)
                        break
                    elif d2 == "2":
                        continue

                elif d == "2":
                    if not turuncu_kapi:
                        yazci(.4, "Yüce Ağaç Meyveleri görüyorsun")
                        d1 = sor("Geri dön(1)  Yüce Ağaç Meyvelerini al(2)", ("1", "2"))
                    else:
                        yazci(.4, "Sadece yerde yatan Bücürler...")
                        d1 = sor("Geri dön(1)", ("1", ))
                    
                    if d1 == "1":
                        continue
                    elif d1 == "2":
                        turuncu_kapi = 1
                        for i in range(10):
                            oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
                        yazci(.4, "10 meyve aldın ve birden Bücürler saklandıkları yerlerden çıktı.")

                        bucur1, bucur2, bucur3 = Bucur(), Bucur(), Bucur()
                        war = savas(bucur1, bucur2, bucur3)

                        if war == "lose":
                            break
                        turuncu_kapi = 1

                elif d == "3":
                    diyalog("Kadın: Keşke kardeşime mektup yazabileceğim bir kalemim olsaydı.")
                    
                    if not hizmetli_gorev:
                        yazci(.4, "Görev: Kadına bir kalem bul.")
                        hizmetli_gorev = 1
                    
                    if hizmetli_item:
                        sor("Kalemi ver(1)", ("1", ))
                        oyuncu.kullan("Kalem")
                        yazci(.4, "Görev Tamamlandı: Kadına bir kalem bul.")
                        diyalog("Kadın: Çok teşekkür ederim!")
                        yazci(.4, "Kadın sana dua etti.")
                        oyuncu.sans += 45
                        pencere()
                        yazci(.7, "Şansın %45 arttı.")
                        hizmetli_gorev_sonuc = 1


            if war == "lose":
                continue
                
            yazci(.6, "Merdivenlerden çıkıyorsun.")

            sparda = Sparda()

            yazci(.4, "İblis savaşçı orada.")
            hafiza()
            sleep(.1)
            yazci(.5, "Sparda!", stil= curses.color_pair(2))

            diyalog("Sparda: Belial'dan sonra benim için de geleceğini biliyordum.",\
                    "Yazık, beraber tüm bu diyarlara hükmedebilirdik.")
            
            d = sor("Aynı tarafta olmamız çok saçma(1)  Olabilir, ama kehaneti gerçekleştirmem lazım(2)", ("1", "2"))
            
            if d == "1":
                diyalog("Sparda: En azından kehanetin gerçekleşme ihtimali ortadan kalkana kadar!")
            elif d == "2":
                diyalog("Sparda: Sana mı kaldı kehanet? Sonunda sen de öleceksin!")
            
            
            diyalog("Glorfindel ile yaptığın savaş aklını kaçırmana sebep olmuş!")
            hafiza()
            sleep(.1)

            diyalog("Bücürler!")
            bucur1, bucur2 = Bucur(), Bucur()

            war = savas(sparda, bucur1, bucur2)

            if war == "lose":
                continue

            yazci(1, "Bize karşı savaşmamalıydın..", stil= diy, getch= False)
            yazci(.4, "Aklın karışık", ", huzursuz hissediyorsun.")
            yazci(.4, "Düşüncelerini toplamakta zorlanıyorsun.")
            hafiza()
            sleep(.1)
            stdscr.clear()
            stdscr.refresh()
            sleep(.1)
            hafiza()
            sleep(.1)
            yazci(.4, "Son İblis kalesine doğru yola çıkıyorsun. Bu seferki İblisi sorgulamayı düşünüyorsun.")

            oyuncu.envantere_ekle(RiversOfBlood())
            yazci(.4, "Sparda'nın hazinesinde sana uygun bir katana buldun: Rivers Of Blood")
            


            oyuncu.bolum += 1
            oyuncu.save()
            yazci(.1, "Kaydediliyor...", getch= False)
















        elif oyuncu.bolum == 4:
            ### 4. Bölüm ###
            stdscr.clear()
            stdscr.refresh()
            sleep(2)
            yazci(2, "9. Bölüm", stil= curses.color_pair(2), getch= False)
            yazc("Yani...", y= maxy//2-4, x=maxx//2+10)
            sleep(.4)
            yazc("4. Bölüm", y= maxy//2-3, x= maxx//2+10)
            for s, i in enumerate(range(8, -1, -1), 1):
                stdscr.addstr(maxy//2-s, maxx//2-4, str(i), curses.color_pair(2))
                stdscr.refresh()
                sleep(.4)
            hafiza()
            sleep(.2)
            stdscr.clear()
            stdscr.refresh()
            sleep(1)
            
            yazci(1, "Bir ruhu ne tanımlar?", getch= False)
            yazci(.4, "Bazıları ona karanlıkla savaşan, yaşamı için yanan bir kıvılcım der.", y=maxy//2+1, clear= False)
            yazci(.4, "Peki ya sen o İblisleri öldürdüğünde ne hissettin?")
            yazci(.4, "Huzursuzluk.")
            yazci(1, "Elf kolyene bakıyorsun", ", daha da huzursuzlanıyorsun.")

            for i in range(4):
                hafiza()
                sleep(.1)
                stdscr.clear()
                stdscr.refresh()
                sleep(.1)

            yazci(.4, "Kaleye geldin.")
            yazci(.4, "Gardiyanlar ve bücürler var.")
            yazci(.4, "Seni içeri alıyorlar")
            yazci(.4, "İblisi sorgulamak için zaman kaybetmeyeceğin için memnunsun.")
            yazci(.4, "İçeride 6 tane Yüce Ağaç Meyvesi var.")
            for i in range(6):
                oyuncu.envantere_ekle("Yüce Ağaç Meyvesi")
            yazci(.4, "Merdivenden çıkıyorsun.")
            yazci(.4, "Odada kimse yok.")
            hafiza()
            sleep(.1)
            yazci(.4, "Odanın baş köşesinde duran büyük sandalyeye bir alışkanlıkla oturuyorsun.")
            for i in range(5):
                hafiza()
                sleep(.1)
                stdscr.clear()
                stdscr.refresh()
                sleep(.1)
            yazci(.4, "Hatırladın.")

            yazci(1, "3. İblis savaşçı sensin.")

            yazci(.4, "Alt kattan sesler geliyor.")
            yazci(.4, "Tüm gardiyanlar ve bücürler yeniliyor.")
            yazci(.4, "Glorfindel senin ondan çaldığın kolyeyi ve canını almak için geliyor.")

            glorfindel = Glorfindel()

            glorfindel.envantere_ekle(Katana())
            for i in range(5):
                glorfindel.envantere_ekle("Yüce Ağaç Meyvesi")

            diyalog("Glorfindel: @!")
            diyalog("Buraya kadar!",\
                    "Baştaki tek kişi olmak için diğer iblisleri öldürdün.",\
                    "Fakat kehaneti gerçekleştirmek için ben buradayım!")
            
            yazci(0, "Elf ile savaş(1)", y= maxy//2-1, getch= False)
            d = sor("Elfin kazanmasına izin vererek canını ve kolyeyi sun(2)", ("1", "2"), clear= False)


            if d == "1":
                war = savas(glorfindel)

                if war == "lose":
                    yazci(.4, "Böylece Elf son iblisi ortadan kaldırmış oldu.")
                    yazci(.4, "Halklar ona hediyeler sundular ve hep mutlu yaşadılar.")
                    yazci(.4, "Çok da kötü değil", ", değil mi?")

                elif war == "win":
                    yazci(.4, "Elfi öldürdün.")
                    yazci(.4, "Ve artık diyarların hakimi olman için engel kalmamıştı.")
                    yazci(.4, "Ama o kadar iyilik için savaştıktan sonra böyle yapabilir miydin?")
                    yazci(.4, "Kolyene bakıyorsun ve cesaretleniyorsun.")
                    yazci(.4, "Ve İblis savaşçı diyarlara hükmeder.")
            
            elif d == "2":
                yazci(.4, "Glorfindel bu hareketine çok şaşırdı.")
                yazci(.4, "Glorfindel kolyeyi aldı fakat seni öldürmedi.")
                yazci(.4, "Silahını aldı ve sana normal biri gibi yaşama şansı verdi.")
                yazci(.4, "Sen de kimliğini değiştirdin. İnsanlar son iblisin öldüğünü düşündü.")
                yazci(.4, "Seni iblisleri öldürmede Elfe yardım eden bir kahraman olarak tanıdılar.")
                yazci(.4, "Size hediyeler sundular ve hep mutlu yaşadılar.")

            curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
            yazci(0, "SON", stil= curses.color_pair(6))
            yazci(1, "Oyunu oynadığın için teşekkürler!", stil= curses.color_pair(6))
            win.destroy()
            



        else:
            yazci(2, "Sanırım", " ... ", " kayboldun.")
            oyuncu.save_sil()
            break

    win.destroy()



oyna = threading.Thread(target= lambda: curses.wrapper(Oyna), daemon= True)
oyna.start()

win.mainloop()
