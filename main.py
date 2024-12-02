from classfile import *
from datetime import datetime as dt
import os

VERSION = "1.0.4"
AUTHOR = "Jesús Mendoza"

ALG_LIST = {
    "2":["belady","fifo","lru","clock"],
    "3":["belady"],
    "4":["fifo"],
    "5":["lru"],
    "6":["clock"]
}

# Lanza un error, pero bonito y controlado :P
def error(msg:str):
    print(f"[!] ERROR: {msg}")
    input("Pulsa [Intro] para continuar...")

# Limpia la pantalla mediante comando de shell
def clear() -> None:
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")

# Guarda data en un archivo determinado por el nombre (usamos el algoritmo) y formato con fecha
def save_to_file(data:str,name:str) -> None:
    with open(f"{name}-{dt.now().strftime('%y-%m-%d_%H-%M-%S')}.txt","w",encoding="utf8") as file:
        file.write(data)

# Calculamos y guardamos un algoritmo
def calc_alg(alg:str,data:list) -> None:
    mem_access, ram_size, process_size, frame_size, frame_state = data
    mem_access_safe = copy(mem_access) # Versiones seguras de usar, que no cambian los valores del usuario
    frame_state_safe = copy(frame_state)
    if alg == "belady":
        memmngr = MemoryManagerBelady(mem_access_safe, ram_size, process_size, frame_size, frame_state_safe)
    elif alg == "fifo":
        memmngr = MemoryManagerFIFO(mem_access_safe, ram_size, process_size, frame_size, frame_state_safe)
    elif alg == "lru":
        memmngr = MemoryManagerLRU(mem_access_safe, ram_size, process_size, frame_size, frame_state_safe)
    elif alg == "clock":
        memmngr = MemoryManagerClock(mem_access_safe, ram_size, process_size, frame_size, frame_state_safe)
    else:
        raise ValueError()

    result:str = memmngr.print_history(verbose=False)

    save_to_file(result,alg)

# Funcion main
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
        print("1. Establecer valores del sistema")
        print("2. Calcular todos los algoritmos")
        print("3. Calcular algoritmo de Belady")
        print("4. Calcular algoritmo de FIFO")
        print("5. Calcular algoritmo de LRU")
        print("6. Calcular algoritmo de reloj")
        print("0. Salir")

        opc = input(" Opción: ")
        if opc == "0":
            break
        elif opc == "1":
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
            frame_state = frame_state if frame_state != [""] else []
            if len(frame_state) > (ram_size // frame_size):
                error("tamano no valido del estado")
                continue
            for frame in frame_state:
                if not frame.isnumeric():
                    error("valor no valido")
                    fail = True
                    break
            frame_state = [int(x) for x in frame_state]
            if fail:
                continue

            setup = True
        elif opc in ["2", "3", "4", "5", "6"]:
            if not setup: # Si no se han iniciado los valores del usuario
                error("inicia los valores del sistema antes")
                continue

            algs = ALG_LIST[opc] # Seleccionar que algoritmos calcular
            # se que usar esto de ALG_LIST no es lo mas intuitivo, pero
            # es facilmente extensible si se annaden mas
            for alg in algs:
                try:
                    calc_alg(alg,[mem_access, ram_size, process_size, frame_size, frame_state])
                except ValueError as e:
                    error("selección de algoritmo no válido")
            print("[+] HECHO!")
            input("Pulsa [Intro] para continuar...")

# Ejecuta main
if __name__ == "__main__":
    main()
