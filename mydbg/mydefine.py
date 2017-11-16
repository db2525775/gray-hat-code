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
  
#常量  
DEBUG_PROCESS = 0x00000001  
CREATE_NEW_CONSOLE = 0x00000010  
  
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
 
 
