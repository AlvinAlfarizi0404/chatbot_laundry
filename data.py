# data.py
import sqlite3
from datetime import datetime, timedelta, timezone

def get_wib_now():
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=7)
# Data Harga Laundry Pakaian
# Format: { 'Item': { 'Layanan': Harga } }
HARGA_PAKAIAN = {
    'Kaos': {
        'Reguler': 2000,
        'Express': 3000,
        'Same Day': 5000
    },
    'Kemeja': {
        'Reguler': 2500,
        'Express': 3500,
        'Same Day': 5500
    },
    'Celana': {
        'Reguler': 2500,
        'Express': 3500,
        'Same Day': 5500
    },
    'Jaket Hoodie': {
        'Reguler': 3000,
        'Express': 5000,
        'Same Day': 6000
    },
    'Selimut': {
        'Reguler': 7000,
        'Express': 10000,
        'Same Day': 15000
    }
}

# Data Harga Laundry Sepatu
HARGA_SEPATU = {
    'Sneakers': {
        'Fast Clean': 20000,
        'Deep Clean': 25000
    },
    'Running': {
        'Fast Clean': 25000,
        'Deep Clean': 30000
    },
    'Canvas': {
        'Fast Clean': 20000,
        'Deep Clean': 25000
    },
    'Kulit': {
        'Fast Clean': 27000,
        'Deep Clean': 35000
    }
}

# Helper untuk mendapatkan nama layanan
LAYANAN_PAKAIAN_MAP = {
    '1': 'Reguler',
    '2': 'Express',
    '3': 'Same Day'
}

LAYANAN_SEPATU_MAP = {
    '1': 'Fast Clean',
    '2': 'Deep Clean'
}

def get_db_connection():
    conn = sqlite3.connect('laundry.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pesanan (
            id_pesanan TEXT PRIMARY KEY,
            waktu_pesan TEXT,
            estimasi_jam INTEGER,
            status TEXT,
            layanan TEXT,
            jenis TEXT,
            total INTEGER,
            metode_pembayaran TEXT DEFAULT 'Tidak Diketahui',
            status_pembayaran TEXT DEFAULT 'Belum Dibayar'
        )
    ''')
    # Migrasi kolom untuk DB lama
    for kolom, default in [
        ("metode_pembayaran", "'Tidak Diketahui'"),
        ("status_pembayaran", "'Belum Dibayar'"),
    ]:
        try:
            c.execute(f"ALTER TABLE pesanan ADD COLUMN {kolom} TEXT DEFAULT {default}")
            conn.commit()
        except Exception:
            pass  # Kolom sudah ada, abaikan
    c.execute('''
        CREATE TABLE IF NOT EXISTS member (
            id_member TEXT PRIMARY KEY,
            nama TEXT,
            whatsapp TEXT,
            alamat TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS keluhan (
            id_keluhan TEXT PRIMARY KEY,
            kategori TEXT,
            id_pesanan TEXT,
            isi_keluhan TEXT,
            waktu TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_member(member_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM member WHERE id_member = ?', (member_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'Nama': row['nama'], 'WhatsApp': row['whatsapp'], 'Alamat': row['alamat']}
    return None

def add_member(member_id, nama, whatsapp, alamat):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO member (id_member, nama, whatsapp, alamat) VALUES (?, ?, ?, ?)',
              (member_id, nama, whatsapp, alamat))
    conn.commit()
    conn.close()

def add_keluhan(id_keluhan, kategori, id_pesanan, isi_keluhan):
    conn = get_db_connection()
    c = conn.cursor()
    waktu = get_wib_now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO keluhan (id_keluhan, kategori, id_pesanan, isi_keluhan, waktu) VALUES (?, ?, ?, ?, ?)',
              (id_keluhan, kategori, id_pesanan, isi_keluhan, waktu))
    conn.commit()
    conn.close()

def add_pesanan(id_pesanan, layanan, jenis, total, estimasi_jam, metode_pembayaran='Tidak Diketahui'):
    conn = get_db_connection()
    c = conn.cursor()
    waktu_pesan = get_wib_now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'Sedang Dicuci'
    # QRIS = langsung lunas, metode lain = belum dibayar
    status_pembayaran = 'Sudah Dibayar' if metode_pembayaran == 'Qris' else 'Belum Dibayar'
    c.execute('''
        INSERT INTO pesanan (id_pesanan, waktu_pesan, estimasi_jam, status, layanan, jenis, total, metode_pembayaran, status_pembayaran)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_pesanan, waktu_pesan, estimasi_jam, status, layanan, jenis, total, metode_pembayaran, status_pembayaran))
    conn.commit()
    conn.close()

def get_all_pesanan():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pesanan ORDER BY waktu_pesan DESC')
    rows = c.fetchall()

    result = []
    for row in rows:
        pesanan = dict(row)
        # Auto-update status pengerjaan jika sudah melewati estimasi
        if pesanan['status'] != 'Selesai':
            waktu_pesan = datetime.strptime(pesanan['waktu_pesan'], '%Y-%m-%d %H:%M:%S')
            estimasi_selesai = waktu_pesan + timedelta(hours=pesanan['estimasi_jam'])
            if get_wib_now() >= estimasi_selesai:
                c.execute('UPDATE pesanan SET status = ? WHERE id_pesanan = ?', ('Selesai', pesanan['id_pesanan']))
                conn.commit()
                pesanan['status'] = 'Selesai'

        result.append({
            'ID': pesanan['id_pesanan'],
            'Waktu': pesanan['waktu_pesan'],
            'Jenis': pesanan['jenis'],
            'Layanan': pesanan['layanan'],
            'Total': pesanan['total'],
            'Status': pesanan['status'],
            'MetodePembayaran': pesanan.get('metode_pembayaran') or 'Tidak Diketahui',
            'StatusPembayaran': pesanan.get('status_pembayaran') or 'Belum Dibayar',
        })

    conn.close()
    return result

def get_pesanan(id_pesanan):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pesanan WHERE id_pesanan = ?', (id_pesanan,))
    row = c.fetchone()
    
    if not row:
        conn.close()
        return None
        
    pesanan = dict(row)
    
    if pesanan['status'] != 'Selesai':
        waktu_pesan = datetime.strptime(pesanan['waktu_pesan'], '%Y-%m-%d %H:%M:%S')
        estimasi_selesai = waktu_pesan + timedelta(hours=pesanan['estimasi_jam'])
        
        if get_wib_now() >= estimasi_selesai:
            c.execute('UPDATE pesanan SET status = ? WHERE id_pesanan = ?', ('Selesai', id_pesanan))
            conn.commit()
            pesanan['status'] = 'Selesai'
            
    conn.close()
    
    return {
        'Status': pesanan['status'],
        'Layanan': pesanan['layanan'],
        'Jenis': pesanan['jenis'],
        'Total': pesanan['total']
    }
