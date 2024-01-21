"""!
@file step_response.py
This file contains code that measures the time response of the output voltage at pin B0 in response to a change from 0 V to 3.3 V.

TODO: Create a timer interupt service routine to measure the output and a function that is responsible for setting C0 pin high and gathering the time response of the output voltage.

@author Paul, Seamus, Zaw
@date   20-Jan-2024
"""
import time
import micropython
micropython.alloc_emergency_exception_buf(100)
import cqueue   
import pyb
 
def timer_int(dummy):
    """!
This function measures the output response for every 10 ms.
"""
    volt_queue.put(adc0.read())
    
def step_response():
    """!
This function is used to set pin C0 high, run the callback, and stop the call back when queue is full.
"""
    pinC0.value(1)
    timmy.callback(timer_int)
    while not volt_queue.full():
        pass
    timmy.deinit()
   
if __name__ == "__main__":

    #The following code only runs if this file is run as the main script;
    #It does not run if this file is imported as a module:
    adc0 = pyb.ADC(pyb.Pin.board.PB0)
    QUEUE_SIZE = 200
    volt_queue = cqueue.IntQueue(QUEUE_SIZE)
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)
    pinC0.value(0) 
    time.sleep(2)
    timmy = pyb.Timer (1, freq = 100)
    step_response()
    for idx in range(QUEUE_SIZE):
        print(f'{10*idx}, {volt_queue.get()*3.3/4096}')
    print('END')
