# -*- coding: utf-8 -*-  
# @Date    : 2016-08-12 14:18:10  
# @Author  : giantbranch (giantbranch@gmail.com)  
# @Link    : http://blog.csdn.net/u012763794?viewmode=contents  
  
import my_debugger
import my_debugger_defines
debugger = my_debugger.debugger()  
#path_to_exe="C:\\Windows\\System32\\calc.exe"
#debugger.load(path_to_exe.encode())
pid =input("Enter the pid of the process to attach to:")
debugger.attach(pid)
address = debugger.func_resolve("msvcrt.dll", "printf")
#threadList = debugger.enumerate_threads()#枚举进程下的线程列表
#print(threadList)
print("0x%08x"%address)
'''
for thread in threadList:#遍历线程下的寄存器内容
    thread_context = debugger.get_thread_context(thread)
    print("[*]Dumping registers for thread ID:0x%08x"%thread)
    print("[**] EIP:0x%08x" % thread_context.Eip)  
    print("[**] ESP:0x%08x" % thread_context.Esp)  
    print("[**] EBP:0x%08x" % thread_context.Ebp)  
    print("[**] EAX:0x%08x" % thread_context.Eax)  
    print("[**] EBX:0x%08x" % thread_context.Ebx)  
    print("[**] ECX:0x%08x" % thread_context.Ecx)  
    print("[**] EDX:0x%08x" % thread_context.Edx)  
    print("[*] END DUMP" )
''' 
#print("0x%x"%int(ord(debugger.read_process_memory(address,1))))
#debugger.bp_set(address)
#debugger.bp_set_hw(address,1,my_debugger_defines.HW_EXECUTE)
debugger.bp_set_mem(address,4)
#print("0x%x"%int(ord(debugger.read_process_memory(address,1))))
debugger.run()
debugger.detach()