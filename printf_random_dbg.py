# -*- coding: utf-8 -*-  
# @Date    : 2017-11-15 11:00  
# @Author  : dengbo (db2525775@gmail.com)  
# @Link    :   

from pydbg import *
from pydbg.pydbg import *
import struct
import random

#�Զ���һ���ص�����
def printf_randomizer(dbg):
    #�Ӻ���ջ�ϣ�ESP+0X4����ȡһ��˫�ִ�С��ָ�룬���ָ�����Ǽ�������ӡ�ַ����Ļ�ַ
    parameter_addr = dbg.context.Esp + 0x4
    parameter_addr = dbg.read_process_memory(parameter_addr,4)
    parameter_addr =  struct.unpack("L",parameter_addr)[0]
    #����������������ڵ��ڴ�δ֪
    parameter_addr = int(parameter_addr)+15
    #��ȡ��bytes���ڴ�ֵ������ֵ��
    counter        = dbg.read_process_memory(parameter_addr,2)
    

    #������ʹ��read_process_memory����ʱ�����õ��ķ���ֵ������һ��
    #������Ķ������ַ�����������ʹ���������֮ǰ�����ȶ�����н������
    counter        = struct.unpack("2s",counter)[0]
    print("Counter:%s"%counter)
    #����һ�������������������ֵ����ɶ����Ƹ�ʽ����
    #�������ܽ�����ȷ��д����̵��ڴ��ַ��
    random_counter = random.randint(1,100)
    print("random wirte in memroy :%s lenth:%d"%(random_counter,len(str(random_counter))))
    #�ַ���������ֵ
    random_counter=str(random_counter)
    if len(random_counter) == 2:
        random_counter = struct.pack("2s",random_counter)
        
    elif len(random_counter) == 1:
        random_counter = struct.pack("1s",random_counter)
    #���ڽ�Ŀ��������ֵ�������ǵ���������ָ����̵�ִ��״̬  
    dbg.write_process_memory(parameter_addr,random_counter,length=len(random_counter))
    return DBG_CONTINUE
    
dbg = pydbg()
pid = input("Enter the print_loop.py PID:")
#�����������ӵ����������
dbg.attach(int(pid))

#���öϵ㲢��printf_randomizer������Ϊ�ϵ�ص����������ж�����
printf_address = dbg.func_resolve("msvcrt","printf")
print("0x%08x"%printf_address)
dbg.bp_set(printf_address,description="print_address",handler=printf_randomizer)
dbg.run()