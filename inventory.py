# -- coding: utf-8 --
"""
Created on Tue Jun 22 06:36:45 2021

@authors: Hassan Khaleghhi Rad and Nadia Yazdani
"""
import array as myarray
import math
zrng = myarray.array('l', [1, 1973272912, 281629770,  20006270,1280689831,2096730329,1933576050,  913566091, 246780520,1363774876, 604901985,1511192140,1259851944,  824064364, 150493284, 242708531,  75253171,1964472944,1202299975,  233217322,1911216000, 726370533, 403498145, 993232223,1103205531,  762430696,1922803170,1385516923,  76271663, 413682397, 726466604,  336157058,1432650381,1120463904, 595778810, 877722890,1046574445,   68911991,2088367019, 748545416, 622401386,2122378830, 640690903, 1774806513,2132545692,2079249579,  78130110, 852776735,1187867272, 1351423507,1645973084,1997049139, 922510944,2045512870, 898585771,  243649545,1004818771, 773686062, 403188473, 372279877,1901633463,  498067494,2087759558, 493157915, 597104727,1530940798,1814496276,  536444882,1663153658, 855503735,  67784357,1432404475, 619691088,  119025595, 880802310, 176192644,1116780070, 277854671,1366580350, 1142483975,2026948561,1053920743, 786262391,1792203830,1494667770, 1923011392,1433700034,1244184613,1147297105, 539712780,1545929719,  190641742,1645390429, 264907697, 620389253,1502074852, 927711160,  364849192,2049576050, 638580085, 547070247])
MODLUS = 2147483647
MULT1  =     24112
MULT2  =     26143

smalls = 0
bigs = 0
time_next_event = myarray.array('d', [0.00000000, 1.00000002e+30, 0.0914971903, 120.000000, 0.00000000])
initial_inv_level = 60
num_months = 120
num_values_demand = 4
holding_cost = 1.0
incremental_cost = 3.0
maxlag = 1.0
mean_interdemand = 0.1
minlag = 0.5
setup_cost = 32.0
shortage_cost = 5.0
sim_time = 0 
num_events = 4
inv_level = 0
time_last_event = 0
next_event_type = 4
total_ordering_cost = 0.0
prob_distrib_demand = []
area_shortage = 0 
amount = 0
rea_holding = 0



def initialize():
    global prob_distrib_demand
    global area_shortage
    global initial_inv_level
    global inv_level
    global amount
    global area_holding    
    global sim_time        
    global time_last_event
    global total_ordering_cost
    global time_next_event     
    global smalls
    global bigs
    global setup_cost	
    global num_months
    global num_values_demand
    global shortage_cost
    global holding_cost
    global incremental_cost
    global num_events
    global next_event_type
    global maxlag
    global mean_interdemand
    global minlag 

    

    
    smalls = 40
    bigs = 100
	
    prob_distrib_demand = myarray.array('d',  [0.00000000, 0.166999996, 0.500000000, 0.833000004, 1.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000])
    area_shortage = 0
    initial_inv_level = 60
    inv_level = 0
    inv_level  = initial_inv_level
    amount = 0
    area_holding	= 0
    sim_time = 0
    time_last_event = 0
    total_ordering_cost = 0.0
    num_months = 120
    time_next_event[0] = 0
    time_next_event[1] = 1.0e+30 
    time_next_event[3] = num_months  
    time_next_event[4] = 0.0 
    setup_cost = 32.0
    num_values_demand = 4
    shortage_cost = 5.0
    holding_cost = 1.0
    incremental_cost = 3.0
    num_events = 4
    next_event_type = 0
    maxlag = 1.0	    
    mean_interdemand = 0.1
    minlag = 0.5


    
def timing():
    global sim_time
    global time_next_event
    global min_time_next_event
    global next_event_type 
    i = 1 
    min_time_next_event = 1.0e+29
    next_event_type = 0
    
    
    while i < 5:        
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type     = i            
        i += 1
        
    if next_event_type == 0: 
        print( "\nEvent list empty at time") 
        exit(1)
    sim_time = min_time_next_event
    
def update_time_avg_stats():
    global sim_time
    global time_last_event
    global area_shortage
    global area_holding
    global inv_level
    time_since_last_event = 0
    time_since_last_event = sim_time - time_last_event
    time_last_event       = sim_time
    
    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
        
    if inv_level > 0:
        area_holding  += inv_level * time_since_last_event
        
    
def switch():
    global next_event_type

    if next_event_type == 1:
        order_arrival()
 
    elif next_event_type == 2:
        demand()
        
    
    elif next_event_type == 4:
        evaluate()
        
 
    elif next_event_type == 3:
        #next_event_type = 0
        #time_next_event[3] = 120
        report()
  

def evaluate(): 
    global total_ordering_cost
    global amount
    global inv_level
    global smalls
    global bigs
    global incremental_cost
    global minlag
    global maxlag
    global time_last_event
    global setup_cost
    global sim_time
    
    if inv_level < smalls: 
        amount               = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount
        time_next_event[1] = sim_time + uniform(minlag, maxlag)

    time_next_event[4] = sim_time + 1.0
        
def uniform(a, b):
    return a + lcgrand(1) * (b - a)        

def random_integer(prob_distrib):
    i = 0
    u = 0.0
    u = lcgrand(1);
    while u >= prob_distrib[i]:
        i += 1
    return i


def demand(): 
    global inv_level
    global prob_distrib_demand
    global mean_interdemand
    global sim_time
    global time_next_event
    inv_level -= random_integer(prob_distrib_demand)
    time_next_event[2] = sim_time + expon(mean_interdemand)

    
def order_arrival():
    global inv_level
    global amount
    global time_last_event
    inv_level += amount
    time_next_event[1] = 1.0e+30

def main():    
    global next_event_type
    initialize()
    while next_event_type != 3:
        timing()
        update_time_avg_stats()
        switch()
            

def report():
    global area_holding
    global total_ordering_cost
    global num_months
    global holding_cost
    global shortage_cost
    global smalls
    global next_event_type

    avg_holding_cost = 0 
    avg_ordering_cost = 0
    avg_shortage_cost = 0

    avg_ordering_cost = total_ordering_cost / num_months;
    avg_holding_cost  = holding_cost * area_holding / num_months;
    avg_shortage_cost = shortage_cost * area_shortage / num_months;
    print("s                                                        =",smalls)
    print("S                                                        =",bigs)
    print("avg_ordering_cost + avg_holding_cost + avg_shortage_cost =",avg_ordering_cost + avg_holding_cost + avg_shortage_cost)
    print("avg_ordering_cost                                        =",avg_ordering_cost)
    print("avg_holding_cost                                         =",avg_holding_cost)
    print("avg_shortage_cost                                        =", avg_shortage_cost)


def lcgrand(stream):    
    zi = 0
    lowprd = 0
    hi31 = 0
    zi = zrng[stream]
    lowprd = (zi & 65535) * MULT1
    hi31   = (zi >> 16) * MULT1 + (lowprd >> 16)
    zi     = ((lowprd & 65535) - MODLUS) +  ((hi31 & 32767) << 16) + (hi31 >> 15)
    if (zi < 0):
        zi += MODLUS
    lowprd = (zi & 65535) * MULT2
    hi31   = (zi >> 16) * MULT2 + (lowprd >> 16)
    zi     = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if (zi < 0):
        zi += MODLUS
    zrng[stream] = zi;
    return (zi >> 7 | 1) / 16777216.0

def expon(mean):
    return -mean * math.log(lcgrand(1))



    

if __name__ == "__main__":
    main()
