# Çağdaş Türkçe Sözlük

**Çağdaş Türkçe Sözlük**, açık kaynak kodlu, hızlı ve LLM-dostu bir Türkçe sözlük projesidir.

Projenin amacı; Türkçe kelimelere erişimi kolaylaştıran, modern bir kullanıcı deneyimi sunan ve aynı zamanda yapay zekâ uygulamaları tarafından kolayca işlenebilen açık bir sözlük altyapısı oluşturmaktır.

<p align="center">
  <img src="assets/cover.png" alt="Çağdaş Türkçe Sözlük" width="300">
</p>

## 🌐 Canlı Site

👉 [sozluk.online](https://sozluk.online)

## ✨ Özellikler

* 📖 Güncel ve kapsamlı Türkçe kelime veritabanı
* 🔍 Arama çubuğu ve harf bazlı gezinme
* 🎲 Rastgele kelime keşfi
* ⚡ Hızlı, statik ve mobil uyumlu arayüz
* 🌐 Jekyll tabanlı yapı ve GitHub Pages desteği
* 🤖 LLM ve diğer yazılım uygulamaları için JSON tabanlı veri erişimi
* 🎨 Minimal ve modern kullanıcı arayüzü

## 🚀 Yerel Kurulum

Depoyu klonlayın:

```bash
git clone https://github.com/anilyesilkaya/turkce-sozluk.git
cd turkce-sozluk
```

Ardından projeyi standart Jekyll geliştirme ortamınızda çalıştırabilirsiniz.

## 📁 Proje Yapısı

```text
_turkce-sozluk/
├── _terms/               # Kelimeler için Markdown içerik dosyaları
├── assets/               # CSS, JavaScript ve medya dosyaları
├── _layouts/             # Sayfa şablonları
├── _includes/            # Ortak HTML bileşenleri
├── assets/terms.json     # JSON formatında kelime listesi
└── index.html            # Ana sayfa
```

Bu yapı, sözlük verisinin web uygulamaları, araştırma araçları ve LLM tabanlı sistemler tarafından doğrudan işlenebilmesini kolaylaştırır.

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak için:

1. Depoyu fork edin.
2. Yeni bir branch oluşturun:

```bash
git checkout -b yeni-ozellik
```

3. Değişikliklerinizi yapın ve commit edin:

```bash
git commit -m "Yeni özellik eklendi"
```

4. Pull request gönderin.

## 📄 Lisans ve Veri Kaynağı

Proje kodu **MIT Lisansı** ile lisanslanmıştır. Ayrıntılar için [LICENSE](./LICENSE) dosyasına bakabilirsiniz.

Sözlük verisi, `v12.gts.json.tar.gz` arşivindeki JSON dosyasından alınmıştır:

* **Kaynak:** [ogun/guncel-turkce-sozluk](https://github.com/ogun/guncel-turkce-sozluk)
* **Depodaki konum:** `sozluk/v12/v12.gts.json.tar.gz`
* **Erişim tarihi:** 15 Ağustos 2025
* **Veri lisansı:** Orijinal deponun lisans koşullarına tabidir.

---

**Çağdaş Türkçe Sözlük**
Açık, hızlı ve makine tarafından okunabilir Türkçe sözlük altyapısı.
