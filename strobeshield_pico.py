import machine
import time
import network
import urequests
import date
import utime

ssid = "MYHDSB"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print("Connected to Wi-Fi")

running = True
hertz = 60
photoresistor = machine.ADC(1)
delay = 0.2023

motor = machine.Pin(10, machine.Pin.OUT)

red = machine.Pin(7, machine.Pin.OUT)
green = machine.Pin(8, machine.Pin.OUT)
blue = machine.Pin(9, machine.Pin.OUT)

time_curr = utime.localtime(utime.time() - 4*3600)

year, month, day, hour, minute, second, weekday, yearday = time_curr

flashing = []
button = machine.ADC(0)

motor.value(0)

def post_to_api():
    
    time_curr = utime.localtime(utime.time() - 4*3600)

    year, month, day, hour, minute, second, weekday, yearday = time_curr
    
    date = weekday + ", " + day + ", " + month + ", " + year + ", " + hour + ":" + minute + ":" + second
    
    url = "http://example.com/api"
    data = {"timestamp": date, "description": "Activated by Flashing Lights: Photoepilepsy Risk", "advisory": "Ensure communication with the loved one. Medical Aid is contacted as specified in setup."}
    response = urequests.post(url, json=data)
    print(response.text)

def rotate():
    motor.value(1)
    time.sleep(delay)
    motor.value(0)

def polarize():
    button_pressed = False
   
    rotate()
   
    print("LOCKED!")
    time.sleep(1)

    while not button_pressed:
        red.high()
        green.low()
        blue.low()
        time.sleep(0.4)
       
        red.high()
        green.high()
        blue.high()
        time.sleep(0.4)
       
        if button.read_u16() > 60000:
            button_pressed = True
            rotate()
   
       

def concat_elements(list):
    grouped_list = []
    current_group = []

    for elem in list:
        if not current_group or elem == current_group[0]:
            current_group.append(elem)
        else:
            grouped_list.append(current_group)
            current_group = [elem]

    if current_group:
        grouped_list.append(current_group)

    for i in range(len(grouped_list)):
        grouped_list[i] = len(grouped_list[i])

    return grouped_list

# function to check how fast flashes/flickers are
def check_flashes(concat):
   
    # if the amount of instances is enough to be significantly quick, run the checker
    if len(concat) >= 6:
   
        # for each group of 6 run the sum checker to see if the total change is less than the "slow" value of 30 counts
        for i in range (len(concat)-5):
           
            # reset sum
            concat_instance_sum = 0
           
            # check for every 6 in the list
            for j in range (i, i+6):
                concat_instance_sum += concat[j]
                # print(concat_instance_sum)
               
            # if there are small enough changes for less than half of a second (60hz), say its flashing
            if concat_instance_sum <= 30:
                return True
           
        # otherwise, say that flashes are insignificant
        return False
   
    else:
        # if not enough changes to be "fast" automatically return 'false'
        return False


def listcomp(flashing, x):
    if len(flashing) >= hertz:
        flashing.pop(0)
        flashing.append(x)
        return flashing
    else:
        flashing.append(x)
        return flashing

while running:
    red.low()
    green.high()
    blue.high()
   
    bright_level = photoresistor.read_u16()
    if bright_level > 56000:
        listcomp(flashing,1)
        time.sleep(1/hertz)
    else:
        listcomp(flashing,0)
       
    concat = concat_elements(flashing)
       
    if check_flashes(concat):
        print(True)
        polarize()
        flashing = []
   
    motor.value(0)