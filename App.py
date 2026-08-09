import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Monitoring Penjualan Harian",
    page_icon="📊",
    layout="wide"
)

# --- INISIALISASI SESSION STATE ---
# 1. Aturan Tanggal Periode Promosi
if "start_date" not in st.session_state:
    st.session_state.start_date = datetime.date(2026, 8, 1)
if "end_date" not in st.session_state:
    st.session_state.end_date = datetime.date(2026, 8, 15)

# 2. Data Master Item (Dinamis: W1, W2, W3, W4)
if "items_data" not in st.session_state:
    st.session_state.items_data = pd.DataFrame([
        # Week 1
        {"Periode": "Week 1", "Deskripsi": "Baby Happy", "Target Toko": 37, "Target Kasir": 13, "Actual": 10},
        {"Periode": "Week 1", "Deskripsi": "Goodtime", "Target Toko": 101, "Target Kasir": 34, "Actual": 90},
        {"Periode": "Week 1", "Deskripsi": "Aqua", "Target Toko": 233, "Target Kasir": 78, "Actual": 344},
        {"Periode": "Week 1", "Deskripsi": "SGM", "Target Toko": 46, "Target Kasir": 16, "Actual": 7},
        {"Periode": "Week 1", "Deskripsi": "Bango", "Target Toko": 48, "Target Kasir": 16, "Actual": 43},
        {"Periode": "Week 1", "Deskripsi": "Lifebuoy", "Target Toko": 56, "Target Kasir": 19, "Actual": 41},
        {"Periode": "Week 1", "Deskripsi": "Glow", "Target Toko": 33, "Target Kasir": 11, "Actual": 35},
        {"Periode": "Week 1", "Deskripsi": "My baby", "Target Toko": 42, "Target Kasir": 14, "Actual": 58},
        # Week 2
        {"Periode": "Week 2", "Deskripsi": "Oishi", "Target Toko": 45, "Target Kasir": 15, "Actual": 25},
        {"Periode": "Week 2", "Deskripsi": "Le mineral", "Target Toko": 361, "Target Kasir": 121, "Actual": 180},
        {"Periode": "Week 2", "Deskripsi": "Indomilk", "Target Toko": 35, "Target Kasir": 12, "Actual": 15},
        {"Periode": "Week 2", "Deskripsi": "Sunlight", "Target Toko": 130, "Target Kasir": 43, "Actual": 60},
        {"Periode": "Week 2", "Deskripsi": "Shinzui", "Target Toko": 84, "Target Kasir": 28, "Actual": 30},
        {"Periode": "Week 2", "Deskripsi": "Pantene", "Target Toko": 43, "Target Kasir": 15, "Actual": 20},
        {"Periode": "Week 2", "Deskripsi": "Tango", "Target Toko": 63, "Target Kasir": 21, "Actual": 40},
        {"Periode": "Week 2", "Deskripsi": "Ff uht", "Target Toko": 54, "Target Kasir": 18, "Actual": 22},
    ])

# 3. Data Kasir (Week 1 & Week 2)
if "kasir_data" not in st.session_state:
    st.session_state.kasir_data = pd.DataFrame([
        {"Nama": "Aris", "Actual_W1": 146, "Actual_W2": 64},
        {"Nama": "Tika", "Actual_W1": 190, "Actual_W2": 95},
        {"Nama": "Rizki", "Actual_W1": 110, "Actual_W2": 65},
        {"Nama": "Adel", "Actual_W1": 79, "Actual_W2": 81},
        {"Nama": "Ilham", "Actual_W1": 36, "Actual_W2": 154},
    ])

