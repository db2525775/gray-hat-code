# -*- coding: utf-8 -*-  
# @Date    : 2017-11-15 11:00  
# @Author  : dengbo (db2525775@gmail.com)  
# @Link    :   

from mydbg import *
import struct
import random

#自定义一个回调函数
def printf_randomizer(dbg):
    #从函数栈上（ESP+0X8）读取一个双字大小的数值，这个值正是计数器的值
    parameter_addr = dbg.context.Esp + 0x8
    counter        = dbg.read_process_memory(parameter_addr,4)
    
    #当我们使用read_process_memory函数时，所得到的返回值类型是一个
    #打包过的二进制字符串。在我们使用这个数据之前必须先对其进行解包操作
    counter = struct.unpack("L",counter)[0]
    print("Counter:%d"%int(counter))
    #生成一个随机数并将这个随机数值打包成二进制格式串，
    #这样才能将其正确的写入进程的内存地址中
    random_counter = random.randint(1,100)
    random_counter = struct.pack("L",random_counter)[0]
    #现在换入我们的随机数并恢复进程的执行状态
    dbg.write_process_memory(parameter_addr,random_counter)
    return DBG_CONTINUE
    
dbg = debugger()
pid = input("Enter the print_loop.py PID:")
#将调试器附加到这个进程上
dbg.attach(int(pid))

#设置断点并以printf_randomizer函数作为断点回调函数处理中断事务
printf_address = dbg.func_resolve("msvcrt","printf")
dbg.bp_set(printf_address,description="print_address",handler=printf_randomizer)
dbg.run()