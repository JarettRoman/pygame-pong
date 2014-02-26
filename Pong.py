try:
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
        self.window = pygame.display.set_mode((800,600))
        
        #clock for ticking
        self.clock = pygame.time.Clock()
        
        #set window title
        pygame.display.set_caption("Pygame tutorial 2 - Basic")
        
        #tell pygame to only pay attention to certain events
        #we want ot know if the user hits the X on the window, and we
        #want keys so we can close the window with the esc key
        pygame.event.set_allowed([QUIT, KEYDOWN])
    
    
    def run(self):
        """Runs the game.  Contains the game loop that computes and renders each frame."""
        
        print 'Starting Event Loop'
        
        running = True
        #run until something tells us to stop
        while running:
            #tick pygame clock
            #you can limit the fps by passing the desired frames per second through tick()
            self.clock.tick()
            
            #hanlde pygame events -- if users closes game, stop running
            running = self.handleEvents()
            
            #render the screen, even though we don't have anything happening right now
            pygame.display.set_caption('Pygame Tutorial 2 - Basic   %d fps' % self.clock.get_fps())
            
            #render the screen, evne though we don't have anything going on right now
            pygame.display.flip()
        
        print 'Quitting. Thanks for playing'
        
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
        return True
    

#create game and run it
if __name__ == '__main__':
    game = Game()
    game.run()
            