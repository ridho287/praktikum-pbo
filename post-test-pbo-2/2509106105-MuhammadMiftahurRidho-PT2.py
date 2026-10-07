"""
POSTTEST PBO - Sistem Manajemen Pemesanan Tiket dan Penjadwalan Stage Konser di Pestapora

Relasi UML:
  Asosiasi  : PetugasGate ..> Pemesanan, Stage   (dipakai lewat parameter method)
  Agregasi  : Pemesanan o-- TiketKonser          (tiket dibuat di luar)
              JadwalTampil o-- Artis             (artis dibuat di luar)
  Komposisi : Pemesanan *-- CatatanStatus        (dibuat di dalam Pemesanan)
              Stage *-- JadwalTampil             (dibuat di dalam Stage)
Inheritance:
  TiketKonser <|-- TiketEarlyBird, TiketPresale, TiketVIP
"""

LEBAR = 64

def judul_bagian(nomor, teks):
    """Cetak judul bagian dengan tampilan seragam."""
    print("\n" + "=" * LEBAR)
    print(f" {nomor}. {teks}")
    print("=" * LEBAR)

class PestaporaApp:
    nama_event = "Pestapora Festival 2026"
    total_tiket_terjual = 0
    kategori_tersedia = ["Early Bird", "Presale", "VIP"]

    def __init__(self, nama_lokasi: str, versi_aplikasi: str):
        self.nama_lokasi = nama_lokasi
        self.versi_aplikasi = versi_aplikasi

    def tampilkan_info_app(self):
        print(f"  {self.nama_lokasi:<24} | Versi App: {self.versi_aplikasi}")

    @staticmethod
    def format_rupiah(nilai: float) -> str:
        """Contoh: 982500 -> 'Rp 982.500'"""
        return "Rp " + f"{nilai:,.0f}".replace(",", ".")


class TiketKonser:
    """Superclass: atribut & perilaku yang dimiliki SEMUA jenis tiket."""
    pajak_standar = 11.0

    def __init__(self, id_tiket: str, kategori: str, harga_dasar: float):
        self.id_tiket = id_tiket
        self._kategori = None
        self._harga_dasar = 0.0
        self.__kode_keamanan = f"SEC-{id_tiket[-3:]}"

        self.kategori = kategori
        self.harga_dasar = harga_dasar

    def verifikasi_kode(self, kode: str) -> bool:
        """Akses terkontrol ke data private."""
        return kode == self.__kode_keamanan

    def kode_tersamar(self) -> str:
        return "***" + self.__kode_keamanan[-3:]

    @property
    def kategori(self) -> str:
        return self._kategori

    @kategori.setter
    def kategori(self, value: str):
        if not value or not isinstance(value, str):
            print("    [!] Peringatan Validasi: kategori tiket tidak boleh kosong.")
            return
        clean_input = value.strip()
        match = next((k for k in PestaporaApp.kategori_tersedia if k.lower() == clean_input.lower()), None)
        if not match:
            pilihan = ", ".join(PestaporaApp.kategori_tersedia)
            print(f"    [!] Peringatan Validasi: kategori '{value}' tidak valid. Pilihan: {pilihan}")
            return
        self._kategori = match

    @property
    def harga_dasar(self) -> float:
        return self._harga_dasar

    @harga_dasar.setter
    def harga_dasar(self, value: float):
        if not isinstance(value, (int, float)) or value <= 0:
            print(f"    [!] Peringatan Validasi: harga tiket harus positif (input: {value}).")
            return
        self._harga_dasar = float(value)

    def hitung_harga_akhir(self) -> float:
        """Harga akhir = harga dasar + pajak."""
        return self._harga_dasar + TiketKonser.hitung_pajak(self._harga_dasar, self.pajak_standar)

    def tampilkan_detail(self):
        print(f"  [{self.id_tiket}] {self.kategori:<10} | Harga Dasar: "
              f"{PestaporaApp.format_rupiah(self.harga_dasar)}")

    @classmethod
    def buat_dari_dict(cls, data: dict):
        return cls(data.get("id_tiket", "UNKNOWN"),
                   data.get("kategori", "Presale"),
                   data.get("harga_dasar", 100000))

    @staticmethod
    def hitung_pajak(harga: float, persentase_pajak: float = 11.0) -> float:
        return harga * (persentase_pajak / 100.0) if harga > 0 else 0.0


