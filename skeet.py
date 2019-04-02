"""
File: skeet.py

Completed by: Cu La
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15

class Point():
    """ This class handles the positions of the game objects"""
    def __init__(self):
        self.x = 0
        self.y = 0

class Velocity():
    """ This class handles the velocity of the game moving objects """
    def __init__(self):
        self.dx = 0
        self.dy = 0

class flyingObject():
    """ This is the parent class for the game flying objects """
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True;

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
    def is_off_screen(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        offScreen = False
        if self.center.x > SCREEN_WIDTH or self.center.x < 0:
            offScreen = True
        elif self.center.y > SCREEN_HEIGHT or self.center.y < 0:
            offScreen = True

        return offScreen
              
class Target(flyingObject):
    """This is a child of flyingObject, and the parent of the target types"""
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(SCREEN_WIDTH/2, SCREEN_WIDTH - 40)
        self.velocity.dx = random.uniform(1/3, 5/3)
        self.velocity.dy = random.uniform(-2/3, 5/3)

    """
        This portion is to make the targets bounce against each other
        instead of overlapping. However, I haven't figured out all the physics
        yet, so the bouncing is rather eratic. Thus it is commented out for now.
        But there is no bug! Un-commnet anytime to try it out
    """

    # def bounce(self):
    #     self.velocity.dx *= -1
    #     self.velocity.dy *= -1

class SafeTarget(Target):
    """ A shy child of the Target class, and grandchild of flyingObject class"""
    def __init__(self):
        super().__init__()
        self.hitPoint = 1
        self.radius = TARGET_SAFE_RADIUS

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_SAFE_COLOR)

    def hit(self):
        self.hitPoint -= 1
        if self.hitPoint <= 0:
            self.scoreValue = -10
            self.alive = False

        return self.scoreValue

class StrongTarget(Target):
    """ A strong child of the Target class, and grandchild of flyingObject class"""
    def __init__(self):
        super().__init__()
        self.velocity.dx = random.uniform(1/3, 3/3) 
        self.velocity.dy = random.uniform(-2/3, 3/3)
        self.hitPoint = 3
        self.radius = 40

    def draw(self):
        arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.hitPoint), text_x, text_y, TARGET_COLOR, font_size=20)

    def hit(self):
        self.hitPoint -= 1
        self.scoreValue = 1
        self.radius -= 10       # This makes the strong target smaller every time it is hit
        if self.hitPoint <= 0:
            self.alive = False
            self.scoreValue = 3

        return self.scoreValue

class StandardTarget(Target):
    """ A boring child of the Target class, and grandchild of flyingObject class"""
    def __init__(self):
        super().__init__()
        self.hitPoint = 1
        self.radius = TARGET_RADIUS

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)

    def hit(self):
        self.hitPoint -= 1
        if self.hitPoint <= 0:
            self.alive = False
            self.scoreValue = 1

        return self.scoreValue

class Bullet(flyingObject):
    """ A child of the flyingObject class, and handles the logic of bullets"""
    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
    
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BULLET_RADIUS, BULLET_COLOR)

    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED

class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """
        # TODO: Decide what type of target to create and append it to the list
        onTop = False

        typeRoller = random.randint(1, 3)
        if typeRoller == 1:
            standard = StandardTarget()
            """
            This is the logic that prevents the targets from spawning
            on top of existing ones.
            """
            for target in self.targets:
                too_close = standard.radius + target.radius
                if (abs(standard.center.x - target.center.x) < too_close and
                        abs(standard.center.y - target.center.y) < too_close):
                    onTop = True
            if onTop == False:
                self.targets.append(standard)
        elif typeRoller == 2:
            strong = StrongTarget()
            """
            This is the logic that prevents the targets from spawning
            on top of existing ones.
            """
            for target in self.targets:
                too_close = strong.radius + target.radius
                if (abs(strong.center.x - target.center.x) < too_close and
                        abs(strong.center.y - target.center.y) < too_close):
                    onTop = True
            if onTop == False:
                self.targets.append(strong)
        elif typeRoller == 3:
            safe = SafeTarget()
            """
            This is the logic that prevents the targets from spawning
            on top of existing ones.
            """
            for target in self.targets:
                too_close = safe.radius + target.radius
                if (abs(safe.center.x - target.center.x) < too_close and
                        abs(safe.center.y - target.center.y) < too_close):
                    onTop = True
            if onTop == False:
                self.targets.append(safe)


    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()


        """
        This portion is to make the targets bounce against each other
        instead of overlapping. However, I haven't figured out all the physics
        yet, so the bouncing is rather eratic. Thus it is commented out for now.
        But there is no bug! Un-comment anytime to try it out.
        """

        # for a in range(len(self.targets) - 1):
        #     for b in range(1, len(self.targets)):
        #         too_close = self.targets[a].radius + self.targets[b].radius
        #         if a != b:
        #             if (abs(self.targets[a].center.x - self.targets[b].center.x) < too_close and
        #                     abs(self.targets[a].center.y - self.targets[b].center.y) < too_close):
        #                 self.targets[a].bounce()
        #                 self.targets[b].bounce()


                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        Note: This could be a static method, but we haven't
        discussed them yet...
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()