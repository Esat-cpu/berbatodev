Tek python dosyası olarak istendiğinden tek bir python dosyası olacak şekilde yazılmıştır.

Python versiyonu en az 3.10 olmalıdır.

Şu modüller kullanılmıştır. Kurulu değil ise kurunuz:

windows için: windows-curses==2.4.1
linux/unix için kurmanıza gerek yok, zaten yüklüdür.

Oyun terminalde başlatılmalı ve terminalin boyutlarının en az 100x25 olması tavsiye edilmektedir. 
Oyun başladıktan sonra terminalin büyüklüğünü değiştirmeyiniz.
Oyun sırasında oluşturulan json dosyalarını oyun boyunca silmeyiniz veya değiştirmeyiniz.
Oyun çalışırken terminale yazılar yazılırken herhangi bir tuşa basmayınız.
"»" karakterini gördüğünüzde eğer soru sorulmuyorsa herhangi bir tuşa basarak ilerleyebilirsiniz(soruluyorsa da seçeneklerden birini seçin)
"»" karakterini görmeden tuşlara basmayınız.
Aksi halde hatalarla karşılaşabilirsiniz.

Oyun 4 bölümden oluşur.
Oyuncu önce ismini belirler. Diyaloglarda karakterinin söyleyeceği seçenekleri seçer.
Seçtiği seçeneklerle hikayeye yön verebilir.
Yan görevler yapar ve güçlenir.
Karşısına çıkan düşmanlarla savaşır.

Seçenekler şöyle gösterilir: seçenek(1)  seçenek(2)  ...
Seçmek istedğiniz seçeneğin sonundaki parantezdeki sayıyı tuşlayın. Sonrasında Enter'a basmanıza gerek yok.
"»" karakterini görmeden herhangi bir tuşa bastıysanız sonraki "»" karakterinde beklendiğini görene kadar bekleyiniz.
