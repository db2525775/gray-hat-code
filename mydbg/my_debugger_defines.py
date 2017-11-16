# -*- coding: utf-8 -*-  
# @Date    : 2016-08-11 16:07:38  
# @Author  : giantbranch (giantbranch@gmail.com)  
# @Link    : http://blog.csdn.net/u012763794?viewmode=contents  
  
#把所有的结构体，联合体，常量等放这，方便以后维护  
  
from ctypes import *  
  
# 给ctypes类型重新命名，跟windows编程接轨吧  
WORD    = c_ushort  
DWORD   = c_ulong  
LPBYTE  = POINTER(c_ubyte)  
LPTSTR  = POINTER(c_char)  
HANDLE  = c_void_p  
BYTE = c_ubyte
CHAR = c_char
PVOID = c_void_p
ULONG_PTR = POINTER(c_ulong)
LPVOID    = c_void_p
UINT_PTR  = c_ulong
SIZE_T    = c_ulong
DWORD64 = c_uint64
LPSTR = POINTER(CHAR)
LPBYTE = POINTER(BYTE)


THREAD_ALL_ACCESS              = 0x001F03FF
TH32CS_SNAPHEAPLIST = 0x00000001
TH32CS_SNAPPROCESS  = 0x00000002
TH32CS_SNAPTHREAD   = 0x00000004
TH32CS_SNAPMODULE   = 0x00000008
TH32CS_INHERIT      = 0x80000000
TH32CS_SNAPALL      = (TH32CS_SNAPHEAPLIST | TH32CS_SNAPPROCESS | TH32CS_SNAPTHREAD | TH32CS_SNAPMODULE)
#常量  
DEBUG_PROCESS      = 0x00000001  
CREATE_NEW_CONSOLE = 0x00000010 
PROCESS_ALL_ACCESS = 0X001F0FFF
DBG_CONTINUE       = 0X00010002 
INFINITE           = 0xFFFFFFFF

PAGE_NOACCESS                  = 0x00000001
PAGE_READONLY                  = 0x00000002
PAGE_READWRITE                 = 0x00000004
PAGE_WRITECOPY                 = 0x00000008
PAGE_EXECUTE                   = 0x00000010
PAGE_EXECUTE_READ              = 0x00000020
PAGE_EXECUTE_READWRITE         = 0x00000040
PAGE_EXECUTE_WRITECOPY         = 0x00000080
PAGE_GUARD                     = 0x00000100
PAGE_NOCACHE                   = 0x00000200
PAGE_WRITECOMBINE              = 0x00000400

CONTEXT_CONTROL                = 0x00010001
CONTEXT_FULL                   = 0x00010007
CONTEXT_DEBUG_REGISTERS        = 0x00010010

# debug exception codes.
EXCEPTION_ACCESS_VIOLATION     = 0xC0000005
EXCEPTION_BREAKPOINT           = 0x80000003
EXCEPTION_GUARD_PAGE           = 0x80000001
EXCEPTION_SINGLE_STEP          = 0x80000004


EXCEPTION_DEBUG_EVENT          = 0x00000001
CREATE_THREAD_DEBUG_EVENT      = 0x00000002
CREATE_PROCESS_DEBUG_EVENT     = 0x00000003
EXIT_THREAD_DEBUG_EVENT        = 0x00000004
EXIT_PROCESS_DEBUG_EVENT       = 0x00000005
LOAD_DLL_DEBUG_EVENT           = 0x00000006
UNLOAD_DLL_DEBUG_EVENT         = 0x00000007
OUTPUT_DEBUG_STRING_EVENT      = 0x00000008
RIP_EVENT                      = 0x00000009

# hw breakpoint conditions
HW_ACCESS                      = 0x00000003
HW_EXECUTE                     = 0x00000000
HW_WRITE                       = 0x00000001
  
class MEMORY_BASIC_INFORMATION(Structure):
    _fields_ = [
        ("BaseAddress", PVOID),
        ("AllocationBase", PVOID),
        ("AllocationProtect", DWORD),
        ("RegionSize", SIZE_T),
        ("State", DWORD),
        ("Protect", DWORD),
        ("Type", DWORD),
]  
  