class TiketEarlyBird(TiketKonser):
    """Atribut unik: diskon_persen, batas_pembelian."""

    def __init__(self, id_tiket: str, harga_dasar: float, diskon_persen: float, batas_pembelian: str):
        super().__init__(id_tiket, "Early Bird", harga_dasar)
        self.diskon_persen = diskon_persen
        self.batas_pembelian = batas_pembelian

    def hitung_harga_akhir(self) -> float:
        harga_diskon = self._harga_dasar * (1 - self.diskon_persen / 100)
        return harga_diskon + TiketKonser.hitung_pajak(harga_diskon, self.pajak_standar)

    def tampilkan_detail(self):
        super().tampilkan_detail()
        print(f"      -> Diskon {self.diskon_persen:g}% | berlaku s.d. {self.batas_pembelian}")


class TiketPresale(TiketKonser):
    """Atribut unik: gelombang."""

    def __init__(self, id_tiket: str, harga_dasar: float, gelombang: int):
        super().__init__(id_tiket, "Presale", harga_dasar)
        self.gelombang = gelombang

    def hitung_harga_akhir(self) -> float:
        harga_gelombang = self._harga_dasar + (self.gelombang - 1) * 25000
        return harga_gelombang + TiketKonser.hitung_pajak(harga_gelombang, self.pajak_standar)

    def tampilkan_detail(self):
        super().tampilkan_detail()
        print(f"      -> Gelombang ke-{self.gelombang}")


class TiketVIP(TiketKonser):
    """Atribut unik: akses_lounge, paket_merchandise."""
    BIAYA_LOUNGE = 150000

    def __init__(self, id_tiket: str, harga_dasar: float, akses_lounge: bool, paket_merchandise: str):
        super().__init__(id_tiket, "VIP", harga_dasar)
        self.akses_lounge = akses_lounge
        self.paket_merchandise = paket_merchandise

    def hitung_harga_akhir(self) -> float:
        total = super().hitung_harga_akhir()
        return total + (TiketVIP.BIAYA_LOUNGE if self.akses_lounge else 0)

    def coba_akses_private(self):
        """Seperti contoh modul: subclass tidak bisa mengakses atribut private superclass."""
        return self.__kode_keamanan 

    def tampilkan_detail(self):
        super().tampilkan_detail()
        lounge = "Ya" if self.akses_lounge else "Tidak"
        print(f"      -> Lounge: {lounge} | Merchandise: {self.paket_merchandise}")


class Artis:
    def __init__(self, nama_artis: str, genre: str):
        self.nama_artis = nama_artis
        self.genre = genre

    def __str__(self):
        return f"{self.nama_artis} ({self.genre})"


class JadwalTampil:
    def __init__(self, artis: Artis, jam: str):
        self.artis = artis
        self.jam = jam


class Stage:
    def __init__(self, id_stage: str, nama_stage: str, kapasitas_maksimal: int):
        self.id_stage = id_stage
        self.nama_stage = nama_stage
        self.__kapasitas_maksimal = 0
        self.__daftar_jadwal = []

        self.kapasitas_maksimal = kapasitas_maksimal

    @property
    def kapasitas_maksimal(self) -> int:
        return self.__kapasitas_maksimal

    @kapasitas_maksimal.setter
    def kapasitas_maksimal(self, value: int):
        if not isinstance(value, int) or value < 100:
            print(f"    [!] Peringatan Validasi: kapasitas {self.nama_stage} minimal 100 penonton (input: {value}).")
            return
        self.__kapasitas_maksimal = value

    def tambah_penampil(self, artis: Artis, jam_tampil: str):
        """Agregasi: 'artis' dibuat di luar. Komposisi: JadwalTampil dibuat di sini."""
        if not Stage.validasi_format_jam(jam_tampil):
            print(f"    [!] Peringatan Validasi: format jam '{jam_tampil}' salah. Gunakan HH:MM (contoh: 19:30).")
            return
        self.__daftar_jadwal.append(JadwalTampil(artis, jam_tampil))
        print(f"    [OK] {artis.nama_artis:<16} -> {self.nama_stage}, pukul {jam_tampil}")

    def tampilkan_jadwal(self):
        print(f"\n  {self.nama_stage} (Kapasitas: {self.kapasitas_maksimal:,} penonton)".replace(",", "."))
        if not self.__daftar_jadwal:
            print("    (Belum ada penampil yang terdaftar)")
        for j in self.__daftar_jadwal:
            print(f"    {j.jam} WIB  |  {j.artis}")

    @classmethod
    def buat_stage_utama(cls, id_stage: str):
        return cls(id_stage, "Pestapora Main Stage", 15000)

    @staticmethod
    def validasi_format_jam(jam_str: str) -> bool:
        parts = jam_str.split(":")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59
        return False


