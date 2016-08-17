#coding=utf-8
from bitarray import bitarray

def bit_encript(text,passwd,block_size):
    text_length=len(text)
    passwd_length=len(passwd)
    encripted_text=bitarray(text_length)
#     encripted_text=text_length * bitarray('0')
    index=0
    left_index=0 #start_with
    right_index=text_length-1 #end_with
    pass_index=0
    
#     print text
    while True :
        #print index,left_index,right_index
        if passwd[pass_index] :
            #put it on left
            temp_index=left_index
            temp_index_start=temp_index
            while temp_index<=right_index and temp_index<=left_index+block_size-1 :
#                 print "LEFT",temp_index
                encripted_text[temp_index]=not(passwd[pass_index+1] ^ text[index+temp_index-temp_index_start])
                temp_index+=1
            left_index+=block_size
        else :
            #put it on right
            if right_index-block_size+1 > left_index : #if is last one
                temp_index=right_index-block_size+1 
            else :
                temp_index=left_index
            temp_index_start=temp_index
            
            while temp_index<=right_index :
#                 print "right",temp_index
                encripted_text[temp_index]=not(passwd[pass_index+1] ^ text[index+temp_index-temp_index_start])
                temp_index+=1
            right_index-=block_size
        index+=block_size
        pass_index+=2
        if pass_index>passwd_length-1:
            pass_index=0
        #print(encripted_text)
        #end
        if index >= text_length :
            return encripted_text


def bit_decript(encripted_text,passwd,block_size):
    text_length=len(encripted_text)
    passwd_length=len(passwd)
#     print "pass_len=",passwd_length 

    
#     text=bitarray(text_length)
    text=text_length * bitarray('0')
    
    #how many bit left
    leave_num=text_length % block_size
    if block_size> text_length:
        leave_num=text_length
    
    #encripted_text_index
    move_times=text_length/block_size+(leave_num and True)
#     print "text_length/block_size+(leave_num and True)",text_length,block_size
    
    #how many times move leave
    leave_times=0 
    if passwd_length/2*block_size <= text_length:
        leave_times=((text_length-leave_num)%(passwd_length/2*block_size))/block_size+(leave_num and True)
    
#     if leave_num :
#         leave_times+=1
        
    
    if passwd_length/2*block_size > text_length:
        leave_times=text_length / block_size +(leave_num and True)
        if leave_times==0:#if block size >text_length
            leave_times=1
    passwd_index=passwd_length-2
    if leave_times:
        passwd_index=(leave_times-1)*2
    
#     print "passwd index=",passwd_index
#     exit(0)
    left_times_once=0 #
    for temp in range(0,passwd_length/2 ):
        if passwd[temp*2] :
            left_times_once+=1
    left_times_complety_part=0
    if left_times_once :
        if move_times-leave_times>0 :
            left_times_complety_part=(move_times-leave_times)/(passwd_length/2)*left_times_once
#     print "left_times_complety_part=",left_times_complety_part, leave_times,left_times_once
#     print "move_times-leave_times",move_times,leave_times
#     exit(0)
    left_times_leave_part=0
    for temp in range(0,leave_times):
        if(passwd[temp*2]):
            left_times_leave_part+=1
    left_times=left_times_complety_part+left_times_leave_part
#     print 'left_times=',left_times,left_times_complety_part,left_times_leave_part
#     print "move_times=",move_times,leave_times
   
    encripted_text_index=(left_times-1+(not passwd[passwd_index] and True))*block_size
   
#     print "encripted_text_index=",encripted_text_index
#     print "leave_num=",leave_num
        
    left_index=encripted_text_index
    right_index=encripted_text_index+leave_num+(not(leave_num and True))*block_size-1
#     print "left ,right =",left_index,right_index
########### get last move back start ###########################################       
    text_index=text_length-leave_num-(not(leave_num and True))*block_size
    temp_index=left_index
    temp_index_start=temp_index
    while temp_index<left_index+block_size and temp_index<=right_index:
#         print " temp_index=",temp_index
        text[text_index+temp_index-temp_index_start]=not(passwd[passwd_index+1] ^encripted_text[temp_index])
        temp_index+=1
        
    left_index-=block_size
    right_index+=block_size
    
    passwd_index-=2
    if passwd_index<0:
        passwd_index=passwd_length-2
        
    text_index-=block_size
########### get last move back end ########################################### 
    
    while text_index>-1:
#         print "text_index=",text_index,"##",text,passwd_index
#         print "l,r=",left_index,right_index;
        if passwd[passwd_index]:
            ##left
            temp_index=left_index
            temp_index_start=temp_index
#             print"################"
            while temp_index<left_index+block_size and left_index<=right_index:
#                 print "left temp_index=",temp_index
                text[text_index+temp_index-temp_index_start]=not(passwd[passwd_index+1] ^encripted_text[temp_index])
                temp_index+=1
            left_index-=block_size
                                                    
        else :
            ##right
            temp_index=right_index-block_size+1
            temp_index_start=temp_index
#             print"################"
            while temp_index<=right_index and right_index<text_length:
#                 print "right temp_index=",temp_index
                text[text_index+temp_index-temp_index_start]=not(passwd[passwd_index+1] ^encripted_text[temp_index])
                temp_index+=1
            right_index+=block_size
        
        passwd_index-=2
        if passwd_index<0:
            passwd_index=passwd_length-2    
        
        text_index-=block_size
        
    return text

def turn_around (text):
    text_length=len(text)
    new_text=bitarray(text_length)
    index=0
    while index <text_length/2:
        new_text[index]=text[text_length/2-1-index]
        index+=1
    while index <text_length:
        new_text[index]=text[text_length-1-index+text_length/2]
        index+=1
    return new_text

def blender_encript(text,passwd,block_size_list):

    for block_size in block_size_list:
        text=bit_encript(text,passwd,block_size)
#         print text
        text=turn_around(text)
    return text
def blender_decript(text,passwd,block_size_list):

    block_size_list.reverse()# 反转
    for block_size in block_size_list:
        text=turn_around(text)
        text=bit_decript(text,passwd,block_size)
#         print "miwen",text,block_size
    return text    

      
temp=bitarray()
temp.frombytes("123")
passwd=temp
 
 
temp=bitarray()
text =temp.frombytes("卧槽")
text =temp


block_size_list=[1,2,3,7,3,4]
 
print "encript",text,passwd
encripted_text=blender_encript(text,passwd,block_size_list)
i=1
while i<1000:
    i+=1
    text=blender_encript(text,passwd,block_size_list)
    print text,i
#   
print "######################################## decript",encripted_text,passwd
print blender_decript(encripted_text, passwd,block_size_list).tobytes()

