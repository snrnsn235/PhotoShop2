#미니 포토샵 프로젝트
#포토샵과 같은 소프트웨어를 '영상처리(IMAGE PROCESSING) 프로그램'이라 함.
#원칙적으로 영상처리에 대한이론과 알고리즘을 익힌 후 미니 포토샵 프로그램을 작성하면 좋음
#현실적으로 이론은 배제하고 화면에 구현되는 것 위주로 진행

#주의 사항1. 이미지 파일명이나 저장된 경로에 한글이 들어가면 안됨
#주의 사항2. 이미지 크기는 가로와 세로가 동일해야 함.
#주의 사항3. 처리학는 속도가 다소 오래 걸림.

#사용할 라이브러리 또는 모듈을 임포트

#윈도우 프로그래밍을 하기 위한 모듈
from tkinter import *
     
#파일 입출력을 위한 모듈
from tkinter.filedialog import *

#숫자나 문자를 입력 받기 위한 모듈
from tkinter.simpledialog import *

#설치한 이미지 처리 기능을 제공하는 이미지매직의 라이브러리 임포트
#gif, png 뿐 아니라 jpg 같은 이미지를 모두 처리하기 위해 외부 라이브러리 이미지 매직 사용
from wand.image import *

#모든 함수들이 공통적으로 사용할 전역 변수 선언부
window, canvas, paper = None, None, None
photo, photo2=None, None #photo는 처음 불러들인 원본 이미지, photo2는 처리결과를 저장할 변수
oriX, oriY=0,0 #원본 이미지의 폭과 높이를 저장하는 변수


#함수 정의 부분
#이미지를 화면상에 출력하는 사용자 정의 함수 선언
def displayimage(img, width, height):
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    #이전 캔버스가 존재한다면 이전 캔버스를 삭제하여 기존에 이미지가 출력된 캔버스를 깨끗하게 처리
    if canvas != None:
        canvas.destroy()
    # 새 캔버스 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    canvas = Canvas(window, width = width, height=height)
    # 새 캔버스에 붙일 종이(paper) 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    paper = PhotoImage(width=width, height=height)
    # 새 캔버스에 종이(paper)를 붙임 (차후 그 종이 위에 처리된 이미지를 출력)
    # 생성될 위치는 가로 세로의 사이즈의 중간 위치
    canvas.create_image((width/2, height/2), image=paper, state="normal")

    blob = img.make_blob(format='RGB') #이미지를 바이너리 코드로 변환해주는 함수, 배열의 형태로 저장
    for i in range(0, width):
        for k in range(0, height):
            r=blob[(i*3*width)+(k*3)+0] # blob[0, blob[3], blob[6], blob[9]의 값을 r에 저장
            g=blob[(i*3*width)+(k*3)+1]
            b=blob[(i*3*width)+(k*3)+2]
            #paper에 칼라로 점을 찍어줌, 세로로 높이만큼 찍고 가로를 너비만큼 반복
            paper.put("#%02x%02x%02x" % (r,g,b), (k,i))
    canvas.pack()


