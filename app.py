import streamlit as st
from chatbot import LaundryFSM
from data import init_db

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
        <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
        <style>
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
        </ul>
        <a href="?go=chat" target="_self" class="lp-btn-nav">
            Coba Chatbot
        </a>
    </nav>

    <!-- HERO -->
    <section id="hero" class="lp-hero">
        <div class="lp-hero-content">
            <span class="lp-badge"><i class='bx bx-trending-up'></i> Inovasi Layanan 2026</span>
            <h1>Revolusi Layanan Laundry dengan <span class="lp-highlight">AI Chatbot</span></h1>
            <p>Memesan laundry, mengecek status pesanan, dan menyampaikan keluhan kini semudah mengirim pesan. Nikmati pengalaman cerdas bersama Astroclean.</p>
            <div class="lp-hero-btns">
                <a href="?go=chat" target="_self" class="lp-btn-primary">
                    <i class='bx bx-message-rounded-dots'></i> Mulai Percakapan
                </a>
                <a href="#features" class="lp-btn-secondary">Pelajari Lebih Lanjut</a>
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
                <div class="lp-info-row"><i class='bx bx-map'></i><span>Jl. Bersih Kilau No. 99, Kota Baru</span></div>
                <div class="lp-info-row"><i class='bx bx-time'></i><span>Buka Setiap Hari: 08.00 – 21.00 WIB</span></div>
                <div class="lp-info-row"><i class='bx bxl-whatsapp'></i><span>0812-XXXX-XXXX (Customer Service)</span></div>
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
    <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
    <style>
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
            <i class='bx bxs-washer'></i>
            <span>Astroclean</span>
        </div>
        <div class="cb-right">
            <div class="cb-status">
                <div class="cb-dot"></div>
                Bot Aktif
            </div>
            <a href="?go=landing" target="_self" class="cb-back-btn">
                ← Beranda
            </a>
        </div>
    </div>
    """)

    # ── Render pesan ──────────────────────────────
    def render_message(role, content):
        content_html = content.replace('\n', '<br>')
        if role == "user":
            st.html(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:14px;padding:0 4px;">
                <div style="background:#0b1a47;color:white;padding:12px 18px;
                    border-radius:20px 20px 0 20px;max-width:75%;
                    font-size:15px;line-height:1.5;font-family:'Inter',sans-serif;
                    box-shadow:0 4px 12px rgba(11,26,71,.18);">
                    {content_html}
                </div>
            </div>""")
        else:
            st.html(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:14px;padding:0 4px;align-items:flex-end;gap:10px;">
                <div style="font-size:20px;background:white;border-radius:50%;
                    width:38px;height:38px;min-width:38px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 4px 10px rgba(0,0,0,.08);">🤖</div>
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
# ROUTER
# ══════════════════════════════════════════════════════
if st.session_state.page == 'landing':
    show_landing_page()
else:
    show_chatbot_page()
