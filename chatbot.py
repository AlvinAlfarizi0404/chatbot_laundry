import random
from data import HARGA_PAKAIAN, HARGA_SEPATU, LAYANAN_PAKAIAN_MAP, LAYANAN_SEPATU_MAP, get_pesanan, add_pesanan, get_member, add_member, add_keluhan

class LaundryFSM:
    def __init__(self):
        # FSM Definition
        self.q0 = 'q_MENU_PILIHAN'
        self.state = self.q0
        self.order_data = self._init_order_data()

    def _init_order_data(self):
        return {
            'jenis_laundry': None, # 'Pakaian' or 'Sepatu'
            'layanan': None,       # 'Reguler', 'Express', dll
            'items_pakaian': {'Kaos': 0, 'Kemeja': 0, 'Celana': 0, 'Jaket Hoodie': 0, 'Selimut': 0},
            'jenis_sepatu': None,  # 'Sneakers', dll
            'member_id': None,
            'is_member': False,
            'diskon': 0,
            'total_harga': 0,
            'metode_pembayaran': None,
            # Data pendaftaran member baru
            'new_member': {'Nama': '', 'WhatsApp': '', 'Alamat': ''},
            # Data keluhan pelanggan
            'keluhan': {'kategori': None, 'id_pesanan': None, 'isi': None}
        }

    def reset_fsm(self):
        self.state = self.q0
        self.order_data = self._init_order_data()

    def process_input(self, user_input):
        """
        Fungsi transisi (delta).
        Menerima input (Sigma) dan mengembalikan balasan serta mengubah state (Q).
        """
        user_input = user_input.strip()
        current_state = self.state

        # --- TRANSISI FSM ---

        if current_state == 'q_MENU_PILIHAN':
            if user_input == '1':
                self.state = 'q_PILIH_LAUNDRY'
                return self._msg_pilih_laundry()
            elif user_input == '2':
                self.state = 'q_CEK_PESANAN'
                return "Silakan masukkan ID Pesanan Anda (contoh: ORD-1234):"
            elif user_input == '3':
                self.state = 'q_INFO_LAYANAN_MENU'
                return self._msg_info_layanan_menu()
            elif user_input == '4':
                self.state = 'q_INFO_MEMBER'
                return self._msg_info_member()
            elif user_input == '5':
                self.state = 'q_KATEGORI_KELUHAN'
                return self._msg_kategori_keluhan()
            else:
                return "Input tidak valid. Silakan pilih angka 1-5.\n\n" + self._msg_start()

        elif current_state == 'q_CEK_PESANAN':
            pesanan = get_pesanan(user_input)
            if pesanan:
                msg = f"Data Pesanan ditemukan!\n\n"
                msg += f"ID Pesanan: {user_input}\n"
                msg += f"Jenis: {pesanan['Jenis']} - {pesanan['Layanan']}\n"
                msg += f"Total: Rp {pesanan['Total']:,}\n"
                msg += f"Status saat ini: {pesanan['Status']}\n\n"
                msg += "Ketik apapun untuk kembali ke menu utama."
                self.reset_fsm()
                return msg
            else:
                msg = "Nomor pesanan salah atau Anda belum melakukan pemesanan.\n\n"
                msg += "Ketik apapun untuk kembali ke menu utama."
                self.reset_fsm()
                return msg

        elif current_state == 'q_PILIH_LAUNDRY':
            if user_input == '1':
                self.order_data['jenis_laundry'] = 'Pakaian'
                self.state = 'q_LAYANAN_PAKAIAN'
                return self._msg_layanan_pakaian()
            elif user_input == '2':
                self.order_data['jenis_laundry'] = 'Sepatu'
                self.state = 'q_JENIS_SEPATU'
                return self._msg_jenis_sepatu()
            else:
                return "Input tidak valid. Silakan pilih 1 atau 2.\n\n" + self._msg_pilih_laundry()

        # --- ALUR PAKAIAN ---
        elif current_state == 'q_LAYANAN_PAKAIAN':
            if user_input in LAYANAN_PAKAIAN_MAP:
                self.order_data['layanan'] = LAYANAN_PAKAIAN_MAP[user_input]
                self.state = 'q_INPUT_PAKAIAN'
                msg = "Masukkan jumlah item yang akan dicuci (pisahkan dengan koma):\n"
                msg += "1. Jumlah Kaos\n2. Jumlah Kemeja\n3. Jumlah Celana\n4. Jumlah Jaket Hoodie\n5. Jumlah Selimut\n\n"
                msg += "Contoh ketik: 2,1,0,1,0"
                return msg
            else:
                return "Input tidak valid.\n\n" + self._msg_layanan_pakaian()

        elif current_state == 'q_INPUT_PAKAIAN':
            import re
            parts = re.findall(r'\d+', user_input)
            if len(parts) == 5:
                self.order_data['items_pakaian']['Kaos'] = int(parts[0])
                self.order_data['items_pakaian']['Kemeja'] = int(parts[1])
                self.order_data['items_pakaian']['Celana'] = int(parts[2])
                self.order_data['items_pakaian']['Jaket Hoodie'] = int(parts[3])
                self.order_data['items_pakaian']['Selimut'] = int(parts[4])
                self._hitung_total_pakaian()
                self.state = 'q_CONFIRM_PESANAN_PAKAIAN'
                return self._msg_ringkasan_pakaian()
            else:
                return "Format tidak valid. Mohon masukkan tepat 5 angka dipisahkan koma.\nContoh: 2,1,0,1,0"

        elif current_state == 'q_CONFIRM_PESANAN_PAKAIAN':
            if user_input == '1':
                self.state = 'q_TANYA_MEMBER'
                return self._msg_tanya_member()
            elif user_input == '2':
                self.state = 'q_LAYANAN_PAKAIAN'
                # Reset pakaian items
                self.order_data['items_pakaian'] = {k: 0 for k in self.order_data['items_pakaian']}
                return self._msg_layanan_pakaian()
            else:
                return "Input tidak valid.\n\nApakah pesanan sudah benar?\n1. Ya\n2. Ulangi"

        # --- ALUR SEPATU ---
        elif current_state == 'q_JENIS_SEPATU':
            jenis_sepatu_map = {'1': 'Sneakers', '2': 'Running', '3': 'Canvas', '4': 'Kulit'}
            if user_input in jenis_sepatu_map:
                self.order_data['jenis_sepatu'] = jenis_sepatu_map[user_input]
                self.state = 'q_LAYANAN_SEPATU'
                return self._msg_layanan_sepatu()
            else:
                return "Input tidak valid.\n\n" + self._msg_jenis_sepatu()

        elif current_state == 'q_LAYANAN_SEPATU':
            if user_input in LAYANAN_SEPATU_MAP:
                self.order_data['layanan'] = LAYANAN_SEPATU_MAP[user_input]
                self._hitung_total_sepatu()
                # Langsung ke Tanya Member setelah memilih layanan sepatu
                self.state = 'q_TANYA_MEMBER'
                msg = f"Pesanan: {self.order_data['jenis_sepatu']} - {self.order_data['layanan']}\nTotal: Rp {self.order_data['total_harga']:,}\n\n"
                return msg + self._msg_tanya_member()
            else:
                return "Input tidak valid.\n\n" + self._msg_layanan_sepatu()

        # --- ALUR MEMBER ---
        elif current_state == 'q_TANYA_MEMBER':
            if user_input == '1':
                self.state = 'q_INPUT_ID_MEMBER'
                return "Masukan Nomor Member: "
            elif user_input == '2':
                self.state = 'q_TAWARKAN_MEMBER'
                return self._msg_tawarkan_member()
            else:
                return "Input tidak valid.\n\n" + self._msg_tanya_member()
        
        elif current_state == 'q_INPUT_ID_MEMBER':
            member = get_member(user_input)
            if member:
                self.order_data['is_member'] = True
                self.order_data['member_id'] = user_input
                self._apply_discount()
                self.state = 'q_LANJUT_PESANAN'
                return f"Member ditemukan ({member['Nama']}).\nDiskon 5% diterapkan.\nTotal setelah diskon: Rp {self.order_data['total_harga']:,}\n\nLanjut Pesanan :\n1. Iya\n2. Tidak"
            else:
                self.state = 'q_TANYA_MEMBER'
                return "Nomor Member tidak ditemukan.\n\n" + self._msg_tanya_member()

        elif current_state == 'q_TAWARKAN_MEMBER':
            if user_input == '1':
                self.state = 'q_DAFTAR_MEMBER'
                msg = "Isi form pendaftaran member (pisahkan dengan koma):\n"
                msg += "Nama Lengkap, Nomor WhatsApp, Alamat\n\n"
                msg += "Contoh ketik: Budi Santoso, 08123456789, Jl. Merdeka No. 10"
                return msg
            elif user_input == '2':
                self.state = 'q_METODE_PEMBAYARAN'
                return self._msg_pilih_pembayaran()
            else:
                return "Input tidak valid.\n\nApakah ingin mendaftar member?\n1. Ya\n2. Tidak"

        elif current_state == 'q_DAFTAR_MEMBER':
            parts = [p.strip() for p in user_input.split(',')]
            if len(parts) == 3:
                self.order_data['new_member']['Nama'] = parts[0]
                self.order_data['new_member']['WhatsApp'] = parts[1]
                self.order_data['new_member']['Alamat'] = parts[2]
                
                # Generate new member ID
                new_id = f"MBR-{random.randint(100, 999)}"
                add_member(new_id, parts[0], parts[1], parts[2])
                
                self.order_data['is_member'] = True
                self.order_data['member_id'] = new_id
                self._apply_discount()
                
                self.state = 'q_METODE_PEMBAYARAN'
                msg = f"Selamat member anda sudah jadi. ID Anda: {new_id}\nDiskon 5% diterapkan. Total: Rp {self.order_data['total_harga']:,}\n\n"
                return msg + self._msg_pilih_pembayaran()
            else:
                return "Format tidak valid. Mohon masukkan tepat 3 data dipisahkan koma.\nContoh: Budi Santoso, 08123456789, Jl. Merdeka No. 10"

        elif current_state == 'q_INFO_MEMBER':
            if user_input == '1':
                self.state = 'q_DAFTAR_MEMBER_BARU'
                msg = "Isi form pendaftaran member (pisahkan dengan koma):\n"
                msg += "Nama Lengkap, Nomor WhatsApp, Alamat\n\n"
                msg += "Contoh ketik: Budi Santoso, 08123456789, Jl. Merdeka No. 10"
                return msg
            elif user_input == '2':
                self.reset_fsm()
                return "Kembali ke menu utama.\n\n" + self._msg_start()
            else:
                return "Input tidak valid.\n\n" + self._msg_info_member()

        elif current_state == 'q_DAFTAR_MEMBER_BARU':
            parts = [p.strip() for p in user_input.split(',')]
            if len(parts) == 3:
                nama, whatsapp, alamat = parts[0], parts[1], parts[2]
                new_id = f"MBR-{random.randint(100, 999)}"
                add_member(new_id, nama, whatsapp, alamat)
                
                msg = f"🎉 Selamat! Pendaftaran member berhasil.\n"
                msg += f"ID Member Anda: {new_id}\n"
                msg += "Silakan simpan ID Member ini untuk digunakan saat memesan laundry.\n\n"
                msg += "Ketik apapun untuk kembali ke menu utama."
                self.reset_fsm()
                return msg
            else:
                return "Format tidak valid. Mohon masukkan tepat 3 data dipisahkan koma.\nContoh: Budi Santoso, 08123456789, Jl. Merdeka No. 10"

        # --- ALUR INFORMASI LAYANAN ---
        elif current_state == 'q_INFO_LAYANAN_MENU':
            if user_input == '1':
                self.state = 'q_INFO_LAYANAN_DETAIL'
                return self._msg_info_harga_pakaian() + "\n\nKetik apapun untuk kembali ke Menu Informasi Layanan."
            elif user_input == '2':
                self.state = 'q_INFO_LAYANAN_DETAIL'
                return self._msg_info_harga_sepatu() + "\n\nKetik apapun untuk kembali ke Menu Informasi Layanan."
            elif user_input == '3':
                self.state = 'q_INFO_LAYANAN_DETAIL'
                return self._msg_info_estimasi() + "\n\nKetik apapun untuk kembali ke Menu Informasi Layanan."
            elif user_input == '4':
                self.state = 'q_INFO_LAYANAN_DETAIL'
                return self._msg_info_lokasi() + "\n\nKetik apapun untuk kembali ke Menu Informasi Layanan."
            elif user_input == '5':
                self.state = 'q_INFO_LAYANAN_DETAIL'
                return self._msg_info_snk() + "\n\nKetik apapun untuk kembali ke Menu Informasi Layanan."
            elif user_input == '0':
                self.reset_fsm()
                return "Kembali ke menu utama.\n\n" + self._msg_start()
            else:
                return "Input tidak valid. Silakan pilih 0-5.\n\n" + self._msg_info_layanan_menu()

        elif current_state == 'q_INFO_LAYANAN_DETAIL':
            self.state = 'q_INFO_LAYANAN_MENU'
            return self._msg_info_layanan_menu()

        # --- ALUR KELUHAN PELANGGAN ---
        elif current_state == 'q_KATEGORI_KELUHAN':
            kategori_map = {'1': 'Keterlambatan Layanan', '2': 'Hasil Cucian Kurang Bersih/Rusak', '3': 'Pelayanan Karyawan', '4': 'Lainnya'}
            if user_input in kategori_map:
                self.order_data['keluhan']['kategori'] = kategori_map[user_input]
                self.state = 'q_ID_PESANAN_KELUHAN'
                return "Silakan masukkan ID Pesanan Anda jika ada (contoh: ORD-1234), atau ketik '0' jika Anda tidak mengingatnya atau tidak ada:"
            else:
                return "Input tidak valid.\n\n" + self._msg_kategori_keluhan()

        elif current_state == 'q_ID_PESANAN_KELUHAN':
            if user_input != '0':
                self.order_data['keluhan']['id_pesanan'] = user_input
            else:
                self.order_data['keluhan']['id_pesanan'] = 'Tidak ada/Lupa'
            
            self.state = 'q_ISI_KELUHAN'
            return "Silakan ceritakan detail keluhan Anda secara lengkap. Kami siap mendengarkan dan memperbaikinya:"

        elif current_state == 'q_ISI_KELUHAN':
            self.order_data['keluhan']['isi'] = user_input
            
            ticket_id = f"TIK-{random.randint(1000, 9999)}"
            kategori = self.order_data['keluhan']['kategori']
            id_pesanan = self.order_data['keluhan']['id_pesanan']
            
            add_keluhan(ticket_id, kategori, id_pesanan, user_input)
            
            msg = f"🙏 Terima kasih atas masukan Anda. Keluhan Anda telah kami terima dengan nomor tiket: {ticket_id}\n\n"
            msg += "Tim kami akan segera menindaklanjuti laporan Anda secepatnya. Mohon maaf atas ketidaknyamanan yang terjadi.\n\n"
            msg += "Ketik apapun untuk kembali ke menu utama."
            
            self.reset_fsm()
            return msg

        # --- ALUR PEMBAYARAN ---
        elif current_state == 'q_LANJUT_PESANAN':
            if user_input == '1':
                self.state = 'q_METODE_PEMBAYARAN'
                return self._msg_pilih_pembayaran()
            elif user_input == '2':
                self.reset_fsm()
                return "Pesanan dibatalkan.\n\n" + self._msg_start()
            else:
                return "Input tidak valid.\nLanjut Pesanan :\n1. Iya\n2. Tidak"

        elif current_state == 'q_METODE_PEMBAYARAN':
            metode_map = {'1': 'Qris', '2': 'Bayar di Tempat', '3': 'Bayar Setelah Jadi'}
            if user_input in metode_map:
                self.order_data['metode_pembayaran'] = metode_map[user_input]
                self.state = 'q_MENU_PILIHAN' # Kembali ke awal setelah selesai
                
                # Buat kode pesanan
                kode_pesanan = f"ORD-{random.randint(1000, 9999)}"
                estimasi = self._get_estimasi()
                estimasi_jam = self._get_estimasi_jam()
                
                # Simpan ke DB Pesanan
                add_pesanan(
                    id_pesanan=kode_pesanan,
                    layanan=self.order_data['layanan'],
                    jenis=self.order_data['jenis_laundry'],
                    total=self.order_data['total_harga'],
                    estimasi_jam=estimasi_jam
                )
                
                msg = f"Berhasil membuat pesanan!\nKode Pesanan: {kode_pesanan}\nEstimasi selesai: {estimasi}\n\nTerima kasih telah menggunakan CleanWash Laundry."
                # Reset FSM behind the scenes but we wait for next input to show menu, or just show it now
                msg += "\n\nKetik apapun untuk kembali ke menu utama."
                self.reset_fsm()
                return msg
            else:
                return "Input tidak valid.\n\n" + self._msg_pilih_pembayaran()
                
        else:
            # Fallback (Safety)
            self.reset_fsm()
            return "Terjadi kesalahan state. Memulai ulang...\n\n" + self._msg_start()

    # --- HELPER MESSAGES ---

    def _msg_start(self):
        return "Selamat datang di CleanWash Laundry\nSaya dapat membantu Anda:\n1. Buat Pesanan Laundry\n2. Cek Status Pesanan\n3. Informasi Layanan\n4. Informasi Member\n5. Keluhan Pelanggan"

    def _msg_pilih_laundry(self):
        return "Jenis laundry yang ingin Anda pesan:\n1. Laundry Pakaian\n2. Laundry Sepatu"

    def _msg_layanan_pakaian(self):
        return "Jenis layanan yang Anda inginkan:\n1. Reguler (3-4 Hari)\n2. Express (1 Hari)\n3. Same Day (8 jam)"

    def _msg_jenis_sepatu(self):
        return "Jenis sepatu yang akan dicuci:\n1. Sneakers\n2. Running\n3. Canvas\n4. Kulit\nSilakan pilih:"
    
    def _msg_layanan_sepatu(self):
        return "Pilih layanan:\n1. Fast Clean (2 Hari)\n2. Deep Clean (2 Hari)\nSilakan pilih:"
        
    def _msg_tanya_member(self):
        return "Apakah Anda sudah menjadi member?\n1. Ya\n2. Belum"

    def _msg_tawarkan_member(self):
        return "Apakah Ingin Mendaftar Sebagai Member?, Keuntunganya menarik lohh :\n✓ Diskon 5%\n✓ Promo bulanan\n✓ Prioritas layanan\nApakah ingin mendaftar member?\n1. Ya\n2. Tidak"

    def _msg_pilih_pembayaran(self):
        return "Pilih Metode Pembayaran:\n1. Qris\n2. Bayar di Tempat\n3. Bayar Setelah Jadi"
        
    def _msg_info_member(self):
        msg = "✨ Keuntungan Menjadi Member CleanWash ✨\n"
        msg += "✓ Diskon 5% untuk setiap transaksi\n"
        msg += "✓ Promo bulanan eksklusif\n"
        msg += "✓ Prioritas layanan pengerjaan\n\n"
        msg += "Apakah Anda ingin mendaftar sebagai member sekarang?\n"
        msg += "1. Ya, daftar member\n"
        msg += "2. Kembali ke menu utama"
        return msg

    def _msg_kategori_keluhan(self):
        msg = "Kami mohon maaf atas ketidaknyamanan Anda. Silakan pilih kategori keluhan:\n"
        msg += "1. Keterlambatan Layanan\n"
        msg += "2. Hasil Cucian Kurang Bersih/Rusak\n"
        msg += "3. Pelayanan Karyawan\n"
        msg += "4. Lainnya\n\n"
        msg += "Ketik angka pilihan Anda:"
        return msg

    def _msg_info_layanan_menu(self):
        msg = "Berikut adalah informasi layanan CleanWash Laundry. Silakan pilih informasi yang ingin Anda ketahui:\n"
        msg += "1. Daftar Harga & Layanan Pakaian 👕\n"
        msg += "2. Daftar Harga & Layanan Sepatu 👟\n"
        msg += "3. Estimasi Waktu Pengerjaan ⏱️\n"
        msg += "4. Lokasi & Jam Operasional 📍\n"
        msg += "5. Syarat & Ketentuan Layanan 📜\n"
        msg += "0. Kembali ke Menu Utama 🏠"
        return msg

    def _msg_info_harga_pakaian(self):
        msg = "📋 **Daftar Harga Layanan Pakaian**\n"
        msg += "• Kaos: Rp 2.000 - Rp 5.000 / pcs\n"
        msg += "• Kemeja & Celana: Rp 2.500 - Rp 5.500 / pcs\n"
        msg += "• Jaket Hoodie: Rp 3.000 - Rp 6.000 / pcs\n"
        msg += "• Selimut: Rp 7.000 - Rp 15.000 / pcs\n"
        msg += "*(Harga bervariasi bergantung pada pilihan Reguler/Express/Same Day)*"
        return msg

    def _msg_info_harga_sepatu(self):
        msg = "📋 **Daftar Harga Layanan Sepatu**\n"
        msg += "• Sneakers & Canvas: Rp 20.000 - Rp 25.000 / pasang\n"
        msg += "• Running: Rp 25.000 - Rp 30.000 / pasang\n"
        msg += "• Kulit (Leather): Rp 27.000 - Rp 35.000 / pasang\n"
        msg += "*(Harga bergantung pada layanan Fast Clean atau Deep Clean)*"
        return msg

    def _msg_info_estimasi(self):
        msg = "⏱️ **Estimasi Waktu Pengerjaan**\n"
        msg += "• Reguler (Pakaian): Selesai 3-4 Hari\n"
        msg += "• Express (Pakaian): Selesai 1 Hari (24 Jam)\n"
        msg += "• Same Day (Pakaian): Selesai 8 Jam\n"
        msg += "• Fast Clean / Deep Clean (Sepatu): Selesai 2 Hari"
        return msg

    def _msg_info_lokasi(self):
        msg = "📍 **Lokasi & Jam Operasional**\n"
        msg += "• Jam Buka: Senin - Minggu (08.00 - 21.00 WIB)\n"
        msg += "• Alamat: Jl. Bersih Kilau No. 99, Kota Baru\n"
        msg += "• WhatsApp CS: 0812-XXXX-XXXX"
        return msg

    def _msg_info_snk(self):
        msg = "📜 **Syarat & Ketentuan Layanan**\n"
        msg += "1. Pakaian luntur harap dipisah atau diinfokan sebelumnya kepada kami.\n"
        msg += "2. Pihak laundry tidak bertanggung jawab atas barang berharga yang tertinggal di kantong.\n"
        msg += "3. Klaim komplain atau garansi cuci ulang maksimal 1x24 jam setelah cucian diambil dengan menyertakan nota.\n"
        msg += "4. Cucian yang tidak diambil lebih dari 30 hari di luar tanggung jawab kami."
        return msg

    # --- HELPER LOGIC ---

    def _hitung_total_pakaian(self):
        total = 0
        layanan = self.order_data['layanan']
        for item, qty in self.order_data['items_pakaian'].items():
            if qty > 0:
                harga_satuan = HARGA_PAKAIAN[item][layanan]
                total += harga_satuan * qty
        self.order_data['total_harga'] = total

    def _hitung_total_sepatu(self):
        jenis = self.order_data['jenis_sepatu']
        layanan = self.order_data['layanan']
        self.order_data['total_harga'] = HARGA_SEPATU[jenis][layanan]

    def _apply_discount(self):
        if self.order_data['is_member']:
            diskon = int(self.order_data['total_harga'] * 0.05)
            self.order_data['diskon'] = diskon
            self.order_data['total_harga'] -= diskon

    def _msg_ringkasan_pakaian(self):
        items = self.order_data['items_pakaian']
        msg = "Ringkasan Pesanan:\n"
        msg += f"Kaos    : {items['Kaos']}\n"
        msg += f"Kemeja  : {items['Kemeja']}\n"
        msg += f"Celana  : {items['Celana']}\n"
        msg += f"Jaket   : {items['Jaket Hoodie']}\n"
        msg += f"Selimut : {items['Selimut']}\n"
        msg += f"Total: Rp {self.order_data['total_harga']:,}\n\n"
        msg += "Apakah pesanan sudah benar?\n1. Ya\n2. Ulangi"
        return msg

    def _get_estimasi(self):
        layanan = self.order_data['layanan']
        if layanan == 'Reguler': return '3-4 Hari'
        elif layanan == 'Express': return '1 Hari'
        elif layanan == 'Same Day': return '8 jam'
        elif layanan == 'Fast Clean': return '2 Hari'
        elif layanan == 'Deep Clean': return '2 Hari'
        return 'TBD'
        
    def _get_estimasi_jam(self):
        layanan = self.order_data['layanan']
        if layanan == 'Reguler': return 72 # 3 days
        elif layanan == 'Express': return 24 # 1 day
        elif layanan == 'Same Day': return 8
        elif layanan == 'Fast Clean': return 48
        elif layanan == 'Deep Clean': return 48
        return 24 # default
