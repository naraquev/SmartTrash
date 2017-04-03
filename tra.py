import time
import json
import RPi.GPIO as GPIO
import datetime
import urllib3
import config



'''****************************************************************************************
HCP services Variables
****************************************************************************************'''
http = urllib3.PoolManager()
headers = urllib3.util.make_headers(user_agent=None)
headers['Authorization'] = 'Bearer ' + config.oauth_credentials_for_device
headers['Content-Type'] = 'application/json;charset=utf-8'
url='https://iotmms' + config.hcp_account_id + config.hcp_landscape_host + '/com.sap.iotservices.mms/v1/api/http/data/'
	+ str(config.device_id)


'''****************************************************************************************
Pin Configurations
****************************************************************************************'''
TRIG = 5 # Broadcom pin 18 (P1 pin 12)                                          
ECHO = 6 # Broadcom pin 23 (P1 pin 16)                                          
LIDCOVER = 15
alarmOut = 22 # Broadcom pin 22 (P1 pin 15) 

'''****************************************************************************************
Function Name 	:	ultrasonicSensorInit()
Description		:	Function which initilizes the GPIO pins
Parameters 		:	-
****************************************************************************************'''

def ultrasonicSensorInit():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.setup(LIDCOVER,GPIO.IN)
	GPIO.setup(alarmOut,GPIO.OUT)
	GPIO.output(TRIG, False)
	GPIO.output(alarmOut,False)
	
	
'''****************************************************************************************
Function Name 	:	distanceMeasurement()
Description		:	Function calculates the amount of waste in the trashcan and send it to the client
					and sends an alert message when trash can reaches the threshold
Parameters 		:	-
****************************************************************************************'''
currentCriticalLevelFlag = False
criticalLevelChangeOverFlag = False
distanceRecordedTime = 0
criticalLevelReachedTime = 0
currentDistance = 0
notificationSentTime = 0
LOOP_SAMPLING_TIME = 2
CRITICAL_DISTANCE = 100
NOTIFICATION_TIME_DELAY = 15
lidCoverSendMessage0 = True
lidCoverSendMessage1 = True



try:
	start = 0
	l_prev_distance = 0
	ultrasonicSensorInit()
	while 1:
		if GPIO.input(LIDCOVER) == 0:
			if(lidCoverSendMessage0 == True):
				lidCoverSendMessage1 = True
				timestamp= time.time()
				body= '{"mode":"async", "messageType":"' + str(config.message_type_id_isOpen) + '", "messages":[{"timestamp":' + str(timestamp) + '"'+ ', "isOpen": False }]}'
				r = http.urlopen('POST', url, body=body, headers=headers)
				lidCoverSendMEssage0= False
			time.sleep(LOOP_SAMPLING_TIME)		
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)
			#Starts the timer 
			while (GPIO.input(ECHO)==0):
			    start = time.time()
			#Waits for the timer to end once the pin is high
			while GPIO.input(ECHO)==1:
				end = time.time()
			pulse_duration = end - start
			l_distance = pulse_duration * 17150
			l_distance = round(l_distance, 2)
			currentDistance = l_distance
			timestamp= time.time()			
			body= '{"mode":"async", "messageType":"' + str(config.message_type_id_From_device) + '", "messages":[{"timestamp":' + str(timestamp) + '"'+ ', "distance":"' + str(l_distance) + '"}]}'
			r = http.urlopen('POST', url, body=body, headers=headers)
			if currentDistance < 50:
			    GPIO.output(alarmOut,False)
		else:
			if(lidCoverSendMessage1 == True):
				timestamp= time.time()
				body= '{"mode":"async", "messageType":"' + str(config.message_type_id_isOpen) + '", "messages":[{"timestamp":' + str(timestamp) + '"'+ ', "isOpen": True }]}'
				r = http.urlopen('POST', url, body=body, headers=headers)
				lidCoverSendMEssage1= False
except KeyboardInterrupt: 
		GPIO.cleanup()
