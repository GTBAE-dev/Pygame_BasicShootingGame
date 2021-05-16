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

''' 3. 메인루프(메인 이벤트 처리) '''
running = True
while running:

    ''' 3-1. FPS '''
    FPS_correction = clock.tick(200) # FPS 설정 후 1000 / FPS 값으로 게임 내 요소 움직임 보완
    # print("fps:" + str(clock.get_fps())) # 프레임 수 출력
    
    ''' 3-2. 이벤트 처리(키, 마우스, 종료 등) '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 종료 이벤트(타이틀바 X 키)
            running = False # 메인루프(while문) 탈출 및 종료
    
    ''' 3-3. 게임 내 요소 위치 정의 '''

    ''' 3-4. 충돌처리 '''

    ''' 3-5. 화면에 그리기 '''
    # 경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 경과 시간 : 새로 받은 현재 tick - 메인 루프 밖 시작 tick, 단위변환(ms → s) 
    timer = game_font.render("Time : {0}".format(int(total_time - elapsed_time)), True, (255, 255, 255)) # render(text msg, antialias, color) / antalias : 선을 부드럽게 만드는 기법
    screen.blit(timer, (10,10)) # blit을 통한 화면에 객체 그리기

    pygame.display.update() # 매 frame마다 화면을 새로 그려주는 동작(이전 화면이 지워지는게 아님, 덮어쓰기)

''' 4. 종료 '''
pygame.quit() # pygame 종료
