import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def run_explicit_euler_animation(
    riwayatSuhu,
    waktu,
    intervalAnimasi=50,
):
    # 1. (INPUT & INISIALISASI ANIMASI)
    # Ambil jumlah titik dari data riwayat suhu hasil Euler Eksplisit
    N = riwayatSuhu.shape[1]

    # Buat posisi x dalam persen agar tampilannya sejalan dengan steady-state
    posisi_x = np.linspace(0, 100, N)

    # Siapkan figure dan garis awal untuk animasi distribusi suhu
    fig, ax = plt.subplots(figsize=(8, 5))

    garis, = ax.plot(
        posisi_x,
        riwayatSuhu[0],
        "r-",
        marker="o",
        label="Distribusi Suhu",
    )

    # Teks kecil di dalam grafik untuk menunjukkan waktu simulasi saat ini
    teks_waktu = ax.text(
        0.02,
        0.95,
        "",
        transform=ax.transAxes,
        verticalalignment="top",
    )

    # 2. ATUR KOMPONEN GRAFIK
    # Komponen visual dibuat mirip dengan grafik steady-state
    ax.set_title("Animasi Distribusi Suhu Transient (Euler Eksplisit 1D)")
    ax.set_xlabel("Posisi Panjang Pelat Pendingin (%)")
    ax.set_ylabel("Temperatur (C)")
    ax.set_xlim(0, 100)
    ax.set_ylim(np.min(riwayatSuhu) - 5, np.max(riwayatSuhu) + 5)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()

    # 3. UPDATE FRAME ANIMASI
    # Fungsi ini dipanggil berulang oleh FuncAnimation untuk setiap langkah waktu
    def update(frame):
        garis.set_ydata(riwayatSuhu[frame])
        teks_waktu.set_text(f"Waktu = {waktu[frame]:.2f}")
        return garis, teks_waktu

    # Buat animasi dari data suhu awal sampai akhir durasi simulasi
    animasi = FuncAnimation(
        fig,
        update,
        frames=len(waktu),
        interval=intervalAnimasi,
        repeat=False,
    )

    # Tampilkan animasi ke layar
    plt.show()

    # Return animasi agar object tidak langsung dibuang oleh Python
    return animasi
