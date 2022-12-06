#!/usr/bin/env python2
import time
import rospy
from std_msgs.msg import Int32,Int16,String
from nav_msgs.msg import Path
from geometry_msgs.msg import Vector3
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from std_msgs.msg import Int32MultiArray as HoldingRegister
from actionlib_msgs.msg import GoalStatus
from std_msgs.msg import Int16
from move_base_msgs.msg import MoveBaseActionGoal,MoveBaseActionResult

import math
class Server:
  def __init__(self):
    self.battery_status = rospy.Subscriber("voltage_percentage", Int32, self.batterycallback)
    self.robot_status = rospy.Subscriber("robot_status", Int16, self.robotcallback)
    self.newgoal =  rospy.Publisher("newcoordinates",Vector3 ,queue_size=10) 
    self.mission_status = rospy.Publisher("missionstatus",Int16 ,queue_size=10) 
    self.plan_distance = rospy.Subscriber("path_test_server", Path, self.distance_callback)
    self.batterypercentage=100
    self.ro_status=0
    self.status=2
    self.outputregister = HoldingRegister()
    '''
    ROBOT STATUS / GOAL STATUS
        uint8 PENDING=0
        uint8 ACTIVE=1
        uint8 PREEMPTED=2
        uint8 SUCCEEDED=3
        uint8 ABORTED=4
        uint8 REJECTED=5
        uint8 PREEMPTING=6
        uint8 RECALLING=7
        uint8 RECALLED=8
        uint8 LOST=9
        actionlib_msgs/GoalID goal_id
        uint8 status
        string text
    '''
    #Registers: RobotStatus, Goalx, Goaly, Battery, MissionStatus, Distance,
    self.modbusmode = {
	"Battery": 0,   #0-100
	"RobotStatus": 0,    
	"Distance": 0,
    }
    self.distancegoal= 0.0
    self.distancerobot=0
  def batterycallback(self, msg):
      self.batterypercentage=msg.data
  def robotcallback(self, msg):
      self.ro_status=msg.data
  def distance_callback(self,data):
      if self.status==1: #Move
          for i in range(len(data.poses)-1):
              self.distancegoal += math.sqrt(pow((data.poses[i+1].pose.position.x - data.poses[i].pose.position.x),2) + pow((data.poses[i+1].pose.position.y - data.poses[i].pose.position.y), 2))
          self.distancerobot=int(self.distancegoal*1000)

if __name__ == '__main__':
    try:
        rospy.init_node('Server_info')
        robot = Server()
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            try:
                client =  ModbusClient("10.22.240.51",port=12345) #Server second computer
                UNIT = 0x1
                conexion = client.connect()
                rospy.logwarn("Modbus connection ready")
            except Exception as error:
                rospy.logwarn("Modbus connection error")
                rospy.logwarn(error)
            try:
                rr = client.read_holding_registers(0,15,unit=UNIT)
                rospy.logwarn(rr.registers)
                rospy.logwarn("Info robot working")
                robot.status = rr.registers[0] #MissionStatus 0-Charge, 1-Move, 2-Free, 3-Success, 4-Failure
                #Transform modbus coordinate 10->Positive; 11->Negative
                firstx=int(rr.registers[1]/1000)
                firsty=int(rr.registers[2]/1000)
                angle = int(rr.registers[3])
                rospy.logwarn("Testt1")
                rospy.logwarn(firstx)
                rospy.logwarn(firsty)
                if firstx==10:
                    firstx=(rr.registers[1]-firstx*1000)
                else:
                    firstx=-(rr.registers[1]-firstx*1000)

                if firsty==10:
                    firsty=(rr.registers[2]-firsty*1000)
                else:
                    firsty=-(rr.registers[2]-firsty*1000)
                rospy.logwarn("Testt2")
                rospy.logwarn(firstx)
                rospy.logwarn(firsty)
                goalx = firstx/100.0  #Goalx
                goaly = firsty/100.0  #Goaly
                robot.mission_status.publish(robot.status)
                #Send info to planner trayectory to receive distance
                robot.newgoal.publish(Vector3(goalx,goaly,angle))
                robot.modbusmode["Battery"] = robot.batterypercentage
                robot.modbusmode["RobotStatus"] = robot.ro_status
                robot.modbusmode["Distance"] = robot.distancerobot
                myregisters = list(robot.modbusmode.values())
                robot.outputregister.data = [int(i) for i in myregisters]
                rospy.logwarn("Testt3")
                rospy.logwarn(goalx)
                rospy.logwarn(goaly)
                rospy.logwarn(robot.outputregister.data)
                rq = client.write_registers(3, robot.outputregister.data, unit=UNIT)     
                rospy.logwarn(robot.outputregister.data)
                client.close()
                rospy.sleep(1)
            except Exception as error:
                rospy.logwarn("Reading registers not ready")
                rospy.logwarn(error)  
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
