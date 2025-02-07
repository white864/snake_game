import pygame
import random
import os

FPS=10
score = 0
LIGHTSKYBLUE=(135,206,250)
RED=(255,0,0)
GREEN=(0,255,0)
BLACK=(0,0,0)
WHITE=(255,255,255)
YELLOW=(255,255,87)
PINK=(255,140,250)
GREEN_BLUE=(10,209,139)
GREY=(150,150,150)
DEEPPINK1=(255,20,147)
NAVYBLUE=(0,0,128)
DARK_YELLOW = (200, 180, 0)

HEIGHT=600
WIDTH=700

#遊戲初始化 and 創建視窗
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("貪食蛇遊戲")
clock=pygame.time.Clock()  #經過一段時間後才會跑下一次迴圈
running=True

# 讀取儲存檔案(白)
save_path = os.path.join('file', 'save.txt')

# 確保目錄存在 (避免 'file' 資料夾不存在的錯誤)
os.makedirs('file', exist_ok=True)

# 如果檔案不存在，建立一個新的並寫入預設分數
if not os.path.exists(save_path):
    with open(save_path, 'w') as file:
        file.writelines(["0\n"] * 5)  # 建立預設排行榜 (5 筆 0 分數)

# 讀取儲存檔案
with open(save_path, 'r') as file:
    SCORE_SAVE = file.readlines()

# 移除換行符並確保內容都是數字
SCORE_SAVE = [line.strip() for line in SCORE_SAVE if line.strip().isdigit()]

#蛇的設定
snake_size=16
snake_speed=20
snake_body=[(80,100),(60,100),(40,100)]
snake_head=snake_body[0]
snake_len=len(snake_body)

snake_color=BLACK
food_color=DEEPPINK1
score_color=NAVYBLUE

