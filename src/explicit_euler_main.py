from src.explicit_euler_animate import run_explicit_euler_animation
from src.explicit_euler_terminal import (
    run_explicit_euler_calculation,
    run_explicit_euler_terminal,
)


def run_explicit_euler_simulation(
    N=10,
    T_hot=80.0,
    T_cold=25.0,
    alpha=0.1,
    panjangPelat=1.0,
    durasiSimulasi=3.0,
    deltaT=0.01,
    intervalAnimasi=50,
    mode="terminal",
):
    # 1. (INPUT & INISIALISASI)
    # Parameter default dibuat stabil dan cukup terlihat untuk demonstrasi

    # 2. PILIH MODE OUTPUT
    # Mode terminal menampilkan suhu semua titik per Delta t
    if mode == "terminal":
        riwayatSuhu, waktu, r = run_explicit_euler_terminal(
            N=N,
            T_hot=T_hot,
            T_cold=T_cold,
            alpha=alpha,
            panjangPelat=panjangPelat,
            durasiSimulasi=durasiSimulasi,
            deltaT=deltaT,
        )
        return riwayatSuhu, waktu, r, None

    # Mode animasi hanya menghitung data, lalu menampilkan pergerakan suhu
    if mode == "animasi":
        riwayatSuhu, waktu, _deltaX, r, _jumlahLangkahWaktu = run_explicit_euler_calculation(
            N=N,
            T_hot=T_hot,
            T_cold=T_cold,
            alpha=alpha,
            panjangPelat=panjangPelat,
            durasiSimulasi=durasiSimulasi,
            deltaT=deltaT,
        )

        # 3. OUTPUT ANIMASI PERUBAHAN SUHU
        # Data riwayat suhu dipakai untuk menggerakkan animasi
        animasi = run_explicit_euler_animation(
            riwayatSuhu=riwayatSuhu,
            waktu=waktu,
            intervalAnimasi=intervalAnimasi,
        )

        # Mengembalikan data jika nanti ingin dipakai oleh menu atau modul lain
        return riwayatSuhu, waktu, r, animasi

    raise ValueError("Mode Euler Eksplisit harus 'terminal' atau 'animasi'.")


if __name__ == "__main__":
    run_explicit_euler_simulation()
