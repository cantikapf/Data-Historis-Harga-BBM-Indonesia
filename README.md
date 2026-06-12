# Mesin Waktu Harga BBM Indonesia ⛽

Sebuah *dashboard* portofolio web interaktif yang merangkum sejarah panjang pergerakan harga Bahan Bakar Minyak (BBM) di Indonesia sejak tahun 1980 hingga 2026. Aplikasi ini tidak sekadar menampilkan angka historis, melainkan membandingkannya menggunakan konsep **Daya Beli Setara Masa Kini (*Time Value of Money*)** akibat efek inflasi berkepanjangan.

## 🌟 Fitur Utama

- **Penurunan Nilai Uang (Visualisasi Tangki CSS)**: Melihat simulasi berapa banyak liter bensin yang bisa Anda dapatkan dengan uang pas Rp 100.000 di masa lampau dibandingkan dengan hari ini.
- **Ekuivalensi Tangki Motor**: Secara instan mengkonversi volume liter menjadi metrik kehidupan sehari-hari ("Seberapa banyak isi *full tank* untuk standar motor Honda BeAT berkapasitas 4.2 Liter?").
- **Time Value of Money (Grafik Interaktif)**: Menyajikan grafik ganda *(Dual-Line Chart)* yang menyoroti perbedaan dramatis antara **Harga Nominal** lampau vs **Daya Beli** jika nilai uangnya ditarik ke masa kini.
- **Konteks Sejarah Otomatis**: Menyajikan peristiwa penting, pergantian rezim, atau alasan di balik lonjakan/stabilitas harga BBM pada tahun spesifik yang sedang Anda pilih di *slider*.
- **Mendukung 3 Jenis BBM Mayoritas**: Premium/Pertalite, Solar, dan Pertamax.

## 🛠️ Teknologi yang Digunakan (Stack)

Proyek web portofolio ini sengaja dibangun menggunakan fondasi *vanilla/static* yang sangat ringan dan performatif:

- **HTML5 & Vanilla JavaScript**: Ringan, cepat, interaktif tanpa harus bergantung pada infrastruktur *backend* atau server Python.
- **Tailwind CSS (v3)**: Mengendalikan struktur *layout Grid/Flexbox* dan menciptakan desain *UI* bergaya premium-elegan (mengandalkan paduan warna *Sage Green* dan *Cream* dengan *micro-animations*).
- **Chart.js**: Untuk menggambar kurva grafik perbandingan harga historis secara halus.
- **Python (Data Preparation Layer)**: Digunakan murni di fase *development* (awal) untuk melakukan pembersihan (*data cleaning*) dan kalkulasi *forward-fill* interpolasi interpolasi data. File mentahnya diekstraksi menjadi data statis murni (`data.js`) siap baca oleh *browser*.

## 🚀 Cara Menjalankan Secara Lokal

Proyek ini sepenuhnya berwujud berkas statis tanpa arsitektur peladen (*Serverless*). Siapa pun dapat menjalankannya dengan mudah:

1. *Clone* atau *Download* repository ini ke komputer Anda.
2. Buka folder/direktori proyek hasil unduhan.
3. **Klik ganda (*double-click*)** *file* `index.html` — otomatis akan terbuka melalui Web Browser favorit Anda (Google Chrome, Firefox, Safari).
   
*Selesai! Tidak perlu meng-install lingkungan Node.js, NPM, apalagi web server. Aplikasi langsung berjalan sepenuhnya.*

## 📊 Metodologi Perhitungan

Untuk menyetarakan daya beli, aplikasi ini menggunakan formula sederhana:
```text
Harga Setara Masa Kini = Harga Nominal × (CPI 2026 ÷ CPI Tahun Tersebut)
```

**Referensi Data**:
1. **Data Inflasi**: Rasio Indeks Harga Konsumen (IHK) atau *Consumer Price Index (CPI)* Indonesia didapatkan langsung dari arsip data terbuka **[Bank Dunia / World Bank](https://data.worldbank.org/indicator/FP.CPI.TOTL?locations=ID)**.
2. **Data Harga BBM**: Dikompilasi dari regulasi pemerintah, catatan publik, serta repositori **[Wikipedia: Bahan Bakar Minyak di Indonesia](https://id.wikipedia.org/wiki/Bahan_bakar_minyak_di_Indonesia)**.

## 🤖 Otomatisasi Publikasi (CI/CD)

Proyek ini telah dilengkapi dengan berkas *workflow* GitHub Actions (`.github/workflows/deploy.yml`). Saat *source code* ini Anda ungah/kirim (*push*) ke *branch* utama di repositori GitHub Anda, GitHub Actions akan **secara otomatis membangun (*build*) dan mempublikasikannya** menjadi *website* nyata melalui fitur **GitHub Pages**.

---
*Dibuat khusus sebagai Mahakarya Portofolio Analisis Data & Visualisasi Web.*