#食物
class Food():
    def __init__(self,x,y):
        self.image=pygame.Surface((18,18))
        self.image.fill(food_color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        screen.blit(self.image,self.rect)
# 隨機生成食物的函數 (lee)
def generate_food():
    while True:
        x = random.randint(0, WIDTH // snake_size - 1) * snake_size
        y = random.randint(0, HEIGHT // snake_size - 1) * snake_size
        if (x, y) not in snake_body:  # 確保食物不生成在蛇的身體上
            return Food(x, y)

# 初始化食物 (lee)
food = generate_food()

# 顯示文字函數
def text_draw(text, font, color, x,y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))

# 遊戲字形設定
score_font = pygame.font.SysFont('Bauhaus 93', 40)  # 分數字形
title_font = pygame.font.SysFont('Bauhaus 93', 70)  # title 字形
rules_font = pygame.font.SysFont('Bauhaus 93', 25)  # rule 字形
start_font = pygame.font.SysFont('Bauhaus 93', 35)  # start 字形
die_font = pygame.font.SysFont('Bauhaus 93', 55)  # start 字形
c_font = pygame.font.SysFont('Bauhaus 93', 25)    # 繼續字形
rank_font = pygame.font.SysFont('Bauhaus 93', 45)
new_record_font = pygame.font.SysFont('Bauhaus 93', 30)

# 遊戲主畫面內容設定
title = 'Greedy Snake'
rules = '[WASD] to control the Snake!'
start = 'PRESS [SPACE] TO START'
Fake_snake = [(520,222),(500,222),(480,222),(460,222)]

# 死亡顯示畫面設定
die = 'YOU ARE DEAD!!'
score_text = 'YOUR SCROE: '
Continue = 'PRESS [SPACE] TO CONTINUE'


# 遊戲迴圈前置設定
running = True
direction = 1       # 預設往右移動
food_check = False  # 確認是否有食物
menu = 0            # 畫面

save = False        # 使否已儲存分數
new_record = 99     # 進到榜單的名次
new_high = False    # 是否破紀錄

       

#遊戲迴圈
while running:
    clock.tick(FPS)  #一秒鐘之內最多執行幾次

    #取得輸入
    for event in pygame.event.get():  #回傳發生的多個事件
        if event.type==pygame.QUIT:   #事件的類型
            running=False

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE) and (menu != 1):
                menu += 1
   
    #更新遊戲
    screen.fill((LIGHTSKYBLUE))  #RGB
    pygame.display.flip()



 # 顯示主菜單
    if menu==0:
        text_draw(title,title_font,NAVYBLUE, 140,HEIGHT/4)           # 印出標題
        text_draw(rules,rules_font,GREY, 200,360)                       # 印出規則
        text_draw(start,start_font,GREEN_BLUE, 170,(WIDTH/3)*2) # 印出開始
        for i in range(len(Fake_snake)):                                # 印出假蛇
            pygame.draw.rect(screen, snake_color, pygame.Rect(Fake_snake[i][0],Fake_snake[i][1],snake_size, snake_size))
            pygame.display.flip()

        # 初始化遊戲
        snake_body = [(80,100),(60,100),(40,100)]   # 蛇身體
        snake_head = snake_body[0]                  # 蛇頭
        direction = 1
        food_check = False
        save = False
        score = 0
        new_record = 99
        new_high = False

#范宇辰start
    elif menu==1:
       
        # 取得蛇移動方向
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d] and (direction !=2):    # 往右
            direction = 1  
        if key_pressed[pygame.K_a] and (direction !=1):    # 往左
            direction = 2
        if key_pressed[pygame.K_w] and (direction !=4):    # 往上
            direction = 3
        if key_pressed[pygame.K_s] and (direction !=3):    # 往下
            direction = 4


       
        # 蛇移動
        if direction == 1:
            snake_head = (snake_head[0]+snake_speed, snake_head[1])
        elif direction == 2:
            snake_head = (snake_head[0]-snake_speed, snake_head[1])
        elif direction == 3:
            snake_head = (snake_head[0], snake_head[1]-snake_speed)
        elif direction == 4:
            snake_head = (snake_head[0], snake_head[1]+snake_speed)

        # 檢測撞牆 (lee)
        if (
            snake_head[0] < 0 or snake_head[0] >= WIDTH or
            snake_head[1] < 0 or snake_head[1] >= HEIGHT
        ):
            menu = 2  # 切換到死亡畫面

        # 檢測撞到自己 (lee)
        if snake_head in snake_body:
            menu = 2  # 切換到死亡畫面

        # 蛇頭 Rect設定
        head_rect = pygame.Rect(snake_head[0],snake_head[1],snake_size,snake_size)  # 蛇頭 Rect設定
        for body in snake_body :
            pygame.draw.rect(screen, snake_color, pygame.Rect(body[0], body[1], snake_size, snake_size))
            pygame.display.flip()
        snake_body.insert(0,snake_head)
        snake_body.pop()


        # 檢查蛇是否吃到食物 (lee)
        if head_rect.colliderect(food.rect):
            score += 1
            tail = snake_body[-1]         # 獲取當前尾巴的座標
            snake_body.append(tail)       # 在尾巴新增一節
            food = generate_food()
        

        # 更新食物和分數 (lee)
        food.update()
        text_draw(f"Score: {score}", score_font, score_color, 10, 10)

    elif menu == 2:  

        if  save == False:  #排名(白)
            change_index = 0
            save_sure = False
            for i in range(5):
                if int(SCORE_SAVE[i]) <= score :          # 如果原始分數<=新分數

                    if int(SCORE_SAVE[i]) == score:       # 相同分數不增加紀錄
                        new_record = i
                        break

                    if i == 4:                             # 如果新分數是第五名
                        SCORE_SAVE[i]=str(score)           # 將新分數加入排行榜(覆蓋原儲存分數) 
                        new_record = i
                        break
                    else:
                        if i == 0:                         # 檢查是否破紀錄
                            new_high = True
                        new_record = i
                        save_sure = True                   # 是否確定儲存
                        change_index = i                   # 要加入排行的名次
                        break


        # 更新儲存分數(白)
        index = 4                                      # 最後排行開始更新
        while save_sure:
            if index == 4:                             # 最後一名(第五名)更新
                st = SCORE_SAVE[index-1].strip()
                SCORE_SAVE[index]= st
                #print(st)
            elif index==change_index:                  # 到達要更換(刷新)的名次
                SCORE_SAVE[index]=str(score)+'\n'
                save_sure = False
            else:                                      # 其他名次更新
                SCORE_SAVE[index]=SCORE_SAVE[index-1]
            index -= 1
                
        # 回傳給檔案(白)
        with open(os.path.join('file', 'save.txt'), 'w') as file:
            file.writelines([f"{x}\n" for x in SCORE_SAVE])
                
        save = True

        # 死亡畫面 (lee)
        screen.fill((RED))
        text_draw(die, die_font, WHITE, WIDTH // 4, HEIGHT // 3)
        text_draw(f"{score_text} {score}", score_font, WHITE, WIDTH // 4, HEIGHT // 2)
        text_draw(Continue, c_font, WHITE, WIDTH // 4, HEIGHT // 1.5)

        # 顯示排行分數(白)
        for i in range(5):
            n = i+1
            text_draw(f'No.{n}: ', rank_font, GREY, 500, 170 + 48 * i)
            text_draw(str(SCORE_SAVE[i]), rank_font, GREY, 600, 170 + 48 * i)
        
        #lee
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            menu = 0  # 回到主菜單
    pygame.display.flip()

pygame.quit()


