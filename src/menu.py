import matplotlib.pyplot as plt
import numpy as np

from src.explicit_euler_main import run_explicit_euler_simulation
from src.steady_state import run_steady_state_simulation


def show_menu():
    print("=== Heat Distribution 1D ===")
    print("1. Simulasi Euler Eksplisit")
    print("2. Simulasi Steady-State")
    print("3. Keluar")


def input_float(prompt, default):
    val = input(f"{prompt} (Default {default}): ").strip()
    if not val:
        return default
    try:
        return float(val)
    except ValueError:
        print("Input tidak valid, menggunakan nilai default.")
        return default


def input_int(prompt, default):
    val = input(f"{prompt} (Default {default}): ").strip()
    if not val:
        return default
    try:
        return int(val)
    except ValueError:
        print("Input tidak valid, menggunakan nilai default.")
        return default



def show_euler_menu():
    print("\n=== Mode Euler Eksplisit ===")
    print("1. Output Terminal Per Delta t")
    print("2. Animasi Perubahan Suhu")
    print("3. Kembali")


def run_steady_state_from_menu():
    print("\n=== Simulasi Steady-State ===")
    print("1. Gunakan Parameter Default (N=20, Thot=80, Tcold=25)")
    print("2. Input Parameter Manual")
    pilihan = input("Pilihan: ").strip()

    # 1. (INPUT & INISIALISASI)
    if pilihan == "2":
        print("\n--- Input Parameter Steady-State ---")
        JUMLAH_TITIK = input_int("Jumlah Titik (N)", 20)
        SUHU_CPU = input_float("Suhu CPU / Titik Panas (C)", 80.0)
        SUHU_LINGKUNGAN = input_float("Suhu Lingkungan / Ujung Dingin (C)", 25.0)
        TOLERANSI = input_float("Toleransi Error", 0.0001)
    else:
        JUMLAH_TITIK = 20
        SUHU_CPU = 80.0
        SUHU_LINGKUNGAN = 25.0
        TOLERANSI = 0.0001

    print(f"\nMenjalankan simulasi dengan N={JUMLAH_TITIK}, T_hot={SUHU_CPU}, T_cold={SUHU_LINGKUNGAN}...")

    # 2. HITUNGAN GAUSS-SEIDEL
    # Fungsi steady-state mengembalikan suhu awal, suhu akhir, dan jumlah iterasi
    T_awal, T_akhir, total_iterasi = run_steady_state_simulation(
        N=JUMLAH_TITIK,
        T_hot=SUHU_CPU,
        T_cold=SUHU_LINGKUNGAN,
        toleransiError=TOLERANSI,
    )

    # 3. OUTPUT TERMINAL
    # Cetak ringkasan hasil agar flow menu punya feedback numerik
    print("=== HASIL SIMULASI GAUSS-SEIDEL (STEADY STATE) ===")
    print(f"Total Iterasi hingga Konvergen: {total_iterasi} kali")
    print(f"Suhu Titik Tengah Akhir       : {T_akhir[JUMLAH_TITIK // 2]:.2f} C")
    print("==================================================")

    # 4. OUTPUT VISUALISASI
    # Render grafik before vs after seperti blok eksekusi steady_state.py
    posisi_x = np.linspace(0, 100, JUMLAH_TITIK)

    plt.figure(figsize=(8, 5))
    plt.plot(
        posisi_x,
        T_awal,
        "b--",
        marker="o",
        label="Before (Awal Mulai / Komputer Mati)",
    )
    plt.plot(
        posisi_x,
        T_akhir,
        "r-",
        marker="s",
        label=f"After (Stabil / Konvergen pada Iterasi ke-{total_iterasi})",
    )

    plt.title("Profil Distribusi Suhu Stabil pada Papan Induk (Gauss-Seidel 1D)")
    plt.xlabel("Posisi Panjang Pelat Pendingin (%)")
    plt.ylabel("Temperatur (C)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.show()


def run_explicit_euler_from_menu():
    print("\n=== Simulasi Euler Eksplisit ===")
    print("1. Gunakan Parameter Default (N=10, dt=0.01, Durasi=3s)")
    print("2. Input Parameter Manual")
    pilihan = input("Pilihan: ").strip()

    # 1. (INPUT & INISIALISASI)
    if pilihan == "2":
        print("\n--- Input Parameter Euler Eksplisit ---")
        JUMLAH_TITIK = input_int("Jumlah Titik (N)", 10)
        SUHU_CPU = input_float("Suhu CPU / Titik Panas (C)", 80.0)
        SUHU_LINGKUNGAN = input_float("Suhu Lingkungan / Ujung Dingin (C)", 25.0)
        ALPHA = input_float("Difusivitas Termal (Alpha)", 0.1)
        PANJANG_PELAT = input_float("Panjang Pelat", 1.0)
        DURASI = input_float("Durasi Simulasi (Detik)", 3.0)
        DELTA_T = input_float("Langkah Waktu (Delta t)", 0.01)
        INTERVAL_ANIMASI = input_int("Interval Animasi (ms)", 50)
    else:
        JUMLAH_TITIK = 10
        SUHU_CPU = 80.0
        SUHU_LINGKUNGAN = 25.0
        ALPHA = 0.1
        PANJANG_PELAT = 1.0
        DURASI = 3.0
        DELTA_T = 0.01
        INTERVAL_ANIMASI = 50

    # 2. PILIH MODE OUTPUT
    # Submenu ini memisahkan output tabel terminal dan output animasi
    while True:
        show_euler_menu()
        choice = input("Pilih mode Euler Eksplisit: ").strip()

        try:
            match choice:
                case "1":
                    run_explicit_euler_simulation(
                        N=JUMLAH_TITIK,
                        T_hot=SUHU_CPU,
                        T_cold=SUHU_LINGKUNGAN,
                        alpha=ALPHA,
                        panjangPelat=PANJANG_PELAT,
                        durasiSimulasi=DURASI,
                        deltaT=DELTA_T,
                        intervalAnimasi=INTERVAL_ANIMASI,
                        mode="terminal",
                    )
                    break
                case "2":
                    run_explicit_euler_simulation(
                        N=JUMLAH_TITIK,
                        T_hot=SUHU_CPU,
                        T_cold=SUHU_LINGKUNGAN,
                        alpha=ALPHA,
                        panjangPelat=PANJANG_PELAT,
                        durasiSimulasi=DURASI,
                        deltaT=DELTA_T,
                        intervalAnimasi=INTERVAL_ANIMASI,
                        mode="animasi",
                    )
                    break
                case "3":
                    break
                case _:
                    print("Pilihan mode tidak valid.\n")
        except ValueError as e:
            print(f"\n[ERROR SIMULASI] {e}")
            print("Pesan: Simulasi eksplisit tidak stabil. Silakan ulangi dan ubah parameter (misalnya Delta t lebih kecil).\n")
            break


def run_menu():
    while True:
        show_menu()
        choice = input("Pilih menu: ").strip()

        match choice:
            case "1":
                run_explicit_euler_from_menu()
            case "2":
                run_steady_state_from_menu()
            case "3":
                print("Program selesai.")
                break
            case _:
                print("Pilihan tidak valid.\n")
