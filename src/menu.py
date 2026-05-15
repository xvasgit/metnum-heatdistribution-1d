from src.steady_state import run_steady_state_simulation
from src.explicit_euler import run_explicit_euler_simulation


def show_menu():
    print("=== Heat Distribution 1D ===")
    print("1. Simulasi Steady-State")
    print("2. Simulasi Euler Eksplisit")
    print("3. Keluar")


def run_menu():
    while True:
        show_menu()
        choice = input("Pilih menu: ")

        match choice:
            case "1":
                run_steady_state_simulation()
            case "2":
                run_explicit_euler_simulation()
            case "3":
                print("Program selesai.")
                break
            case _:
                print("Pilihan tidak valid.\n")