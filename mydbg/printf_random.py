# -*- coding: utf-8 -*-  
# @Date    : 2017-11-15 11:00  
# @Author  : dengbo (db2525775@gmail.com)  
# @Link    :   

from mydbg import *
import struct
import random

#�Զ���һ���ص�����
def printf_randomizer(dbg):
    #�Ӻ���ջ�ϣ�ESP+0X8����ȡһ��˫�ִ�С����ֵ�����ֵ���Ǽ�������ֵ
    parameter_addr = dbg.context.Esp + 0x8
    counter        = dbg.read_process_memory(parameter_addr,4)
    
    #������ʹ��read_process_memory����ʱ�����õ��ķ���ֵ������һ��
    #������Ķ������ַ�����������ʹ���������֮ǰ�����ȶ�����н������
    counter = struct.unpack("L",counter)[0]
    print("Counter:%d"%int(counter))
    #����һ�������������������ֵ����ɶ����Ƹ�ʽ����
    #�������ܽ�����ȷ��д����̵��ڴ��ַ��
    random_counter = random.randint(1,100)
    random_counter = struct.pack("L",random_counter)[0]
    #���ڻ������ǵ���������ָ����̵�ִ��״̬
    dbg.write_process_memory(parameter_addr,random_counter)
    return DBG_CONTINUE
    
dbg = debugger()
pid = input("Enter the print_loop.py PID:")
#�����������ӵ����������
dbg.attach(int(pid))

#���öϵ㲢��printf_randomizer������Ϊ�ϵ�ص����������ж�����
printf_address = dbg.func_resolve("msvcrt","printf")
dbg.bp_set(printf_address,description="print_address",handler=printf_randomizer)
dbg.run()