import matplotlib.pyplot as plt
import numpy as np

def run_steady_state_simulation(
    N, T_hot, T_cold, toleransiError=0.0001, maxIterasi=10000
):
    # 1. (INPUT & INISIALISASI)
    # Buat array suhu sepanjang N titik, diinisialisasi awal dengan suhu 20°C
    T = np.full(N, T_cold)

    # Kunci nilai batas ujung kiri (Suhu CPU) dan ujung kanan (Suhu Lingkungan)
    T[0] = T_hot
    T[N - 1] = T_cold

    # Salin array awal (kondisi datar 20°C) sebagai data "Before" untuk visualisasi grafik
    T_before = T.copy()

    # Inisialisasi variabel loop iterasi
    k = 0  # Penghitung jumlah iterasi (k)
    error = 1.0  # Set awal error > epsilon agar loop berjalan pertama kali

    # 2. HITUNGAN (NESTED LOOPS)
    # LOOP LUAR - Terus berjalan melakukan koreksi selama nilai belum dibawah toleransi error dan belum mencapai iterasi maksimum
    while error > toleransiError and k < maxIterasi:
        maxSelisihLokal = 0.0  # Reset penanda perubahan terbesar di setiap awal iterasi baru
        # LOOP DALAM - Menyusur indeks koordinat titik jarak (Hanya titik bagian dalam yaitu 1 sampai N-2)
        for i in range(1, N - 1):
            T_sebelumnya = T[i]  # Simpan nilai suhu titik ini sebelum dikoreksi

            # Rumus koreksi Gauss-Seidel yang diturunkan dari matriks tridiagonal [1, -2, 1]
            # Nilai T[i-1] yang dipakai otomatis adalah nilai terbaru dari iterasi saat ini
            T[i] = (T[i - 1] + T[i + 1]) / 2.0

            # Hitung selisih perubahan angka absolut setelah dilakukan koreksi rumus
            selisih = abs(T[i] - T_sebelumnya)

            # Cari dan catat penyimpangan terbesar yang terjadi di sepanjang batang logam
            if selisih > maxSelisihLokal:
                maxSelisihLokal = selisih

        # Perbarui nilai evaluasi error global dengan deviasi terbesar dari loop dalam
        error = maxSelisihLokal

        # Naikkan indeks hitungan iterasi
        k += 1

    # Mengembalikan data suhu sebelum, suhu sesudah, dan total iterasi koreksi
    return T_before, T, k


# 3. EKSEKUSI PROGRAM & OUTPUT VISUALISASI
if __name__ == "__main__":
    # Tentukan parameter input simulasi
    JUMLAH_TITIK = 20  # Nilai N (Resolusi grid pelat logam)
    SUHU_CPU = 80.0  # T_hot dalam derajat Celsius
    SUHU_LINGKUNGAN = 25.0  # T_cold dalam derajat Celsius
    TOLERANSI = 0.0001  # Batas nilai epsilon untuk kriteria berhenti

    # Jalankan Gauss-Seidel
    T_awal, T_akhir, total_iterasi = run_steady_state_simulation(
        N=JUMLAH_TITIK,
        T_hot=SUHU_CPU,
        T_cold=SUHU_LINGKUNGAN,
        toleransiError=TOLERANSI,
    )

    # Cetak hasil performa hitungan numerik ke terminal
    print("=== HASIL SIMULASI GAUSS-SEIDEL (STEADY STATE) ===")
    print(f"Total Iterasi hingga Konvergen: {total_iterasi} kali")
    print(f"Suhu Titik Tengah Akhir       : {T_akhir[JUMLAH_TITIK//2]:.2f} °C")
    print("==================================================")

    # Render Grafik Profil Suhu: BEFORE vs AFTER
    posisi_x = np.linspace(0, 100, JUMLAH_TITIK)  # Skala posisi dalam persen (0% s.d 100%)

    plt.figure(figsize=(8, 5))
    plt.plot(
        posisi_x,
        T_awal,
        "b--",
        marker="o",
        label=f"Before (Awal Mulai / Komputer Mati)",
    )
    plt.plot(
        posisi_x,
        T_akhir,
        "r-",
        marker="s",
        label=f"After (Stabil / Konvergen pada Iterasi ke-{total_iterasi})",
    )

    # Atur komponen grafik
    plt.title(
        "Profil Distribusi Suhu Stabil pada Papan Induk (Gauss-Seidel 1D)"
    )
    plt.xlabel("Posisi Panjang Pelat Pendingin (%)")
    plt.ylabel("Temperatur (°C)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()

    # Tampilkan grafik ke layar
    plt.show()
