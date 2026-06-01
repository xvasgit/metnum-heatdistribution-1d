import numpy as np


def run_explicit_euler_calculation(
    N=10,
    T_hot=80.0,
    T_cold=25.0,
    alpha=0.1,
    panjangPelat=1.0,
    durasiSimulasi=3.0,
    deltaT=0.01,
):
    # 1. (INPUT & INISIALISASI)
    # Validasi sederhana agar jumlah titik dan parameter fisik masuk akal
    if N < 3:
        raise ValueError("N minimal 3 karena harus ada batas kiri, titik tengah, dan batas kanan.")
    if panjangPelat <= 0:
        raise ValueError("panjangPelat harus lebih besar dari 0.")
    if durasiSimulasi <= 0:
        raise ValueError("durasiSimulasi harus lebih besar dari 0.")
    if deltaT <= 0:
        raise ValueError("deltaT harus lebih besar dari 0.")

    # Hitung jarak antar titik grid pada pelat 1D
    deltaX = panjangPelat / (N - 1)

    # Hitung bilangan stabilitas r dari metode Euler Eksplisit
    # r = alpha * Delta t / Delta x^2
    r = alpha * deltaT / (deltaX ** 2)

    # Cek syarat stabilitas eksplisit untuk persamaan panas 1D
    # Agar simulasi stabil, nilai r sebaiknya tidak lebih dari 0.5
    if r > 0.5:
        raise ValueError(
            f"Simulasi tidak stabil karena r = {r:.4f}. "
            "Perkecil deltaT, perkecil alpha, atau perbesar deltaX."
        )

    # Buat array suhu sepanjang N titik, diinisialisasi awal dengan suhu lingkungan
    T = np.full(N, T_cold, dtype=float)

    # Kunci nilai batas ujung kiri (Suhu CPU) dan ujung kanan (Suhu Lingkungan)
    T[0] = T_hot
    T[N - 1] = T_cold

    # Siapkan list untuk menyimpan riwayat suhu setiap waktu
    riwayatSuhu = [T.copy()]
    waktu = [0.0]

    # Hitung jumlah langkah waktu berdasarkan durasi simulasi dan Delta t
    jumlahLangkahWaktu = int(durasiSimulasi / deltaT)

    # 2. HITUNGAN (NESTED LOOPS)
    # LOOP LUAR - Bergerak dari waktu awal sampai waktu akhir simulasi
    for n in range(1, jumlahLangkahWaktu + 1):
        # Salin suhu saat ini agar update Euler Eksplisit memakai kondisi waktu lama
        T_lama = T.copy()

        # LOOP DALAM - Menyusur titik bagian dalam yaitu indeks 1 sampai N-2
        for i in range(1, N - 1):
            # Rumus Euler Eksplisit dari Finite Difference persamaan panas 1D
            # T[i]^(n+1) = T[i]^n + r * (T[i-1]^n - 2T[i]^n + T[i+1]^n)
            T[i] = T_lama[i] + r * (
                T_lama[i - 1] - 2.0 * T_lama[i] + T_lama[i + 1]
            )

        # Kunci ulang boundary condition agar batas kiri dan kanan tetap konstan
        T[0] = T_hot
        T[N - 1] = T_cold

        # Simpan hasil suhu pada langkah waktu ini
        riwayatSuhu.append(T.copy())
        waktu.append(n * deltaT)

    # Ubah riwayat suhu menjadi array 2D: baris = waktu, kolom = posisi
    riwayatSuhu = np.array(riwayatSuhu)
    waktu = np.array(waktu)

    # Mengembalikan data numerik agar bisa dipakai terminal dan animasi
    return riwayatSuhu, waktu, deltaX, r, jumlahLangkahWaktu


def print_explicit_euler_terminal_output(
    riwayatSuhu,
    waktu,
    deltaX,
    deltaT,
    durasiSimulasi,
    r,
    jumlahLangkahWaktu,
):
    # 3. OUTPUT TERMINAL PER DELTAT
    # Cetak ringkasan parameter simulasi
    print("=== HASIL SIMULASI EULER EKSPLISIT (TRANSIENT) ===")
    print(f"Jumlah Titik Grid            : {riwayatSuhu.shape[1]}")
    print(f"Delta x                      : {deltaX:.6f}")
    print(f"Delta t                      : {deltaT:.6f}")
    print(f"Durasi Simulasi              : {durasiSimulasi:.2f}")
    print(f"Jumlah Langkah Waktu         : {jumlahLangkahWaktu}")
    print(f"Nilai r                      : {r:.6f}")
    print("===================================================")

    # Cetak header tabel suhu
    header = "Waktu".rjust(10)
    for i in range(riwayatSuhu.shape[1]):
        header += f"T{i}".rjust(10)

    print(header)
    print("-" * len(header))

    # Cetak suhu semua titik untuk setiap Delta t
    for n in range(len(waktu)):
        baris = f"{waktu[n]:10.2f}"
        for suhu in riwayatSuhu[n]:
            baris += f"{suhu:10.2f}"
        print(baris)


def run_explicit_euler_terminal(
    N=10,
    T_hot=80.0,
    T_cold=25.0,
    alpha=0.1,
    panjangPelat=1.0,
    durasiSimulasi=3.0,
    deltaT=0.01,
):
    # 4. EKSEKUSI TERMINAL
    # Jalankan hitungan Euler Eksplisit lalu tampilkan semua suhu per Delta t
    riwayatSuhu, waktu, deltaX, r, jumlahLangkahWaktu = run_explicit_euler_calculation(
        N=N,
        T_hot=T_hot,
        T_cold=T_cold,
        alpha=alpha,
        panjangPelat=panjangPelat,
        durasiSimulasi=durasiSimulasi,
        deltaT=deltaT,
    )

    print_explicit_euler_terminal_output(
        riwayatSuhu=riwayatSuhu,
        waktu=waktu,
        deltaX=deltaX,
        deltaT=deltaT,
        durasiSimulasi=durasiSimulasi,
        r=r,
        jumlahLangkahWaktu=jumlahLangkahWaktu,
    )

    # Mengembalikan data agar bisa dilanjutkan ke animasi
    return riwayatSuhu, waktu, r


if __name__ == "__main__":
    run_explicit_euler_terminal()