#CreateProcessA()函数的结构,(用于设置创建子进程的各种属性)  
class STARTUPINFO(Structure):  
    _fields_ = [
        ("cb",  DWORD),  
        ("lpReserved",  LPTSTR),  
        ("lpDesktop",   LPTSTR),  
        ("lpTitle", LPTSTR),  
        ("dwX", DWORD),  
        ("dwY", DWORD),  
        ("dwXSize", DWORD),  
        ("dwYSize", DWORD),  
        ("dwXCountChars",   DWORD),  
        ("dwYCountChars",   DWORD),  
        ("dwFillAttribute", DWORD),  
        ("dwFlags", DWORD),  
        ("wShowWindow", WORD),  
        ("cbReserved2", WORD),  
        ("lpReserved2", LPTSTR),  
        ("hStdInput",   DWORD),  
        ("hStdOutput",  DWORD),  
        ("hStdError",   DWORD),
    ]  
  
#进程的信息：进程线程的句柄，进程线程的id    
class PROCESS_INFORMATION(Structure):  
    _fields_ = [  
        ("hProcess",    HANDLE),  
        ("hThread",     HANDLE),  
        ("dwProcessId", DWORD),  
        ("dwThreadId",  DWORD),  
    ]

    
class EXCEPTION_RECORD(Structure):
    pass
    
EXCEPTION_RECORD._fields_ = [
        ("ExceptionCode",        DWORD),
        ("ExceptionFlags",       DWORD),
        ("ExceptionRecord",      POINTER(EXCEPTION_RECORD)),
        ("ExceptionAddress",     PVOID),
        ("NumberParameters",     DWORD),
        ("ExceptionInformation", UINT_PTR * 15),
    ]
    
    
#该联合体实际上包含许多成员，但我们的调试器只需要用到EXCEPTION_DEBUG_INFO一个就足够了。

class EXCEPTION_DEBUG_INFO(Structure):
    _fields_ = [
        ("ExceptionRecord", EXCEPTION_RECORD),
        ("dwFirstChance", DWORD)
    ]
    
class _CREATE_THREAD_DEBUG_INFO(Structure):
    pass

# macos compatability.
try:
    PTHREAD_START_ROUTINE = WINFUNCTYPE(DWORD, c_void_p)
except:
    PTHREAD_START_ROUTINE = CFUNCTYPE(DWORD, c_void_p)

LPTHREAD_START_ROUTINE = PTHREAD_START_ROUTINE
_CREATE_THREAD_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 645
    ('hThread', HANDLE),
    ('lpThreadLocalBase', LPVOID),
    ('lpStartAddress', LPTHREAD_START_ROUTINE),
]
assert sizeof(_CREATE_THREAD_DEBUG_INFO) == 12, sizeof(_CREATE_THREAD_DEBUG_INFO)
assert alignment(_CREATE_THREAD_DEBUG_INFO) == 4, alignment(_CREATE_THREAD_DEBUG_INFO)
CREATE_THREAD_DEBUG_INFO = _CREATE_THREAD_DEBUG_INFO    


class _CREATE_PROCESS_DEBUG_INFO(Structure):
    pass
_CREATE_PROCESS_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 651
    ('hFile', HANDLE),
    ('hProcess', HANDLE),
    ('hThread', HANDLE),
    ('lpBaseOfImage', LPVOID),
    ('dwDebugInfoFileOffset', DWORD),
    ('nDebugInfoSize', DWORD),
    ('lpThreadLocalBase', LPVOID),
    ('lpStartAddress', LPTHREAD_START_ROUTINE),
    ('lpImageName', LPVOID),
    ('fUnicode', WORD),
]
assert sizeof(_CREATE_PROCESS_DEBUG_INFO) == 40, sizeof(_CREATE_PROCESS_DEBUG_INFO)
assert alignment(_CREATE_PROCESS_DEBUG_INFO) == 4, alignment(_CREATE_PROCESS_DEBUG_INFO)
CREATE_PROCESS_DEBUG_INFO = _CREATE_PROCESS_DEBUG_INFO

class _EXIT_THREAD_DEBUG_INFO(Structure):
    pass
_EXIT_THREAD_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 664
    ('dwExitCode', DWORD),
]
assert sizeof(_EXIT_THREAD_DEBUG_INFO) == 4, sizeof(_EXIT_THREAD_DEBUG_INFO)
assert alignment(_EXIT_THREAD_DEBUG_INFO) == 4, alignment(_EXIT_THREAD_DEBUG_INFO)
EXIT_THREAD_DEBUG_INFO = _EXIT_THREAD_DEBUG_INFO


class _EXIT_PROCESS_DEBUG_INFO(Structure):
    pass
