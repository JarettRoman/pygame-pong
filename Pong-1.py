try:
    import sys, os, math, random
    import pygame
    from pygame.locals import *
    
except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    import sys
    sys.exit(1)

class Game(object):
    """Our game object!  This is a fairly simple object that handles the initialization of
    pygame and sets up our game to run."""
    def __init__(self):
        """Called when the Game object is initialized.  Initializes pygame and sets up our
        pygame window and other pygame tools that we will need for more complicated
        tutorials"""
        
        #load and set up pygame
        pygame.init()
        
        #create our window
        self.window = pygame.display.set_mode((800,400))
        
        #clock for ticking
        self.clock = pygame.time.Clock()
        
        #set window title
        pygame.display.set_caption("Pygame tutorial 3 - Pong")
        
        #tell pygame to only pay attention to certain events
        #we want ot know if the user hits the X on the window, and we
        #want keys so we can close the window with the esc key
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        
        #make background -- all white, with black line down the middle
        self.background = pygame.Surface((800,400))
        self.background.fill((255,255,255))
        #draw the line vertically down the center
        pygame.draw.line(self.background, (0,0,0), (400,0), (400,400), 2)
        self.window.blit(self.background, (0,0))
        #flip the display so the background is on there
        pygame.display.flip()
        
        #a sprite rending group for our ball and paddles
        self.sprites = pygame.sprite.RenderUpdates()
        
        #create our paddles and add to sprite group
        self.leftpaddle = Paddle((50,200))
        self.sprites.add(self.leftpaddle)
        self.rightpaddle = Paddle((750,200))
        self.sprites.add(self.rightpaddle)
        
        #create ball
        self.ball = Ball((400,200))
        self.sprites.add(self.ball)
        
        #score image
        self.scoreImage = Score((400,50))
        self.sprites.add(self.scoreImage)
        
        self.pingsound = pygame.mixer.Sound(os.path.join('sound','ping.wav'))
        self.pongsound = pygame.mixer.Sound(os.path.join('sound','pong.wav'))
    
    def run(self):
        """Runs the game.  Contains the game loop that computes and renders each frame."""
        
        print 'Starting Event Loop'
        
        running = True
        #run until something tells us to stop
        while running:
            #tick pygame clock
            #you can limit the fps by passing the desired frames per second through tick()
            self.clock.tick(60)
            
            #hanlde pygame events -- if users closes game, stop running
            running = self.handleEvents()
            
            #render the screen, even though we don't have anything happening right now
            pygame.display.set_caption('Pygame Tutorial 3 - Pong   %d fps' % self.clock.get_fps())
            
            #update our sprites
            for sprite in self.sprites:
                sprite.update()
                
            #render our sprites
            self.sprites.clear(self.window, self.background)    #clears the window where the sprites currently are, using the background
            dirty = self.sprites.draw(self.window)              #calculates the 'dirty' rectangles that need to be redrawn
            
            #blit the dirty areas of the screen
            pygame.display.update(dirty)                        #updates just the 'dirty' areas
            
            #handle ball -- all our ball management here
            self.manageBall()
        
        print 'Quitting. Thanks for playing'
        
    def manageBall(self):
        """This basically runs the game.  Moves the ball and hadnles wall and paddle collisions."""
        
        #move the ball according to its velocity
        self.ball.rect.x += self.ball.velx
        self.ball.rect.y += self.ball.vely
        
        #check if ball is off the top
        if self.ball.rect.top < 0:
            self.pongsound.play()
            self.ball.rect.top = 1
            
            #reverse Y velocity so it bounces
            self.ball.vely *= -1
            
        #check if ball is off the bottom
        elif self.ball.rect.bottom > 400:
            self.pongsound.play()
            self.ball.rect.bottom = 399
            
            #reverse Y velocity so it 'bounces'
            self.ball.vely *= -1
            
        
        #check if the ball hits the left side -- point for right!
        if self.ball.rect.left < 0:
            #keep score
            self.scoreImage.right()
            
            #reset ball
            self.ball.reset()
            return
        
        #check if the ball htis the right sid e-- point for left!
        elif self.ball.rect.right > 800:
            #keep score
            self.scoreImage.left()
            
            #reset ball
            self.ball.reset()
            return
        
        #check for collisions with the paddles using pygame's collision functions
        collided = pygame.sprite.spritecollide(self.ball, [self.leftpaddle, self.rightpaddle], dokill=False)
        
        #if the ball hit a paddle, it will be in the collided list
        if len(collided) > 0:
            self.pingsound.play()
            hitpaddle = collided[0]
            
            #reverse the x velocity on the ball
            self.ball.velx *= -1
            
            #need to make srue the ball is no longer int he paddle -- goign to move it again manually
            self.ball.rect.x += self.ball.velx
            
             #give a little of the paddle's velocity to the ball
            self.ball.vely += hitpaddle.velocity/3.0
            
       
        
        
        
    def handleEvents(self):
        """Poll for PyGame events and behave accordingly.  Return false to stop the event loop and end the game."""
        
        #poll fo rpygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            #handle user input
            elif event.type == KEYDOWN:
                #if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False
                
                #paddle control
                if event.key == K_w:
                    self.leftpaddle.up()
                if event.key == K_s:
                    self.leftpaddle.down()
                
                if event.key == K_UP:
                    self.rightpaddle.up()
                if event.key == K_DOWN:
                    self.rightpaddle.down()
                    
                if event.key == K_SPACE:
                    if self.ball.velx == 0 and self.ball.vely == 0:
                        self.ball.serve()
            
            elif event.type == KEYUP:
                #paddle control
                if event.key == K_w:
                    self.leftpaddle.down()
                if event.key == K_s:
                    self.leftpaddle.up()
                    
                if event.key == K_UP:
                    self.rightpaddle.down()
                if event.key == K_DOWN:
                    self.rightpaddle.up()
            
                
        return True
    
