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
    except :
        print("그런 파일은 안 보이는데요, 다시 확인해 주시겠어요?")
    else:
        Midi=Midi.split("\n")
        break
    finally:
        print()

#음정과 박자 조정
print("피치 조정값을 입력하세요. 1음은 0.5입니다.")
print("이 기능은 범위를 벗어난 노트가 연주되지 않는 것을 방지하기 위한 것입니다.")
Pitch=input()
try:
    Pitch=float(Pitch)
except:
    Pitch=0
else:
    if Pitch*2!=int(Pitch*2) :
        Pitch=0
    else :
        Pitch=int(Pitch*2)

#미디 파일 분석
Notes=['라0', '라#0', '시0', '도1', '도#1', '레1', '레#1', '미1', '파1', '파#1', '솔1', '솔#1', '라1', '라#1', '시1', '도2', '도#2', '레2', '레#2', '미2', '파2', '파#2', '솔2', '솔#2', '라2', '라#2', '시2', '도3', '도#3', '레3', '레#3', '미3', '파3', '파#3', '솔3', '솔#3', '라3', '라#3', '시3', '도4', '도#4', '레4', '레#4', '미4', '파4', '파#4', '솔4', '솔#4', '라4', '라#4', '시4', '도5', '도#5', '레5', '레#5', '미5', '파5', '파#5', '솔5', '솔#5', '라5', '라#5', '시5', '도6', '도#6', '레6', '레#6', '미6', '파6', '파#6', '솔6', '솔#6', '라6', '라#6', '시6', '도7', '도#7', '레7', '레#7', '미7', '파7', '파#7', '솔7', '솔#7', '라7', '라#7', '시7', '도8']
Sheet=[]
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
    elif LineX[0].strip()=="MidiTrack" and Type==1 : #새 트랙
        Time=0
        Sheet+=["트랙"]
    elif LineX[0].strip()=="MetaMessage" or LineX[0].strip()=="Message" : #(Meta)Message의 경우
        LineY=LineX[1].split(",")
        Note=3*[None]
        for J in range(len(LineY)):
            LineZ=LineY[J].split("=")
            if LineZ[0].strip()=="tempo" : #tempo 확인
                Note[0]="템포"
                Note[1]=int(LineZ[1])
            elif LineZ[0].strip()=="'note_on'" : #노트 재생?
                Note[0]="켜짐"
            elif LineZ[0].strip()=="'note_off'" : #노트 중단
                Note[0]="꺼짐"
            elif LineZ[0].strip()=="note" : #범위 내 노트인지 확인
                if 0<=int(LineZ[1])-21+Pitch<=83 :
                    Note[1]=int(LineZ[1])-21+Pitch
                else :
                    Note[0]="기타"
            elif LineZ[0].strip()=="velocity" : #velocity가 0이면 중단으로 처리
                if int(LineZ[1])==0 :
                    Note[0]="꺼짐"
            elif LineZ[0].strip()=="'end_of_track'" : #트랙 종료
                Note[0]="종료"
            elif LineZ[0].strip()=="time" : #time 추가
                Time+=int(LineZ[1].split(")")[0])
                Note[2]=Time
        if Note[0]!=None :
            Sheet+=[Note]

#분석한 파일을 악보로 변환
Code=""
Playing=-1
for I in range(len(Sheet)):
    if Sheet[I]=="트랙" : #트랙 변경
        Code+="트랙\n"
        Time=0
    else :
        if Sheet[I][0]=="템포" or Sheet[I][0]=="켜짐" : #템포 변경, 노트 재생
            if Sheet[I][2]-Time>0 : #앞 명령어와 간격이 있는 경우
                if Playing==-1 :
                    Code+="대기 "+str((Sheet[I][2]-Time)/TPB)+"\n"
                else :
                    Code+=" "+str((Sheet[I][2]-Time)/TPB)+"\n"
                Time=Sheet[I][2]
            else : #아닌 경우
                if Playing!=-1 :
                    Code+="\n"
            if Sheet[I][0]=="템포" : #템포 변경
                Code+=str(round(60000000/Sheet[I][1]))
                if Playing==-1 :
                    Code+="\n"
            else : #노트 재생
                Code+=Notes[Sheet[I][1]]
                Playing=Sheet[I][1]
        elif Sheet[I][0]=="꺼짐" : #노트 중단
            if Playing==Sheet[I][1] : #연주 중이던 노트 중단
                Code+=" "+str((Sheet[I][2]-Time)/TPB)+"\n"
                Playing=-1
                Time=Sheet[I][2]
        elif Sheet[I][0]=="종료" : #트랙 종료
            if Sheet[I][2]-Time>0 : #앞 명령어와 간격이 있는 경우
                Code+="대기 "+str((Sheet[I][2]-Time)/TPB)+"\n"

#출력
with open(File+"/"+Name+".txt","w",encoding="UTF-8") as file:
    file.write(Code)
input("\n완료! 엔터를 눌러 종료합니다.")
print("\n이용해주셔서 감사합니다!",end="")
exit(0)