#파일 열기        
def func_open():
    #pass #기능이 없는 빈 함수 생성
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    #askopenfilename() 함수로 파일 열기 대화상자를 나타내어 그림 파일 선택 
    readFp=askopenfilename(parent=window, filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif"), ("모든 파일", "*.*")))

    #이미지는 gif, jpg, png를 불러와 모두 처리하기 위해 photoimage()가 아닌 wand라이브러리에서 제공하는 image()를 사용
    #이미지를 준비하는 단계
    #photo는 처음 불러들인 원본 이미지
    photo=Image(filename=readFp)
    oriX = photo.width #원본 이미지의 가로 사이즈를 oriX에 저장
    oriY = photo.height #원본 이미지의 세로 사이즈를 oriY에 저장

    #photo2는 처리 결과를 저장할 변수
    photo2 = photo.clone() #원본 이미지의 photo를 복사하여 photo2에 저장
    newX = photo2.width
    newY = photo2.height
    #복제된 photo2를 캔버스의 페이퍼에 디스플레이하는 사용자 정의 함수 실행
    displayimage(photo2, newX, newY)
    
#파일 저장
def func_save():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    saveFp = asksaveasfile(parent=window, mode="w", defaultextension=".jpg", filetypes=(("jpg파일", "*.jpg;*.jpeg"), ("모든 파일", "*.*")))
    savePhoto = photo2.convert("jpg") #결과 이미지인 photo2를 눌렀을 때 함수를 빠져나감
    savePhoto.save(filename=saveFp.name) #파일 저장 대화창에서 입력받은 파일 이름으로 저                                                                   

#되돌리기
def func_revert():
     global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
     photo2=photo.clone() #원본을 복제해서 photo2 덥어쓰
     newX = photo2.width
     newY = photo2.height
     displayimage(photo2, newX, newY)

#프로그램 종료  
def func_exit():
    window.quit()
    window.destroy()

#이미지 처리1>확대및 축소
#wand 라이브러리에서 제공하는 resize(가로, 세로)함수를 사용
def func_zoomin():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    #askinteger()함수를 실행해 대화 상자로 확대할 배수 입력받음
    scale = askinteger("확대배수", "확대할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    photo2.resize(int(newX*scale), int(newY*scale))
    newX=photo2.width #변경된 이미지의 가로 사이즈 newX에 저장
    newY=photo2.height #변경된 이미지의 세로 사이즈 newY에 저장 
    displayimage(photo2, newX, newY)

    
def func_zoomout():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    #askinteger()함수를 실행해 대화 상자로 확대할 배수 입력받음
    scale = askinteger("축소배수", "축소할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    photo2.resize(int(newX/scale), int(newY/scale))
    newX=photo2.width #변경된 이미지의 가로 사이즈 newX에 저장
    newY=photo2.height #변경된 이미지의 세로 사이즈 newY에 저장 
    displayimage(photo2, newX, newY)

#상하반전, flip() 함수 사용   
def func_mirror1():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    photo2.flip()
    newX = photo2.width
    newY = photo2.height
    displayimage(photo2, newX, newY)
#좌우반전, flop() 함수 사용
def func_mirror2():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY #전역변수선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    photo2.flop()
    newX = photo2.width
    newY = photo2.height
    displayimage(photo2, newX, newY)
#이미지 처리1> 회전
#wand 라이브러리에서 제공하는 rotate(각도)함수를 사용
def func_rotate() :
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
    #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    degree = askinteger("회전", "회전할 각도를 입력하세요(0~360)", minvalue=0, maxvalue=360) 
    photo2.rotate(degree)
    newX = photo2.width 
    newY = photo2.height
    displayimage(photo2, newX, newY)

#이미지 처리2> 밝게/어둡게
#wand 라이브러리에서 제공하는 modulate(명도값, 채도값, 색상값)함수를 사용
#명도는 modulate(명도값, 100,100) 함수를 사용
#원본의 명다값이 100이므로 100이상은 '밝게', 100이하는 '어둡게'처리
    #밝게, modulate(밝기값, 100, 100)함수에 100~200값 입력
def func_bright():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
     #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    value = askinteger("밝게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX=photo2.width
    newY=photo2.height
    displasyimage(photo2, newX, newY)

    
#어둡게, modulate(밝기값, 100,100)함수에 0~100값 입력
def func_dark():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
      #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    value = askinteger("어둡게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(value, 100, 100)
    newX = photo2.width 
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리2> 선명하게/탁하게
# wand 라이브러리에서 제공하는 modulate(100, 채도값, 100)함수를 사용
# 선명하게, modulate(100,채도값,100)함수에 100~200 값 입력
def func_clear():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
      #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    value = askinteger("선명하게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayimage(photo2, newX, newY)
    
def func_unclear():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
     #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    value = askinteger("탁하게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(100, value, 100)
    newX = photo2.width 
    newY = photo2.height
    displayimage(photo2, newX, newY)


#이미지 처리2> 흑백이미지
#이미지의 type값을 "grayscale"로 설정
def func_bw():
    global window,canvas, paper, photo, photo2, oriX, oriY,newX, newY  # 전역 변수 선언
      #파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return
    photo2.type="grayscale"
    newX = photo2.width 
    newY = photo2.height
    displayimage(photo2, newX, newY)



#메인 코드 부분
window = Tk()
window.geometry("400x400")
window.title("미니 포토샵(ver 0.1)")

#메뉴 생성
#1. 메뉴 자체 생성
#메뉴 자체 = menu(부모 윈도우)
#부모 윈도우.config(menu=메뉴자체)
mainMenu=Menu(window)
window.config(menu=mainMenu)

#2. 상위 메뉴 생성
#상위 메뉴=Menu(메뉴자체)
#메뉴자체.add_cascade(label="상위 메뉴 텍스트", menu=상위메뉴)
#add_cascade() 메소드는 상위 메뉴와 하위 메뉴 연결 
fileMenu=Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)

#3. 하위 메뉴 생성
#상위메뉴.add_command(label="하위 메뉴1", command=함수1)
#add_command() 메소드는 기본 메뉴 항목 생성
fileMenu.add_command(label="파일 열기", command=func_open)
fileMenu.add_command(label="파일 저장", command=func_save)
fileMenu.add_separator() #구분선 삽입
fileMenu.add_command(label="되돌리기", command=func_revert)
fileMenu.add_separator() #구분선 삽입
fileMenu.add_command(label="프로그램 종료", command=func_exit)


#두번째 상위 메뉴 생성
image1Menu=Menu(mainMenu)
mainMenu.add_cascade(label="이미지 처리(1)", menu=image1Menu)
#하위 메뉴 생성
image1Menu.add_command(label="확대", command=func_zoomin)
image1Menu.add_command(label="축소", command=func_zoomout)
image1Menu.add_separator() #구분선 삽입
image1Menu.add_command(label="상하반전", command=func_mirror1)
image1Menu.add_command(label="좌우반전", command=func_mirror2)
image1Menu.add_separator() #구분선 삽입
image1Menu.add_command(label="회전", command=func_rotate)

#세번째 상위 메뉴 생성
image2Menu=Menu(mainMenu)
mainMenu.add_cascade(label="이미지 처리(2)", menu=image2Menu)
#하위 메뉴 생성
image2Menu.add_command(label="밝게", command=func_bright)
image2Menu.add_command(label="어둡게", command=func_dark)
image2Menu.add_separator() #구분선 삽입
image2Menu.add_command(label="선명하게", command=func_clear)
image2Menu.add_command(label="탁하게", command=func_unclear)
image2Menu.add_separator() #구분선 삽입
image2Menu.add_command(label="흑백이미지", command=func_bw)








window.mainloop()










