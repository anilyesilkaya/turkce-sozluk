# Modern Türkçe Sözlük
<p align="center">
  <img src="assets/cover.png" alt="Türkçe Sözlük Projesi" width="300">
</p>

## Canlı Önizleme

👉 [Proje Sitesi - sozluk.pro](https://sozluk.pro/)

**Modern Türkçe Sözlük**, açık kaynak kodlu ve LLM dostu bir Türkçe sözlük projesidir.  
Amacı, mevcut çevrim içi sözlüklerden daha hızlı, erişilebilir, estetik ve yapay zekâ tarafından kolay işlenebilir bir sözlük altyapısı sunmaktır.

## Özellikler

- 📖 **Güncel ve kapsamlı** Türkçe kelime veritabanı
- ⚡ **Hızlı erişim**: Harf bazlı ve arama çubuğu ile kelime bulma
- 🎲 **Rastgele kelime** butonu ile keşfetme
- 🌐 **Jekyll tabanlı statik site** — GitHub Pages uyumlu
- 🔍 **LLM uyumlu JSON formatı** ile veri sunumu
- 🎨 Minimal, modern ve mobil uyumlu arayüz

## Kurulum

Bu projeyi yerel ortamda çalıştırmak için:

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/anilyesilkaya/turkce-sozluk.git
   cd turkce-sozluk
   ```

## Proje Yapısı
```
_turkce-sozluk/
├── _terms/               # Her bir kelime için Markdown formatlı içerik dosyaları
├── assets/               # CSS, JS ve medya dosyaları
├── _layouts/             # Sayfa şablonları (default, term vb.)
├── _includes/            # Ortak HTML parçaları (header, footer vb.)
├── assets/terms.json     # JSON formatında kelime listesi
└── index.html            # Ana sayfa
```

## JSON Formatı
Her kelime aşağıdaki yapıda saklanır:
```
{
  "dulda": {
    "lisan": "Türkçe",
    "anlamlar": [
      "Yağmur, güneş ve rüzgârın etkileyemediği gizli, kuytu yer; siper",
      "Birine yapılan himaye"
    ],
    "ozellikler": [
      ["isim", "ağızlardan"],
      ["isim", "ağızlardan", "mecaz"]
    ],
    "ornekler": [
      ["Demirkır, güney tepelerinin duldalarına çektiği atları gece yarısına doğru yeniden ovaya indirdi."],
      ["Yiğit duldasında yiğit saklanır."]
    ],
    "orneklerkaynak": [
      ["Abbas Sayar"],
      ["Karacaoğlan"]
    ]
  }
}
```

## Katkıda Bulunma
1. Fork yapın.

2. Yeni bir branch oluşturun:

```bash
git checkout -b yeni-ozellik
```

3. Değişikliklerinizi yapın ve commit edin:
```bash
git commit -m "Yeni özellik eklendi"
```
4. Pull request gönderin.

## Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Ayrıntılar için LICENSE dosyasına bakın
- Kodlar: [MIT Lisansı](./LICENSE)  
