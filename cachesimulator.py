# File: cachesimulator.py
# Author(s): Senhe Hao
# Date: 12/08/2021
# Section: 507 
# E-mail(s): senhehao@tamu.edu
# Description: This is the project. The comments below will explain what each part of the code does.


import sys
import math
import random

RAM = []
CACHE = []
RECENTS = []
FREQUENTS = []
cache_size = 0
data_block_size = 0
associativity = 0
replacement_policy = 0
write_hit_policy = 0
write_miss_policy = 0
cache_hits = 0
cache_misses = 0

RAM_start = ""
RAM_end = ""


# function to flush the cache
def flush():
    global CACHE
    for i in range(int(cache_size/(data_block_size*associativity))):
        RECENTS[i].clear()
        for j in range(associativity):
            if CACHE[i][j][1] == '1':
                set_indexer = bin(i).zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[i][j][2],16))[2:] + set_indexer[2:] + offsets
                former_start = int(combination.zfill(8), 2)
                kk = 3
                for l in range(former_start, former_start+data_block_size):
                    RAM[l] = CACHE[i][j][kk]
                    kk += 1
            CACHE[i][j][0] = '0'
            CACHE[i][j][1] = '0'
            for k in range(2, int(data_block_size)+3):
                CACHE[i][j][k] = '00'
    print('cache_cleared')


def dump():
    f = open('cache.txt', 'w')
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            printed = ""
            for k in range(3, len(CACHE[i][j])):
                printed+=CACHE[i][j][k]
                printed+=' '
            f.write(printed)
            f.write('\n')
    f.close()

def mem_dump():
    f = open('ram.txt', 'w')
    for i in RAM:
        f.write(i)
        f.write('\n')
    f.close()


def view():
    print('cache_size:%d'%(cache_size))
    print('data_block_size:%d'%(data_block_size))
    print('associativity:%d'%(associativity))
    if replacement_policy == 1:
        print('replacement_policy:random_replacement')
    elif replacement_policy == 2:
        print('replacement_policy:least_recently_used')
    if write_hit_policy == 1:
        print('write_hit_policy:write_through')
    elif write_hit_policy == 2:
        print('write_hit_policy:write_back')
    if write_miss_policy == 1:
        print('write_miss_policy:write_allocate')
    elif write_miss_policy == 2:
        print('write_miss_policy:no_write_allocate')
    print('number_of_cache_hits:%d'%(cache_hits))
    print('number_of_cache_misses:%d'%(cache_misses))
    print('cache_content:')
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            printed = ""
            for k in range(len(CACHE[i][j])):
                printed+=CACHE[i][j][k]
                printed+=' '
            print(printed)

def mem_view():
    print("memory_size:%d"%len(RAM))
    print("memory_content:")
    print("address:data")
    counter = 0
    start = int(RAM_start[2:], base=16)
    for i in range(int(len(RAM)/8)):
        line = ""
        line += "0x" + hex(start + counter)[2:].zfill(2).upper()
        line += ":"
        for j in range(8):
            line += str(RAM[counter]) + " "
            counter += 1
        print(line)


# program will start with initializing the physical memory
def init_ram():
    filename = sys.argv[1]
    global RAM
    global RAM_start
    global RAM_end
    for i in range(256):
        RAM.append("00")
    # prompts the user for the file name and prints on to the screen
    print('*** Welcome to the cache simulator ***')
    print('initialize the RAM: ')
    inputer = input()
    inputer_list = inputer.split()
    RAM_start = inputer_list[1]
    RAM_end = inputer_list[2]
    # opens the file and reads the lines into the RAM
    RAM_temp = [] 
    with open(filename) as f:
        RAM_temp = f.readlines()
        RAM_temp = [i.strip('\n') for i in RAM_temp]
    for i in range(int(RAM_end[2:], 16)+1):
        RAM[i] = RAM_temp[i]
    print('RAM successfully initialized!')


# function to handle configuring the cache
def config():
    global CACHE
    global RAM
    global RECENTS
    global FREQUENTS
    global cache_size
    global data_block_size
    global associativity
    global replacement_policy
    global write_hit_policy
    global write_miss_policy
    print('configure the cache: ')
    while(True):
        cache_size = int(input('cache size: '))
        if cache_size >= 8 and cache_size <= 256:
            break
        else:
            print("Error, invalid cache size")
    data_block_size = int(input('data block size: '))
    while(True):
        associativity = int(input('associativity: '))
        if associativity == 1 or associativity == 2 or associativity == 4:
            break
        else:
            print("Error, invalid associativity")
    while(True):
        replacement_policy = int(input('replacement policy: '))
        if replacement_policy == 1 or replacement_policy == 2: 
            break
        else:
            print("Error, invalid replacement policy")
    while(True):
        write_hit_policy = int(input('write hit policy: '))
        if write_hit_policy == 1 or write_hit_policy == 2: 
            break
        else:
            print("Error, invalid write hit policy")
    while(True):
        write_miss_policy = int(input('write miss policy: '))
        if write_miss_policy == 1 or write_miss_policy == 2: 
            break
        else:
            print("Error, invalid write miss policy")
    for i in range(int(cache_size/(associativity*data_block_size))):
        CACHE.append([])
        RECENTS.append([])
        FREQUENTS.append([])
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            CACHE[i].append([])
            FREQUENTS[i].append(0)
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            CACHE[i][j].append('0')
            CACHE[i][j].append('0')
            CACHE[i][j].append('00')
            for k in range(int(data_block_size)):
                CACHE[i][j].append('00')
    print('cache successfully configured!')



