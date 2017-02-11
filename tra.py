import time
import json
import RPi.GPIO as GPIO
import datetime





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
CRITICAL_DISTANCE = 50
NOTIFICATION_TIME_DELAY = 15



def distanceMeasurement():
	try:
		global client,deviceType,LOOP_SAMPLING_TIME,NOTIFICATION_TIME_DELAY,CRITICAL_DISTANCE,currentCriticalLevelFlag,criticalLevelChangeOverFlag
		l_prev_distance = 0
		ultrasonicSensorInit()
		while 1:
			if GPIO.input(LIDCOVER) == 0:
				time.sleep(LOOP_SAMPLING_TIME)		
				GPIO.output(TRIG, True)
				time.sleep(0.00001)
				GPIO.output(TRIG, False)
				#Starts the timer 
				while GPIO.input(ECHO)==0:
					pulse_start = time.time()
				#Waits for the timer to end once the pin is high
				while GPIO.input(ECHO)==1:
					pulse_end = time.time()
				pulse_duration = pulse_end - pulse_start
				l_distance = pulse_duration * 17150
				l_distance = round(l_distance, 2)
				currentDistance = l_distance
				print(l_distance)
				distanceRecordedTime = datetime.datetime.now()
                print(distanceRecordedTime)
                if currentDistance < CRITICAL_DISTANCE:
                    GPIO.output(alarmOut,True)
                    if currentCriticalLevelFlag == False:#6.1.1
                        currentCriticalLevelFlag = True#6.1.1.2
                        criticalLevelChangeOverFlag = True#6.1.1.3
                        criticalLevelReachedTime = datetime.datetime.now()
                    else:
                        criticalLevelChangeOverFlag = False
                else:
                    GPIO.output(alarmOut,False)					
                    currentCriticalLevelFlag = False
                    criticalLevelChangeOverFlag = False


				

				# This means that in this measurement loop the level stays at the critical level
				
				#if (currentCriticalLevelFlag == True):
					#calculate timedifference
				#	diff = distanceRecordedTime - notificationSentTime 
	
				#	day  = diff.days
				#	hour = (day*24 + diff.seconds/3600)
				#	diff_minutes = (diff.days *24*60)+(diff.seconds/60)			

				#	if diff_minutes > NOTIFICATION_TIME_DELAY:
				
			
						
	except KeyboardInterrupt: 
		GPIO.cleanup()
	
		
if __name__ == '__main__':
	distanceMeasurement()