class Paddle(pygame.sprite.Sprite):
    """A paddle sprite.  Subclasses the pygame sprite class.
    Handles its own position so it will not go off the screen."""
    
    def __init__(self, xy):
        #initialize the pygame sprite part
        pygame.sprite.Sprite.__init__(self)
        #set image and rect
        self.image = pygame.image.load(os.path.join('images','pong_paddle.gif'))
        self.rect = self.image.get_rect()
        
        #set position
        self.rect.centerx, self.rect.centery = xy
        
        #the movement speed of our paddle
        self.movementspeed = 5
        
        #the current velocity of the paddle -- can only move in Y direction
        self.velocity = 0
    
    def up(self):
        """increases the vertical velocity"""
        self.velocity -= self.movementspeed
        
    def down(self):
        """decreases the vertical velocity"""
        self.velocity += self.movementspeed
        
    def move(self, dy):
        """move the paddle in the y direction.  Don't go out the top or bottom."""
        if self.rect.bottom + dy > 400:
            self.rect.bottom = 400
        elif self.rect.top + dy < 0:
            self.rect.top = 0
        else:
            self.rect.y += dy
            
    def update(self):
        """Called to updat ethe sprite.  Do this every frame.  Handles moving the sprite by its velocity"""
        self.move(self.velocity)
        
class Ball(pygame.sprite.Sprite):
    """A ball sprite.  Subclasses the pygame sprite class."""
    
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'pong_ball.gif'))
        self.rect = self.image.get_rect()
        
        self.rect.centerx, self.rect.centery = xy
        self.maxspeed = 10
        self.servespeed = 5
        self.velx = 0
        self.vely = 0
        
    def reset(self):
        """Put the ball back in the middle and stop it fro moving"""
        self.rect.centerx, self.rect.centery = 400, 200
        self.velx = 0
        self.vely = 0
        
    def serve(self):
        angle = random.randint(-45, 45)
        
        #if close to zero, adjust again)
        if abs(angle) < 5 or abs(angle-180) < 5:
            angle = random.randint(10,20)
            
        #pick a side with a random call
        if random.random() > .5:
            angle += 180
            
        # do the trig to get the x and y components
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        
        self.velx = self.servespeed * x
        self.vely = self.servespeed * y
        
class Score(pygame.sprite.Sprite):
    """A sprite for the score."""
    
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        
        self.xy = xy    #save xy -- will center our rect on it when we change the score
        
        self.font = pygame.font.Font(None, 50)  #load the default font, size 50
        
        self.leftscore = 0
        self.rightscore = 0
        self.reRender()
        
    def update(self):
        pass
    
    def left(self):
        """Adds a point ot the left side score."""
        self.leftscore += 1
        self.reRender()
        
    def right(self):
        """Adds a point to the right side score."""
        self.rightscore += 1
        self.reRender()
        
    def reset(self):
        """Resets the scores to zero."""
        self.leftscore = 0
        self.rightscore = 0
        self.reRender()
        
    def reRender(self):
        """Updates the score.  Renders a new image and re-centers at the initial coordinates."""
        self.image = self.font.render("%d    %d"%(self.leftscore, self.rightscore), True, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.xy
    
    
#create game and run it
if __name__ == '__main__':
    game = Game()
    game.run()
            