#displays the prompt for simulating the cache
def prompt():
    print('*** Cache simulator menu ***')
    print('type one command:')
    print('1. cache-read')
    print('2. cache-write')
    print('3. cache-flush')
    print('4. cache-view')
    print('5. memory-view')
    print('6. cache-dump')
    print('7. memory-dump')
    print('8. quit')
    print('****************************')
    return input()

def read_write(address):
    global CACHE
    global RECENTS
    global RAM
    # gets the cache values again
    cache_address = bin(int(address[2:], 16))[2:].zfill(8)
    set_index_bits = int(math.log(len(CACHE), 2))
    block_offset_bits = int(math.log(len(CACHE[0][0]), 2))
    tag_bits = 8 - set_index_bits - block_offset_bits
    tag = cache_address[0:tag_bits]
    set_index = cache_address[tag_bits:(tag_bits+set_index_bits)]
    if set_index == '':
        set_index = '0'
    block_offset = cache_address[(tag_bits+set_index_bits):]
    # first checks for if the tag is there in the wanted block set
    complete = False
    for i in range(associativity):
        if CACHE[int(set_index, 2)][i][0] == '0':
            CACHE[int(set_index, 2)][i][0] = '1'
            CACHE[int(set_index, 2)][i][2] = hex(int(tag,2))[2:].zfill(2)
            complete = True
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][i][k+3] = RAM[j]
                k += 1
            print("hit:no")
            print("eviction_line:-1")
            print("ram_address:%s"%address)
            print("data:0x%s"%CACHE[int(set_index, 2)][i][int(block_offset, 2)+3])
            if not (i in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(i)
            else:
                RECENTS[int(set_index, 2)].remove(i)
                RECENTS[int(set_index, 2)].append(i)
            break
    # we failed to find an invalid part and now have to replace
    if not complete:
        if replacement_policy == 1:
            random_int = random.randint(0, associativity-1)
            if CACHE[int(set_index, 2)][random_int][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][random_int][2],16))[2:] + set_indexer[2:] + offsets
                former_start = int(combination.zfill(8), 2)
                kk = 3
                for j in range(former_start, former_start+data_block_size):
                    RAM[j] = CACHE[int(set_index, 2)][random_int][kk]
                    kk += 1
            CACHE[int(set_index, 2)][random_int][0] = '1'
            CACHE[int(set_index, 2)][random_int][1] = '0'
            CACHE[int(set_index, 2)][random_int][2] = hex(int(tag,2))[2:].zfill(2)
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][random_int][k+3] = RAM[j]
                k += 1
            print("hit:no")
            print("eviction_line:%d"%random_int)
            print("ram_address:%s"%address)
            print("data:0x%s"%CACHE[int(set_index, 2)][random_int][int(block_offset, 2)+3])
            if not (random_int in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(random_int)
            else:
                RECENTS[int(set_index, 2)].remove(random_int)
                RECENTS[int(set_index, 2)].append(random_int)
        elif replacement_policy == 2:
            to_be = RECENTS[int(set_index, 2)][0]
            if CACHE[int(set_index, 2)][to_be][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer[2:] + offsets
                former_start = int(combination.zfill(8), 2)
                kk = 3
                for j in range(former_start, former_start+data_block_size):
                    RAM[j] = CACHE[int(set_index, 2)][to_be][kk]
                    kk += 1
            CACHE[int(set_index, 2)][to_be][0] = '1'
            CACHE[int(set_index, 2)][to_be][1] = '0'
            CACHE[int(set_index, 2)][to_be][2] = hex(int(tag,2))[2:].zfill(2)
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][to_be][k+3] = RAM[j]
                k += 1
            print("hit:no")
            print("eviction_line:%d"%to_be)
            print("ram_address:%s"%address)
            print("data:0x%s"%CACHE[int(set_index, 2)][to_be][int(block_offset, 2)+3])
            RECENTS[int(set_index, 2)].pop(0)
            RECENTS[int(set_index, 2)].append(to_be)
        elif replacement_policy == 3:
            print("least frequent")


def read(address):
    global cache_hits
    global cache_misses
    global RECENTS
    cache_address = bin(int(address[2:], 16))[2:].zfill(8)
    set_index_bits = int(math.log(len(CACHE), 2))
    block_offset_bits = int(math.log(len(CACHE[0][0]), 2))
    tag_bits = 8 - set_index_bits - block_offset_bits
    tag = cache_address[0:tag_bits]
    set_index = cache_address[tag_bits:(tag_bits+set_index_bits)]
    if set_index == '':
        set_index = '0'
    block_offset = cache_address[(tag_bits+set_index_bits):]
    # Displays message
    print("set:%d"%int(set_index,2))
    print("tag:%s"%hex(int(tag,2))[2:].zfill(2))
    # checks to see if hit or miss
    hit = False
    for cache_line in CACHE[int(set_index, 2)]:
        # Hit
        if cache_line[2] == hex(int(tag,2))[2:].zfill(2) and cache_line[0] == '1':
            cache_hits += 1
            print("hit:yes")
            print("eviction_line:-1")
            print("ram_address:-1")
            print("data:%s"%cache_line[int(block_offset, 2)+3])
            indexer = CACHE[int(set_index, 2)].index(cache_line)
            if not (indexer in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(indexer)
            else:
                RECENTS[int(set_index, 2)].remove(indexer)
                RECENTS[int(set_index, 2)].append(indexer)
            hit = True
    # A miss
    if not hit:
        cache_misses += 1
        read_write(address)


def write_miss_allocate(address, data):
    global CACHE
    global RECENTS
    global RAM
    # gets the cache values again
    cache_address = bin(int(address[2:], 16))[2:].zfill(8)
    set_index_bits = int(math.log(len(CACHE), 2))
    block_offset_bits = int(math.log(len(CACHE[0][0]), 2))
    tag_bits = 8 - set_index_bits - block_offset_bits
    tag = cache_address[0:tag_bits]
    set_index = cache_address[tag_bits:(tag_bits+set_index_bits)]
    if set_index == '':
        set_index = '0'
    block_offset = cache_address[(tag_bits+set_index_bits):]
    # first checks for if the tag is there in the wanted block set
    complete = False
    for i in range(associativity):
        if CACHE[int(set_index, 2)][i][0] == '0':
            CACHE[int(set_index, 2)][i][0] = '1'
            CACHE[int(set_index, 2)][i][1] = '1'
            CACHE[int(set_index, 2)][i][2] = hex(int(tag,2))[2:].zfill(2)
            complete = True
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][i][k+3] = RAM[j]
                k += 1
            print("eviction_line:-1")
            print("ram_address:%s"%address)
            print("data:%s"%data)
            print("dirty_bit:1")
            if not (i in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(i)
            else:
                RECENTS[int(set_index, 2)].remove(i)
                RECENTS[int(set_index, 2)].append(i)
            if write_hit_policy == 1:
                CACHE[int(set_index, 2)][i][1] = '0'
                RAM[int(address[2:], 16)] = data[2:]
            CACHE[int(set_index, 2)][i][int(block_offset, 2)+3] = str(data[2:])
            break
    # we failed to find an invalid part and now have to replace
    if not complete:
        if replacement_policy == 1:
            random_int = random.randint(0, associativity-1)
            if CACHE[int(set_index, 2)][random_int][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][random_int][2],16))[2:] + set_indexer[2:] + offsets
                former_start = int(combination.zfill(8), 2)
                kk = 3
                for j in range(former_start, former_start+data_block_size):
                    RAM[j] = CACHE[int(set_index, 2)][random_int][kk]
                    kk += 1
            CACHE[int(set_index, 2)][random_int][0] = '1'
            CACHE[int(set_index, 2)][random_int][1] = '1'
            CACHE[int(set_index, 2)][random_int][2] = hex(int(tag,2))[2:].zfill(2)
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][random_int][k+3] = RAM[j]
                k += 1
            print("write_hit:no")
            print("eviction_line:%d"%random_int)
            print("ram_address:%s"%address)
            print("data:%s"%data)
            print("dirty_bit:1")
            CACHE[int(set_index, 2)][random_int][int(block_offset, 2)+3] = str(data[2:])
            if write_hit_policy == 1:
                CACHE[int(set_index, 2)][i][1] = '0'
                RAM[int(address[2:], 16)] = data[2:]
            if not (random_int in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(random_int)
            else:
                RECENTS[int(set_index, 2)].remove(random_int)
                RECENTS[int(set_index, 2)].append(random_int)
        elif replacement_policy == 2:
            to_be = RECENTS[int(set_index, 2)][0]
            if CACHE[int(set_index, 2)][to_be][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer[2:] + offsets
                former_start = int(combination.zfill(8), 2)
                kk = 3
                for j in range(former_start, former_start+data_block_size):
                    RAM[j] = CACHE[int(set_index, 2)][to_be][kk]
                    kk += 1
            CACHE[int(set_index, 2)][to_be][0] = '1'
            CACHE[int(set_index, 2)][to_be][1] = '1'
            CACHE[int(set_index, 2)][to_be][2] = hex(int(tag,2))[2:].zfill(2)
            k = 0
            for j in range((int(address[2:], 16)//data_block_size)*data_block_size,((int(address[2:], 16)//data_block_size)*data_block_size)+data_block_size):
                CACHE[int(set_index, 2)][to_be][k+3] = RAM[j]
                k += 1
            print("eviction_line:%d"%to_be)
            print("ram_address:%s"%address)
            print("data:%s"%data)
            print("dirty_bit:1")
            CACHE[int(set_index, 2)][to_be][int(block_offset, 2)+3] = data[2:]
            if write_hit_policy == 1:
                CACHE[int(set_index, 2)][i][1] = '0'
                RAM[int(address[2:], 16)] = data[2:]
            RECENTS[int(set_index, 2)].pop(0)
            RECENTS[int(set_index, 2)].append(to_be)
        elif replacement_policy == 3:
            print("least frequent")




def write(address, data):
    global RECENTS
    global RAM
    global CACHE
    global cache_hits
    global cache_misses
    cache_address = bin(int(address[2:], 16))[2:].zfill(8)
    set_index_bits = int(math.log(len(CACHE), 2))
    block_offset_bits = int(math.log(len(CACHE[0][0]), 2))
    tag_bits = 8 - set_index_bits - block_offset_bits
    tag = cache_address[0:tag_bits]
    set_index = cache_address[tag_bits:(tag_bits+set_index_bits)]
    if set_index == '':
        set_index = '0'
    block_offset = cache_address[(tag_bits+set_index_bits):]
    # Displays message
    print("set:%d"%int(set_index,2))
    print("tag:%s"%hex(int(tag,2))[2:].zfill(2))
    # checks to see if hit or miss
    hit = False
    for index in range(len(CACHE[int(set_index, 2)])):
        # Hit
        if CACHE[int(set_index, 2)][index][2] == hex(int(tag,2))[2:].zfill(2) and CACHE[int(set_index, 2)][index][0] == '1':
            hit = True
            print("write_hit:yes")
            cache_hits += 1
            print("eviction_line:-1")
            print("ram_address:-1")
            print("data:%s"%data)
            if not (index in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(index)
            else:
                RECENTS[int(set_index, 2)].remove(index)
                RECENTS[int(set_index, 2)].append(index)
            if write_hit_policy == 1:
                print("dirty_bit:0")
                CACHE[int(set_index, 2)][index][int(block_offset, 2)+3] = data[2:]
                RAM[int(address[2:], 16)] = data[2:]
            else:
                print("dirty_bit:1")
                CACHE[int(set_index, 2)][index][1] = '1'
                CACHE[int(set_index, 2)][index][int(block_offset, 2)+3] = data[2:]
    # Miss
    if not hit:
        print("write_hit:no")
        cache_misses += 1
        if write_miss_policy == 2:
            RAM[int(address[2:], 16)] = data[2:]
            print("eviction_line:-1")
            print("ram_address:%s"%address)
            print("data:%s"%data)
            print("dirty_bit:0")
            if not (index in RECENTS[int(set_index, 2)]):
                RECENTS[int(set_index, 2)].append(index)
            else:
                RECENTS[int(set_index, 2)].remove(index)
                RECENTS[int(set_index, 2)].append(index)
        else:
            write_miss_allocate(address, data)



# handles the actual simulating of the cache by controlling the flow of the program
# this function really only prompts and handles which functions to call
def activate():
    while True:
        chosen_command = prompt()
        optional = chosen_command.split()
        if chosen_command == 'quit':
            break
        elif chosen_command == 'cache-flush':
            flush()
        elif chosen_command == 'cache-view':
            view()
        elif chosen_command == 'cache-dump':
            dump()
        elif chosen_command == 'memory-dump':
            mem_dump()
        elif chosen_command == 'memory-view':
            mem_view()
        elif optional[0] == 'cache-read':
            read(optional[1])
        elif optional[0] == 'cache-write':
            write(optional[1], optional[2])
        else:
            print("Invalid command")


# main function and driver for the project
def main():
    # the raM will always start as initialized.
    init_ram()
    # then we must configure the cache
    config()
    # now we simulate the cache
    activate()

# ensures that this file is only run if it's the main file
if __name__ == '__main__':
    main()
