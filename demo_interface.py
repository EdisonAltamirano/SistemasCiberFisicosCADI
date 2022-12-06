import pygame
import random
from pyModbusTCP.client import ModbusClient
import numpy as np
import time
pygame.init()
screen_x= 500
screen_y = 600
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
myhost = "10.22.240.51"
myport = 12345
c = ModbusClient(host=myhost,port=myport)
class Missions:
    # Robot 1
    #1:MissionStatus 0-Charge, 1-Move, 2-Free
    #2: #Goalx
    #3: #Goaly
    #4: Angle
    #5: Battery
    #6: RobotStatus 0-Charging, 1:Moving, 2:Free,3-Success,4-Failure
    #7: Distance
    #8: Locationx robot
    #9: Locationy robot
    #10: Goalxpi robot
    #11: Goalypi robot
    #12: Locationxpi robot
    #13: Locationypi robot
    #14: PLC Communication
    # Robot Arm
    #15: Axis 1
    #16: Axis 2
    #17: Axis 3
    #18: Axis 4
    #19: Axis 5
    # Robot 2
    #20:MissionStatus 0-Charge, 1-Move, 2-Free
    #21: #Goalx
    #22: #Goaly
    #23: Angle
    #24: Battery
    #25: RobotStatus 0-Charging, 1:Moving, 2:Free,3-Success,4-Failure
    #26: Distance
    #27: Locationx robot
    #28: Locationy robot
    #29: Goalxpi robot
    #30: Goalypi robot
    #31: Locationxpi robot
    #32: Locationypi robot
    #33: PLC Communication
    # Robot Arm
    #34: Axis 1
    #35: Axis 2
    #36: Axis 3
    #37: Axis 4
    #38: Axis 5

    def __init__(self):
        self.inforobot=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.missions = [[[584,176],[11412,10106, 15]],[[355,175],[10212,10078, 0]],[[528,105],[11206,10717, 15]]]
        self.smart_missions = [[[584,176],[10754,10502, 8]],[[584,176],[10385,10360, 8]],[[584,176],[10342,10208, 0]],[[584,176],[10466,10595, 105]],[[584,176],[11071,11138, 100]]]
        self.unity_missions = [[[584,176],[11412,10106, 15]],[[355,175],[10212,10078, 0]],[[528,105],[11206,10717, 15]],[[584,176],[11380,10201, 105]],[[584,176],[11182,10024, 100]],[[584,176],[10139,10624, 100]]]
        self.come_back_coord = [[355,175],[10212,10078,60]]
        self.come_back_mission = [10,11,12]
        self.activate_plc = [11,22,33]
    def change_mission(self,index):
        if index in self.activate_plc:
            #Send PLC command
            self.inforobot[0]=2
            self.inforobot[13]=index
        else:
            #Robot 1
            self.inforobot[0]=1
            mymission = self.unity_missions[index]
            #Goal Robot x,y
            self.inforobot[1] = mymission[1][0]
            self.inforobot[2] = mymission[1][1]
            self.inforobot[3] = mymission[1][2]
            #PI /Locationx,y
            self.inforobot[9] = mymission[0][0]
            self.inforobot[10] = screen_y - mymission[0][1]
            #Robot 2
            self.inforobot[19]=1
            mymission = self.unity_missions[(len(self.unity_missions)-index-1)]
            #Goal Robot x,y
            self.inforobot[20] = mymission[1][0]
            self.inforobot[21] = mymission[1][1]
            self.inforobot[22] = mymission[1][2]
            #PI /Locationx,y
            self.inforobot[28] = mymission[0][0]
            self.inforobot[29] = screen_y - mymission[0][1]