class CatatanStatus:
    def __init__(self, status: str):
        self.status = status

    def __str__(self):
        return self.status


class Pemesanan:
    def __init__(self, id_pemesanan: str, nama_pemesan: str, tiket: TiketKonser):
        self.id_pemesanan = id_pemesanan
        self.nama_pemesan = nama_pemesan
        self.tiket = tiket
        self.__status_pembayaran = "Pending"
        self._catatan = [CatatanStatus("Pending")]

        PestaporaApp.total_tiket_terjual += 1

    @property
    def status_pembayaran(self) -> str:
        return self.__status_pembayaran

    @status_pembayaran.setter
    def status_pembayaran(self, status_baru: str):
        opsi_valid = ["Pending", "Lunas", "Batal"]
        if not status_baru or status_baru.capitalize() not in opsi_valid:
            print(f"    [!] Peringatan Validasi: status '{status_baru}' tidak valid. "
                  f"Pilihan: {', '.join(opsi_valid)}")
            return
        self.__status_pembayaran = status_baru.capitalize()
        self._catatan.append(CatatanStatus(self.__status_pembayaran))

    def cetak_tiket_resmi(self):
        total = self.tiket.hitung_harga_akhir()
        garis = "  " + "=" * 46
        print(f"\n{garis}")
        print(f"  {'TICKET PASS - ' + PestaporaApp.nama_event.upper():^46}")
        print(garis)
        print(f"   {'ID Pemesanan':<13}: {self.id_pemesanan}")
        print(f"   {'Nama Pemesan':<13}: {self.nama_pemesan}")
        print(f"   {'Jenis Tiket':<13}: {type(self.tiket).__name__}")
        print(f"   {'Kategori':<13}: {self.tiket.kategori}")
        print(f"   {'Harga Dasar':<13}: {PestaporaApp.format_rupiah(self.tiket.harga_dasar)}")
        print(f"   {'Total Bayar':<13}: {PestaporaApp.format_rupiah(total)}")
        print(f"   {'':<13}  (termasuk pajak & ketentuan jenis tiket)")
        print(f"   {'Status':<13}: {self.status_pembayaran}")
        print(f"   {'Riwayat':<13}: {' -> '.join(str(c) for c in self._catatan)}")
        print(garis)

    @classmethod
    def reset_total_penjualan(cls):
        PestaporaApp.total_tiket_terjual = 0
        print("    [Admin] Counter total tiket terjual di-reset ke 0.")

    @staticmethod
    def buat_kode_transaksi(index: int) -> str:
        return f"PSTPR-2026-{index:04d}"


class PetugasGate:
    def __init__(self, nama: str, id_petugas: str):
        self.nama = nama
        self.id_petugas = id_petugas

    def scan_masuk(self, pemesanan: Pemesanan, stage: Stage):
        print(f"  {self.nama} memindai {pemesanan.id_pemesanan} ({pemesanan.nama_pemesan}) "
              f"di {stage.nama_stage}")
        if pemesanan.status_pembayaran != "Lunas":
            print(f"    [DITOLAK]  Status pembayaran masih '{pemesanan.status_pembayaran}'.")
            return False
        print(f"    [DITERIMA] Tiket {pemesanan.tiket.kategori} valid, silakan masuk.")
        return True

