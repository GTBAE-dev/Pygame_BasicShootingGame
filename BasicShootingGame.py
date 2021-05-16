import pygame # pygame module 불러오기, 모듈 설치여부 확인 가능
from pygame.locals import* # pygame.locals 내 하위 모듈 불러오기
pygame.init() # 기본 라이브러리 초기화 작업(pygame 뼈대, 반드시 필요)

''' 1. 기본 설정 '''
''' 1-1. 화면'''
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height)) # 변수 지정, 화면 그릴 시 활용
    ## pygame.display.set_mode((가로, 세로), FULLSCREEN | HWSURFACE | OPENGL | DOUBLEBUF) : 각 flag들을 | 조합으로 함께 사용 가능
    ## FULLSCREEN(전체화면), HWSURFACE(하드웨어 가속, 전체화면에서만 가능), OPENGL(OPENGL(2~3D) 사용가능 디스플레이), DOUBLEBUF(더블 버퍼(프론트, 백) 모드 사용)
pygame.display.set_caption("BasicShootingGame") # 게임 이름 설정(타이틀바 텍스트)

''' 1-2. font '''
# print(pygame.font.get_fonts()) : pygame 내 font 종류 출력
game_font = pygame.font.SysFont("gigi", 40, True, False) # system 내 font 불러오기 SysFont(font name, size, bold, italic)
    ## pygame.font.Font(font name, size) : system 내 font 가 아닌 font file 불러오기
total_time = 100
start_ticks = pygame.time.get_ticks() # 현재 tick 받아오기(시작 시간 기준)

''' 1-3. FPS '''
clock = pygame.time.Clock() # FPS(초당 프레임수) 설정: 메인루프 내 목표 프레임수 clock.tick(int) 통해 입력

''' 1-4. 음악 '''
background_music = pygame.mixer.Sound(r"C:\Users\qorbx\OneDrive\바탕 화면\ToGit\PyGame\BasicShootingGame\music\LP1607180049_김재영_Waltz For A Child.wav") # 파일주소를 이용한 bgm 불러오기, 주소 처리 방법
background_music.play(-1) # -1 : 반복재생 / int값으로 재생 횟수 설정 가능
# pygame.mixer.music.load("C:\\Users\\qorbx\\OneDrive\\바탕 화면\\ToGit\\PyGame\\BasicShootingGame\\music\\LP1607180049_김재영_Waltz For A Child.wav") # 음악 불러오기 다른 방법, 다른 주소 처리 방법
# pygame.mixer.music.play(-1)

''' 2. 게임 내 요소 '''
''' 2-1. 배경 '''
import os
current_path = os.path.dirname(__file__) # os module 사용하여 파일 위치 반환하는 방법(os.path.dirname : 현재 파일의 위치 반환)
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size # 사각형(rect)의 크기에 대한 정보를 tuple 형식으로 받아옴
stage_height = stage_size[1] # [0]자리: 넓이 / [1]자리: 높이

''' 2-2. 캐릭터 '''
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1] # 캐릭터 위치 처리 변수
character_x_pos = (screen_width / 2) - (character_width / 2) # 캐릭터를 stage 위 정 가운데 위치
character_y_pos = screen_height - stage_height - character_height
character_to_x = 0 # 캐릭터 이동방향 변수
character_speed = 5 # 캐릭터 이동속도 변수

''' 2-3. 무기 '''
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0] # 무기 위치 처리 변수
weapons = [] # 무기 여러 개 처리 리스트
weapon_speed = 10 # 무기 이동속도 변수
weapon_to_remove = -1 # 사라질 무기에 대한 처리 변수