# 4. Data Penjualan Harian (Tren)
if "daily_sales" not in st.session_state:
    st.session_state.daily_sales = pd.DataFrame([
        {"Tanggal": "2026-08-01", "Item": "Aqua", "Qty": 50, "Kasir": "Tika"},
        {"Tanggal": "2026-08-01", "Item": "Goodtime", "Qty": 20, "Kasir": "Aris"},
        {"Tanggal": "2026-08-02", "Item": "Aqua", "Qty": 60, "Kasir": "Tika"},
        {"Tanggal": "2026-08-03", "Item": "Goodtime", "Qty": 30, "Kasir": "Rizki"},
        {"Tanggal": "2026-08-04", "Item": "Aqua", "Qty": 80, "Kasir": "Adel"},
        {"Tanggal": "2026-08-05", "Item": "My baby", "Qty": 40, "Kasir": "Ilham"},
        {"Tanggal": "2026-08-08", "Item": "Le mineral", "Qty": 90, "Kasir": "Tika"},
        {"Tanggal": "2026-08-09", "Item": "Le mineral", "Qty": 90, "Kasir": "Ilham"},
    ])

# --- PERHITUNGAN TIME FACTOR & UTILS ---
today = datetime.date.today()
start_d = st.session_state.start_date
end_d = st.session_state.end_date

total_promo_days = max((end_d - start_d).days + 1, 1)

if today < start_d:
    days_passed = 0
elif today > end_d:
    days_passed = total_promo_days
else:
    days_passed = (today - start_d).days + 1

tf_percent = (days_passed / total_promo_days) * 100
remaining_days = max(total_promo_days - days_passed, 1)

df_items = st.session_state.items_data.copy()
df_kasir = st.session_state.kasir_data.copy()

target_total_toko = df_items["Target Toko"].sum()
actual_total_toko = df_items["Actual"].sum()
ach_total_percent = (actual_total_toko / target_total_toko * 100) if target_total_toko > 0 else 0

remaining_target = max(target_total_toko - actual_total_toko, 0)
realtime_target_per_day = int(round(remaining_target / remaining_days)) if remaining_days > 0 and remaining_target > 0 else 0

is_lulus = ach_total_percent >= tf_percent

# --- STRUCTURE 5 TABS NAVIGASI ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 1. Home / Resume",
    "📦 2. Detail Item",
    "👥 3. Personil & Tren",
    "🏆 4. Leaderboard Kasir",
    "⚙️ 5. Pengaturan Admin"
])

# ==========================================
# BAGIAN 1: HOME / RESUME
# ==========================================
with tab1:
    st.header("🏠 Resume Keseluruhan Penjualan Toko")
    
    col_status1, col_status2 = st.columns([3, 1])
    with col_status1:
        st.subheader(f"Periode Promosi: {start_d.strftime('%d %b %Y')} s.d. {end_d.strftime('%d %b %Y')}")
        st.caption(f"Hari Ke-{days_passed} dari {total_promo_days} Hari Kerja")
    with col_status2:
        if is_lulus:
            st.success("STATUS: 🟢 LULUS (Ach ≥ TF)")
        else:
            st.error("STATUS: 🔴 BELUM LULUS (Ach < TF)")

    st.divider()

    # KPI Metrics Cards
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Time Factor (TF)", f"{tf_percent:.0f}%", f"{days_passed}/{total_promo_days} Hari")
    k2.metric("Target Toko Total", f"{target_total_toko:,} pcs")
    k3.metric("Actual Toko Total", f"{actual_total_toko:,} pcs")
    k4.metric("Ach %", f"{ach_total_percent:.1f}%", f"{ach_total_percent - tf_percent:.1f}% vs TF")
    k5.metric("Target Realtime / Hari", f"{realtime_target_per_day:,} pcs/hari")

    st.divider()

    # Diagram Komparasi Week 1 vs Week 2
    st.subheader("📊 Perbandingan Penjualan Week 1 vs Week 2")
    df_week_summary = df_items.groupby("Periode")[["Target Toko", "Actual"]].sum().reset_index()
    
    fig_w1_w2 = px.bar(
        df_week_summary,
        x="Periode",
        y=["Target Toko", "Actual"],
        barmode="group",
        text_auto=True,
        title="Target vs Actual Per Minggu",
        color_discrete_map={"Target Toko": "#34495e", "Actual": "#2ecc71"}
    )
    fig_w1_w2.update_layout(height=400, yaxis_title="Jumlah (Pcs)")
    st.plotly_chart(fig_w1_w2, use_container_width=True)


