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
import sys

from exception import *

def ARM64_HW_PGTABLE_LEVEL_SHIFT(n):
    return ((self.PAGE_SHIFT - 3) * (4 - (n)) + 3)

def pxd_none(pxd):
    return not(pxd & 0b1)

def pxd_block(pxd):
    return pxd & 0b10

def desc_to_table_address(pxdp):
    """Only for 48bit 4KB"""
    return pxdp & 0xFFFFFFFFF000

def address_range_check(func):
    def func_wrapper(self, address):
        if address < 0 or address > 0xFFFFFFFFFFFFFFFF:
            raise AddressRangeError()
        func(self, address)

class Paging_info():
    def __init__(self, shift=0,size=0,ptrs=0):
        self.SHIFT = shift
        self.SIZE = size
        self.PTRS = ptrs

    def address_to_index(self, address):
        return ((address >> self.SHIFT) & self.PTRS) * 8
    
    def address_offset(self, address):
        return (address & (self.SIZE - 1))

class VirtualMachine():
    def __init__(self):
        return
    
class mmu:
    def __init__(self, physical_memory, CONFIG_ARM64_PAGE_SHIFT=12, CONFIG_PGTABLE_LEVELS=4, va_bit=48):
        self._mmu_on = False
        self._ttbr1 = 0
        self._ttbr0 = 0
        self._physical_memory = physical_memory
        self._va_bit = va_bit
         
        #Paging option
        self.pte = Paging_info(CONFIG_ARM64_PAGE_SHIFT, 1 << self.PAGE_SHIFT, (1 << (self.PAGE_SHIFT - 3)))
        
        # PMD initialize
        if CONFIG_PGTABLE_LEVELS > 2:
            pxd_shift = ARM64_HW_PGTABLE_LEVEL_SHIFT(2)
            self.pmd = Paging_info(pxd_shift, 1 << pxd_shift, self.pte.PTRS) 
        else:
            self.pmd = Paging_info()
            
        # PUD initialize
        if CONFIG_PGTABLE_LEVELS > 3:
            pxd_shift = ARM64_HW_PGTABLE_LEVEL_SHIFT(1)
            self.pud = Paging_info(pxd_shift, 1 << pxd_shift, self.pte.PTRS) 
        else:
            self.pud = Paging_info()
            
        # PGD initialize
        pxd_shift = ARM64_HW_PGTABLE_LEVEL_SHIFT(4 - self.CONFIG_PGTABLE_LEVELS)
        self.pgd = Paging_info(pxd_shift, 1 << pxd_shift, 1 << (self._va_bit - self.pte.PTRS)) 

        # section init
        self.section = self.pmd
        
    def address_translation(self, address):
        if self._mmu_on:
            return self.translation_table_walk(address)
        else:
            return address
    
    def translation_table_walk(self, address):
        pxd = self._ttbr1 if (address >> self._va_bit) != 0 else self._ttbr0
    
        if pxd % self.PAGE_SIZE:
            raise PageFaultError()

        level_list = [self.pgd, self.pud, self.pmd, self.pte]

        for level in level_list:
            if level.SHIFT:
                pxdp = desc_to_table_address(pxd) + level.address_to_index(address)
                pxd = self._physical_memory.load(pxdp, 8) 
            
            if pxd_none(pxd):
                raise PageFaultError()

            if pxd_block(pxd):
                if level == self.pte:
                    raise PageFaultError()

                return self.desc_to_table_address(pxd) + level.address_offset(address)

        return self.desc_to_table_address(pxd) + self.pte.address_offset(address)

class PhysicalMemory:
    def __init__(self):
        """512MB 바이트 배열을 생성, 커널 이미지를 로드한다."""
        self.memory = array('B',(0 for i in range(0,512*1024*1024)))
        self.kimg = Kimage()

    def load(self, address, size):
        """ Return unsigned value """
        memv = memoryview(self.memory[address:address+size])
        return memv.cast(self.size_to_suffix(size))[0]
    
    def store(self, address, size, value):
        barray = value.to_bytes(size,sys.byteorder)
        
        for src, dest in zip(barray, range(address, address + size)):
            self.memory[dest] = src
    
    def size_to_suffix(self, size):
        if size == 1:
            return 'B'
        elif size == 2:
            return 'H'
        elif size == 4:
            return 'L'
        elif siez == 8:
            return 'Q'
        else:
            raise UnSupportedOperandSize()

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
    pass

def write(address, value):
    #if mmu.mmu_on:
        #Translation
    #else:
        #Physical
    pass

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
