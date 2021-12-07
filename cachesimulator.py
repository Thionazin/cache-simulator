## @package cachesimulator
# Documentation for this program
#
# This is the documentation for my cache simulator program. The cache itself is stored as a 3 dimensional python list. The first one is the set, second is the line, and third is the element in each line.


# File: cachesimulator.py
# Author(s): Senhe Hao
# Date: 12/08/2021
# Section: 507 
# E-mail(s): senhehao@tamu.edu
# Description: This is the project. The comments below will explain what each part of the code does.

## Imports required for the program
#
# This program uses the sys, math, and random modules. Random is used for random replacement. Math is used for the various operations. Sys is used so that data can be passed when launching with the command line.
import sys
import math
import random

# massive list of variables
## RAM list
#
# A list used to store the values in the 256 byte RAM. These are represented as two character strings.
RAM = []
## CACHE list
#
# A three dimensional list. Used to store the values in the cache. The first dimension is the set. The second is the line in the set. The third is the item in the line. The first two items are the valid and the dirty bit. The third is the tag. Then the remaining elements are the memory bytes stored in the cache.
CACHE = []
## RECENCY queue
#
# Queue used for the least recently used replacement policy. Has two dimensions. One is used for the set. In that inner list, it will store a queue of lines. This is in order of which one was accessed least recently. With the most recent one being the last one.
RECENTS = []
## FREQUENCY storage
#
# A dictionary used to store how many times a particular line or memory is used. That is stored as a simple integer. In the LFU policy, the line with the lowest frequency count will be replaced.
FREQUENTS = {}
## Cache Size
#
# Global variable for the cache size.
cache_size = 0
## Data Block Size
#
# Global variable to store the data block size.
data_block_size = 0
## Associativity
#
# Global variable for associativity.
associativity = 0
## Replacement Policy
#
# Global variable for replacement policy.
replacement_policy = 0
## Write Hit Policy
#
# Global variable for write hit policy.
write_hit_policy = 0
## Write Miss Policy
#
# Global variable for write miss policy.
write_miss_policy = 0
## Cache Hits
#
# Global variable to store the amount of cache hits.
cache_hits = 0
## Cache Misses
#
# Global variable to store the amount of cache misses.
cache_misses = 0
## RAM_start
#
# Used only shortly to determine the start when initializing RAM.
RAM_start = ""
## RAM_end
#
# Used only one to determine the end when initializing RAM.
RAM_end = ""


## The flush function
#
# This function is called when we use the command cache flush. It loops through the three dimensions of the cache list. On each line of a set, it will write the data in the line back to the ram if the dirty bit is one. Then afterwards regardless, it will clear all the values in the cache and set them back to 0 or 00.
def flush():
    global CACHE
    for i in range(int(cache_size/(data_block_size*associativity))):
        RECENTS[i].clear()
        for j in range(associativity):
            if CACHE[i][j][1] == '1':
                set_indexer = bin(i).zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = '0b'
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

## Cache Dump
#
# This function is called by the cache dump command. Essentially it writes the data of each line in the cache to an output file called 'cache.txt'.
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

## Memory Dump
#
# Function for dumping the contents of the simulated RAM into a text file named 'ram.txt'
def mem_dump():
    f = open('ram.txt', 'w')
    for i in RAM:
        f.write(i)
        f.write('\n')
    f.close()


## Cache View
#
# Function for printing to the console the current contents of the cache. It will print the basic information of the cache such as sizes or replacement policies in place. Then it will loop through the entire cache and print out the contents.
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

## Memory View
#
# Function to view the current contents of the memory in the console. Will print it out. Prints out the size as well as the content. Has addresses on the left with the values on the right. Every line contains eight values with the address going by eights.
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


## Initialize Ram
# 
# Function called at the start of the program. The program will start with initializing the memory. The memory is always 256 bytes. The function will prompt you for a command to initialize the ram along with the start of the ram that we're copying in and the ending address. The starting address will always be 0x00. Then based off of the ending address it will load in values from the input to the simulated ram in the program.
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


## Configuration Function
#
# Function called at the start by default. This is when the CACHE list as well as the global variables are initialized. The cache is set based on the global variables. This function also has slight error checking to make sure that some of the configuration inputs are within the bounds of what we want. If the values are invalid, the user is re prompted.
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
        if replacement_policy == 1 or replacement_policy == 2 or replacement_policy == 3: 
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
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            CACHE[i].append([])
    for i in range(int(cache_size/(associativity*data_block_size))):
        for j in range(associativity):
            CACHE[i][j].append('0')
            CACHE[i][j].append('0')
            CACHE[i][j].append('00')
            for k in range(int(data_block_size)):
                CACHE[i][j].append('00')
    print('cache successfully configured!')



## Prompt
#
# All this function is used for is to print out the prompt and wait for an input. This is called by default by the infinite loop that controls the flow of this program. Once a value has been given, it will then return the value, which will then be used by the main logic.
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