class Button:
    def __init__(self, text,  pos, font,index):
        self.x, self.y = pos
        self.size=(200,50)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.title = text
        self.font = pygame.font.SysFont("Arial", font)
        self.color = 'black'
        self.oldcolor='black'
        self.index=index
        self.mymission=Missions()
    def show(self):
        self.surface = pygame.Surface(self.size)
        self.text = self.font.render(self.title, 1, pygame.Color("White"))
        while self.oldcolor == self.color:
            self.color = random.choice(['black','blue','green','orange','red'])
        self.surface.fill(self.color)
        self.oldcolor = self.color
        self.surface.blit(self.text, (0, 0))
        screen.blit(self.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.show()
                    self.mymission.change_mission(self.index)
                    self.send_info()
    def send_info(self):
        if c.open():
            #Robot1
            #Read Battery / RobotStatus /Distance (Modbus)
            bits = c.read_holding_registers(0, 13)
            self.mymission.inforobot[4]=bits[4]
            self.mymission.inforobot[5] = bits[5]
            self.mymission.inforobot[6] = bits[6] 
            #Update registers self.mymissionStatus,Goalx,Goaly
            c.write_multiple_registers(0,[self.mymission.inforobot[0],self.mymission.inforobot[1],self.mymission.inforobot[2],self.mymission.inforobot[3]])
            c.write_multiple_registers(9,[self.mymission.inforobot[9],self.mymission.inforobot[10]])
            c.write_multiple_registers(13,[self.mymission.inforobot[13]])
            #Robot2
            #Read Battery / RobotStatus /Distance (Modbus)
            bits = c.read_holding_registers(19, 37)
            self.mymission.inforobot[23]=bits[4]
            self.mymission.inforobot[24] = bits[5]
            self.mymission.inforobot[25] = bits[6] 
            #Update registers self.mymissionStatus,Goalx,Goaly
            c.write_multiple_registers(19,[self.mymission.inforobot[19],self.mymission.inforobot[20],self.mymission.inforobot[21],self.mymission.inforobot[22]])
            c.write_multiple_registers(28,[self.mymission.inforobot[28],self.mymission.inforobot[29]])
            c.write_multiple_registers(32,[self.mymission.inforobot[32]])
        else:
            print("unable to connect to "+myhost+":"+str(myport))

def mapping(x,game,ros):
    return (x*game)/ros
def map_conversion():
    if c.open():
        #Robot1
        #Read Battery / RobotStatus /Distance (Modbus)
        bits = c.read_holding_registers(0, 12)
        #Map coordinate location to pi
        theta = np.radians(13)
        offsetx=7.9115512
        offsety=2.50132282
        rheight=11.29203556
        rwidth=17.69995916
        c1, s = np.cos(theta), np.sin(theta)
        R = np.array(((c1, -s), (s, c1)))
        #Convert bit +-
        #Transform modbus coordinate 10->Positive; 11->Negative
        firstx=int(bits[7]/1000)
        firsty=int(bits[8]/1000)
        if firstx==10:
            firstx=(bits[7]-firstx*1000)
        else:
            firstx=-(bits[7]-firstx*1000)

        if firsty==10:
            firsty=(bits[8]-firsty*1000)
        else:
            firsty=-(bits[8]-firsty*1000)
        goalx = firstx/100.0  #Goalx
        goaly = firsty/100.0  #Goaly
        localx=int(mapping(goalx+offsetx,screen_x,rwidth))
        localy=int(mapping(goaly+offsety,screen_y,rheight))
        c.write_multiple_registers(11,[localx,localy])
        #Robot2
        #Read Battery / RobotStatus /Distance (Modbus)
        bits2 = c.read_holding_registers(19, 37)
        #Map coordinate location to pi
        theta = np.radians(13)
        offsetx=7.9115512
        offsety=2.50132282
        rheight=11.29203556
        rwidth=17.69995916
        c1, s = np.cos(theta), np.sin(theta)
        R = np.array(((c1, -s), (s, c1)))
        #Convert bit +-
        #Transform modbus coordinate 10->Positive; 11->Negative
        firstx=int(bits2[7]/1000)
        firsty=int(bits2[8]/1000)
        if firstx==10:
            firstx=(bits2[7]-firstx*1000)
        else:
            firstx=-(bits2[7]-firstx*1000)

        if firsty==10:
            firsty=(bits2[8]-firsty*1000)
        else:
            firsty=-(bits2[8]-firsty*1000)
        goalx = firstx/100.0  #Goalx
        goaly = firsty/100.0  #Goaly
        localx=int(mapping(goalx+offsetx-0.5,screen_x,rwidth))
        localy=int(mapping(goaly+offsety-0.5,screen_y,rheight))
        c.write_multiple_registers(30,[localx,localy])
    else:
        print("unable to connect to "+myhost+":"+str(myport))

def mainloop():
    pygame.display.set_caption('SmartFactory Demo')
    Icon = pygame.image.load('LogoSF.jpg')
    font1 = pygame.font.SysFont('chalkduster.ttf', 36)
    screen.blit(pygame.image.load("fondo.png"), (10 ,10))
    img1 = font1.render('SmartFactory Demo', True, 'red')
    screen.blit(img1, (130, 50))
    pygame.display.set_icon(Icon)
    button1.show()
    button2.show()
    button3.show()
    button4.show()
    button5.show()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
            button4.click(event)
            button5.click(event)
        
        map_conversion()

        clock.tick(30)
        pygame.display.update()
"""
button1 = Button(
    "Ir a modula",
    (screen_x/2-100, 100),
    font=30,
    index= 0)
button2 = Button(
    "Entregar paquete",
    (screen_x/2-100, 200),
    font=30,
    index=1)
 
button3 = Button(
    "Sacar paquete",
    (screen_x/2-100,300),
    font=30,
    index=2)
 
button4 = Button(
    "Entregar Yummy",
    (screen_x/2-100, 400),
    font=30,
    index= 3)
button5 = Button(
    "Carga",
    (screen_x/2-100, 500),
    font=30,
    index= 4)
"""
button1 = Button(
    "Mision1",
    (screen_x/2-100, 100),
    font=30,
    index= 0)
button2 = Button(
    "Mision2",
    (screen_x/2-100, 200),
    font=30,
    index=1)
 
button3 = Button(
    "Mision3",
    (screen_x/2-100,300),
    font=30,
    index=2)
 
button4 = Button(
    "Mision4",
    (screen_x/2-100, 400),
    font=30,
    index= 3)
button5 = Button(
    "Pick",
    (screen_x/2-100, 500),
    font=30,
    index= 11)
mainloop()