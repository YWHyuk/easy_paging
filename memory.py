"""
가상 머신 객체를 생성.
가상 머신 객체는 mmu를 가진다.
가상 머신 객체는 physical 메모리를 가진다.

physical 메모리 객체는 커널 이미지를 가진다.
physical 메모리 객체는 커널 이미지의 offset을 가진다.
physical 메모리 객체는 물리 메모리 정보를 가진다(start/end of dram)

mmu 객체는 ttbr0, ttbr1를 가진다.
mmu 객체는 tranlation 함수를 가진다.
mmu 객체는 가상 메모리 객체에 대해 translation을 수행한다.(Page fault를 발생할 수 도 있다.)

사용자는 메모리 객체에 대해 읽고/쓰기를 수행한다.
사용자는 심볼에 대해 접근할 수 있다.
사용자는 mmu를 킬 수 있다.
사용자는 ttbr0 ttrb1에 값을 설정할 수 있다.
사용자는 물리 메모리의 정보를 읽을 수 있다.
사용자는 커널 이미지의 오프셋을 알 수 있다.
"""
from array import array

class VirtualMachine():
    def __init__(self):
        return
    
class mmu:
    def __init__(self, CONFIG_ARM64_PAGE_SHIFT=12, CONFIG_PGTABLE_LEVELS=4, va_bit=48):
        self._mmu_on = False
        self._ttbr1 = 0
        self._ttbr0 = 0
        
        #Paging option
        self.PAGE_SHIFT = CONFIG_ARM64_PAGE_SHIFT
        self.PAGE_SIZE = 1 << self.PAGE_SHIFT
        self.PTRS_PER_PTE = (1 << (self.PAGE_SHIFT - 3))
        self.CONFIG_PGTABLE_LEVELS = CONFIG_PGTABLE_LEVELS
        self._va_bit = va_bit
        
        # PMD initialize
        if CONFIG_PGTABLE_LEVELS > 2:
            self.PMD_SHIFT = self.ARM64_HW_PGTABLE_LEVEL_SHIFT(2)
            self.PMD_SIZE = 1 << self.PMD_SHIFT
            self.PTRS_PER_PMD = self.PTRS_PER_PTE
        else:
            self.PMD_SHIFT = 0
            self.PMD_SIZE = 0
            self.PTRS_PER_PMD = 0
        
        # PUD initialize
        if CONFIG_PGTABLE_LEVELS > 3:
            self.PUD_SHIFT = self.ARM64_HW_PGTABLE_LEVEL_SHIFT(1)
            self.PUD_SIZE = 1 << self.PUD_SHIFT
            self.PTRS_PER_PUD = self.PTRS_PER_PTE
        else:
            self.PUD_SHIFT = 0
            self.PUD_SIZE = 0
            self.PTRS_PER_PUD = 0
        
        # PGD initialize
        self.PGDIR_SHIFT = self.ARM64_HW_PGTABLE_LEVEL_SHIFT(4 - self.CONFIG_PGTABLE_LEVELS)
        self.PGDIR_SIZE = 1 << self.PUD_SHIFT
        self.PTRS_PER_PGD = 1 << (self._va_bit - self.PTRS_PER_PTE)

        # section init
        self.SECTION_SHIFT = self.PMD_SHIFT
        self.SECTION_SIZE = self.PMD_SIZE

        self.physical_memory = PhysicalMemory()

    def address_translation(self, address):
        if address < 0 or address > 0xFFFFFFFFFFFFFFFF:
            raise AddressRangeError()
        
        if self._mmu_on:
            return self.translation_table_walk(address)
        else:
            return address
    
    def translation_table_walk(self, address):
        pgd_address = self._ttbr1 if address >> self._va_bit != 0 else self._ttbr0
        
        if pgd_address % self.PAGE_SIZE:
            raise PageFaultError()
        

        # 4k 4level hard coding

    def ARM64_HW_PGTABLE_LEVEL_SHIFT(self, n):
        return ((self.PAGE_SHIFT - 3) * (4 - (n)) + 3)

def operandsize_check(func):
    def func_wrapper(self, address, size, *argv):
        if size == 1:
            prefix = 'B'
        elif size == 2:
            prefix = 'H'
        elif size == 4:
            prefix = 'L'
        elif size == 8:
            prefix = 'Q'
        else:
            raise UnSupportedOperandSize()
        func(self, address, size, *argv)

class PhysicalMemory:
    def __init__(self):
        """512MB 바이트 배열을 생성, 커널 이미지를 로드한다."""
        self.memory = array('b',(0 for i in range(0,512*1024*1024)))
    def load_kimg(self):
        pass

    @operandsize_check
    @addressrange_check
    def load(self, address, size):
        
        memv = memoryview(self.memory[address:address+size])    
        pass
    def store(self):
        pass

class VirtualMemory:
    def __init__(self):
        return

class Symbol:
    def __init__(self):
        return        

# User api
def read(address, value):
    #if mmu.mmu_on:
        #Translation
        #  else:
        #Physical
def write(address, value):
    #if mmu.mmu_on:
        #Translation
    #else:
        #Physical

def get_symbol():
    return

def mmu_on():
    mmu.mmu_on = True

def mmu_off():
    mmu.mmu_on = False

def set_ttbr1(address):
    mmu.ttrb1 = address

def set_ttbr0(address):
    mmu.ttrb0 = address

def get_dram_info():
    return

def get_kimg_offset():
    return


def UnSupportedOperandSize(exception):
    pass
def PageFaultError(exception):
    pass
def AddressRangeError(exception):
    pass