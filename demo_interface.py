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

    # mision2: 
    # position: 
    # x: 3.42990972043
    # y: 2.0819644574
    # z: 0.138
    # orientation: 
    # x: 0.0
    # y: 0.0
    # z: -0.0661802246268
    # w: 0.997807685813
    # mision1:
    # position: 
    # x: 3.94221117048
    # y: 3.67269146655
    # z: 0.138
    # orientation: 
    # x: 0.0
    # y: 0.0
    # z: -0.105558523392
    # w: 0.994413092301
    # mision yumi: 
    # position: 
    # x: 4.85615631865
    # y: 6.13694085073
    # z: 0.138
    # orientation: 
    # x: 0.0
    # y: 0.0
    # z: 0.641184667524
    # w: 0.767386618421
    # modula:
    # position: 
    # x: 7.54760425418
    # y: 5.02011003048
    # z: 0.138
    # orientation: 
    # x: 0.0
    # y: 0.0
    # z: -0.0694481228828
    # w: 0.997585564364
    # charging:
    # position: 
    # x: -0.582173010534
    # y: -1.86394989796
    # z: 0.138
    # orientation: 
    # x: 0.0
    # y: 0.0
    # z: -0.769825721204
    # w: 0.638254149202
    def __init__(self):
        self.inforobot=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.missions = [[[584,176],[11412,10106, 15]],[[355,175],[10212,10078, 0]],[[528,105],[11206,10717, 15]]]
        self.smart_missions = [[[584,176],[10754,10502, 8]],[[584,176],[10385,10360, 8]],[[584,176],[10342,10208, 0]],[[584,176],[10466,10595, 105]],[[584,176],[11071,11138, 100]]]
        self.come_back_coord = [[355,175],[10212,10078,60]]
        self.come_back_mission = [10,11,12]
        self.activate_plc = [11,22,33]
    def change_mission(self,index):
        if index in self.activate_plc:
            #Send PLC command
            self.inforobot[0]=2
            self.inforobot[13]=index
        else:
            self.inforobot[0]=1
            mymission = self.smart_missions[index]
            #Goal Robot x,y
            self.inforobot[1] = mymission[1][0]
            self.inforobot[2] = mymission[1][1]
            self.inforobot[3] = mymission[1][2]
            #PI /Locationx,y
            self.inforobot[9] = mymission[0][0]
            self.inforobot[10] = screen_y - mymission[0][1]


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
            #Read Battery / RobotStatus /Distance (Modbus)
            bits = c.read_holding_registers(0, 13)
            self.mymission.inforobot[4]=bits[4]
            self.mymission.inforobot[5] = bits[5]
            self.mymission.inforobot[6] = bits[6] 
            #Update registers self.mymissionStatus,Goalx,Goaly
            c.write_multiple_registers(0,[self.mymission.inforobot[0],self.mymission.inforobot[1],self.mymission.inforobot[2],self.mymission.inforobot[3]])
            time.sleep(1)
            c.write_multiple_registers(9,[self.mymission.inforobot[9],self.mymission.inforobot[10]])
            c.write_multiple_registers(13,[self.mymission.inforobot[13]])
        else:
            print("unable to connect to "+myhost+":"+str(myport))

def mapping(x,game,ros):
    return (x*game)/ros
def map_conversion():
    if c.open():
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
mainloop()