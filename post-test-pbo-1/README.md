# Sistem Manajemen Pemesanan Tiket & Penjadwalan Stage - Pestapora Festival 2026
Dokumentasi ini berisi penjelasan program, struktur class, dan panduan pengujian untuk sistem pengelolaan tiket dan jadwal panggung pada festival musik Pestapora Festival 2026.

## Penjelasan Program
Sistem ini dirancang untuk mensimulasikan manajemen operasional acara festival musik berbasis Pemrograman Berorientasi Objek (PBO). Fitur utama dari sistem ini meliputi:
1. **Konfigurasi Aplikasi Festival:** Menyimpan informasi lokasi acara, versi aplikasi, serta tracking jumlah tiket terjual.
2. **Manajemen Tiket Konser:** Mengatur jenis tiket (Early Bird, Presale, VIP) beserta perhitungan pajak otomatis (11%) dan validasi harga.
3. **Penjadwalan Stage:** Mengatur nama panggung, kapasitas penonton, dan jadwal tampil *lineup* artis dengan validasi format jam.
4. **Pemrosesan Pemesanan:** Menghubungkan data pemesan dengan tiket yang dipilih, mengenerate kode transaksi otomatis, serta memperbarui status pembayaran.

## Struktur Class
Sistem ini dibangun menggunakan 4 class utama yang saling berinteraksi:
### 1. PestaporaApp
Menampung konfigurasi utama festival.
* **Atribut Kelas:** `nama_event`, `total_tiket_terjual`, `kategori_tersedia`
* **Atribut Instance:** `nama_lokasi`, `versi_aplikasi`
* **Method Utama:** `tampilkan_info_app()` (Instance Method)

### 2. TiketKonser
Mengelola informasi tiket dan perhitungan harga.
* **Atribut Private:** `__kategori`, `__harga_dasar`
* **Getter & Setter (`@property`):**
  * `kategori`: Memastikan input sesuai dengan opsi pada `PestaporaApp.kategori_tersedia`.
  * `harga_dasar`: Memastikan nilai harga berbentuk numerik positif (> 0).
* **Method Utama:**
  * `tampilkan_detail()` (Instance Method)
  * `buat_dari_dict()` (Class Method - *factory method*)
  * `hitung_pajak()` (Static Method - menghitung pajak standar 11%)

### 3. Stage
Mengatur informasi panggung dan jadwal acara.
* **Atribut Private:** `__kapasitas_maksimal`, `__daftar_penampil`
* **Getter & Setter (`@property`):**
  * `kapasitas_maksimal`: Memastikan kapasitas minimal 100 penonton.
* **Method Utama:**
  * `tambah_penampil()`, `tampilkan_jadwal()` (Instance Method)
  * `buat_stage_utama()` (Class Method)
  * `validasi_format_jam()` (Static Method - memeriksa format HH:MM)

### 4. Pemesanan
Menghubungkan data pemesan dengan objek `TiketKonser`.
* **Atribut Private:** `__status_pembayaran`
* **Getter & Setter (`@property`):**
  * `status_pembayaran`: Memastikan status hanya diisi pilihan "Pending", "Lunas", atau "Batal".
* **Method Utama:**
  * `cetak_tiket_resmi()` (Instance Method)
  * `reset_total_penjualan()` (Class Method)
  * `buat_kode_transaksi()` (Static Method)

---

## Panduan Pengujian (Testing Guide)
Pengujian program dilakukan pada blok `if __name__ == "__main__":` yang terbagi ke dalam 3 tahap utama:
### 1. Pembuatan Objek
Memastikan setiap class dapat diinstansiasi minimal 2 kali:
* `PestaporaApp`: Objek `app1` dan `app2`.
* `TiketKonser`: Objek `tiket1` dan `tiket2` (dibuat via `buat_dari_dict`).
* `Stage`: Objek `stage1` dan `stage2` (dibuat via `buat_stage_utama`).
* `Pemesanan`: Objek `pesanan1` (nama: Ridho) dan `pesanan2` (nama: Puput).

### 2. Pengujian Method
* **Instance Method:** Pemanggilan `.tampilkan_info_app()`, `.tampilkan_detail()`, `.tambah_penampil()`, `.tampilkan_jadwal()`, dan `.cetak_tiket_resmi()`.
* **Static Method:** Pengujian fungsi `.hitung_pajak()` dan pengujian `.validasi_format_jam()` dengan input '25:99' (salah) dan '19:30' (benar).
* **Class Method:** Memeriksa `total_tiket_terjual` sebelum dan sesudah dipanggilnya `Pemesanan.reset_total_penjualan()`.

### 3. Pengujian Validasi Data (Setter & Enkapsulasi)
Menguji keandalan *property setter* saat menerima data bernilai valid dan tidak valid:

| Objek & Atribut | Input Valid | Input Tidak Valid | Hasil Ekspektasi |
| :--- | :--- | :--- | :--- |
| `TiketKonser.harga_dasar` | `800000` | `-50000` | Menampilkan peringatan bahwa harga harus positif. |
| `TiketKonser.kategori` | `'Early Bird'` | `'VIP Ekstra'` | Menampilkan peringatan bahwa kategori tidak terdaftar. |
| `Stage.kapasitas_maksimal` | `1000` | `50` | Menampilkan peringatan bahwa kapasitas minimal 100. |
| `Pemesanan.status_pembayaran` | `'Lunas'` | `'Belum Lunas'` | Menampilkan peringatan bahwa status tidak valid. |