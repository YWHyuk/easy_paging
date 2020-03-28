# Install
## Dependency

1. numpy

## Install pythom module

1. install numpy
```
pip install numpy
```

# How to use
python interperter을 열고, memory.py를 임포트합니다.
그런다음 VirtualMachine 객체를 생성하면 됩니다.
```
vm = VirtualMachine()
```
해당 객체에서 사용할 수 있는 메소드들은 다음과 같습니다.

#### store(address, size, value)
```
해당 주소에 value를 저장한다. size는 오퍼랜드의 크기를 의미한다.
addresss : 0x0000000000000000~0xFFFFFFFFFFFFFFFF
size : 1 | 2 | 4 | 8
```
#### load(address, size)
```
해당 주소에서 size만큼 읽어와 리턴한다.
addresss : 0x0000000000000000~0xFFFFFFFFFFFFFFFF
size : 1 | 2 | 4 | 8
```
#### mmu_on()
```
mmu를 활성화 한다.
```
#### mmu_off()
```
mmu를 비활성화 한다.
```
#### is_mmu_on()
```
mmu를 활성화 되었는지를 리턴한다.
```
#### set_ttbr0(address)
```
ttbr0 레지스터에 어드레스의 값을 대입한다.
```
#### set_ttbr1(address)
```
ttbr1 레지스터에 어드레스의 값을 대입한다.
```
#### symbols()
```
페이징에 관련된 중요 심볼들을 딕셔너리 형태로 리턴한다.
```
#### kimg_offset()
```
가상주소와 실제 이미지의 주소의 차이를 리턴한다.
```

# Limitation
1. No TLB
2. No permission check
3. No continuos mapping
4. No memory allocator

# Todo

1. GraphViz
2. PageFault visualize
3. symbol table widget
3. memory allocator
