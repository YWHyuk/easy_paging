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
import sys, random

from exception import *

def ARM64_HW_PGTABLE_LEVEL_SHIFT(n):
    return ((self.PAGE_SHIFT - 3) * (4 - (n)) + 3)

def desc_to_table_address(pxdp):
    """Only for 48bit 4KB"""
    return pxdp & 0xFFFFFFFFF000
    
def pxd_none(pxd):
    return not(pxd & 0b1)

def pxd_block(pxd):
    return pxd & 0b10


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
        self._physical_memory = PhysicalMemory()
        self._kimage = Kimage()
        self.mmu = MMU(self._physical_memory)
    
    # User api
    def load(self, address, size):
        if size != 1 and size != 2 and size != 4 and size != 8:
            raise UnSupportedOperandSize()

        if address < 0 or (address + size) > 0xFFFFFFFFFFFFFFFF:
            raise AddressRangeError()
        
        if address // self.mmu.pte.SHIFT != address+size // self.mmu.pte.SHIFT:
            raise BoundaryError()
        
        physical_address = self.mmu.address_translation(address)
        return self._physical_memory.load(physical_address, size)
        
    def store(self, address, size, value):
        if size != 1 and size != 2 and size != 4 and size != 8:
            raise UnSupportedOperandSize()

        if address < 0 or (address + size) > 0xFFFFFFFFFFFFFFFF:
            raise AddressRangeError()
        
        if address // self.mmu.pte.SHIFT != address+size // self.mmu.pte.SHIFT:
            raise BoundaryError()

        physical_address = self.mmu.address_translation(address)
        self._physical_memory.store(physical_address, size, value)
        
    def symbols(self):
        return self._kimage.symbols()
    
    def kimg_offset(self):
        return self._kimage.kimg_offset

class MMU:
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
    
    def mmu_on(self):
        self._mmu_on = True

    def mmu_off(self):
        self._mmu_on = False

    def set_ttbr1(self, address):
        mmu._ttrb1 = address

    def set_ttbr0(self, address):
        mmu._ttrb0 = address
    
class PhysicalMemory:
    def __init__(self):
        """512MB 바이트 배열을 생성, 커널 이미지를 로드한다."""
        self._memory = array('B',(0 for i in range(0,512*1024*1024)))
        
    def load(self, address, size):
        """ Return unsigned value """
        memv = memoryview(self._memory[address:address+size])
        return memv.cast(self.size_to_suffix(size))[0]
    
    def store(self, address, size, value):
        barray = value.to_bytes(size,sys.byteorder)
        
        for src, dest in zip(barray, range(address, address + size)):
            self._memory[dest] = src
    
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

class Kimage:
    def __init__(self):
        """4k 4level system.map을 기준으로 하드 코딩됨"""
        self._symbol = {}
        self._symbol["_text"] = 0xffff000010080000
        self._symbol["_end"] = 0xffff00001144d000
        self._symbol["swapper_pg_dir"] = 0xffff0000110c5000
        self._symbol["swapper_pg_end"] = 0xffff0000110c6000
        self._symbol["init_pg_dir"] = 0xffff00001144a000
        self._symbol["init_pg_end"] = 0xffff00001144d000
        self._symbol["bm_pud"] = 0xffff0000113db000
        self._symbol["bm_pmd"] = 0xffff0000113dc000
        self._symbol["bm_pte"] = 0xffff0000113dd000

        # Fixmap address
        self._symbol["FIX_PTE"] = 0xffff7dfffe633000
        self._symbol["FIX_PMD"] = 0xffff7dfffe634000
        self._symbol["FIX_PUD"] = 0xffff7dfffe635000
        self._symbol["FIX_PGD"] = 0xffff7dfffe636000
        
        #2~256MB사이에 2MB align으로, 커널 이미지 시작 위치를 정한다.
        physical_kimg_offset = random.randint(1,128) * 2 * 1024 * 1024
        self._kimg_offset = self._symbol["_text"] - physical_kimg_offset
    
    def symbols(self):
        return dict(self._symbol)        
    
    def kimg_offset(self):
        return self._kimg_offset
