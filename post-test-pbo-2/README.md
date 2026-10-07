# 1. PEMBUATAN OBJEK
Bagian ini menampilkan inisialisasi awal seluruh objek utama di dalam sistem.
  Class & Instance: Membuat instance dari `PestaporaApp` untuk menyimpan konfigurasi lokasi dan versi aplikasi.
  *Inisialisasi Objek: Membuka instansiasi awal untuk objek `Tiket` (`TiketVIP`, `TiketPresale`, `TiketEarlyBird`), `Artis`, `Stage`, dan `Pemesanan` yang nantinya akan saling berinteraksi.

# 2. INHERITANCE - Detail Tiap Subclass
Bagian ini menampilkan informasi detail dan spesifik dari setiap jenis tiket.
Inheritance (Pewarisan) Menguji atribut unik yang dimiliki masing-masing *subclass* dari *superclass* `TiketKonser`:
    VIP: Memiliki atribut tambahan fasilitas lounge (`Lounge: Ya`) dan jenis merchandise (`Hoodie + Lanyard`).
    Presale: Memiliki atribut khusus penanda `Gelombang ke-2`.
    Early Bird: Memiliki atribut persentase diskon (`20%`) dan tenggat batas pembelian.

# 3. METHOD OVERRIDING - `hitung_harga_akhir()`
Bagian ini menampilkan hasil perbandingan kalkulasi total harga tiket dari masing-masing tipe tiket.
Polymorphism & Method Overriding Membuktikan bahwa pemanggilan fungsi `hitung_harga_akhir()` pada tiap *subclass* mengeksekusi logika yang berbeda-beda:
    `TiketVIP`: Menambahkan kalkulasi biaya *lounge* tambahan di luar pajak.
    `TiketPresale`: Menghitung penyesuaian biaya berdasarkan urutan gelombang.
    `TiketEarlyBird`: Menerapkan diskon pada harga dasar terlebih dahulu sebelum dikenakan pajak.
    `TiketKonser`: Menggunakan perhitungan dasar superclass (harga dasar + pajak standar).

# 4. AGREGASI & KOMPOSISI - Jadwal Stage
Bagian ini menampilkan proses penambahan penampil ke panggung, penanganan error validasi jam, dan rekap jadwal stage.
  Agregasi: Objek `Artis` dibuat secara independen di luar dan dimasukkan ke dalam `Stage`.
  Komposisi: Objek `JadwalTampil` dibentuk di dalam internal `Stage`.
  Validasi Format: Sistem berhasil menolak pendaftaran jam `25:99` karena format jam tidak valid (`HH:MM`).

# 5. ASOSIASI - PetugasGate Memindai Tiket
Simulasi alur verifikasi tiket di pintu masuk (*gate*) oleh petugas dan cetak bukti transaksi.
Asosiasi: `PetugasGate` menggunakan objek `Pemesanan` dan `Stage` melalui parameter method `scan_masuk()` tanpa memiliki hubungan kepemilikan permanen.
  Alur Logika:
    Pemindaian awal pemesanan Ridho [DITOLAK] karena status pembayaran masih `Pending`.
    Setelah pemesanan diubah menjadi `Lunas`, pemindaian berikutnya [DITERIMA].
    Diakhiri dengan mencetak struk fisik `TICKET PASS` yang menampilkan riwayat perubahan status (`Pending -> Lunas`).

# 6. CLASS METHOD & STATIC METHOD
Demonstrasi eksekusi method pembantu (*utility*) dan method level class.
  Static Method: Menjalankan fungsi independen tanpa membutuhkan data instansiasi objek, seperti `hitung_pajak()`, `validasi_format_jam()`, dan pembuatan kode transaksi otomatis.
  Class Method: Menggunakan `@classmethod` untuk menginisialisasi objek dari dictionary (`buat_dari_dict()`) serta mengelola *state* variabel global class (reset total tiket terjual).

# 7. PROTECTED vs PRIVATE
Menguji batasan hak akses atribut berdasarkan prinsip Encapsulation (Pembungkusan).
  Protected (`_`)**: Atribut `_harga_dasar` tetap bisa diakses dan dibaca oleh *subclass*.
  Private (`__`)**: Atribut `__kode_keamanan` tidak bisa diakses langsung dari *subclass* maupun luar class (memicu `AttributeError` karena *Name Mangling*), namun bisa ditampilkan secara tersamar via method kontrol internal (`***001`).

# 8. PENGUJIAN SETTER (Valid vs Tidak Valid)
Menguji keandalan fitur validasi data pada properti setter.
  Encapsulation & Validation:
    Harga Dasar nilai positif (`800000`) diterima, sedangkan nilai negatif (`-50000`) ditolak dan nilai lama tetap dipertahankan

# 9. BUKTI SIKLUS HIDUP
Membuktikan secara nyata perbedaan mendasar antara relasi Agregasi dan Komposisi ketika objek induk dihapus (`del`).
  Bukti Agregasi yaitu Ketika objek `Stage` dan `Pemesanan` dihapus dari memori, objek `Artis` dan `Tiket` di dalamnya tetap eksis dan dapat diakses.
  Bukti Komposis yaitu Ketika objek `Stage` dan `Pemesanan` dihapus, objek `JadwalTampil` dan `CatatanStatus` ikut musnah secara otomatis bersama induknya.