# ==========================================
# BAGIAN 2: DETAIL PENJUALAN PER ITEM
# ==========================================
with tab2:
    st.header("📦 Detail Penjualan Per Item")
    
    sort_option = st.radio("Urutkan Data Penjualan:", ["Penjualan Terbanyak (Highest)", "Penjualan Terkecil (Lowest)"], horizontal=True)
    ascending_val = True if sort_option == "Penjualan Terkecil (Lowest)" else False

    periodes = df_items["Periode"].unique().tolist()
    sub_tabs = st.tabs([f"Slide {p}" for p in periodes])

    for idx, p in enumerate(periodes):
        with sub_tabs[idx]:
            st.subheader(f"Data Item {p}")
            df_p = df_items[df_items["Periode"] == p].copy()
            df_p["Ach %"] = (df_p["Actual"] / df_p["Target Toko"] * 100).round(1)
            df_p = df_p.sort_values(by="Actual", ascending=ascending_val)

            col_tabel, col_chart = st.columns([1, 1])
            with col_tabel:
                st.dataframe(
                    df_p[["Deskripsi", "Target Toko", "Target Kasir", "Actual", "Ach %"]],
                    hide_index=True,
                    use_container_width=True
                )
            
            with col_chart:
                fig_item_p = px.bar(
                    df_p,
                    x="Ach %",
                    y="Deskripsi",
                    orientation="h",
                    text="Ach %",
                    color="Ach %",
                    color_continuous_scale="Blues" if ascending_val else "Greens",
                    title=f"Persentase Pencapaian Item ({p})"
                )
                fig_item_p.add_vline(x=100, line_dash="dash", line_color="red")
                fig_item_p.update_traces(texttemplate='%{text}%', textposition='outside')
                st.plotly_chart(fig_item_p, use_container_width=True)


