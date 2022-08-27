import pygame    

pygame.init()# initializing the constructor
res = (769,500)# screen resolution
screen = pygame.display.set_mode(res)# opens up a window
color = (255,255,255)# white color
color_light = (170,170,170)# light shade of the button
color_dark = (100,100,100)# dark shade of the button
width = screen.get_width() # stores the width of the screen into a variable
height = screen.get_height()# stores the height of the screen into a variable
smallfont = pygame.font.SysFont('Corbel',35)  # defining a font
smallfont1 = pygame.font.SysFont('Corbel',50)
text = smallfont.render('quit' , True , color)# rendering a text written in this font
texto = smallfont1.render('TÍTULO' , True , (0,0,0))
fondo = pygame.image.load("D:/Descargas/fondo.jpeg").convert()

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        #checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:
            #if the mouse is clicked on the
            # button the game is terminated
            if 412+84 <= mouse[0] <= 412+150 and 3*height/4-20 <= mouse[1] <= 3*height/4-20+40:
                pygame.quit()
                  
    # fills the screen with a color
    screen.blit(fondo,(0,0))  
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
    
    # if mouse is hovered on a button it
    # changes to lighter shade
    pygame.draw.rect(screen,color_light,[width/2-82,height/6-1,160,50])
    if 412+84 <= mouse[0] <= 412+150+84 and 3*height/4-20 <= mouse[1] <= 3*height/4-20+40:
        pygame.draw.rect(screen,color_light,[412+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,(255,0,0),[412+84,3*height/4-20,150,40])
          
    else:
        pygame.draw.rect(screen,color_dark,[412+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,(255,0,0),[412+84,3*height/4-20,150,40])
        
    if 412-37-150+84 <= mouse[0] <= 412-37-150+150+84 and 3*height/4-20 <= mouse[1] <= 3*height/4-20+40:
        pygame.draw.rect(screen,(0,66,255),[412-37-150+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,color_light,[412-37-150+84,3*height/4-20,150,40])
          
    else:
        pygame.draw.rect(screen,(0,66,255),[412-37-150+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,color_dark,[412-37-150+84,3*height/4-20,150,40])
        
    if 412-37-150-37-150+84 <= mouse[0] <= 412-37+84-150-37-150+150 and 3*height/4-20 <= mouse[1] <= 3*height/4-20+40:
        pygame.draw.rect(screen,(0,66,255),[412-37-150-37-150+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,color_light,[412-37-150-37-150+84,3*height/4-20,150,40])
          
    else:
        pygame.draw.rect(screen,(0,66,255),[412-37-150-37-150+84-4,3*height/4-24,158,48])
        pygame.draw.rect(screen,(89,132,255),[412-37-150-37-150+84,3*height/4-20,150,40])
        
#    if 412-37-150-37-150+84 <= mouse[0] <= 412-37+84-150-37-150+150 and 3*height/4-20+100 <= mouse[1] <= 3*height/4-20+40:
 #       pygame.draw.rect(screen,color_light,[412-37-150-37-150+84,3*height/4-20,150,40])
          
  #  else:
    #    pygame.draw.ellipse(screen,(0,66,255),[412-37-150-37-150+84-4,3*height/4-24+80,158,70])
   #     pygame.draw.ellipse(screen,(89,132,255),[412-37-150-37-150+84,3*height/4-20+80,150,62])

      
    # superimposing the text onto our button
    screen.blit(text , (412+50+84,3*height/4-20))
    screen.blit(text,(412-37-150+50+84,3*height/4-20))
    screen.blit(text,(412-37-150-37-150+50+84,3*height/4-20))
    screen.blit(texto,(width/2-80,height/6))
      
    # updates the frames of the game
    pygame.display.update()