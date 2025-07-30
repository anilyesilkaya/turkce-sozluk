# Büyük Dil Modelleri (LLM) Dostu Modern Türkçe Sözlük

Proje demo sayfası: [wwww.sozluk.pro](sozluk.pro)

Günümüzde, büyük dil modellerinin de etkisiyle dillerin önemi katbekat artmış; bu doğrultuda dillere dair araştırmalar da hız kazanmıştır. Bu bağlamda, Türkçe konuşabilen bir dil modelinin temelleri üzerine çalışırken, internette modern, kapsayıcı, kullanışlı, yazılım geliştirmeye elverişli ve estetik bir Türkçe sözlük bulamadım. Buna TDK’nın kendi sözlük sayfası da dâhil, çünkü günümüz Oxford, Cambridge, Merriam-Webster veya Thesaurus sözlüklerinin sunduğu kullanıcı deneyiminin oldukça gerisinde kalıyor. Örneğin:

- Benzer ya da zıt anlamlı kelimelerin sunulmaması,
- Kelimelere dair yeterli örneğin bulunmaması,
- Kelimeler arası ilişkilere dair hiçbir içgörü sunulmaması,
- Dil modelleri üzerinde çalışan araştırmacı ve mühendisler için herhangi bir arayüz olmayışı

gibi nedenlerle, kendi sözlük tasarımımı geliştirmeye karar verdim.

Bu tasarım sürecinde aşağıdaki yol haritasını izlemeyi planlıyorum:

