import machine
import time
import network
import urequests
import date
import utime

# network
ssid = "Abbas's iPhone"
password = "abbas123"

# init wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

print("Connected to Wi-Fi")

# loop state = true for checking lights
running = True

# refresh rate = 60 Hz
hertz = 60

# pin for PR input (analog)
photoresistor = machine.ADC(1)

# specified delay for polarization
delay = 0.2023

# motor control pin
motor = machine.Pin(10, machine.Pin.OUT)

# RGB LED control pins
red = machine.Pin(7, machine.Pin.OUT)
green = machine.Pin(8, machine.Pin.OUT)
blue = machine.Pin(9, machine.Pin.OUT)

# get time for posting episodes
time_curr = utime.localtime(utime.time() - 4*3600)

year, month, day, hour, minute, second, weekday, yearday = time_curr

# list to store 60 occurences of inputs from the PR in a second
flashing = []

# button input for disarming polarization lock
button = machine.ADC(0)

# motor off
motor.value(0)

# function to use urequests and utime to post events of possible seizures to the API
def post_to_api():
    
    time_curr = utime.localtime(utime.time() - 4*3600)

    year, month, day, hour, minute, second, weekday, yearday = time_curr
    
    date = weekday + ", " + day + ", " + month + ", " + year + ", " + hour + ":" + minute + ":" + second
    
    url = "http://172.20.10.2:5000/"
    
    data = {"timestamp": date, "description": "Activated by Flashing Lights: Photoepilepsy Risk"}

    # , "advisory": "Ensure communication with the loved one. Medical Aid is contacted as specified in setup."}
    
    response = urequests.post(url, json=data)
    print(response.text)

# function to rotate the polarizer film ot block light
def rotate():
    motor.value(1)
    time.sleep(delay)
    motor.value(0)

# Actions that get called when sufficiently quick "flashes" occur to be dangerous
def polarize():
    button_pressed = False
   
    # post_to_api()

    # This is where the sms message(s) would be sent if we had paid for Twilio
    # send_sms(account_sid, auth_token, from_number, to_number, "Light-induced seizure imminent!"):
    rotate()
   
    # The StrobeShield stays in the polarized state until deliberately told to exit by the pushbutton being held. 
    print("LOCKED!")
    time.sleep(1)

    while not button_pressed:

        # blink red / white for alerting
        red.high()
        green.low()
        blue.low()
        time.sleep(0.4)
       
        red.high()
        green.high()
        blue.high()
        time.sleep(0.4)
       
        # If the button (on analogread) is pressed, leave the state and rotate out of polarization
        if button.read_u16() > 60000:
            button_pressed = True
            rotate()
   
       
# function to combine the 60 taken measurements from "high" and "low" light in one second into numbers that represent repetitions in occurence
# These repititions all add up to 60 in the output list
def concat_elements(list):

    # two lists are used to count occurences of the same type, and deploy the length of the "current group" list to the "grouped list" once a different reading is reached 
    grouped_list = []
    current_group = []

    
    # Iterate over each element in the input list
for elem in input_list:
    # Check if the current group is empty or if the current element matches the first element of the current group
    if not current_group or elem == current_group[0]:
        # If so, add the element to the current group
        current_group.append(elem)
    else:
        # If not, add the current group to the grouped list and start a new group with the current element
        grouped_list.append(current_group)
        current_group = [elem]

# If there is any remaining group after the loop, add it to the grouped list
if current_group:
    grouped_list.append(current_group)

# Iterate over each group in the grouped list
for i in range(len(grouped_list)):
    # Replace each group with its length (number of elements in the group)
    grouped_list[i] = len(grouped_list[i])

# Return the final grouped list containing the lengths of the groups
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

# main loop to check the occurence of dangerous flashing
while running:

    # stable teal
    red.low()
    green.high()
    blue.high()
   
    # check the PR and if it exceeds the value, append as a flash
    bright_level = photoresistor.read_u16()
    if bright_level > 56000:
        listcomp(flashing,1)
        time.sleep(1/hertz)
    else:
        listcomp(flashing,0)

    # concatenate the 60 occurences in a second
    concat = concat_elements(flashing)
       
    # check if flashes are significantly quick to be dangerous, run the polarization command and reset the check list
    if check_flashes(concat):
        print(True)
        polarize()
        flashing = []
   
    motor.value(0)

from twilio.rest import Client

def send_sms(account_sid, auth_token, from_number, to_number, message):
    """
    Send an SMS message using Twilio.

    Parameters:
    - account_sid (str): Twilio account SID.
    - auth_token (str): Twilio auth token.
    - from_number (str): Twilio phone number from which the SMS will be sent.
    - to_number (str): Recipient's phone number.
    - message (str): Message to be sent.
    
    Returns:
    - str: Message SID if message was sent successfully, otherwise returns None.
    """
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send the message
        sent_message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        
        # Return the message SID to confirm it was sent successfully
        return sent_message.sid
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage:
if __name__ == "__main__":
    # Replace these with your Twilio account details and phone numbers
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    from_number = '+1234567890'  # your Twilio phone number
    to_number = '+9876543210'    # recipient's phone number
    message = "Hello from Twilio!"
    
    # Send the SMS
    message_sid = send_sms(account_sid, auth_token, from_number, to_number, message)
    
    if message_sid:
        print("Message sent successfully. Message SID:", message_sid)
    else:
        print("Failed to send the message.")