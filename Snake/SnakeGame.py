import sys, time, random, math, pygame
from pygame.locals import *
from MyLibrary import *


class Food(MySprite):   #食物类
    def __init__(self):
        MySprite.__init__(self)
        image = pygame.Surface((32,32)).convert_alpha()
        image.fill((255,255,255,0))
        pygame.draw.circle(image, (150,0,0), (16,16), 16, 0)
        self.set_image(image)
        MySprite.update(self, 0, 30) 
        self.X = random.randint(0,23) * 32
        self.Y = random.randint(0,17) * 32            #食物位置随机生成
        
class SnakeSegment(MySprite):          #画蛇方法，一个个的圆形，draw.circle
    def __init__(self,color=(50,50,50)):
        MySprite.__init__(self)
        image = pygame.Surface((32,32)).convert_alpha()
        image.fill((255,255,255,0))
        pygame.draw.circle(image, color, (16,16), 16 ,0)
        self.set_image(image)
        MySprite.update(self, 0, 30) 

class Snake():
    def __init__(self):
        self.velocity = Point(-1,0)
        self.old_time = 0
        head = SnakeSegment((200,100,0))   #画蛇
        head.X = 12*32
        head.Y = 9*32
        self.segments = list()           #放入列表
        self.segments.append(head)
        self.add_segment()               #添加蛇头
        self.add_segment()

    def update(self,ticks):
        if ticks > self.old_time + step_time:
            self.old_time = ticks
            #移动身体（改变位置）
            for n in range(len(self.segments)-1, 0, -1):
                self.segments[n].X = self.segments[n-1].X
                self.segments[n].Y = self.segments[n-1].Y
            #移动蛇头
            self.segments[0].X += self.velocity.x * 32
            self.segments[0].Y += self.velocity.y * 32

    def draw(self,surface):
        for segment in self.segments: 
            surface.blit(segment.image, (segment.X, segment.Y))
    
    def add_segment(self):
        last = len(self.segments)-1
        segment = SnakeSegment()
        start = Point(0,0)
        if self.velocity.x < 0:
            start.x = 32
        elif self.velocity.x > 0:
            start.x = -32
        if self.velocity.y < 0:
            start.y = 32
        elif self.velocity.y > 0:
            start.y = -32
        segment.X = self.segments[last].X + start.x
        segment.Y = self.segments[last].Y + start.y
        self.segments.append(segment)


def get_current_direction():
    global head_x,head_y     #蛇头位置设置为全局变量
    first_segment_x = snake.segments[1].X//32
    first_segment_y = snake.segments[1].Y//32
    
        


def get_food_direction():    #吃到食物时，身长增加
    global head_x,head_y     #蛇头位置设置为全局变量
    food = Point(0,0)
    for obj in food_group:
        food = Point(obj.X//32,obj.Y//32)

        

    

    
#初始化
def game_init():
    global screen, backbuffer, font, timer, snake, food_group  #设置全局变量

    pygame.init()
    screen = pygame.display.set_mode((24*32,18*32)) #分辨率适配
    pygame.display.set_caption("Snake Game")
    font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()
    backbuffer = pygame.Surface((screen.get_rect().width,screen.get_rect().height))

    #画蛇
    snake = Snake()
    image = pygame.Surface((60,60)).convert_alpha()
    image.fill((255,255,255,0))
    pygame.draw.circle(image, (80,80,220,70), (30,30), 30, 0)
    pygame.draw.circle(image, (80,80,250,255), (30,30), 30, 4)

    #挑战：添加食物
    food_group = pygame.sprite.Group()
    food = Food()
    food2 = Food()
    food3 = Food()
    food_group.add(food, food2, food3)



game_init()
game_over = False
last_time = 0

auto_play = False #初始化时关闭自动
step_time = 400

#主程序
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    #event section
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    elif keys[K_UP] or keys[K_w]:
        snake.velocity = Point(0,-1)
    elif keys[K_DOWN] or keys[K_s]:
        snake.velocity = Point(0,1)
    elif keys[K_LEFT] or keys[K_a]:
        snake.velocity = Point(-1,0)
    elif keys[K_RIGHT] or keys[K_d]:
        snake.velocity = Point(1,0)
    elif keys[K_SPACE]:
        step_time -= 10
    if game_over and keys[K_RETURN]:   #按回车重来
        game_over=False
        snake = Snake()
        image = pygame.Surface((60,60)).convert_alpha()
        image.fill((255,255,255,0))
        pygame.draw.circle(image, (80,80,220,70), (30,30), 30, 0)
        pygame.draw.circle(image, (80,80,250,255), (30,30), 30, 4)
        step_time = 400

    
    if not game_over:
        snake.update(ticks)
        food_group.update(ticks)
        
        
        hit_list = pygame.sprite.groupcollide(snake.segments, \
            food_group, False, True)
        if len(hit_list) > 0:
            food_group.add(Food())
            snake.add_segment()

        
        for n in range(1, len(snake.segments)):
            if pygame.sprite.collide_rect(snake.segments[0], snake.segments[n]):
                game_over = True

        
        head_x = snake.segments[0].X//32
        head_y = snake.segments[0].Y//32
        if head_x < 0 or head_x > 24 or head_y < 0 or head_y > 18:
            game_over = True
            

    

    
    backbuffer.fill((100,100,200)) 
    snake.draw(backbuffer)
    food_group.draw(backbuffer)
    screen.blit(backbuffer, (0,0))

    if not game_over:
        print_text(font, 0, 0, "Length " + str(len(snake.segments)))
        print_text(font, 0, 20, "Position " + str(snake.segments[0].X//32) + \
                   "," + str(snake.segments[0].Y//32))
    else:
        print_text(font, 0, 0, "GAME OVER")
        print_text(font, 0, 20, "Please press the 'return' button to continue")

        
   
    pygame.display.update() 
    


