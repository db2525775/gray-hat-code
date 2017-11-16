# -*- coding: utf-8 -*-  
# @Date    : 2016-08-11 16:48:16  
# @Author  : giantbranch (giantbranch@gmail.com)  
# @Link    : http://blog.csdn.net/u012763794?viewmode=contents  
  
from ctypes import *  
from my_debugger_defines import *  
kernel32 = windll.kernel32  
class debugger():  
      
    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debuger_active = False
        self.breakpoints = {}
        self.h_thread = None
        self.context = None
        self.exception =None
        self.exception_address = None
        self.first_breakpoint = True
        self.hardware_breakpoints = {}
        system_info = SYSTEM_INFO()
        kernel32.GetSystemInfo(byref(system_info))
        self.page_size = system_info.dwPageSize
        self.guarded_pages = []
        self.memory_breakpoints ={}
        
        
    def open_process(self,pid):
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
        return  h_process
        
    def attach(self,pid):
        self.h_process = self.open_process(pid)
        a=kernel32.DebugActiveProcess(pid)
        print(a)
        if a:
            
            self.debuger_active = True
            self.pid = pid
            #self.run()
        else:
            print("[*]Unable to attach to the process")
    def run(self):
        while self.debuger_active == True:
            self.get_debug_event()
            
    def exception_handler_breakpoint(self):
        print("*[*] Inside the breakpoint handler.")
        print("Exception address:0x%08x"%self.exception_address)
        return DBG_CONTINUE
        
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event),INFINITE):
            #print("attached!")
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(self.h_thread)
            print("Event Code:%d Thread ID:%d"%(debug_event.dwDebugEventCode,debug_event.dwThreadId))
            #input("input any word gono!")
        if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
            self.exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
            self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
            
        if self.exception == EXCEPTION_ACCESS_VIOLATION:
            print("Access Vlolation Deteced.")
        elif self.exception == EXCEPTION_BREAKPOINT:
            continue_status = self.exception_handler_breakpoint()
        elif self.exception == EXCEPTION_GUARD_PAGE:
            print("Guard Page Access Detected.")
        elif self.exception == EXCEPTION_SINGLE_STEP:
            self.exception_handler_single_step()
            #print("*Single stepping.")
            
                        
        kernel32.ContinueDebugEvent(debug_event.dwProcessId,debug_event.dwThreadId,continue_status)
            
    def detach(self):
        if kernel32.DebugActiveProcessStop(self.pid):
            print("[*]Finished debuging.Exiting...")
        else:
            print("There was an error")
            return False
    def read_process_memory(self,address,length):
        data=""
        read_buf = create_string_buffer(length)
        count = c_ulong(0)
        if not kernel32.ReadProcessMemory(self.h_process,
                                        address,
                                        read_buf,
                                        length,
                                        byref(count)):
            return False
        else:
            data+=read_buf.raw
            return data
            
    def write_process_memory(self,address,data):
        count = c_ulong(0)  
        length = len(data)  
        c_data = c_char_p(data[count.value:])  
        if not kernel32.WriteProcessMemory(self.h_process, address, c_data, length, byref(count)):  
            return False  
        else:  
            return True  
    def bp_set(self, address,handle=None):  
        # 看看断点的字典里是不是已经存在这个断点的地址了  
        if not self.breakpoints.has_key(address):  
            try:  
                # 先读取原来的一个字节，保存后再写入0xCC  
                original_byte = self.read_process_memory(address, 1)  #读取目标地址的一个字节
                self.write_process_memory(address, '\xCC')  #保存int3到读取的那个地址
                self.breakpoints[address] = (address, original_byte)  #保存断点地址
                print("already set breakpoint at address 0x%08x source data 0x%x"%(address,int(ord(original_byte))))
            except:  
                return False  
        return True  
        
    def func_resolve(self, dll, function):  #查找库函数地址
        handle = kernel32.GetModuleHandleA(dll)  
        address = kernel32.GetProcAddress(handle, function)  
        kernel32.CloseHandle(handle)  
        return address  
    def open_thread(self, thread_id):  #打开一个线程，类似开启一个进程。返回一个线程句柄
        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)  
        if h_thread is not None:  
            return h_thread  
        else:  
            print ("[*] Could not obtain a valid thread handle.")
            return False 
    def enumerate_threads(self):  #枚举线程列表
        thread_entry = THREADENTRY32()  
        thread_list = []  
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, self.pid)  #返回一个指向快照的句柄，可以获取线程列表，
        if snapshot is not None:  #如果快照不为空获取快照
            thread_entry.dwSize = sizeof(thread_entry)  
            success = kernel32.Thread32First(snapshot,  byref(thread_entry))  #获取第一个线程
            while success:  
                if thread_entry.th32OwnerProcessID == self.pid:  
                    thread_list.append(thread_entry.th32ThreadID)  
                success = kernel32.Thread32Next(snapshot, byref(thread_entry)) #获取下一个线程
  
            kernel32.CloseHandle(snapshot)  #关闭线程快照句柄
            return thread_list  #返回线程列表
        else:  
            print ("enumerate_threads fail.") 
            return False  
            
    def get_thread_context(self, thread_id):  #获取线程内容
        context = CONTEXT()  #线程内容结构体
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS  
        h_thread = self.open_thread(thread_id)  
        if kernel32.GetThreadContext(h_thread, byref(context)):  #获取线程内容
            kernel32.CloseHandle(h_thread)  #关闭句柄
            return context  
        else:  
            print ("get_thread_context fail.")  
            return False
    
    def load(self, path_to_exe):  
        print("open %s start debug"%path_to_exe)
        creation_flags = DEBUG_PROCESS  
        startupinfo = STARTUPINFO()  
        process_information = PROCESS_INFORMATION()  
        startupinfo.dwFlags = 0x1  
        startupinfo.wShowWindow = 0x0  
        startupinfo.cb = sizeof(startupinfo)  
        if kernel32.CreateProcessA(path_to_exe,
                                    None, 
                                    None,  
                                    None,   
                                    None,                                    
                                    creation_flags,   
                                    None,
                                    None,  
                                    byref(startupinfo),  
                                    byref(process_information)):  
            print ("[*] we have successfully launched the process!")  
            print ("[*] PID:%d" %process_information.dwProcessId)
        else:                                                      
            print ("[*] Error:0x%08x."%kernel32.GetLastError())
            
    def bp_set_hw(self,address,length,condition):
        #检查硬件断点的长度是否有效
        if length not in (1,2,4):
            return False
        else:
            length -=1
        #检测硬件断点触发条件是否有效
        
        if condition not in (HW_ACCESS,HW_EXECUTE,HW_WRITE):
            return False
        #检测是否存在空置的调试寄存器槽
        available = None
        #for slot in xrange(4):
        #    if context.Dr7 & (1 << (slot * 2)) == 0:
        #        available = slot
        #        break
        for thread_id in self.enumerate_threads():
            if not self.hardware_breakpoints.has_key(0):
                available = 0
            if not self.hardware_breakpoints.has_key(1):
                available = 1
            if not self.hardware_breakpoints.has_key(2):
                available = 2
            if not self.hardware_breakpoints.has_key(3):
                available = 3
            else:
                return False
        
        
        
        
            context = self.get_thread_context(thread_id=thread_id)
            #通过设置DR7中相应的标志位激活断点
            context.Dr7 |= 1 << (available*2)
            #在空置的寄存器中写入我们的断点
            if available == 0:
                context.Dr0 = address
                
            elif available == 1:
                context.Dr1 = address
            elif available == 2:
                context.Dr2 = address
            elif available == 3:
                context.Dr3 = address
            #设置断点触发条件
            context.Dr7 |= condition <<((available * 4)+16)
            #设置硬件断点的长度
            context.Dr7 |= length <<((available *4 )+18)
            #提交经改动后的线程上下文环境信息
            h_thread = self.open_thread(thread_id)
            print("beafor SET HW BP:Dr3=0x%08x Dr7=0x%08x"%(context.Dr3,context.Dr7))
            print("beafor SET HW BP:Dr2=0x%08x Dr7=0x%08x"%(context.Dr2,context.Dr7))
            print("beafor SET HW BP:Dr1=0x%08x Dr7=0x%08x"%(context.Dr1,context.Dr7))
            print("beafor SET HW BP:Dr0=0x%08x Dr7=0x%08x"%(context.Dr0,context.Dr7))
            kernel32.SetThreadContext(h_thread,byref(context))
            print("after SET HW BP:Dr3=0x%08x Dr7=0x%08x"%(context.Dr3,context.Dr7))
            print("after SET HW BP:Dr2=0x%08x Dr7=0x%08x"%(context.Dr2,context.Dr7))
            print("after SET HW BP:Dr1=0x%08x Dr7=0x%08x"%(context.Dr1,context.Dr7))
            print("after SET HW BP:Dr0=0x%08x Dr7=0x%08x"%(context.Dr0,context.Dr7))
            #更新内部的断点列表
            self.hardware_breakpoints[available] = (address,length,condition)
        return True
            
    def exception_handler_single_step(self):
        #判断这个单步事件是否由一个硬件断点所触发，若是则捕获这个断点事件
        #根据Intel给出的文档，我们应当能够通过检测Dr6寄存器上的BS标志位来判断出
        #这个单步事件的触发原因，然而windows系统似乎并没有正确的将这个标志位传递给我们
        #print(self.context.Dr6)
        '''
        if self.context.Dr6 & 0x1 and self.hardware_breakpoints.has_key(0):
            slot = 0
        elif self.context.Dr6 & 0x2 and self.hardware_breakpoints.has_key(1):
            slot = 1
        elif self.context.Dr6 & 0x4 and self.hardware_breakpoints.has_key(2):
            slot = 2
        elif self.context.Dr6 & 0x8 and self.hardware_breakpoints.has_key(3):
            slot = 3
        else:
            #这个INIT1中断并非由一个硬件断点所引发
             continue_status = DBG_CONTINUE
        '''
        if self.hardware_breakpoints.has_key(0):
            slot = 0
        elif self.hardware_breakpoints.has_key(1):
            slot = 1
        elif self.hardware_breakpoints.has_key(2):
            slot = 2
        elif self.hardware_breakpoints.has_key(3):
            slot = 3
        else:
            #这个INIT1中断并非由一个硬件断点所引发
             continue_status = DBG_CONTINUE
        #从断点列表中移除这个断点
        if self.bp_del_hw(slot):
            continue_status = DBG_CONTINUE
        print("[*]Hardware breakpoint removed.")
        return continue_status
        
        
    def bp_del_hw(self,slot):
        for thread_id in self.enumerate_threads():
            context = self.get_thread_context(thread_id=thread_id)
            #通过重置标志位来移除这个硬件断点
            context.Dr7 &=~(1<<(slot*2))
            
            #将断点地址清零
            if slot == 0:
                context.Dr0 = 0x00000000
            if slot == 1:
                context.Dr1 = 0x00000000
            if slot == 2:
                context.Dr2 = 0x00000000
            if slot == 3:
                context.Dr3 = 0x00000000     
            #清空断点触发条件标志位
            context.Dr7 &=~(3<<((slot*4)+16))
            #清空断点触发长度标志位
            context.Dr7 &=~(3<<((slot*4)+18)) 
            #提交移除断点的线程上下文环境信息
            h_thread = self.open_thread(thread_id)
            kernel32.SetThreadContext(h_thread,byref(context))  
            #将断点从内部的断点列表移除
            del self.hardware_breakpoints[slot]
            return True            
                          
    #设置内存断点
    def bp_set_mem(self,address,size):
        #内存页基址信息结构
        mbi = MEMORY_BASIC_INFORMATION()
        #若函数调用未返回一个完整的MEMORY_BASIC_INFOMATION结构体。
        #则返回false
        if kernel32.VirtualQueryEx(self.h_process,
                                   address,
                                   byref(mbi),
                                   sizeof(mbi)) < sizeof(mbi):
            return False
        #获取基址
        current_page = mbi.BaseAddress
        #我们将对整个内存断点区域所覆盖到的所有内存页设置权限
        while current_page <= address + size:
            #将这个内存页记录在列表中，以便我们将这些保护
            #页与由操作系统或debugee进程自设的保护页区分开来
            self.guarded_pages.append(current_page)
            old_protection = c_ulong(0)
            if not kernel32.VirtualProtectEx(self.h_process,
                                             current_page,size,
                mbi.Protect | PAGE_GUARD,byref(old_protection)):
                return False
            #以系统所设置的内存页尺寸作为步长单位，
            #递增我们的内存断点区域
            current_page+=self.page_size
        self.memory_breakpoints[address] = (address,size,mbi)
        return True
        
