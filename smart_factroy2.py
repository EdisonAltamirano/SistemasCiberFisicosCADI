#!/usr/bin/env python2
import time
import rospy
import tf
from std_msgs.msg import String,Int32,Int16 ,Float32
from std_msgs.msg import Int32MultiArray as HoldingRegister
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import *
from nav_msgs.msg import Path
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionGoal,MoveBaseActionResult
import math
import subprocess

initial_position = None
class StateMachine:
    def __init__(self):
        self.battery_status = rospy.Subscriber("voltage_percentage", Int32, self.batterycallback)
        self.distance_result = rospy.Publisher("distanceresult", Float32, queue_size=10) 
        self.mission_status = rospy.Subscriber("missionstatus",Int16 ,self.missioncallback)
        self.plan_distance = rospy.Subscriber("/move_base/NavfnROS/plan", Path, self.distance_callback)
        self.auto_recharge = rospy.Publisher("recharge_handle", Int16, queue_size=10) 
        self.goal_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=5)
        self.status_sub=rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.status_callback)
        self.robot_status =  rospy.Publisher("robot_status",Int16 ,queue_size=10) 
        self.newcoordinates = rospy.Subscriber('newcoordinates',Vector3,self.newcoordinates_callback)
        self.oldcoordinatex = 0.0
        self.oldcoordinatey = 0.0
        self.oldcoordinatez = 0.0
        self.distancegoal= 0.0
        self.cont=0
        self.batterypercentage=100
        self.manualmode=False
        self.newgoal = 0
        self.mission="Move"
        self.goal = MoveBaseActionGoal()
        self.nextmisssion=True
        self.newcoordinatesvec=Vector3()
        self.oldcoordinatesvec=Vector3(0,0,0)
        
        self.goal_path = [
            [-4.12106657028,1.06650936604,0.000000,0.000000,0.00000,-0.710403,0.703795],#Ax,Ay,Az,qx,qy,qz,qw
            [2.1205573082,0.788665294647,0.000000,0.000000,0.00000,-0.710403,0.703795],
            [-2.06468677521,7.17368368967,0.000000,0.000000,0.00000,-0.710403,0.703795]
        ]
        self.station=[
            [-5.91625070572,5.34506416321,0.000000,0.000000,0.00000,-0.710403,0.703795]
            ]
        self.current_node=None
    def newcoordinates_callback(self,data):
        self.newcoordinatesvec.x=data.x
        self.newcoordinatesvec.y=data.y
        self.newcoordinatesvec.z=data.z
    def distance_callback(self,data):
        if self.distancegoal==0.0 and self.mission=="Move":
            for i in range(len(data.poses)-1):
                self.distancegoal += math.sqrt(pow((data.poses[i+1].pose.position.x - data.poses[i].pose.position.x),2) + pow((data.poses[i+1].pose.position.y - data.poses[i].pose.position.y), 2))
            self.distance_result.publish(self.distancegoal)

    def status_callback(self, msg):
        state = msg.status.status
        if state == GoalStatus.SUCCEEDED:
            rospy.loginfo("Goal succeeded!")
            #Success mobile robot , change coordinate
            rospy.logwarn("I arrive")
            rospy.logwarn(self.newgoal)
            self.robot_status.publish(3)
            if self.manualmode==True:
                if self.newgoal<len(self.goal_path)-1:
                    self.newgoal +=1 
                else:
                    self.newgoal=0
            self.distancegoal=0.0
            if self.mission!=0:
                self.nextmisssion=1

        # elif state == GoalStatus.PREEMPTED:
        #     rospy.logwarn("Next coordinate Preempted")
        #     self.newgoal +=1 if self.newgoal<=1 else 0
        #     self.distancegoal=0.0
        elif state == GoalStatus.ABORTED or state == GoalStatus.REJECTED:
            #Couldn't reach objective
            self.robot_status.publish(4)
            rospy.logwarn("Next coordinate")
            if self.manualmode==True:
                if self.newgoal<len(self.goal_path)-1:
                    self.newgoal +=1 
                else:
                    self.newgoal=0
            self.distancegoal=0.0
            if self.mission!=0:
                self.nextmisssion=1
        
    def batterycallback(self, msg):
        self.batterypercentage=msg.data
    def missioncallback(self, msg):
        self.mission=msg.data
    def sendGoal2(self,goal_position):
        quaternion = Quaternion()
        self.goal.header.frame_id="map"
        self.goal.header.stamp=rospy.Time.now()
        self.goal.goal_id.stamp=rospy.Time.now()
        self.goal.goal_id.id=str(rospy.Time.now().to_sec())
        self.goal.goal.target_pose.header.frame_id = 'map'
        self.goal.goal.target_pose.header.stamp = rospy.Time.now()
        quaternion.x = float(goal_position[3])
        quaternion.y = float(goal_position[4])
        quaternion.z = float(goal_position[5])
        quaternion.w = float(goal_position[6])
        self.goal.goal.target_pose.pose.position.x = float(goal_position[0])
        self.goal.goal.target_pose.pose.position.y = float(goal_position[1])
        self.goal.goal.target_pose.pose.position.z = float(goal_position[2])
        self.goal.goal.target_pose.pose.orientation = quaternion
        self.goal_pub.publish(self.goal)
        rospy.logwarn(self.goal)
    def do_mission(self):
        self.auto_recharge.publish(0)
        listener = tf.TransformListener()
        if self.manualmode==True:
            angle = 30 * math.pi/180
            ax = self.goal_path[self.newgoal][0]
            ay = self.goal_path[self.newgoal][1]
        else:
            ax = self.newcoordinatesvec.x
            ay= self.newcoordinatesvec.y
            angle = self.newcoordinatesvec.z * math.pi/180
        a = [ ax, ay,0.000,0.000,0.000,0.000,0.000] #Ax,Ay,Az,qx,qy,qz,qw
        a[3] = 0.000
        a[4] = 0.000
        a[5] = math.sin(angle/2)
        a[6] = math.cos(angle/2)
        self.sendGoal2(a)
        rospy.sleep(3)
        '''
        if self.nextmisssion==1 and self.newcoordinatesvec != self.oldcoordinatesvec:
            self.sendGoal2(a)
            rospy.sleep(3)
            self.robot_status.publish(1)
            self.nextmisssion=0
            self.oldcoordinatesvec=self.newcoordinatesvec
        '''


        
        
    def go_chargestation(self):
        
        listener = tf.TransformListener()
        if self.manualmode==True:
            angle = 70 * math.pi/180
            ax = self.station[0][0]
            ay = self.station[0][1]
        else:
            angle = 30 * math.pi/180
            ax = self.newcoordinatesvec.x
            ay= self.newcoordinatesvec.y
        a = [ ax, ay,0.000,0.000,0.000,0.000,0.000] #Ax,Ay,Az,qx,qy,qz,qw
        a[3] = 0.000
        a[4] = 0.000
        a[5] = math.sin(angle/2)
        a[6] = math.cos(angle/2)
        if self.nextmisssion==1:
            self.sendGoal2(a)
            self.distancegoal = 0
            self.nextmisssion=2
        if self.mission==0 and self.nextmisssion==2:
            self.robot_status.publish(0)
            rospy.sleep(3)
            self.auto_recharge.publish(1)
        elif self.mission==1 or self.mission==2 and self.nextmisssion==2:
            self.nextmisssion=1
            

if __name__ == '__main__':
    try:
        rospy.init_node('statemachine')
        robot = StateMachine()
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown() and robot.batterypercentage>=30:
            if robot.mission==0:
                #Goto Charge self.station
                rospy.loginfo("Charging")
                robot.go_chargestation()
            elif robot.mission==1:
                #Goto next goal
                rospy.loginfo("Moving")
                robot.do_mission()
            elif robot.mission==4:
                #In Modula machine grab material
                #Include coordinates received from master machine  by modbus in python module
                robot.current_node = subprocess.Popen('exec ' + "python3 /home/eaibot/dashgo_ws/src/dashgo/xArm-Python-SDK/example/wrapper/xarm5/2001-move_joint.py", stdout=subprocess.PIPE, shell = True )  
                
            else:
                #Free Robot 
                rospy.loginfo("Nothing")
            r.sleep()
        #robot.current_node.terminate()
    except rospy.ROSInterruptException:
        rospy.logerr("Navigation test finished.")
