# Install
## Dependency

1. pyqt5
2. numpy
3. pyqtconsole
4. pygraphviz

## Install pythom module

1. install pyqt5
```
pip install pyqt5
```
2. install numpy
```
pip install numpy
```
3. install pyqtconsole
```
pip install pyqtconsole
```
4. install pygraphviz
```
pip install pygraphviz
```

# How to use
인터프리터가 열리면, 해당 네임 스페이스에는 vm이라는 객체가 생성되어 있습니다.
해당 객체를 통해 메모리 관련 메소드를 호출할 수 있습니다.

사용할 수 있는 메소드들은 다음과 같습니다.

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
