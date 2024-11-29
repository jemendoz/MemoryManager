from classfile import *
from datetime import datetime as dt
import os

VERSION = "0.3.1"
AUTHOR = "Jesús Mendoza"

ALG_LIST = {
    "1":["belady","fifo","lru"],
    "2":["belady"],
    "3":["fifo"],
    "4":["lru"]
}

def error(msg:str):
    print(f"[!] ERROR: {msg}")
    input("Pulsa [Intro] para continuar...")


def clear() -> None:
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")


def save_to_file(data:str,name:str) -> None:
    with open(f"{name}-{dt.now().strftime('%y-%m-%d_%H-%M-%S')}.txt","w") as file:
        file.write(data)


def calc_alg(alg:str,data:list) -> None:
    mem_access, ram_size, process_size, frame_size, frame_state = data
    if alg == "belady":
        memmngr = MemoryManagerBelady(mem_access, ram_size, process_size, frame_size, frame_state)
    elif alg == "fifo":
        memmngr = MemoryManagerFIFO(mem_access, ram_size, process_size, frame_size, frame_state)
    elif alg == "lru":
        memmngr = MemoryManagerLRU(mem_access, ram_size, process_size, frame_size, frame_state)
    else:
        raise ValueError()

    result:str = memmngr.print_history(verbose=False)

    save_to_file(result,alg)


def main() -> None:
    fail = False
    setup = False
    mem_access = []
    ram_size = 0
    process_size = 0
    frame_size = 0
    frame_state = []

    while True:
        fail = False
        clear()
        print(f"Memory Manager v{VERSION}, by {AUTHOR}\n")
        print("Selecciona una opción:")
        print("1. Calcular todos los algoritmos")
        print("2. Calcular algoritmo de Belady")
        print("3. Calcular algoritmo de FIFO")
        print("4. Calcular algoritmo de LRU")
        print("5. Establecer valores del sistema")
        print("0. Salir")

        opc = input(" Opción: ")
        if opc == "0":
            break
        elif opc == "5":
            print("Secuencia de acceso a memoria (ej. 9D 0C 4F)")
            mem_access = input("Secuencia: ").strip().split(" ")
            for mem in mem_access:
                try:
                    int(mem,16)
                except ValueError:
                    error("valores no correctos de memoria")
                    fail = True
                    break
            if fail:
                continue

            print("Tamaño de la memoria RAM en bytes: (ej 128)")
            inp = input("RAM: ")
            if not inp.isnumeric():
                error("valor no valido")
                continue
            ram_size = int(inp)

            print("Tamaño del proceso en bytes: (ej 256)")
            inp = input("Proceso: ")
            if not inp.isnumeric():
                error("valor no valido")
                continue
            process_size = int(inp)

            print("Tamaño de los marcos en bytes: (ej 32)")
            inp = input("Marco: ")
            if not inp.isnumeric():
                error("valor no valido")
                continue
            frame_size = int(inp)

            print("Estado inicial de memoria (ej. 0 1 5 4)")
            frame_state = input("Estado: ").strip().split(" ")
            if len(frame_state) > (ram_size // frame_size):
                error("tamano no valido del estado")
                continue
            for frame in frame_state:
                if not frame.isnumeric():
                    error("valor no valido")
                    fail = True
                    break
            if fail:
                continue

            setup = True
        elif opc in ["1", "2", "3", "4"]:
            if not setup:
                error("inicia los valores del sistema antes")
                continue

            algs = ALG_LIST[opc]
            for alg in algs:
                try:
                    calc_alg(alg,[mem_access, ram_size, process_size, frame_size, frame_state])
                except ValueError:
                    error("selección de algoritmo no válido")
            print("[+] HECHO!")
            input("Pulsa [Intro] para continuar...")


if __name__ == "__main__":
    main()
