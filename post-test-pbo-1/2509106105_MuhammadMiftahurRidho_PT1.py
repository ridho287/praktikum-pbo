class PestaporaApp:
    nama_event = "Pestapora Festival 2026"
    total_tiket_terjual = 0
    kategori_tersedia = ["Early Bird", "Presale", "VIP"]

    def __init__(self, nama_lokasi: str, versi_aplikasi: str):
        self.nama_lokasi = nama_lokasi
        self.versi_aplikasi = versi_aplikasi

    def tampilkan_info_app(self):
        print(f"[{PestaporaApp.nama_event}] Lokasi: {self.nama_lokasi} | Versi App: {self.versi_aplikasi}")


class TiketKonser:
    pajak_standar = 11.0

    def __init__(self, id_tiket: str, kategori: str, harga_dasar: float):
        self.id_tiket = id_tiket

        self.__kategori = None
        self.__harga_dasar = 0.0
        
        self.kategori = kategori
        self.harga_dasar = harga_dasar

    @property
    def kategori(self) -> str:
        return self.__kategori

    @kategori.setter
    def kategori(self, value: str):
        if not value or not isinstance(value, str):
            print("[Peringatan Validasi] Kategori tiket tidak boleh kosong!")
            return
        
        clean_input = value.strip()
        match = next((kat for kat in PestaporaApp.kategori_tersedia if kat.lower() == clean_input.lower()), None)
        
        if not match:
            print(f"[Peringatan Validasi] Kategori '{value}' tidak valid. Pilih dari {PestaporaApp.kategori_tersedia}")
            return
        self.__kategori = match

    @property
    def harga_dasar(self) -> float:
        return self.__harga_dasar

    @harga_dasar.setter
    def harga_dasar(self, value: float):
        if not isinstance(value, (int, float)) or value <= 0:
            print(f"[Peringatan Validasi] Harga tiket harus bernilai positif! (Input: {value})")
            return
        self.__harga_dasar = float(value)

    def tampilkan_detail(self):
        print(f"  > ID Tiket : {self.id_tiket} | Kategori: {self.kategori} | Harga: Rp {self.harga_dasar:,.2f}")

    @classmethod
    def buat_dari_dict(cls, data: dict):
        id_t = data.get("id_tiket", "UNKNOWN")
        kat = data.get("kategori", "Presale")
        harga = data.get("harga_dasar", 100000)
        return cls(id_t, kat, harga)

    @staticmethod
    def hitung_pajak(harga: float, persentase_pajak: float = 11.0) -> float:
        return harga * (persentase_pajak / 100.0) if harga > 0 else 0.0


class Stage:
    def __init__(self, id_stage: str, nama_stage: str, kapasitas_maksimal: int):
        self.id_stage = id_stage
        self.nama_stage = nama_stage
        self.__kapasitas_maksimal = 0
        self.__daftar_penampil = []
        
        self.kapasitas_maksimal = kapasitas_maksimal

    @property
    def kapasitas_maksimal(self) -> int:
        return self.__kapasitas_maksimal

    @kapasitas_maksimal.setter
    def kapasitas_maksimal(self, value: int):
        if not isinstance(value, int) or value < 100:
            print(f"[Peringatan Validasi] Kapasitas stage {self.nama_stage} minimal harus 100 penonton!")
            return
        self.__kapasitas_maksimal = value

    @property
    def daftar_penampil(self) -> list:
        return self.__daftar_penampil

    def tambah_penampil(self, nama_artis: str, jam_tampil: str):
        if not Stage.validasi_format_jam(jam_tampil):
            print(f"[Peringatan Validasi] Format jam '{jam_tampil}' salah! Gunakan format HH:MM (contoh: 19:30)")
            return
        self.__daftar_penampil.append({"artis": nama_artis, "jam": jam_tampil})
        print(f"[Sukses] {nama_artis} berhasil dijadwalkan di {self.nama_stage} jam {jam_tampil}.")

    def tampilkan_jadwal(self):
        print(f"\n--- Jadwal Pertunjukan di Stage: {self.nama_stage} (Kapasitas: {self.kapasitas_maksimal}) ---")
        if not self.__daftar_penampil:
            print("  (Belum ada penampil yang terdaftar)")
        else:
            for item in self.__daftar_penampil:
                print(f"  - Jam {item['jam']} WIB : {item['artis']}")

    @classmethod
    def buat_stage_utama(cls, id_stage: str):
        return cls(id_stage, "Pestapora Main Stage", 15000)

    @staticmethod
    def validasi_format_jam(jam_str: str) -> bool:
        parts = jam_str.split(":")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return 0 <= int(parts[0]) <= 23 and 0 <= int(parts[1]) <= 59
        return False