if __name__ == "__main__":
    print("=" * LEBAR)
    print(f"{'WELCOME TO ' + PestaporaApp.nama_event.upper():^{LEBAR}}")
    print(f"{'Sistem Manajemen Pemesanan Tiket & Penjadwalan Stage':^{LEBAR}}")
    print("=" * LEBAR)

    judul_bagian(1, "PEMBUATAN OBJEK")
    app1 = PestaporaApp("Gambir Expo Jakarta", "v1.0.0")
    app2 = PestaporaApp("Parkir Timur Senayan", "v1.2.0")

    tiket_vip = TiketVIP("TKT-001", 750000, True, "Hoodie + Lanyard")
    tiket_pre = TiketPresale("TKT-002", 450000, 2)
    tiket_eb = TiketEarlyBird("TKT-003", 300000, 20, "31 Desember 2026")

    artis1 = Artis("FSTVLST", "Art Rock")
    artis2 = Artis("Teenage Death Star", "Rock Alternatif")
    artis3 = Artis("Dongker", "Punk Rock")

    stage1 = Stage("STG-01", "Standup Stage", 500)
    stage2 = Stage.buat_stage_utama("STG-00")

    pesanan1 = Pemesanan(Pemesanan.buat_kode_transaksi(1), "Ridho", tiket_vip)
    pesanan2 = Pemesanan(Pemesanan.buat_kode_transaksi(2), "Puput", tiket_pre)
    pesanan3 = Pemesanan(Pemesanan.buat_kode_transaksi(3), "Dina", tiket_eb)

    print("  Lokasi & versi aplikasi:")
    app1.tampilkan_info_app()
    app2.tampilkan_info_app()
    print("\n  Objek yang dibuat:")
    print(f"    {'Tiket':<10}: {tiket_vip.id_tiket} ({tiket_vip.kategori}), "
          f"{tiket_pre.id_tiket} ({tiket_pre.kategori}), {tiket_eb.id_tiket} ({tiket_eb.kategori})")
    print(f"    {'Artis':<10}: {artis1.nama_artis}, {artis2.nama_artis}, {artis3.nama_artis}")
    print(f"    {'Stage':<10}: {stage1.nama_stage}, {stage2.nama_stage}")
    print(f"    {'Pemesanan':<10}: {pesanan1.id_pemesanan}, {pesanan2.id_pemesanan}, {pesanan3.id_pemesanan}")

    judul_bagian(2, "INHERITANCE - Detail Tiap Subclass")
    for t in (tiket_vip, tiket_pre, tiket_eb):
        t.tampilkan_detail()

    judul_bagian(3, "METHOD OVERRIDING - hitung_harga_akhir()")
    base = TiketKonser("TKT-BASE", "VIP", 750000)
    print(f"  {'Jenis Tiket':<16} {'Harga Dasar':>14} {'Total Bayar':>14}")
    print(f"  {'-' * 16} {'-' * 14} {'-' * 14}")
    for t in (tiket_vip, tiket_pre, tiket_eb, base):
        nama = type(t).__name__
        print(f"  {nama:<16} {PestaporaApp.format_rupiah(t.harga_dasar):>14} "
              f"{PestaporaApp.format_rupiah(t.hitung_harga_akhir()):>14}")
    print("\n  Catatan: baris TiketKonser memakai versi superclass (hanya harga + pajak).")

    judul_bagian(4, "AGREGASI & KOMPOSISI - Jadwal Stage")
    stage1.tambah_penampil(artis1, "16:00")
    stage2.tambah_penampil(artis2, "21:00")
    stage2.tambah_penampil(artis3, "19:30")
    stage2.tambah_penampil(artis3, "25:99")
    stage1.tampilkan_jadwal()
    stage2.tampilkan_jadwal()

    judul_bagian(5, "ASOSIASI - PetugasGate Memindai Tiket")
    petugas = PetugasGate("Bagas", "GT-01")
    petugas2 = PetugasGate("Sari", "GT-02")
    petugas.scan_masuk(pesanan1, stage2)
    pesanan1.status_pembayaran = "Lunas"
    print("  (Ridho melunasi pembayaran)")
    petugas.scan_masuk(pesanan1, stage2)
    petugas2.scan_masuk(pesanan2, stage1)
    pesanan1.cetak_tiket_resmi()

    judul_bagian(6, "CLASS METHOD & STATIC METHOD")
    print("  [Static Method]")
    print(f"    {'hitung_pajak(500000)':<30}: {PestaporaApp.format_rupiah(TiketKonser.hitung_pajak(500000))}")
    print(f"    {'validasi_format_jam(19:30)':<30}: {Stage.validasi_format_jam('19:30')}")
    print(f"    {'validasi_format_jam(25:99)':<30}: {Stage.validasi_format_jam('25:99')}")
    print(f"    {'buat_kode_transaksi(4)':<30}: {Pemesanan.buat_kode_transaksi(4)}")
    print("\n  [Class Method]")
    t_dict = TiketKonser.buat_dari_dict({"id_tiket": "TKT-009", "kategori": "presale", "harga_dasar": 500000})
    print("    buat_dari_dict():")
    print("  ", end="")
    t_dict.tampilkan_detail()
    print(f"    Total tiket terjual (sebelum reset): {PestaporaApp.total_tiket_terjual}")
    Pemesanan.reset_total_penjualan()
    print(f"    Total tiket terjual (sesudah reset): {PestaporaApp.total_tiket_terjual}")

    judul_bagian(7, "PROTECTED vs PRIVATE")
    print(f"  {'Protected _harga_dasar (subclass)':<36}: {PestaporaApp.format_rupiah(tiket_eb._harga_dasar)}")
    print(f"  {'Private via method terkontrol':<36}: {tiket_vip.kode_tersamar()}")
    try:
        tiket_vip.coba_akses_private()
    except AttributeError as e:
        print(f"  {'Private diakses dari subclass':<36}: AttributeError")
        print(f"      {e}")

    judul_bagian(8, "PENGUJIAN SETTER (Valid vs Tidak Valid)")
    print("  [Harga Dasar - TiketVIP]")
    print("  -> set 800000 (valid)")
    tiket_vip.harga_dasar = 800000
    print(f"     nilai sekarang: {PestaporaApp.format_rupiah(tiket_vip.harga_dasar)}")
    print("  -> set -50000 (tidak valid)")
    tiket_vip.harga_dasar = -50000
    print(f"     nilai sekarang: {PestaporaApp.format_rupiah(tiket_vip.harga_dasar)}")

    print("\n  [Kategori - TiketVIP]")
    print("  -> set 'VIP Ekstra' (tidak valid)")
    tiket_vip.kategori = "VIP Ekstra"
    print(f"     nilai sekarang: {tiket_vip.kategori}")

    print("\n  [Kapasitas - Standup Stage]")
    print("  -> set 1000 (valid)")
    stage1.kapasitas_maksimal = 1000
    print(f"     nilai sekarang: {stage1.kapasitas_maksimal:,} penonton".replace(",", "."))
    print("  -> set 50 (tidak valid)")
    stage1.kapasitas_maksimal = 50
    print(f"     nilai sekarang: {stage1.kapasitas_maksimal:,} penonton".replace(",", "."))

    print("\n  [Status Pembayaran - Pesanan Puput]")
    print("  -> set 'Belum Lunas' (tidak valid)")
    pesanan2.status_pembayaran = "Belum Lunas"
    print(f"     nilai sekarang: {pesanan2.status_pembayaran}")

    judul_bagian(9, "BUKTI SIKLUS HIDUP")
    del stage2
    del pesanan3
    print("  [Agregasi] objek bagian tetap ada setelah induk dihapus")
    print(f"    Stage dihapus      -> artis masih ada : {artis2}")
    print(f"    Pemesanan dihapus  -> tiket masih ada : {tiket_eb.id_tiket} ({tiket_eb.kategori})")
    print("\n  [Komposisi] objek bagian ikut musnah bersama induknya")
    print("    Stage dihapus      -> JadwalTampil ikut musnah")
    print("    Pemesanan dihapus  -> CatatanStatus ikut musnah")

    print("\n" + "=" * LEBAR)
    print(f"{'-- Program selesai --':^{LEBAR}}")
    print("=" * LEBAR)