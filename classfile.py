from copy import copy
from tabulate import tabulate

class MemoryManager:
    def __init__(self,mem_access:list[str],ram_size:int,process_size:int,frame_size:int,
                 frame_state=None) -> None:

        # La lista de accesos a memoria del proceso, viene en hex
        self.mem_access:list[int] = [int(i,16) for i in mem_access]

        self.ram_size:int = ram_size # El tamanno en bytes de la ram fisica
        self.process_size:int = process_size # El tamanno que se asigna en memoria virtual al proceso
        self.frame_size:int = frame_size # El tamano de cada frame

        self.frame_num:int = ram_size // frame_size # La cantidad de frames
        self.page_num:int = process_size // frame_size

        self.pointer: int = 0

        # Este diccionario tiene como key el valor de memoria virtual, y
        # su value es una list con pagina y desplazamiento de la direccion
        self.vmem_locations:dict[int,list[int]] = {i:[i//frame_size,i%frame_size] for i in self.mem_access}

        # El estado de los frames
        if not frame_state:
            self.frame_state:list[int] = []
        else:
            self.frame_state:list[int] = frame_state

    def fix_fail(self,pag:int,index:int) -> int:
        """
        Algoritmo para remplazar paginas en caso de que se intente
        acceder a una no cargada. Debe ser implementado en clases
        derivadas.
        """
        oldpage = self.frame_state[self.pointer]
        self.frame_state[self.pointer] = pag
        return oldpage

    def frame_evolution(self):
        history = []
        for i,mem in enumerate(self.mem_access):
            enter = -1
            oldpage = -1
            page = self.vmem_locations[mem][0]
            if not page in self.frame_state:
                enter = page
                if len(self.frame_state) < self.frame_num:
                    self.frame_state.append(page) # Cargado a demanda
                else:
                    oldpage = self.fix_fail(page,i) # Remplazo
            history.append([mem,copy(self.frame_state),enter,oldpage])
        return history

    def print_history(self,verbose=True):
        history = self.frame_evolution()
        print_info = [[s[0], # Direccion virtual
                       bin(s[0]), # Direccion virtual en binario
                       self.vmem_locations[s[0]][0], # Pagina
                       bin(self.vmem_locations[s[0]][0]), # Pagina en binario
                       self.vmem_locations[s[0]][1], # Desplazamiento
                       bin(self.vmem_locations[s[0]][1]), # Desplazamiento en binario
                       "F" if s[2]!=-1 else "-", # Fallo?
                       s[2] if s[2]!=-1 else "-", # Entra
                       s[3] if s[3]!=-1 else "-", # Sale
                       " | ".join([str(x) for x in s[1]]), # Frames, o marcos de pagina
                       " | ".join(["0, -" if not i in s[1] else "1, " + str(s[1].index(i)) for i in range(self.page_num)]), # Tabla de pagina
                       s[1].index(self.vmem_locations[s[0]][0]), # Marco al que pertenece
                       bin(s[1].index(self.vmem_locations[s[0]][0])*self.frame_size + self.vmem_locations[s[0]][1]), # Dir fisica bin
                       hex(s[1].index(self.vmem_locations[s[0]][0])*self.frame_size + self.vmem_locations[s[0]][1]) # Dir fisica hex
                       ] for s in history]

        print_info.insert(0,["Mem","Mem bin","Pag","Pag bin","Despl","Despl bin","Fallo",
                             "Entra","Sale","Frames","Tabla pag","Marco","Dir bin","Dir hex"])

        if verbose:
            print(tabulate(print_info,headers="firstrow",tablefmt="fancy_grid"))
        else:
            return tabulate(print_info,headers="firstrow",tablefmt="fancy_grid")

class MemoryManagerBelady(MemoryManager):
    def __init__(self,mem_access:list[int]|list[str],ram_size:int,process_size:int,frame_size:int,
                 frame_state=None):
        super().__init__(mem_access, ram_size, process_size, frame_size, frame_state)

    def fix_fail(self,pag:int,index:int):
        replace:int = -1
        access_left = [self.vmem_locations[self.mem_access[i]][0] for i in range(index, len(self.mem_access))] # Los accesos que quedan
        for i,candidate in enumerate(self.frame_state):
            if candidate not in access_left: # Si el candidato no se usa nunca mas, se cambia directamente
                oldpage = candidate
                self.frame_state[i] = pag
                return oldpage
            elif replace == -1 or access_left.index(self.frame_state[replace]) < access_left.index(self.frame_state[i]):
                replace = i

        oldpage = self.frame_state[replace]
        self.frame_state[replace] = pag
        return oldpage

class MemoryManagerFIFO(MemoryManager):
    def __init__(self,mem_access:list[int]|list[str],ram_size:int,process_size:int,frame_size:int,
                 frame_state=None):
        super().__init__(mem_access, ram_size, process_size, frame_size, frame_state)

    def fix_fail(self,pag:int,index:int):
        oldpage = self.frame_state[self.pointer]
        self.frame_state[self.pointer] = pag
        self.pointer = (self.pointer + 1) % self.frame_num
        return oldpage

class MemoryManagerLRU(MemoryManager):
    def __init__(self, mem_access: list[int] | list[str], ram_size: int, process_size: int, frame_size: int,
                 frame_state=None):
        super().__init__(mem_access, ram_size, process_size, frame_size, frame_state)

    def fix_fail(self, pag: int, index: int):
        replace: int = -1
        access_left = [self.vmem_locations[self.mem_access[i]][0] for i in range(index)]  # Los accesos que quedan
        access_left.reverse()
        for i, candidate in enumerate(self.frame_state):
            if candidate not in access_left:  # Si el candidato no se usa nunca mas, se cambia directamente
                oldpage = candidate
                self.frame_state[i] = pag
                return oldpage
            elif replace == -1 or access_left.index(self.frame_state[replace]) < access_left.index(self.frame_state[i]):
                replace = i

        oldpage = self.frame_state[replace]
        self.frame_state[replace] = pag
        return oldpage
