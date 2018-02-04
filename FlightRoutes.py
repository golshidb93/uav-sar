print "Start Simulator (SITL)"
import dronekit_sitl1
connection_string = "127.0.0.1:14550"

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
# Needed for command message definitions
from pymavlink import mavutil

import time
import math

# The drone start with geo cordinates (LAT, LNG, ALT, YAW)
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready = True)

#Get some vehicle attributes (state)
print "Get vehicle attributes:"
print "GPS: %s" % vehicle.gps_0
print "Battery: %s" % vehicle.battery
print "Last Heartbeat: %s" % vehicle.is_armable
print "System status: %s" % vehicle.system.status.state
print "Mode: %s" % vehicle.mode.name # Settable

# ARM and TAKEOFF
def arm_and_takeoff(aTargetAltitude):
		print "Basic pre-arm checks"
		
		# Don't let the user try to arm until autopilot is ready
		while not vehicle.is_armable:
				print "Waiting for vehicle to initialize..."
				time.sleep(1)
				
				print "Arming motors"
				#Coptor should arm in GUIDED mode
				vehicle.mode = VehicleMode("GUIDED")
				vehicle.armed = True
				
				while not vehicle.armed:
						print "Waiting for arming..."
						time.sleep(1)
						
				print "Taking off!"
				#Take off to target altitude
				vehicle.simple_takeoff(aTargetAltitude)
				
				#Wait until the vehicle reaches a safe height before
				#processing the goto (otherwise the command) after
				#Vehicle.simple_takeoff will execute
				while True:
					print "Altitude: ", vehicle.location.global_relative_frame.alt
					#Trigger just below target alt
					if vehicle.location.global_relative_frame.alt >= aTargetAltitude*0.95:
						print "reached target altitude"
						break
					time.sleep(1)
					
# Arm and takeoff to altitude of 20 meters
arm_and_takeoff(20)
print "go to position 1"
#Move to current position, since yaw does not work a move command is given
position1 = LocationGlobalRelative(62.475451, 6.183285, 20)
# A global location object
if vehicle.mode.name == "GUIDED":
		vehicle.simple_goto(position1, groundspeed = 1)
		time.sleep(40)
		
print "Go to position 2"
position2 = LocationGlobalRelative(62.475016, 6.184158, 20)

# A global location object
		
if vehicle.mode.name == "GUIDED":
		vehicle.simple_goto (position2, groundspeed=1)
		time.sleep (30)

print "Go to position 3"
position 3 = LocationGlobalRelative (62.475637, 6.185698, 20)		

# A global location object.

if vehicle.mode.name == "GUIDED":
		vehicle.simple_goto(position3, groundspeed=1)
		time.sleep (40)
		
print "Go to position 4"
position4 = LocationGlobalRelative (62.476083, 6.184908, 20)

# A global position object.

if vehicle.mode.name == "GUIED":
		vehicle.simple_goto (position4, groundspeed =1)
		time.sleep (30)
		
print "Returning to Launch"
if vehicle.mode.name == "GUIDED":
		vehicle.mode = VehicleMode("RTL")
		time.sleep (30)
		
print "Setting LAND mode..."
if vehicle.mode.name == "GUIDED" or vehicle.mode.name == "RTL":
		vehicle.mode = VehicleMode ("LAND")
		time.sleep (30)
		
# Close vehicle object before exiting script
vehicle.close ()

print "Completed"