_EXIT_PROCESS_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 668
    ('dwExitCode', DWORD),
]
assert sizeof(_EXIT_PROCESS_DEBUG_INFO) == 4, sizeof(_EXIT_PROCESS_DEBUG_INFO)
assert alignment(_EXIT_PROCESS_DEBUG_INFO) == 4, alignment(_EXIT_PROCESS_DEBUG_INFO)
EXIT_PROCESS_DEBUG_INFO = _EXIT_PROCESS_DEBUG_INFO
# C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 672
class _LOAD_DLL_DEBUG_INFO(Structure):
    pass
_LOAD_DLL_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 672
    ('hFile', HANDLE),
    ('lpBaseOfDll', LPVOID),
    ('dwDebugInfoFileOffset', DWORD),
    ('nDebugInfoSize', DWORD),
    ('lpImageName', LPVOID),
    ('fUnicode', WORD),
]
assert sizeof(_LOAD_DLL_DEBUG_INFO) == 24, sizeof(_LOAD_DLL_DEBUG_INFO)
assert alignment(_LOAD_DLL_DEBUG_INFO) == 4, alignment(_LOAD_DLL_DEBUG_INFO)
LOAD_DLL_DEBUG_INFO = _LOAD_DLL_DEBUG_INFO
# C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 681
class _UNLOAD_DLL_DEBUG_INFO(Structure):
    pass
_UNLOAD_DLL_DEBUG_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 681
    ('lpBaseOfDll', LPVOID),
]
assert sizeof(_UNLOAD_DLL_DEBUG_INFO) == 4, sizeof(_UNLOAD_DLL_DEBUG_INFO)
assert alignment(_UNLOAD_DLL_DEBUG_INFO) == 4, alignment(_UNLOAD_DLL_DEBUG_INFO)
UNLOAD_DLL_DEBUG_INFO = _UNLOAD_DLL_DEBUG_INFO
# C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 685
class _OUTPUT_DEBUG_STRING_INFO(Structure):
    pass
_OUTPUT_DEBUG_STRING_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 685
    ('lpDebugStringData', LPSTR),
    ('fUnicode', WORD),
    ('nDebugStringLength', WORD),
]
assert sizeof(_OUTPUT_DEBUG_STRING_INFO) == 8, sizeof(_OUTPUT_DEBUG_STRING_INFO)
assert alignment(_OUTPUT_DEBUG_STRING_INFO) == 4, alignment(_OUTPUT_DEBUG_STRING_INFO)
OUTPUT_DEBUG_STRING_INFO = _OUTPUT_DEBUG_STRING_INFO
# C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 691
class _RIP_INFO(Structure):
    pass
_RIP_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 691
    ('dwError', DWORD),
    ('dwType', DWORD),
]
assert sizeof(_RIP_INFO) == 8, sizeof(_RIP_INFO)
assert alignment(_RIP_INFO) == 4, alignment(_RIP_INFO)
RIP_INFO = _RIP_INFO
    
 #该结构体需要用到联合体_DEBUG_EVENT_UNION,我们也把它映射进来：
class _DEBUG_EVENT_UNION(Union):
    _fields_ = [
        ("Exception", EXCEPTION_DEBUG_INFO),
        ('CreateThread', CREATE_THREAD_DEBUG_INFO),
        ('CreateProcessInfo', CREATE_PROCESS_DEBUG_INFO),
        ('ExitThread', EXIT_THREAD_DEBUG_INFO),
        ('ExitProcess', EXIT_PROCESS_DEBUG_INFO),
        ('LoadDll', LOAD_DLL_DEBUG_INFO),
        ('UnloadDll', UNLOAD_DLL_DEBUG_INFO),
        ('DebugString', OUTPUT_DEBUG_STRING_INFO),
        ('RipInfo', RIP_INFO),
 
    ]


    


#调用WaitForDebugEvent需要用DEBUG_EVENT结构体来保存调试事件信息，我们把它映射进来：
class DEBUG_EVENT(Structure):
    _fields_ = [
        ("dwDebugEventCode", DWORD),
        ("dwProcessId", DWORD),
        ("dwThreadId", DWORD),
        ("u",_DEBUG_EVENT_UNION)
    ]
#EXCEPTION_DEBUG_EVENT = _DEBUG_EVENT_UNION.Exception
    
#保存线程信息结构体
class THREADENTRY32(Structure):
    _fields_ = [
        ("dwSize",             DWORD),
        ("cntUsage",           DWORD),
        ("th32ThreadID",       DWORD),
        ("th32OwnerProcessID", DWORD),
        ("tpBasePri",          DWORD),
        ("tpDeltaPri",         DWORD),
        ("dwFlags",            DWORD),
]
 
TH32CS_SNAPTHREAD   = 0x00000004
class _FLOATING_SAVE_AREA(Structure):
    pass