# ==========================================
# BAGIAN 3: PERSONIL TOKO & TREN PENJUALAN
# ==========================================
with tab3:
    st.header("👥 Penjualan Personil Toko & Tren Harian")

    # Resume Personil 2 Minggu
    df_kasir["Total_Actual"] = df_kasir["Actual_W1"] + df_kasir["Actual_W2"]
    target_kasir_per_person = int(round(target_total_toko / len(df_kasir))) if len(df_kasir) > 0 else 0
    df_kasir["Target_Total"] = target_kasir_per_person
    df_kasir["Ach %"] = (df_kasir["Total_Actual"] / df_kasir["Target_Total"] * 100).round(1)

    st.subheader("📋 Resume Personil Toko (W1, W2 & Total)")
    st.dataframe(
        df_kasir[["Nama", "Target_Total", "Actual_W1", "Actual_W2", "Total_Actual", "Ach %"]],
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # Tren Penjualan Harian (Keseluruhan & Per Item)
    st.subheader("📈 Tren Penjualan Harian")
    df_daily = st.session_state.daily_sales.copy()

    if not df_daily.empty:
        c_trend1, c_trend2 = st.columns(2)
        with c_trend1:
            df_daily_total = df_daily.groupby("Tanggal")["Qty"].sum().reset_index()
            fig_daily_total = px.line(
                df_daily_total,
                x="Tanggal",
                y="Qty",
                markers=True,
                title="Total Penjualan per Tanggal"
            )
            st.plotly_chart(fig_daily_total, use_container_width=True)

        with c_trend2:
            df_daily_item = df_daily.groupby(["Tanggal", "Item"])["Qty"].sum().reset_index()
            fig_daily_item = px.bar(
                df_daily_item,
                x="Tanggal",
                y="Qty",
                color="Item",
                title="Breakdown Penjualan per Item per Tanggal"
            )
            st.plotly_chart(fig_daily_item, use_container_width=True)
    else:
        st.info("Belum ada data transaksi harian yang dicatat.")

    st.divider()

    # Diagram Penjualan Per Item tiap Personil
    st.subheader("📊 Diagram Penjualan Item Per Personil Toko")
    selected_kasir = st.selectbox("Pilih Personil Toko:", df_kasir["Nama"].unique())
    
    if not df_daily.empty:
        df_kasir_item = df_daily[df_daily["Kasir"] == selected_kasir].groupby("Item")["Qty"].sum().reset_index()
        fig_kasir_detail = px.bar(
            df_kasir_item,
            x="Item",
            y="Qty",
            text_auto=True,
            title=f"Kontribusi Item oleh {selected_kasir}",
            color="Qty",
            color_continuous_scale="Purples"
        )
        st.plotly_chart(fig_kasir_detail, use_container_width=True)


# ==========================================
# BAGIAN 4: LEADERBOARD KASIR & TANGGA PERINGKAT
# ==========================================
with tab4:
    st.header("🏆 Leaderboard & Tangga Peringkat Kasir")

    df_rank = df_kasir.sort_values(by="Total_Actual", ascending=False).reset_index(drop=True)
    df_rank.index += 1

    def assign_badge(rank):
        if rank == 1: return "🥇 Rank 1"
        elif rank == 2: return "🥈 Rank 2"
        elif rank == 3: return "🥉 Rank 3"
        elif rank == 4: return "4️⃣ Rank 4"
        else: return "5️⃣ Rank 5"

    df_rank["Badge"] = [assign_badge(i) for i in df_rank.index]

    # Visual Tangga Peringkat (Podium)
    st.subheader("🏛️ Tangga Peringkat (Podium)")
    if len(df_rank) >= 3:
        podium_df = pd.DataFrame([
            {"Nama": df_rank.loc[1, "Nama"], "Actual": df_rank.loc[1, "Total_Actual"], "Posisi": "2. Juara 2 (🥈)"},
            {"Nama": df_rank.loc[0, "Nama"], "Actual": df_rank.loc[0, "Total_Actual"], "Posisi": "1. Juara 1 (🥇)"},
            {"Nama": df_rank.loc[2, "Nama"], "Actual": df_rank.loc[2, "Total_Actual"], "Posisi": "3. Juara 3 (🥉)"},
        ])
        fig_podium = px.bar(
            podium_df,
            x="Posisi",
            y="Actual",
            color="Posisi",
            text="Nama",
            color_discrete_map={
                "1. Juara 1 (🥇)": "#f1c40f",
                "2. Juara 2 (🥈)": "#bdc3c7",
                "3. Juara 3 (🥉)": "#e67e22"
            },
            title="Podium Tiga Teratas"
        )
        fig_podium.update_traces(textposition="inside")
        st.plotly_chart(fig_podium, use_container_width=True)

    st.subheader("📋 Tabel Hasil Keseluruhan Periode Promosi")
    st.dataframe(
        df_rank[["Badge", "Nama", "Target_Total", "Actual_W1", "Actual_W2", "Total_Actual", "Ach %"]],
        hide_index=True,
        use_container_width=True
    )


# ==========================================
# BAGIAN 5: PENGATURAN ADMIN (PROTECTED)
# ==========================================
with tab5:
    st.header("⚙️ Pengaturan Sistem & Administrator")
    
    # Input Password Masked
    admin_password = st.text_input("Masukkan Password Admin:", type="password")
    
    if admin_password == "Kanaeru1":
        st.success("Akses Diberikan! Silakan ubah pengaturan di bawah ini.")
        
        tab_adm1, tab_adm2, tab_adm3, tab_adm4 = st.tabs([
            "📅 Edit Periode Promosi",
            "📦 Tambah/Edit Item (W1-W4)",
            "✏️ Edit Aktual Penjualan",
            "💬 Template WA"
        ])

        # 1. Edit Tanggal Periode
        with tab_adm1:
            st.subheader("Pengaturan Tanggal Periode Promosi")
            col_d1, col_d2 = st.columns(2)
            new_start = col_d1.date_input("Tanggal Mulai", value=st.session_state.start_date)
            new_end = col_d2.date_input("Tanggal Selesai", value=st.session_state.end_date)
            
            if st.button("Simpan Tanggal Periode"):
                st.session_state.start_date = new_start
                st.session_state.end_date = new_end
                st.success("Tanggal Periode Promosi Berhasil Disimpan!")
                st.rerun()

        # 2. Tambah / Edit Item (Mendukung W1, W2, W3, W4)
        with tab_adm2:
            st.subheader("Tambah Produk Baru / Tambah Week (W3, W4)")
            with st.form("form_add_item"):
                p_periode = st.selectbox("Pilih Periode/Minggu", ["Week 1", "Week 2", "Week 3", "Week 4"])
                p_desk = st.text_input("Nama Item Produk")
                p_target_toko = st.number_input("Target Toko (Pcs)", min_value=0, value=0)
                p_target_kasir = st.number_input("Target Kasir (Pcs)", min_value=0, value=0)
                p_actual = st.number_input("Actual Sales Awal", min_value=0, value=0)
                
                submit_item = st.form_submit_button("Tambah Item Produk")
                if submit_item and p_desk != "":
                    new_item = {
                        "Periode": p_periode,
                        "Deskripsi": p_desk,
                        "Target Toko": p_target_toko,
                        "Target Kasir": p_target_kasir,
                        "Actual": p_actual
                    }
                    st.session_state.items_data = pd.concat([st.session_state.items_data, pd.DataFrame([new_item])], ignore_index=True)
                    st.success(f"Item '{p_desk}' berhasil ditambahkan ke {p_periode}! Target toko otomatis diperbarui.")
                    st.rerun()

            st.divider()
            st.subheader("Edit/Hapus Item Terdaftar")
            edited_items_df = st.data_editor(
                st.session_state.items_data,
                num_rows="dynamic",
                use_container_width=True
            )
            if st.button("Simpan Perubahan Tabel Item"):
                st.session_state.items_data = edited_items_df
                st.success("Data Item Berhasil Diperbarui!")
                st.rerun()

        # 3. Edit Aktual Penjualan (Toko & Kasir)
        with tab_adm3:
            st.subheader("Update Aktual Penjualan Kasir")
            edited_kasir_df = st.data_editor(
                st.session_state.kasir_data,
                use_container_width=True
            )
            if st.button("Simpan Data Kasir"):
                st.session_state.kasir_data = edited_kasir_df
                st.success("Data Penjualan Kasir Berhasil Diperbarui!")
                st.rerun()

        # 4. Template WhatsApp
        with tab_adm4:
            st.subheader("💬 Template Laporan WhatsApp Auto-Generated")
            
            wa_text = f"""🏆 *REPORT LIGA PSM ASIK-ASIK JOSH* 🏆

🗓 *Periode: {start_d.strftime('%d %b')} - {end_d.strftime('%d %b %Y')}*
TF : {tf_percent:.0f}% (Day {days_passed}/{total_promo_days})
TARGET TOKO : {target_total_toko}
ACTUAL TOKO : {actual_total_toko}
GAP : {'+' if (actual_total_toko - target_total_toko) > 0 else ''}{actual_total_toko - target_total_toko}
ACHIEVEMENT : {ach_total_percent:.0f}% ({'✅ LULUS' if is_lulus else '🔴 BELUM LULUS'})

🎯 *Target Realtime / Hari: {realtime_target_per_day} pcs/hari*

💼 *Report By Item :*
Deskripsi / Target Toko / Actual / %
"""
            for i, row in df_items.iterrows():
                ach_item = (row['Actual'] / row['Target Toko'] * 100) if row['Target Toko'] > 0 else 0
                wa_text += f"{i+1}. [{row['Periode']}] {row['Deskripsi']} : {row['Target Toko']}/{row['Actual']}/{ach_item:.0f}%\n"

            wa_text += f"\n🏆 *Rank Sementara Kasir:*\n"
            for i, row in df_rank.iterrows():
                wa_text += f"{row['Badge']} {row['Nama']} | Act: {row['Total_Actual']} pcs ({row['Ach %']} %)\n"

            st.code(wa_text, language="markdown")

    elif admin_password != "":
        st.error("Password Salah! Akses ditolak.")
    else:
        st.info("Ketikkan password di atas untuk mengedit data.")