## Read Writer
#
# This function is called whenever we have a read miss in the cache. When this happens, we need to take the values from the RAM and throw them into the cache. It checks first if there's an invalid line in that set. If there is, then we write over the invalid. Otherwise we'll choose a block to evict based on policy and then evict that line to make room for the new one.
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
                combination = bin(int(CACHE[int(set_index, 2)][random_int][2],16))[2:] + set_indexer + offsets
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
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer + offsets
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
            set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
            if len(CACHE) == 1:
                set_indexer = ''
            offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
            combination = bin(int(CACHE[int(set_index, 2)][0][2],16))[2:] + set_indexer + offsets
            former_start = int(combination.zfill(8), 2)
            minimum_used = FREQUENTS[hex(former_start)[2:].zfill(2)]
            min_index = 0
            for i in range(associativity):
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][i][2],16))[2:] + set_indexer + offsets
                former_start = int(combination.zfill(8), 2)
                if FREQUENTS[hex(former_start)[2:].zfill(2)] < minimum_used:
                    minimum_used = FREQUENTS[hex(former_start)[2:].zfill(2)]
                    min_index = i
            to_be = min_index
            if CACHE[int(set_index, 2)][to_be][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer + offsets
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


## Cache Read
#
# This function is the main logic for the cache read function. This is called when we specify the command cache read. First it gets the tag, set index, and block offset from the input address. Then it checks if it's a hit or not. If it's a hit, it will read what we want from the line and output it along with some other information otherwise it will call the read write function if it's a miss. 
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
    if not (hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2) in FREQUENTS):
        FREQUENTS[hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2)] = 0 
    FREQUENTS[hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2)] += 1
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

## Write Miss Allocate
#
# Function to do the logic for write miss if we are using the write allocate policy. This is called when we have a write miss. A lot of this logic is similar to having a read miss. We'll first find an invalid line and try to replace that first. Otherwise what it will do is based off of the replacement policy it will evict the line and replace it with the new wanted data.
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
                combination = bin(int(CACHE[int(set_index, 2)][random_int][2],16))[2:] + set_indexer + offsets
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
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer + offsets
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
            set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
            if len(CACHE) == 1:
                set_indexer = ''
            offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
            combination = bin(int(CACHE[int(set_index, 2)][0][2],16))[2:] + set_indexer + offsets
            former_start = int(combination.zfill(8), 2)
            minimum_used = FREQUENTS[hex(former_start)[2:].zfill(2)]
            min_index = 0
            for i in range(associativity):
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][i][2],16))[2:] + set_indexer + offsets
                former_start = int(combination.zfill(8), 2)
                if FREQUENTS[hex(former_start)[2:].zfill(2)] < minimum_used:
                    minimum_used = FREQUENTS[hex(former_start)[2:].zfill(2)]
                    min_index = i
            to_be = min_index
            if CACHE[int(set_index, 2)][to_be][1] == '1':
                set_indexer = set_index.zfill(int(math.log(len(CACHE), 2)))
                if len(CACHE) == 1:
                    set_indexer = ''
                offsets = ''.zfill(int(math.log(len(CACHE[0][0]), 2)))
                combination = bin(int(CACHE[int(set_index, 2)][to_be][2],16))[2:] + set_indexer + offsets
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



## Cache Write
#
# This is the function called when we use the command cache write. What it does is first check if it's a hit or miss. On a hit it will update the dirty bit based off of policy and either write to cache or write to both memory and cache. Otherwise on a miss it will either write directly to the address in the ram or call the write allocate function based off of the write miss policy.
def write(address, data):
    global RECENTS
    global RAM
    global CACHE
    global cache_hits
    global cache_misses
    global FREQUENTS
    cache_address = bin(int(address[2:], 16))[2:].zfill(8)
    set_index_bits = int(math.log(len(CACHE), 2))
    block_offset_bits = int(math.log(len(CACHE[0][0]), 2))
    tag_bits = 8 - set_index_bits - block_offset_bits
    tag = cache_address[0:tag_bits]
    set_index = cache_address[tag_bits:(tag_bits+set_index_bits)]
    if set_index == '':
        set_index = '0'
    block_offset = cache_address[(tag_bits+set_index_bits):]
    if not (hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2) in FREQUENTS):
        FREQUENTS[hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2)] = 0 
    FREQUENTS[hex((int(address[2:], 16)//data_block_size)*data_block_size)[2:].zfill(2)] += 1
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
## Activate
#
# Final function called by the main. It is responsible for the main flow of the program. It contains an infinite for loop that prompts the user to enter in the command with the prompt function. Then based off of the command that we're given back, it will call one of the functions corresponding to the command.
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
        elif chosen_command == 'debug':
            print(FREQUENTS)
        else:
            print("Invalid command")


# main function and driver for the project
## Main
#
# Main function. Is called if this file is the main file that is run. It will call Initialize RAM, then call the Config function, then call the Activate function.
def main():
    # the raM will always start as initialized.
    init_ram()
    # then we must configure the cache
    config()
    # now we simulate the cache
    activate()



# ensures that this file is only run if it's the main file
## name main
#
# This is just part of the driver. It will call the main function if this is the file that is run.
if __name__ == '__main__':
    main()