_FLOATING_SAVE_AREA._fields_ = [
    # C:/PROGRA~1/gccxml/bin/Vc6/Include/winnt.h 1539
    ('ControlWord', DWORD),
    ('StatusWord', DWORD),
    ('TagWord', DWORD),
    ('ErrorOffset', DWORD),
    ('ErrorSelector', DWORD),
    ('DataOffset', DWORD),
    ('DataSelector', DWORD),
    ('RegisterArea', BYTE * 80),
    ('Cr0NpxState', DWORD),
]
assert sizeof(_FLOATING_SAVE_AREA) == 112, sizeof(_FLOATING_SAVE_AREA)
assert alignment(_FLOATING_SAVE_AREA) == 4, alignment(_FLOATING_SAVE_AREA)
FLOATING_SAVE_AREA = _FLOATING_SAVE_AREA


class _CONTEXT(Structure):
    pass
CONTEXT = _CONTEXT
_CONTEXT._fields_ = [
    # C:/PROGRA~1/gccxml/bin/Vc6/Include/winnt.h 1563
    ('ContextFlags', DWORD),
    ('Dr0', DWORD),
    ('Dr1', DWORD),
    ('Dr2', DWORD),
    ('Dr3', DWORD),
    ('Dr6', DWORD),
    ('Dr7', DWORD),
    ('FloatSave', FLOATING_SAVE_AREA),
    ('SegGs', DWORD),
    ('SegFs', DWORD),
    ('SegEs', DWORD),
    ('SegDs', DWORD),
    ('Edi', DWORD),
    ('Esi', DWORD),
    ('Ebx', DWORD),
    ('Edx', DWORD),
    ('Ecx', DWORD),
    ('Eax', DWORD),
    ('Ebp', DWORD),
    ('Eip', DWORD),
    ('SegCs', DWORD),
    ('EFlags', DWORD),
    ('Esp', DWORD),
    ('SegSs', DWORD),
    ('ExtendedRegisters', BYTE * 512),
]


#系统内存信息，内存页大小
class N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E(Structure):
    pass
N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 500
    ('wProcessorArchitecture', WORD),
    ('wReserved', WORD),
]
assert sizeof(N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E) == 4, sizeof(N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E)
assert alignment(N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E) == 2, alignment(N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E)

class N12_SYSTEM_INFO4DOLLAR_37E(Structure):
    pass
N12_SYSTEM_INFO4DOLLAR_37E._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 498
    ('dwOemId', DWORD),
    # Unnamed field renamed to '_'
    ('_', N12_SYSTEM_INFO4DOLLAR_374DOLLAR_38E),
]
class _SYSTEM_INFO(Structure):
    pass
_SYSTEM_INFO._fields_ = [
    # C:/PROGRA~1/MICROS~2/VC98/Include/winbase.h 497
    # Unnamed field renamed to '_'
    ('_', N12_SYSTEM_INFO4DOLLAR_37E),
    ('dwPageSize', DWORD),
    ('lpMinimumApplicationAddress', LPVOID),
    ('lpMaximumApplicationAddress', LPVOID),
    ('dwActiveProcessorMask', DWORD),
    ('dwNumberOfProcessors', DWORD),
    ('dwProcessorType', DWORD),
    ('dwAllocationGranularity', DWORD),
    ('wProcessorLevel', WORD),
    ('wProcessorRevision', WORD),
]

CHAR = c_char
LPSTR = POINTER(CHAR)
LPBYTE = POINTER(BYTE)

SYSTEM_INFO = _SYSTEM_INFO

#内存页基址信息

PVOID = c_void_p
UINT_PTR = c_ulong
SIZE_T = UINT_PTR
class _MEMORY_BASIC_INFORMATION(Structure):
    pass
_MEMORY_BASIC_INFORMATION._fields_ = [
    # C:/PROGRA~1/gccxml/bin/Vc6/Include/winnt.h 4534
    ('BaseAddress', PVOID),
    ('AllocationBase', PVOID),
    ('AllocationProtect', DWORD),
    ('RegionSize', SIZE_T),
    ('State', DWORD),
    ('Protect', DWORD),
    ('Type', DWORD),
]
assert sizeof(_MEMORY_BASIC_INFORMATION) == 28, sizeof(_MEMORY_BASIC_INFORMATION)
assert alignment(_MEMORY_BASIC_INFORMATION) == 4, alignment(_MEMORY_BASIC_INFORMATION)

MEMORY_BASIC_INFORMATION = _MEMORY_BASIC_INFORMATION