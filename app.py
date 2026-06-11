import streamlit as st
from chatbot import LaundryFSM
from data import init_db, get_all_pesanan

init_db()

st.set_page_config(
    page_title="Astroclean - Laundry Cerdas",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session State ──────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

if 'fsm_v2' not in st.session_state:
    st.session_state.fsm_v2 = LaundryFSM()
    st.session_state.messages = [
        {"role": "assistant", "content": st.session_state.fsm_v2._msg_start()}
    ]


# ══════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════
def show_landing_page():
    # Deteksi navigasi dari tombol HTML (via JS window.parent.location)
    if st.query_params.get('go') == 'chat':
        st.query_params.clear()
        st.session_state.page = 'chatbot'
        st.rerun()
    if st.query_params.get('go') == 'cek_pesanan':
        st.query_params.clear()
        st.session_state.page = 'cek_pesanan'
        st.rerun()

    # Sembunyikan chrome Streamlit
    st.html("""
    <style>
        [data-testid="stHeader"]  { display:none !important; }
        [data-testid="stToolbar"] { display:none !important; }
        .stDeployButton           { display:none !important; }
        #MainMenu                 { visibility:hidden; }
        .block-container          { padding:0 !important; max-width:100% !important; }
        section[data-testid="stMain"] > div { padding:0 !important; }
        [data-testid="stHtml"]    { margin:0 !important; padding:0 !important; }
    </style>
    """)

    # Render seluruh landing page
    st.html("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
        <style>
            @import url('https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css');
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            * { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }
            html { scroll-behavior:smooth; }
            body { overflow-x:hidden; }
            :root {
                --primary:       #2563eb;
                --primary-dark:  #1e40af;
                --primary-light: #60a5fa;
                --secondary:     #0f172a;
                --text-main:     #334155;
                --text-muted:    #64748b;
                --bg-main:       #f8fafc;
                --hero-bg: linear-gradient(135deg,#dbeafe 0%,#eff6ff 55%,#f0f4ff 100%);
            }

            /* ── Navbar ── */
            .lp-navbar {
                width:100%; padding:16px 6%;
                display:flex; justify-content:space-between; align-items:center;
                background:rgba(255,255,255,.92);
                backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px);
                border-bottom:1px solid rgba(0,0,0,.07);
                position:sticky; top:0; z-index:100;
            }
            .lp-logo {
                display:flex; align-items:center; gap:10px;
                font-size:1.35rem; font-weight:700; color:var(--primary);
                text-decoration:none; cursor:pointer;
            }
            .lp-logo i { font-size:1.6rem; }
            .lp-nav-links { display:flex; list-style:none; gap:32px; }
            .lp-nav-links a {
                text-decoration:none; color:var(--text-main);
                font-weight:500; font-size:.95rem; transition:color .25s;
            }
            .lp-nav-links a:hover { color:var(--primary); }
            .lp-btn-nav {
                text-decoration:none; background:var(--primary); color:white;
                padding:10px 24px; border-radius:50px; font-weight:600;
                font-size:.9rem; transition:all .25s; cursor:pointer;
                box-shadow:0 4px 14px rgba(37,99,235,.3); border:none;
                display:inline-block;
            }
            .lp-btn-nav:hover { background:var(--primary-dark); transform:translateY(-2px); }

            /* ── Hero ── */
            .lp-hero {
                display:flex; align-items:center; justify-content:space-between;
                gap:48px; padding:90px 6% 80px;
                background:var(--hero-bg);
                position:relative; overflow:hidden; min-height:88vh;
            }
            .lp-hero::before {
                content:''; position:absolute; top:-8%; right:-4%;
                width:520px; height:520px; background:var(--primary-light);
                border-radius:50%; filter:blur(100px); opacity:.22; z-index:0;
            }
            .lp-hero::after {
                content:''; position:absolute; bottom:-12%; left:-4%;
                width:380px; height:380px; background:#818cf8;
                border-radius:50%; filter:blur(100px); opacity:.14; z-index:0;
            }
            .lp-hero-content { flex:1; max-width:580px; z-index:1; }
            .lp-badge {
                display:inline-flex; align-items:center; gap:6px;
                padding:6px 16px; background:rgba(37,99,235,.1); color:var(--primary);
                border-radius:50px; font-weight:600; font-size:.84rem;
                margin-bottom:22px; border:1px solid rgba(37,99,235,.18);
            }
            .lp-hero-content h1 {
                font-size:clamp(2.1rem,3.8vw,3.4rem);
                line-height:1.2; color:var(--secondary);
                margin-bottom:20px; font-weight:800;
            }
            .lp-highlight { color:var(--primary); }
            .lp-hero-content > p {
                font-size:1.08rem; color:var(--text-muted);
                line-height:1.75; margin-bottom:36px;
            }
            .lp-hero-btns { display:flex; gap:16px; flex-wrap:wrap; align-items:center; }
            .lp-btn-primary {
                display:inline-flex; align-items:center; gap:8px;
                text-decoration:none; background:var(--primary); color:white;
                padding:13px 30px; border-radius:50px; font-weight:600;
                font-size:.97rem; transition:all .25s; cursor:pointer;
                box-shadow:0 8px 22px rgba(37,99,235,.3); border:none;
            }
            .lp-btn-primary:hover { background:var(--primary-dark); transform:translateY(-2px); box-shadow:0 14px 28px rgba(37,99,235,.38); }
            .lp-btn-secondary {
                display:inline-flex; align-items:center;
                text-decoration:none; background:white; color:var(--primary);
                padding:13px 30px; border-radius:50px; font-weight:600;
                font-size:.97rem; border:1px solid rgba(37,99,235,.22); transition:all .25s;
            }
            .lp-btn-secondary:hover { background:#f1f5f9; }
            .lp-hero-image { flex:1; display:flex; justify-content:center; z-index:1; }

            /* ── Mockup card ── */
            .lp-mockup {
                width:335px; padding:22px;
                display:flex; flex-direction:column; gap:16px;
                background:rgba(255,255,255,.72); backdrop-filter:blur(14px);
                border:1px solid rgba(255,255,255,.65);
                box-shadow:0 24px 64px rgba(31,38,135,.1);
                border-radius:24px; animation:lp-float 6s ease-in-out infinite;
            }
            @keyframes lp-float {
                0%,100% { transform:translateY(0); }
                50%      { transform:translateY(-16px); }
            }
            .lp-mock-header {
                display:flex; align-items:center; gap:10px;
                font-weight:600; color:var(--secondary); font-size:.98rem;
                border-bottom:1px solid rgba(0,0,0,.06); padding-bottom:14px;
            }
            .lp-mock-header i { font-size:1.4rem; color:var(--primary); }
            .lp-mock-body { display:flex; flex-direction:column; gap:10px; min-height:200px; }
            .bubble { padding:10px 14px; border-radius:16px; font-size:.86rem; max-width:86%; line-height:1.5; }
            .bubble-bot { background:white; color:var(--text-main); align-self:flex-start; border-bottom-left-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,.05); }
            .bubble-user { background:var(--primary); color:white; align-self:flex-end; border-bottom-right-radius:4px; }
            .lp-mock-footer {
                display:flex; justify-content:space-between; align-items:center;
                padding:9px 14px; background:white; border-radius:50px;
                color:var(--text-muted); font-size:.86rem; border:1px solid #f1f5f9;
            }
            .lp-mock-footer i { color:var(--primary); font-size:1.15rem; }

            /* ── Features ── */
            .lp-features { padding:90px 6%; background:white; }
            .lp-sec-header { text-align:center; max-width:620px; margin:0 auto 56px; }
            .lp-sec-header h2 { font-size:clamp(1.75rem,2.8vw,2.4rem); color:var(--secondary); font-weight:700; margin-bottom:14px; }
            .lp-sec-header p { color:var(--text-muted); font-size:1.03rem; line-height:1.7; }
            .lp-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:24px; max-width:1200px; margin:0 auto; }
            .lp-card { padding:34px 26px; border-radius:22px; background:var(--bg-main); border:1px solid transparent; transition:all .3s ease; }
            .lp-card:hover { background:white; border-color:rgba(37,99,235,.12); box-shadow:0 10px 40px rgba(0,0,0,.07); transform:translateY(-6px); }
            .lp-icon { width:54px; height:54px; border-radius:14px; background:rgba(37,99,235,.1); display:flex; align-items:center; justify-content:center; margin-bottom:16px; }
            .lp-icon i { font-size:26px; color:var(--primary); }
            .lp-card h3 { margin-bottom:10px; font-size:1.1rem; color:var(--secondary); }
            .lp-card p  { color:var(--text-muted); font-size:.9rem; line-height:1.6; }

            /* ── Contact ── */
            .lp-contact { padding:90px 6%; background:linear-gradient(135deg,#f8fafc 0%,#dbeafe 100%); display:flex; justify-content:center; }
            .lp-contact-box { display:flex; width:100%; max-width:1000px; border-radius:24px; overflow:hidden; background:rgba(255,255,255,.72); backdrop-filter:blur(14px); border:1px solid rgba(255,255,255,.55); box-shadow:0 20px 60px rgba(31,38,135,.07); }
            .lp-contact-info { flex:1; padding:50px; }
            .lp-contact-info h2 { font-size:2.1rem; margin-bottom:12px; color:var(--secondary); }
            .lp-contact-info > p { color:var(--text-muted); margin-bottom:32px; }
            .lp-info-row { display:flex; align-items:center; gap:14px; margin-bottom:20px; font-size:.98rem; color:var(--secondary); font-weight:500; }
            .lp-info-row i { font-size:1.35rem; color:var(--primary); background:white; padding:10px; border-radius:50%; box-shadow:0 4px 10px rgba(0,0,0,.06); }
            .lp-contact-visual { flex:1; background:linear-gradient(135deg,#2563eb 0%,#1e40af 100%); display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; padding:50px; position:relative; overflow:hidden; }
            .lp-blob { position:absolute; width:260px; height:260px; background:rgba(255,255,255,.08); border-radius:50%; filter:blur(38px); }
            .lp-map-icon { font-size:76px; z-index:1; margin-bottom:16px; }
            .lp-contact-visual p { z-index:1; font-size:1.35rem; font-weight:600; }

            /* ── Footer ── */
            .lp-footer { background:var(--secondary); color:white; padding:48px 6% 20px; }
            .lp-footer-inner { display:flex; flex-direction:column; align-items:center; text-align:center; gap:16px; margin-bottom:32px; }
            .lp-footer-logo { font-size:1.65rem; font-weight:700; display:flex; align-items:center; gap:10px; }
            .lp-footer-inner > p { color:#94a3b8; max-width:480px; font-size:.93rem; line-height:1.65; }
            .lp-socials { display:flex; gap:11px; }
            .lp-socials a { color:white; background:rgba(255,255,255,.1); width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:50%; text-decoration:none; font-size:1.2rem; transition:all .3s; }
            .lp-socials a:hover { background:var(--primary); transform:translateY(-3px); }
            .lp-footer-bottom { text-align:center; padding-top:18px; border-top:1px solid rgba(255,255,255,.08); color:#64748b; font-size:.87rem; }

            @media (max-width:900px) {
                .lp-hero { flex-direction:column; text-align:center; padding:120px 6% 60px; min-height:auto; }
                .lp-hero-btns { justify-content:center; }
                .lp-contact-box { flex-direction:column; }
                .lp-nav-links { display:none; }
            }
        </style>
    </head>
    <body>

    <!-- NAVBAR -->
    <nav class="lp-navbar">
        <a class="lp-logo" href="#">
            <i class='bx bxs-washer'></i>
            <span>Astroclean</span>
        </a>
        <ul class="lp-nav-links">
            <li><a href="#hero">Beranda</a></li>
            <li><a href="#features">Layanan</a></li>
            <li><a href="#contact">Kontak</a></li>
            <li><a href="?go=cek_pesanan" target="_self" style="display:inline-flex;align-items:center;gap:5px;"><i class='bx bx-list-check' style='font-size:1.05rem;'></i> Cek Pesanan</a></li>
        </ul>
        <a href="?go=chat" target="_self" class="lp-btn-nav">
            <i class='bx bx-message-square-dots' style='vertical-align:middle;margin-right:6px;'></i> Coba Chatbot
        </a>
    </nav>

    <!-- HERO -->
    <section id="hero" class="lp-hero">
        <div class="lp-hero-content">
            <span class="lp-badge"><i class='bx bx-trending-up'></i> Inovasi Layanan 2026</span>
            <h1>Revolusi Layanan Laundry dengan <span class="lp-highlight">Chatbot</span></h1>
            <p>Memesan laundry, mengecek status pesanan, dan menyampaikan keluhan kini semudah mengirim pesan. Nikmati pengalaman cerdas bersama Astroclean.</p>
            <div class="lp-hero-btns">
                <a href="?go=chat" target="_self" class="lp-btn-primary">
                    <i class='bx bx-message-rounded-dots'></i> Mulai Percakapan
                </a>
                <a href="#features" class="lp-btn-secondary"><i class='bx bx-info-circle' style='margin-right:6px;'></i> Pelajari Lebih Lanjut</a>
            </div>
        </div>
        <div class="lp-hero-image">
            <div class="lp-mockup">
                <div class="lp-mock-header">
                    <i class='bx bx-bot'></i><span>Astroclean Bot</span>
                </div>
                <div class="lp-mock-body">
                    <div class="bubble bubble-bot">Halo! Selamat datang di Astroclean. Ada yang bisa saya bantu?</div>
                    <div class="bubble bubble-user">Saya ingin pesan laundry pakaian.</div>
                    <div class="bubble bubble-bot">Baik! Anda ingin layanan Reguler, Express, atau Same Day?</div>
                    <div class="bubble bubble-user">Express aja.</div>
                </div>
                <div class="lp-mock-footer">
                    <span>Ketik pesan Anda...</span>
                    <i class='bx bx-send'></i>
                </div>
            </div>
        </div>
    </section>

    <!-- FEATURES -->
    <section id="features" class="lp-features">
        <div class="lp-sec-header">
            <h2>Layanan Chatbot Pintar Kami</h2>
            <p>Sistem FSM (Finite State Machine) chatbot kami dirancang untuk menangani berbagai kebutuhan laundry Anda secara otomatis selama 24 jam.</p>
        </div>
        <div class="lp-grid">
            <div class="lp-card">
                <div class="lp-icon"><i class='bx bx-shopping-bag'></i></div>
                <h3>Buat Pesanan</h3>
                <p>Pesan layanan laundry pakaian atau sepatu langsung dari chat. Kalkulasi harga otomatis.</p>
            </div>
            <div class="lp-card">
                <div class="lp-icon"><i class='bx bx-search-alt'></i></div>
                <h3>Cek Status</h3>
                <p>Ketahui status cucian secara real-time dengan ID Pesanan (misal: ORD-1234).</p>
            </div>
            <div class="lp-card">
                <div class="lp-icon"><i class='bx bx-info-circle'></i></div>
                <h3>Informasi Layanan</h3>
                <p>Dapatkan daftar harga, estimasi waktu, dan syarat ketentuan layanan secara interaktif.</p>
            </div>
            <div class="lp-card">
                <div class="lp-icon"><i class='bx bx-id-card'></i></div>
                <h3>Pendaftaran Member</h3>
                <p>Daftar menjadi member melalui chat dan nikmati diskon 5% untuk setiap transaksi.</p>
            </div>
            <div class="lp-card">
                <div class="lp-icon"><i class='bx bx-support'></i></div>
                <h3>Layanan Keluhan</h3>
                <p>Sampaikan kendala Anda dan sistem kami langsung mencatat ke database beserta nomor tiket.</p>
            </div>
        </div>
    </section>

    <!-- CONTACT -->
    <section id="contact" class="lp-contact">
        <div class="lp-contact-box">
            <div class="lp-contact-info">
                <h2>Hubungi Kami</h2>
                <p>Butuh bantuan lebih lanjut? Kunjungi kami secara langsung.</p>
                <div class="lp-info-row"><i class='bx bx-map'></i><span>Jl. Kedungmundu No. 99, Kota Semarang</span></div>
                <div class="lp-info-row"><i class='bx bx-time'></i><span>Buka Setiap Hari: 08.00 – 21.00 WIB</span></div>
                <div class="lp-info-row"><i class='bx bxl-whatsapp'></i><span>085769171888 (Customer Service)</span></div>
            </div>
            <div class="lp-contact-visual">
                <div class="lp-blob"></div>
                <i class='bx bxs-map-alt lp-map-icon'></i>
                <p>Outlet Utama CleanWash</p>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="lp-footer">
        <div class="lp-footer-inner">
            <div class="lp-footer-logo"><i class='bx bxs-washer'></i> Astroclean</div>
            <p>Proyek Tugas Akhir / Implementasi FSM Teori Bahasa & Automata — Sistem Chatbot Layanan Laundry</p>
            <div class="lp-socials">
                <a href="#"><i class='bx bxl-instagram'></i></a>
                <a href="#"><i class='bx bxl-facebook-circle'></i></a>
                <a href="#"><i class='bx bxl-twitter'></i></a>
            </div>
        </div>
        <div class="lp-footer-bottom"><p>&copy; 2026 Astroclean Laundry. All rights reserved.</p></div>
    </footer>

    </body>
    </html>
    """)


# ══════════════════════════════════════════════════════
# CHATBOT PAGE
# ══════════════════════════════════════════════════════
def show_chatbot_page():
    # Deteksi navigasi kembali dari tombol HTML
    if st.query_params.get('go') == 'landing':
        st.query_params.clear()
        st.session_state.page = 'landing'
        st.rerun()
    if st.query_params.get('go') == 'cek_pesanan':
        st.query_params.clear()
        st.session_state.page = 'cek_pesanan'
        st.rerun()

    # CSS chatbot
    st.html("""
    <style>
        [data-testid="stHeader"]  { display:none !important; }
        [data-testid="stToolbar"] { display:none !important; }
        .stDeployButton           { display:none !important; }
        #MainMenu                 { visibility:hidden; }
        .stApp { background:linear-gradient(160deg,#dbeafe 0%,#f0f4ff 40%,#ffffff 100%) !important; }
        .block-container { padding:0 0 120px !important; max-width:700px !important; margin:0 auto !important; }
        [data-testid="stHtml"] { margin:0 !important; padding:0 !important; }
        .stChatFloatingInputContainer { background:transparent !important; padding-bottom:20px; }
        .stChatInputContainer {
            background:white !important; border-radius:30px !important;
            box-shadow:0 4px 20px rgba(0,0,0,.07) !important;
            border:1px solid #e2e8f0 !important; padding:4px 10px !important;
        }
    </style>
    """)

    # Topbar dengan tombol Kembali (JS)
    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
    <style>
        @import url('https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        .cb-topbar {
            background:rgba(255,255,255,.92); backdrop-filter:blur(14px);
            border-bottom:1px solid rgba(0,0,0,.07);
            padding:13px 20px; display:flex; align-items:center;
            justify-content:space-between; margin-bottom:20px; border-radius:16px;
            font-family:'Inter',sans-serif;
        }
        .cb-brand { display:flex; align-items:center; gap:10px; font-size:1.1rem; font-weight:700; color:#2563eb; }
        .cb-brand i { font-size:1.4rem; }
        .cb-right { display:flex; align-items:center; gap:16px; }
        .cb-status { display:flex; align-items:center; gap:6px; font-size:.82rem; color:#64748b; font-weight:500; }
        .cb-dot { width:8px; height:8px; border-radius:50%; background:#22c55e; box-shadow:0 0 0 2px rgba(34,197,94,.25); animation:cb-pulse 2s infinite; }
        @keyframes cb-pulse {
            0%,100% { box-shadow:0 0 0 2px rgba(34,197,94,.25); }
            50%      { box-shadow:0 0 0 5px rgba(34,197,94,.1);  }
        }
        .cb-back-btn {
            display:inline-flex; align-items:center; gap:6px;
            text-decoration:none; color:#2563eb;
            background:rgba(37,99,235,.08);
            padding:7px 16px; border-radius:50px; font-weight:600;
            font-size:.85rem; border:1px solid rgba(37,99,235,.2);
            transition:all .25s; cursor:pointer;
            font-family:'Inter',sans-serif;
        }
        .cb-back-btn:hover { background:#2563eb; color:white; }
    </style>
    <div class="cb-topbar">
        <div class="cb-brand">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:6px;"><rect width="18" height="20" x="3" y="2" rx="2"/><circle cx="12" cy="13" r="5"/><path d="M12 10a3 3 0 0 0 0 6"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="10" y1="6" x2="10.01" y2="6"/><line x1="14" y1="6" x2="14.01" y2="6"/></svg>
            <span>Astroclean</span>
        </div>
        <div class="cb-right">
            <div class="cb-status">
                <div class="cb-dot"></div>
                Bot Aktif
            </div>
            <a href="?go=cek_pesanan" target="_self" class="cb-back-btn" style="margin-right:6px;background:rgba(34,197,94,.1);color:#16a34a;border-color:rgba(34,197,94,.25);">
                <i class='bx bx-list-check' style='font-size:1.1rem;vertical-align:middle;margin-right:2px;'></i> Cek Pesanan
            </a>
            <a href="?go=landing" target="_self" class="cb-back-btn">
                <i class='bx bx-left-arrow-alt' style='font-size:1.1rem;vertical-align:middle;margin-right:2px;'></i> Beranda
            </a>
        </div>
    </div>
    """)

    # ── Render pesan ──────────────────────────────
    def render_message(role, content):
        content_html = content.replace('\n', '<br>')
        if role == "user":
            st.html(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:14px;padding:0 4px;align-items:flex-end;gap:10px;">
                <div style="background:#0b1a47;color:white;padding:12px 18px;
                    border-radius:20px 20px 0 20px;max-width:75%;
                    font-size:15px;line-height:1.5;font-family:'Inter',sans-serif;
                    box-shadow:0 4px 12px rgba(11,26,71,.18);">
                    {content_html}
                </div>
                <div style="background:#e2e8f0;color:#475569;border-radius:50%;
                    width:38px;height:38px;min-width:38px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 4px 10px rgba(0,0,0,.05);color:#475569;">
                    <i class='bx bx-user' style='font-size:20px;'></i>
                </div>
            </div>""")
        else:
            st.html(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:14px;padding:0 4px;align-items:flex-end;gap:10px;">
                <div style="background:#2563eb;color:white;border-radius:50%;
                    width:38px;height:38px;min-width:38px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 4px 10px rgba(37,99,235,.2);color:white;">
                    <i class='bx bx-bot' style='font-size:20px;'></i>
                </div>
                <div style="background:white;color:#1e293b;padding:13px 18px;
                    border-radius:20px 20px 20px 0;max-width:75%;
                    font-size:15px;line-height:1.55;font-family:'Inter',sans-serif;
                    box-shadow:0 4px 16px rgba(0,0,0,.05);border:1px solid #f1f5f9;">
                    {content_html}
                </div>
            </div>""")

    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"])

    st.html("<div style='height:40px;'></div>")

    # ── Input ─────────────────────────────────────
    if prompt := st.chat_input("Ketik pesan Anda..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_msg = st.session_state.messages[-1]["content"]
        response = st.session_state.fsm_v2.process_input(last_msg)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


# ══════════════════════════════════════════════════════
# CEK PESANAN PAGE
# ══════════════════════════════════════════════════════
def show_cek_pesanan_page():
    # Deteksi navigasi kembali
    if st.query_params.get('go') == 'landing':
        st.query_params.clear()
        st.session_state.page = 'landing'
        st.rerun()
    if st.query_params.get('go') == 'chat':
        st.query_params.clear()
        st.session_state.page = 'chatbot'
        st.rerun()

    st.html("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        @import url('https://cdn.jsdelivr.net/npm/boxicons@2.1.4/css/boxicons.min.css');
        [data-testid="stHeader"]  { display:none !important; }
        [data-testid="stToolbar"] { display:none !important; }
        .stDeployButton           { display:none !important; }
        #MainMenu                 { visibility:hidden; }
        .stApp { background:linear-gradient(135deg,#dbeafe 0%,#eff6ff 55%,#f0f4ff 100%) !important; }
        .block-container { padding:0 !important; max-width:100% !important; }
        section[data-testid="stMain"] > div { padding:0 !important; }
        [data-testid="stHtml"]    { margin:0 !important; padding:0 !important; }
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }

        .cp-navbar {
            width:100%; padding:16px 6%;
            display:flex; justify-content:space-between; align-items:center;
            background:rgba(255,255,255,.92);
            backdrop-filter:blur(14px);
            border-bottom:1px solid rgba(0,0,0,.07);
            position:sticky; top:0; z-index:100;
        }
        .cp-logo {
            display:flex; align-items:center; gap:10px;
            font-size:1.35rem; font-weight:700; color:#2563eb;
            text-decoration:none;
        }
        .cp-logo i { font-size:1.6rem; }
        .cp-nav-actions { display:flex; gap:12px; align-items:center; }
        .cp-btn {
            display:inline-flex; align-items:center; gap:6px;
            text-decoration:none; padding:9px 20px; border-radius:50px;
            font-weight:600; font-size:.875rem; transition:all .25s;
        }
        .cp-btn-outline {
            color:#2563eb; border:1px solid rgba(37,99,235,.25);
            background:rgba(37,99,235,.06);
        }
        .cp-btn-outline:hover { background:#2563eb; color:white; }
        .cp-btn-primary {
            background:#2563eb; color:white;
            box-shadow:0 4px 14px rgba(37,99,235,.3); border:none;
        }
        .cp-btn-primary:hover { background:#1e40af; transform:translateY(-2px); }

        .cp-hero {
            background:linear-gradient(135deg,#dbeafe 0%,#eff6ff 60%,#f0f4ff 100%);
            padding:56px 6% 40px;
            text-align:center;
        }
        .cp-hero h1 {
            font-size:clamp(1.8rem,3vw,2.6rem); font-weight:800;
            color:#0f172a; margin-bottom:10px;
        }
        .cp-hero p { color:#64748b; font-size:1.05rem; }
        .cp-hero-icon {
            width:72px; height:72px; border-radius:20px;
            background:rgba(37,99,235,.12);
            display:inline-flex; align-items:center; justify-content:center;
            margin-bottom:20px;
        }
        .cp-hero-icon i { font-size:36px; color:#2563eb; }

        .cp-body { padding:40px 6%; max-width:1100px; margin:0 auto; }

        .cp-stats {
            display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
            gap:16px; margin-bottom:36px;
        }
        .cp-stat-card {
            background:white; border-radius:16px; padding:20px 22px;
            border:1px solid #e2e8f0;
            box-shadow:0 2px 8px rgba(0,0,0,.04);
            display:flex; align-items:center; gap:14px;
        }
        .cp-stat-icon {
            width:46px; height:46px; border-radius:12px;
            display:flex; align-items:center; justify-content:center;
            font-size:22px; flex-shrink:0;
        }
        .cp-stat-label { font-size:.8rem; color:#64748b; font-weight:500; margin-bottom:2px; }
        .cp-stat-value { font-size:1.4rem; font-weight:700; color:#0f172a; }

        .cp-section-title {
            font-size:1.15rem; font-weight:700; color:#0f172a;
            margin-bottom:18px; display:flex; align-items:center; gap:8px;
        }

        .cp-order-card {
            background:white; border-radius:18px; padding:24px 28px;
            border:1px solid #e2e8f0; margin-bottom:16px;
            box-shadow:0 2px 10px rgba(0,0,0,.04);
            transition:all .3s ease;
            display:flex; align-items:center; gap:20px; flex-wrap:wrap;
        }
        .cp-order-card:hover {
            box-shadow:0 8px 28px rgba(37,99,235,.1);
            border-color:rgba(37,99,235,.2);
            transform:translateY(-2px);
        }
        .cp-order-icon {
            width:52px; height:52px; border-radius:14px;
            display:flex; align-items:center; justify-content:center;
            font-size:26px; flex-shrink:0;
        }
        .cp-order-info { flex:1; min-width:180px; }
        .cp-order-id {
            font-size:1rem; font-weight:700; color:#2563eb; margin-bottom:4px;
            font-family:'Courier New', monospace; letter-spacing:.5px;
        }
        .cp-order-detail { font-size:.88rem; color:#64748b; line-height:1.6; }
        .cp-order-meta { text-align:right; min-width:130px; }
        .cp-order-total {
            font-size:1.1rem; font-weight:700; color:#0f172a; margin-bottom:8px;
        }
        .cp-badge {
            display:inline-flex; align-items:center; gap:5px;
            padding:5px 14px; border-radius:50px; font-size:.8rem; font-weight:600;
        }
        .cp-badge-done {
            background:rgba(34,197,94,.12); color:#16a34a;
            border:1px solid rgba(34,197,94,.25);
        }
        .cp-badge-process {
            background:rgba(234,179,8,.12); color:#ca8a04;
            border:1px solid rgba(234,179,8,.25);
        }
        .cp-badge-paid {
            background:rgba(37,99,235,.1); color:#2563eb;
            border:1px solid rgba(37,99,235,.22);
        }
        .cp-badge-unpaid {
            background:rgba(239,68,68,.1); color:#dc2626;
            border:1px solid rgba(239,68,68,.22);
        }
        .cp-dot-anim {
            width:7px; height:7px; border-radius:50%; background:currentColor;
            animation:cp-blink 1.5s infinite;
        }
        @keyframes cp-blink {
            0%,100% { opacity:1; } 50% { opacity:.3; }
        }

        .cp-empty {
            text-align:center; padding:80px 20px;
            background:white; border-radius:20px; border:1px dashed #cbd5e1;
        }
        .cp-empty-icon { font-size:64px; color:#cbd5e1; margin-bottom:16px; }
        .cp-empty h3 { font-size:1.2rem; font-weight:700; color:#334155; margin-bottom:8px; }
        .cp-empty p { color:#94a3b8; font-size:.93rem; margin-bottom:24px; }
        .cp-empty-btn {
            display:inline-flex; align-items:center; gap:8px;
            background:#2563eb; color:white;
            padding:12px 28px; border-radius:50px; font-weight:600;
            text-decoration:none; font-size:.93rem;
            box-shadow:0 6px 18px rgba(37,99,235,.3);
            transition:all .25s;
        }
        .cp-empty-btn:hover { background:#1e40af; transform:translateY(-2px); }

        .cp-footer-note {
            text-align:center; color:#94a3b8; font-size:.82rem;
            margin-top:32px; padding-top:20px; border-top:1px solid #f1f5f9;
        }
    </style>
    """)

    # Ambil data pesanan
    semua_pesanan = get_all_pesanan()
    total_pesanan = len(semua_pesanan)
    total_selesai = sum(1 for p in semua_pesanan if p['Status'] == 'Selesai')
    total_proses  = total_pesanan - total_selesai
    total_bayar   = sum(p['Total'] for p in semua_pesanan)

    # Navbar
    st.html(f"""
    <nav class="cp-navbar">
        <a class="cp-logo" href="?go=landing" target="_self">
            <i class='bx bxs-washer'></i>
            <span>Astroclean</span>
        </a>
        <div class="cp-nav-actions">
            <a href="?go=chat" target="_self" class="cp-btn cp-btn-outline">
                <i class='bx bx-message-square-dots'></i> Chatbot
            </a>
            <a href="?go=landing" target="_self" class="cp-btn cp-btn-outline">
                <i class='bx bx-home'></i> Beranda
            </a>
        </div>
    </nav>
    """)

    # Hero header
    st.html("""
    <div class="cp-hero">
        <div class="cp-hero-icon"><i class='bx bx-list-check'></i></div>
        <h1>Riwayat & Status Pesanan</h1>
        <p>Pantau semua pesanan laundry Anda secara real-time di sini.</p>
    </div>
    """)

    # Stats cards
    st.html(f"""
    <div class="cp-body">
        <div class="cp-stats">
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:rgba(37,99,235,.1);color:#2563eb;">
                    <i class='bx bx-package'></i>
                </div>
                <div>
                    <div class="cp-stat-label">Total Pesanan</div>
                    <div class="cp-stat-value">{total_pesanan}</div>
                </div>
            </div>
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:rgba(234,179,8,.1);color:#ca8a04;">
                    <i class='bx bx-loader-alt'></i>
                </div>
                <div>
                    <div class="cp-stat-label">Sedang Diproses</div>
                    <div class="cp-stat-value">{total_proses}</div>
                </div>
            </div>
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:rgba(34,197,94,.1);color:#16a34a;">
                    <i class='bx bx-check-circle'></i>
                </div>
                <div>
                    <div class="cp-stat-label">Selesai</div>
                    <div class="cp-stat-value">{total_selesai}</div>
                </div>
            </div>
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:rgba(168,85,247,.1);color:#9333ea;">
                    <i class='bx bx-money'></i>
                </div>
                <div>
                    <div class="cp-stat-label">Total Transaksi</div>
                    <div class="cp-stat-value" style="font-size:1.1rem;">Rp {total_bayar:,}</div>
                </div>
            </div>
        </div>
    </div>
    """)

    # Daftar pesanan
    if not semua_pesanan:
        st.html("""
        <div class="cp-body">
            <div class="cp-empty">
                <div class="cp-empty-icon"><i class='bx bx-package'></i></div>
                <h3>Belum Ada Pesanan</h3>
                <p>Anda belum memiliki riwayat pesanan laundry. Mulai percakapan dengan chatbot kami untuk memesan sekarang!</p>
                <a href="?go=chat" target="_self" class="cp-empty-btn">
                    <i class='bx bx-message-rounded-dots'></i> Mulai Pesan Sekarang
                </a>
            </div>
        </div>
        """)
    else:
        cards_html = '<div class="cp-body"><div class="cp-section-title"><i class="bx bx-receipt" style="color:#2563eb;font-size:1.3rem;"></i> Daftar Pesanan</div>'
        for p in semua_pesanan:
            jenis = p['Jenis']
            icon_bg = "rgba(37,99,235,.1)" if jenis == 'Pakaian' else "rgba(168,85,247,.1)"
            icon_color = "#2563eb" if jenis == 'Pakaian' else "#9333ea"
            icon_cls = "bx-shopping-bag" if jenis == 'Pakaian' else "bx-run"

            # Badge status pesanan
            if p['Status'] == 'Selesai':
                badge_status = "<span class='cp-badge cp-badge-done'><i class='bx bx-check-circle'></i> Selesai</span>"
            else:
                badge_status = "<span class='cp-badge cp-badge-process'><span class='cp-dot-anim'></span> Sedang Dicuci</span>"

            # Badge status pembayaran
            status_bayar = p.get('StatusPembayaran', 'Belum Dibayar')
            metode_bayar = p.get('MetodePembayaran', '-')
            if status_bayar == 'Sudah Dibayar':
                badge_bayar = f"<span class='cp-badge cp-badge-paid'><i class='bx bx-credit-card'></i> Sudah Dibayar</span>"
            else:
                badge_bayar = f"<span class='cp-badge cp-badge-unpaid'><i class='bx bx-time-five'></i> Belum Dibayar</span>"

            # Format waktu
            waktu_raw = p['Waktu']
            try:
                from datetime import datetime as _dt
                waktu_fmt = _dt.strptime(waktu_raw, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y, %H:%M')
            except:
                waktu_fmt = waktu_raw

            cards_html += f"""
            <div class="cp-order-card">
                <div class="cp-order-icon" style="background:{icon_bg};color:{icon_color};">
                    <i class='bx {icon_cls}'></i>
                </div>
                <div class="cp-order-info">
                    <div class="cp-order-id">{p['ID']}</div>
                    <div class="cp-order-detail">
                        🧺 {p['Jenis']} &nbsp;·&nbsp; ⚡ {p['Layanan']}<br>
                        💳 {metode_bayar} &nbsp;·&nbsp; 🕐 {waktu_fmt}
                    </div>
                </div>
                <div class="cp-order-meta">
                    <div class="cp-order-total">Rp {p['Total']:,}</div>
                    <div style="display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap;margin-top:4px;">
                        {badge_status}
                        {badge_bayar}
                    </div>
                </div>
            </div>"""

        cards_html += '<div class="cp-footer-note">💡 Status pesanan diperbarui otomatis berdasarkan estimasi waktu pengerjaan.</div></div>'
        st.html(cards_html)


# ══════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'cek_pesanan':
    show_cek_pesanan_page()
else:
    show_chatbot_page()