1. TDK sözlük sitesinden (https://sozluk.gov.tr) veriyi otomatik olarak çekme rutini
2. Veriyi işleme
3. Veriyi görselleştirme
4. Kullanıcı arayüzü detaylarının tasarımı

Eğer benzer hisleri paylaşıyorsanız lütfen iletişime geçebilir veya doğrudan katkıda bulunabilirsiniz.

## TDK Sözlük Sitesinden Veri Kazıma

- sozluk.gov.tr adresi aşağıdaki formatı kullanarak veri çağırmaktadır.
```
https://sozluk.gov.tr/gts?ara=<kelime>
```

Örneğin, [https://sozluk.gov.tr/gts?ara=jeton](https://sozluk.gov.tr/gts?ara=jeton) aşağıdaki veriyi döndürür.
```
[{"madde_id":"40466","kac":"0","kelime_no":"26246","cesit":"0","anlam_gor":"0","on_taki":null,"on_taki_html":null,"madde":"jeton","madde_html":"jeton<\/strong>","cesit_say":"1","anlam_say":"1","taki":null,"cogul_mu":"0","ozel_mi":"0","egik_mi":"0","lisan_kodu":"13","lisan":"Fransızca jeton","telaffuz_html":null,"lisan_html":null,"telaffuz":null,"birlesikler":null,"font":null,"madde_duz":"jeton","gosterim_tarihi":null,"anlamlarListe":[{"anlam_id":"45928","madde_id":"40466","anlam_sira":"1","fiil":"0","tipkes":"0","anlam":"Gişelerde, telefon ve türlü oyunlarda para yerine kullanılan küçük, metal veya plastik nesne","anlam_html":null,"gos":"0","gos_kelime":"0","gos_kultur":"0","ozelliklerListe":[{"ozellik_id":"19","tur":"3","tam_adi":"isim","kisa_adi":"a.","ekno":"30"}]}],"atasozu":[{"madde_id":"40467","madde":"jeton geç düşmek","on_taki":null}]}]
```

Yukarıdaki formatta görebileceğimiz önemli değerler
- `"lisan":"Fransızca`

-  `"anlam":"Gişelerde, telefon ve türlü oyunlarda para yerine kullanılan küçük, metal veya plastik nesne"`

- `"tam_adi":"isim"`

- `"atasozu":[{"madde_id":"40467","madde":"jeton geç düşmek","on_taki":null}]`

# Lokal cihazda veritabani kullanmak
```
{
  "_id": 83,
  "madde_id": "83",
  "kac": "0",
  "kelime_no": "14872",
  "cesit": "0",
  "anlam_gor": "0",
  "on_taki": null,
  "madde": "durmak",
  "cesit_say": "4",
  "anlam_say": "14",
  "taki": "ur",
  "cogul_mu": "0",
  "ozel_mi": "0",
  "egik_mi": "0",
  "lisan_kodu": "0",
  "lisan": "",
  "telaffuz": "",
  "birlesikler": "duran top, durmuş oturmuş, dursuz duraksız, durup dinlenmeden, durup durup, durup dururken, süreduran, oladurmak",
  "font": null,
  "madde_duz": "durmak",
  "gosterim_tarihi": null,
  "anlamlarListe": [
    {
      "anlam_id": "25961",
      "madde_id": "83",
      "anlam_sira": "1",
      "fiil": "1",
      "tipkes": "0",
      "anlam": "Hareketsiz durumda olmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "706",
          "anlam_id": "25961",
          "ornek_sira": "1",
          "ornek": "Motorlu su taşıtlarından biri de kanal rıhtımının tam bizim önümüze düşen bir noktasında demir atmış duruyordu.",
          "kac": "1",
          "yazar_id": "29",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "29",
              "tam_adi": "Yakup Kadri Karaosmanoğlu ",
              "kisa_adi": "Y. K. Karaosmanoğlu",
              "ekno": "160"
            }
          ]
        }
      ],
      "ozelliklerListe": [
        {
          "ozellik_id": "23",
          "tur": "3",
          "tam_adi": "nesnesiz",
          "kisa_adi": "nsz.",
          "ekno": "34"
        }
      ]
    },
    {
      "anlam_id": "25962",
      "madde_id": "83",
      "anlam_sira": "2",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "İşlemez olmak, çalışmamak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "707",
          "anlam_id": "25962",
          "ornek_sira": "1",
          "ornek": "Bileğimdeki saat durmuş.",
          "kac": "1",
          "yazar_id": "76",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "76",
              "tam_adi": "Aka Gündüz",
              "kisa_adi": "A. Gündüz",
              "ekno": "215"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25963",
      "madde_id": "83",
      "anlam_sira": "3",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Bir yerde bir süre oyalanmak, eğlenmek, eğleşmek; tevakkuf etmek",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "48760",
          "anlam_id": "25963",
          "ornek_sira": "1",
          "ornek": "Yolda nerede çeşme gördümse durdum, elimi yüzümü yıkadım, su içtim.",
          "kac": "1",
          "yazar_id": "57",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "57",
              "tam_adi": "Necati Cumalı",
              "kisa_adi": "N. Cumalı",
              "ekno": "188"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25964",
      "madde_id": "83",
      "anlam_sira": "4",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Sona ermek; kesilmek",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "69978",
          "anlam_id": "25964",
          "ornek_sira": "1",
          "ornek": "Yağmur durdu.",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ]
    },
    {
      "anlam_id": "25965",
      "madde_id": "83",
      "anlam_sira": "5",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Varlığını sürdürmek",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "710",
          "anlam_id": "25965",
          "ornek_sira": "1",
          "ornek": "Türklerin yüzlerce yıl önceki kitabeleri hâlâ duruyor.",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ]
    },
    {
      "anlam_id": "25966",
      "madde_id": "83",
      "anlam_sira": "6",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Var olmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "711",
          "anlam_id": "25966",
          "ornek_sira": "1",
          "ornek": "Bu kadar dersim dururken sinemaya nasıl gideyim?",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ]
    },
    {
      "anlam_id": "25967",
      "madde_id": "83",
      "anlam_sira": "7",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Beklemek, dikilmek",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "712",
          "anlam_id": "25967",
          "ornek_sira": "1",
          "ornek": "Oturacak değil, ayakta duracak yer yok.",
          "kac": "1",
          "yazar_id": "8",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "8",
              "tam_adi": "Reşat Nuri Güntekin",
              "kisa_adi": "R. N. Güntekin",
              "ekno": "133"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25969",
      "madde_id": "83",
      "anlam_sira": "8",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Birisinin malı olarak bulunmak veya o malla ilişkisi olmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "714",
          "anlam_id": "25969",
          "ornek_sira": "1",
          "ornek": "Yazlık eviniz hâlâ duruyor mu?",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ]
    },
    {
      "anlam_id": "25970",
      "madde_id": "83",
      "anlam_sira": "9",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Bir yerde kalmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "60052",
          "anlam_id": "25970",
          "ornek_sira": "1",
          "ornek": "Artık çok durmamış, yanındaki hanımla birlikte balodan çıkmış.",
          "kac": "1",
          "yazar_id": "9",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "9",
              "tam_adi": "Mahmut Yesari",
              "kisa_adi": "M. Yesari",
              "ekno": "134"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25971",
      "madde_id": "83",
      "anlam_sira": "10",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Bir yerde olmak veya bulunmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "716",
          "anlam_id": "25971",
          "ornek_sira": "1",
          "ornek": "Aspirin getirmeyeceğini adı gibi biliyordu çünkü çekmecesinde dokunulmamış bir kutu duruyordu.",
          "kac": "1",
          "yazar_id": "7",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "7",
              "tam_adi": "Tarık Buğra",
              "kisa_adi": "T. Buğra",
              "ekno": "132"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25972",
      "madde_id": "83",
      "anlam_sira": "11",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Belli bir durumda, bir görevde bulunmak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "717",
          "anlam_id": "25972",
          "ornek_sira": "1",
          "ornek": "Her gelişimde ben de maçları seyreder, kaleci dururdum.",
          "kac": "1",
          "yazar_id": "2",
          "yazar_vd": "",
          "yazar": [
            {
              "yazar_id": "2",
              "tam_adi": "Haldun Taner",
              "kisa_adi": "H. Taner",
              "ekno": "127"
            }
          ]
        }
      ]
    },
    {
      "anlam_id": "25973",
      "madde_id": "83",
      "anlam_sira": "12",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "Ara vermek",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "718",
          "anlam_id": "25973",
          "ornek_sira": "1",
          "ornek": "Sabahtan beri hiç durmadım.",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ]
    },
    {
      "anlam_id": "25968",
      "madde_id": "83",
      "anlam_sira": "13",
      "fiil": "0",
      "tipkes": "0",
      "anlam": "► yaşamak",
      "gos": "0",
      "orneklerListe": [
        {
          "ornek_id": "48761",
          "anlam_id": "25968",
          "ornek_sira": "1",
          "ornek": "Anneannen duruyor mu?",
          "kac": "1",
          "yazar_id": "0",
          "yazar_vd": ""
        }
      ],
      "ozelliklerListe": [
        {
          "ozellik_id": "32",
          "tur": "4",
          "tam_adi": "mecaz",
          "kisa_adi": "mec.",
          "ekno": "43"
        }
      ]
    },
    {
      "anlam_id": "25975",
      "madde_id": "83",
      "anlam_sira": "14",
      "fiil": "1",
      "tipkes": "0",
      "anlam": "Kök veya gövdeleri sonuna -a (-e) zarf-fiil eki almış fiillere gelerek süreklilik bildiren birleşik fiiller oluşturur: Çalışadurmak, bakadurmak, getiredurmak, yiyedurmak gibi",
      "gos": "0",
      "ozelliklerListe": [
        {
          "ozellik_id": "82",
          "tur": "3",
          "tam_adi": "yardımcı  fiil",
          "kisa_adi": "yar.",
          "ekno": "271"
        }
      ]
    }
  ],
  "atasozu": [
    { "madde_id": "84", "madde": "dur! (veya durun!)", "on_taki": null },
    { "madde_id": "86", "madde": "durdu durdu, turnayı gözünden vurdu", "on_taki": null },
    { "madde_id": "87", "madde": "durduğu yerde (veya durduk yerde)", "on_taki": null },
    { "madde_id": "85", "madde": "dur durak (veya dur dinlen veya dur otur) yok", "on_taki": null }
  ]
}
```