''' 2-4. 적 '''
ball_images = [ # 리스트를 통한 여러 크기의 공 불러오기
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]
ball_speed_y = [-18, -15, -12, -9] # 공 이동속도 변수(idx 0, 1, 2, 3에 해당)
balls = [] # 공 쪼개짐 처리 리스트
balls. append({ # 필요 속성들을 사전 형태로 리스트에 append
    "pos_x": 50, # 공 x 좌표 변수
    "pos_y": 50, # 공 y 좌표 변수
    "img_idx": 0, # 공 이미지 변수(0: 제일 큰 공)
    "to_x": 3, # 공 x축 이동, 양수: 오른쪽 / 음수: 왼쪽
    "to_y": -6, # 공 y축 이동, 양수: 아래 / 음수: 위
    "init_spd_y": ball_speed_y[0]}) # 공 y축 최초 속도
balls_to_remove = -1 # 사라질 공에 대한 처리 변수

''' 3. 메인루프(메인 이벤트 처리) '''
running = True
while running:

    ''' 3-1. FPS '''
    FPS_correction = clock.tick(30) # FPS 설정 후 1000 / FPS 값으로 게임 내 요소 움직임 보완
    # print("fps:" + str(clock.get_fps())) # 프레임 수 출력
    
    ''' 3-2. 이벤트 처리(키, 마우스, 종료 등) '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 종료 이벤트(타이틀바 X 키)
            running = False # 메인루프(while문) 탈출 및 종료
        
        if event.type == pygame.KEYDOWN: # 키 눌렀을 때의 이벤트 처리
            if event.key == pygame.K_LEFT: 
                character_to_x -= character_speed # 캐릭터 왼쪽 이동
            elif event.key == pygame.K_RIGHT: 
                character_to_x += character_speed # 캐릭터 오른쪽 이동
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos]) # 여러번 발사된 무기의 위치 처리(리스트 내 좌표 리스트 append)
        if event.type == pygame.KEYUP: # 키를 뗐을 때 이벤트 처리
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
        ## if event.type == MOUSEBUTTONDOWN : 
        ##    if event.button == LEFT : 마우스 눌렀을 때 이벤트 처리
        ## if event.type == MOUSEBUTTUP : 
        ##    if event.button == LEFT : 마우스 버튼 떨어졌을 때 이벤트 처리
        ## if event.type == pygame.MOUSEMOTION : 마우스 이동시 이벤트 처리

    ''' 3-3. 게임 내 요소 위치 정의 '''
    # 캐릭터
    character_x_pos += character_to_x # 이동 처리
    if character_x_pos < 0: # 경계 처리
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 각 무기의 위치 좌표 업데이트
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0] # 천장에 닿은 무기 제거

    # 적
    for ball_idx, ball_val in enumerate(balls): # balls list 내 순번(idx) 와 값을 불러오는 enumerate 함수
        ball_pos_x = ball_val["pos_x"] # 공 좌표 처리
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"] # img_idx를 통한 공 크기 처리
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        # 공 속도 처리
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1) # 공이 벽에 닿았을 때 방향 전환 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] # 공이 바닥에 닿았을 때 방향 전환 처리
        else:
            ball_val["to_y"] = ball_val["to_y"] + 0.5 # 이외의 경우 점진적 속도 변화 처리
        # 공 위치 처리
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    ''' 3-4. 충돌처리 '''

    ''' 3-5. 화면에 그리기 '''
    # 배경
    screen.blit(background, (0, 0)) # 제일 왼쪽 위 점의 좌표 (0, 0)

    # 무기
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    # 스테이지(배경)
    screen.blit(stage, (0, screen_height - stage_height)) # blit 의 순서대로 그려짐

    # 캐릭터
    screen.blit(character, (character_x_pos, character_y_pos))

    # 적
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    # 경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 : 새로 받은 현재 tick - 메인 루프 밖 시작 tick, 단위변환(ms → s) 
    timer = game_font.render("Time : {0}".format(int(total_time - elapsed_time)), True, (255, 255, 255)) # render(text msg, antialias, color) / antalias : 선을 부드럽게 만드는 기법
    screen.blit(timer, (10,10)) # blit을 통한 화면에 객체 그리기

    pygame.display.update() # 매 frame마다 화면을 새로 그려주는 동작(이전 화면이 지워지는게 아님, 덮어쓰기)

''' 4. 종료 '''
pygame.quit() # pygame 종료
