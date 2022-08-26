import pygame
import random
from pyModbusTCP.client import ModbusClient
import numpy as np
import time
pygame.init()
screen_x= 500
screen_y = 400
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
 
class Missions:
    #1:MissionStatus 0-Charge, 1-Move, 2-Free
    #2: #Goalx
    #3: #Goaly
    #4: Battery
    #5: RobotStatus 0-Charging, 1:Moving, 2:Free,3-Success,4-Failure
    #6: Distance
    #7: Locationx robot
    #8: Locationy robot
    #9: Goalxpi robot
    #10: Goalypi robot
    #11: Locationxpi robot
    #12: Locationypi robot
    def __init__(self):
        self.inforobot=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.missions = [[[584,176],[11412,10106]],[[355,175],[10212,10078]],[[528,405],[11206,10717]]]
    def change_mission(self):
        self.inforobot[0]=1
        mymission = random.choice(self.missions)
        #Goal Robot x,y
        self.inforobot[1] = mymission[1][0]
        self.inforobot[2] = mymission[1][1]
        #PI /Locationx,y
        self.inforobot[8] = mymission[0][0]
        self.inforobot[9] = screen_y - mymission[0][1]


class Button:
    def __init__(self, text,  pos, font):
        self.x, self.y = pos
        self.size=(100,50)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.title = text
        self.font = pygame.font.SysFont("Arial", font)
        self.color = 'black'
        self.oldcolor='black'
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
 
SERVER_HOST = "10.22.240.51"
SERVER_PORT = 12345
c = ModbusClient()
c.host(SERVER_HOST)
c.port(SERVER_PORT)
mission=Missions()
def mapping(x,game,ros):
    return (x*game)/ros
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
    while True:
        if not c.is_open():
            if not c.open():
                    print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
        if c.is_open():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                button1.click(event)
                button2.click(event)
                button3.click(event)
            #Read Battery / RobotStatus /Distance (Modbus)
            bits = c.read_holding_registers(0, 12)
            mission.inforobot[3]=bits[3]
            mission.inforobot[4] = bits[4]
            mission.inforobot[5] = bits[5] 
            #Map coordinate location to pi
            theta = np.radians(13)
            offsetx=7.9115512
            offsety=2.50132282
            rheight=11.29203556
            rwidth=17.69995916
            c1, s = np.cos(theta), np.sin(theta)
            R = np.array(((c1, -s), (s, c1)))
            #Convert bit +-
            mission.inforobot[10]=int(mapping(bits[6]+offsetx,screen_x,rwidth))
            mission.inforobot[11]=int(mapping(bits[7]+offsety,screen_y,rheight))
            #Update registers MissionStatus,Goalx,Goaly
            c.write_multiple_registers(0,[mission.inforobot[0],mission.inforobot[1],mission.inforobot[2]])
            c.write_multiple_registers(8,[mission.inforobot[8],mission.inforobot[9],mission.inforobot[10],mission.inforobot[11]])
            time.sleep(1)
        clock.tick(30)
        pygame.display.update()
 
 
button1 = Button(
    "Mision 1",
    (screen_x/2-50, 100),
    font=30)
 
button2 = Button(
    "Mision 2",
    (screen_x/2-50, 200),
    font=30)
 
button3 = Button(
    "Mision 3",
    (screen_x/2-50, 300),
    font=30)
 
mainloop()