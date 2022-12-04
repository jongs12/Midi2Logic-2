from mido import MidiFile
print("Midi2Sheet by jongs\n")

#파일 위치 확인
File=__file__.split("\\")
File[len(File)-1]=""
File="/".join(File)

#미디 이름 받기
while True:
    try:
        Name=input("mid 파일의 이름을 입력하세요. ")
        Midi=File+"/"+Name+".mid"
        Midi=str(MidiFile(Midi))
    except FileNotFoundError:
        print("그런 파일은 안 보이는데요, 다시 확인해 주시겠어요?")
    else:
        Midi=Midi.split("\n")
        break
    finally:
        print()

#음정과 박자 조정
Pitch=input("피치 조정값을 입력하세요. 1음은 0.5입니다. ")
Speed=input("속도 조정값을 입력하세요. 배속으로 적용됩니다. ")
try:
    Pitch=float(Pitch)
except:
    Pitch=0
else:
    if Pitch*2!=int(Pitch*2) :
        Pitch=0
    else :
        Pitch=int(Pitch*2)
try:
    Speed=float(Speed)
except:
    Speed=1
else:
    if Speed<=0 :
        Speed=1

#미디 파일 분석
Notes=['도1', '도#1', '레1', '레#1', '미1', '파1', '파#1', '솔1', '솔#1', '라1', '라#1', '시1', '도2', '도#2', '레2', '레#2', '미2', '파2', '파#2', '솔2', '솔#2', '라2', '라#2', '시2', '도3', '도#3', '레3', '레#3', '미3', '파3', '파#3', '솔3', '솔#3', '라3', '라#3', '시3', '도4', '도#4', '레4', '레#4', '미4', '파4', '파#4', '솔4', '솔#4', '라4', '라#4', '시4', '도5', '도#5', '레5', '레#5', '미5', '파5', '파#5', '솔5', '솔#5', '라5', '라#5', '시5', '도6', '도#6', '레6', '레#6', '미6', '파6', '파#6', '솔6', '솔#6', '라6', '라#6', '시6', '도7', '도#7', '레7', '레#7', '미7', '파7', '파#7', '솔7', '솔#7', '라7', '라#7', '시7']
Sheet=[]
Track=[]
Block=0
Tempo=0
Time=0
for I in range(len(Midi)):
    LineX=Midi[I].split("(")
    if LineX[0].strip()=="MidiFile" : #MidiFile의 경우
        LineY=LineX[1].split(",")
        for J in range(len(LineY)):
            LineZ=LineY[J].split("=")
            if LineZ[0].strip()=="type" : #type 확인
                Type=int(LineZ[1])
            elif LineZ[0].strip()=="ticks_per_beat" : #ticks_per_beat 확인
                TPB=int(LineZ[1])
    elif LineX[0].strip()=="MetaMessage" : #MetaMessage의 경우
        Play=0
        LineY=LineX[1].split(",")
        for J in range(len(LineY)):
            LineZ=LineY[J].split("=")
            if LineZ[0].strip()=="tempo" : #tempo 확인
                Play=1
                Tempo=int(LineZ[1])
            elif LineZ[0].strip()=="time" : #time 추가
                Time+=float(LineZ[1].split(")")[0])
        if LineY[0].strip()=="'end_of_track'" : #end_of_track의 경우
            Play=0
            for J in range(len(Track)):
                if Track[J][0]!="0" : #추가된 노트가 있으면 블록 번호 증가
                    Play=1
            Track+=[[None,None,Time]]
            Sheet+=[Track] #트랙 리셋
            Track=[]
            if Play==1 :
                Block+=1
            if Type==1 : #미디 타입이 1이면 시간 리셋
                Time=0
        elif Play==1 : #템포 변경 감지 시
            Track+=[["0",Tempo,Time]]
    elif LineX[0].strip()=="Message" : #Message의 경우
        Play=[0,0,0]
        LineY=LineX[1].split(",")
        for J in range(len(LineY)):
            LineZ=LineY[J].split("=")
            if LineZ[0].strip()=="'note_on'" : #note_on인지 확인
                Play[0]=1
            elif LineZ[0].strip()=="note" : #범위 내 노트인지 확인
                if 0<=int(LineZ[1])-24+Pitch<=83 :
                    Note=Notes[int(LineZ[1])-24+Pitch]
                    Play[1]=1
            elif LineZ[0].strip()=="velocity" : #velocity가 0이 아닌지 확인
                if int(LineZ[1])!=0 :
                    Play[2]=1
            elif LineZ[0].strip()=="time" : #time 추가
                Time+=float(LineZ[1].split(")")[0])
        if Play==[1,1,1] : #조건 만족 시 노트 추가
            Track+=[[str(Block+1),Note,Time]]
print()

#분석한 파일을 악보(?)로 변환
Code=""
for I in range(len(Sheet)): #트랙마다 반복
    Time=0
    Code+="트랙\n"
    for J in range(len(Sheet[I])): #노트마다 반복
        if Sheet[I][J][2]>0 : #노트 간 간격
            Code+="대기 "+str((Sheet[I][J][2]-Time)/(TPB*Speed))+"\n"
            Time=Sheet[I][J][2]
        if Sheet[I][J][0]=="0" : #BPM 변경
            Code+=str(60000000/Sheet[I][J][1])+"\n"
        elif Sheet[I][J][0]!=None : #노트 연주
            Code+=Sheet[I][J][1]+"\n"

#출력
with open(File+Name+".txt","w",encoding="UTF-8") as file:
    file.write(Code)
print("변환된 악보를 "+Name+".txt 파일에 저장했습니다.")
input("이용해주셔서 감사합니다! 엔터를 눌러 종료합니다.")
exit(0)