class Pemesanan:
    def __init__(self, id_pemesanan: str, nama_pemesan: str, tiket: TiketKonser):
        self.id_pemesanan = id_pemesanan
        self.nama_pemesan = nama_pemesan
        self.tiket = tiket
        self.__status_pembayaran = "Pending"
        
        PestaporaApp.total_tiket_terjual += 1

    @property
    def status_pembayaran(self) -> str:
        return self.__status_pembayaran

    @status_pembayaran.setter
    def status_pembayaran(self, status_baru: str):
        opsi_valid = ["Pending", "Lunas", "Batal"]
        if not status_baru or status_baru.capitalize() not in opsi_valid:
            print(f"[Peringatan Validasi] Status '{status_baru}' tidak valid. Pilih dari {opsi_valid}")
            return
        self.__status_pembayaran = status_baru.capitalize()

    def cetak_tiket_resmi(self):
        pajak = TiketKonser.hitung_pajak(self.tiket.harga_dasar)
        total_harga = self.tiket.harga_dasar + pajak
        
        print(f"\n==========================================")
        print(f"        TICKET PASS - {PestaporaApp.nama_event.upper()}")
        print(f"==========================================")
        print(f" ID Pemesanan : {self.id_pemesanan}")
        print(f" Nama Pemesan : {self.nama_pemesan}")
        print(f" Kategori     : {self.tiket.kategori}")
        print(f" Harga Dasar  : Rp {self.tiket.harga_dasar:,.2f}")
        print(f" Pajak (11%)  : Rp {pajak:,.2f}")
        print(f" Total Bayar  : Rp {total_harga:,.2f}")
        print(f" Status       : {self.status_pembayaran}")
        print(f"==========================================")

    @classmethod
    def reset_total_penjualan(cls):
        PestaporaApp.total_tiket_terjual = 0
        print("\n[Admin] Counter total tiket terjual telah di-reset ke 0.")

    @staticmethod
    def buat_kode_transaksi(index: int) -> str:
        return f"PSTPR-2026-{index:04d}"


if __name__ == "__main__":
    print("=========================================================")
    print(f"   WELCOME TO {PestaporaApp.nama_event.upper()}")
    print("=========================================================\n")

    print("--- 1. Pembuatan Objek (Minimal 2 Objek per Class) ---")
    app1 = PestaporaApp("Gambir Expo Jakarta", "v1.0.0")
    app2 = PestaporaApp("Parkir Timur Senayan", "v1.2.0")

    tiket1 = TiketKonser("TKT-001", "VIP", 750000)
    tiket2 = TiketKonser.buat_dari_dict({"id_tiket": "TKT-002", "kategori": "Presale", "harga_dasar": 450000})

    stage1 = Stage("STG-01", "Standup Stage", 500)
    stage2 = Stage.buat_stage_utama("STG-00")

    pesanan1 = Pemesanan(Pemesanan.buat_kode_transaksi(1), "Ridho", tiket1)
    pesanan2 = Pemesanan(Pemesanan.buat_kode_transaksi(2), "Puput", tiket2)

    app1.tampilkan_info_app()
    app2.tampilkan_info_app()

    print("\n--- 2. Pengujian Method (Instance, Class, dan Static) ---")
    print("[Instance Method]")
    tiket1.tampilkan_detail()
    tiket2.tampilkan_detail()
    
    stage1.tambah_penampil("Komika A", "16:00")
    stage2.tambah_penampil("Band Headliner", "21:00")
    stage1.tampilkan_jadwal()
    
    pesanan1.status_pembayaran = "Lunas"
    pesanan1.cetak_tiket_resmi()

    print("\n[Static Method]")
    pajak_contoh = TiketKonser.hitung_pajak(500000)
    print(f"Hasil hitung pajak Rp 500.000 (11%): Rp {pajak_contoh:,.2f}")
    print(f"Validasi jam '25:99': {Stage.validasi_format_jam('25:99')}")
    print(f"Validasi jam '19:30': {Stage.validasi_format_jam('19:30')}")

    print("\n[Class Method]")
    print(f"Total tiket terjual saat ini: {PestaporaApp.total_tiket_terjual}")
    Pemesanan.reset_total_penjualan()
    print(f"Total tiket terjual setelah di-reset: {PestaporaApp.total_tiket_terjual}")

    print("\n--- 3. Pengujian Setter (Data Valid vs Tidak Valid) ---")
    
    print("\na. Pengujian TiketKonser (Harga Dasar & Kategori):")
    print("-> Set harga dasar VALID (Rp 800.000):")
    tiket1.harga_dasar = 800000
    print(f"   Harga baru: Rp {tiket1.harga_dasar:,.2f}")
    
    print("-> Set harga dasar TIDAK VALID (-50000):")
    tiket1.harga_dasar = -50000

    print("-> Set kategori VALID ('Early Bird'):")
    tiket1.kategori = "Early Bird"
    print(f"   Kategori baru: {tiket1.kategori}")

    print("-> Set kategori TIDAK VALID ('VIP Ekstra'):")
    tiket1.kategori = "VIP Ekstra"

    print("\nb. Pengujian Stage (Kapasitas Maksimal):")
    print("-> Set kapasitas VALID (1000):")
    stage1.kapasitas_maksimal = 1000
    print(f"   Kapasitas baru: {stage1.kapasitas_maksimal}")

    print("-> Set kapasitas TIDAK VALID (50):")
    stage1.kapasitas_maksimal = 50

    print("\nc. Pengujian Pemesanan (Status Pembayaran):")
    print("-> Set status VALID ('Lunas'):")
    pesanan2.status_pembayaran = "Lunas"
    print(f"   Status baru: {pesanan2.status_pembayaran}")

    print("-> Set status TIDAK VALID ('Belum Lunas'):")
    pesanan2.status_pembayaran = "Belum Lunas"