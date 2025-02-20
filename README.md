# Domain-Search

Domain-Search, bir web sitesindeki JavaScript dosyalarını analiz ederek alt alan adlarını (subdomains) çıkartan bir araçtır. Bu araç, güvenlik testleri, alan adı keşfi ve bilgi toplama süreçlerinde kullanılabilir.

## Özellikler
- Belirtilen bir URL veya bir URL listesi üzerinden alt alan adlarını çıkartma.
- JavaScript dosyalarını indirip analiz ederek alt alan adlarını bulma.
- HTTP istekleri sırasında güvenli olmayan bağlantılar için uyarıları devre dışı bırakma.
- Çıkarılan alt alan adlarını bir dosyaya kaydetme.
- Komut satırında ayrıntılı bilgi modu (verbose) ile çalışabilme.

## Gereksinimler
- Python 3.x
- `argparse`
- `requests`
- `beautifulsoup4`
- `urllib3`
- `Color_Console` (renkli çıktılar için)

## Kurulum
1. Bu projeyi klonlayın:
   ```bash
   git clone https://github.com/enesdq/domain-Search.git
   cd Domain-Search
   ```
2. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım
### Temel Kullanım
Bir URL üzerindeki alt alan adlarını taramak için:
```bash
python3 domain-search.py -u example.com
```

Birden fazla URL içeren bir dosyayı taramak için:
```bash
python3 domain-search.py -f urls.txt
```

Sonuçları bir dosyaya kaydetmek için:
```bash
python3 domain-search.py -u example.com -o output.txt
```

### Verbose Modu
Alt alan adlarını tararken detaylı bilgi almak için:
```bash
python3 domain-search.py -u example.com -v
```

## Çalışma Mantığı
1. Script tarama: Belirtilen URL üzerinde HTML içindeki `<script>` etiketleri bulunur.
2. Alt alan adı çıkarma: Her bir JavaScript dosyası regex kullanılarak analiz edilir ve alt alan adları çıkarılır.
3. Sonuçların kaydedilmesi: Bulunan alt alan adları, tekrarlar olmadan listeye eklenir ve belirtilen dosyaya kaydedilir.

## Örnek Çıktı
```plaintext
Subdomains Found:
api.example.com
cdn.example.com
blog.example.com
```

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakabilirsiniz.
