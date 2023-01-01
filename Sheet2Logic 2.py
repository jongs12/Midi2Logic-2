print("Sheet2Logic 2 by jongs\n")

#파일 위치 확인
File=__file__.split("\\")
File[len(File)-1]=""
File="/".join(File)

#파일 이름 받기
while True:
    try:
        Name=input("txt 파일의 이름을 입력하세요. ")
        Midi=File+"/"+Name+".txt"
        with open(Midi,"r",encoding="UTF-8") as file:
            Midi=file.read().split("\n")
    except :
        print("그런 파일은 안 보이는데요, 다시 확인해 주시겠어요?")
    else:
        if len(Name)>32 : #긴 이름 잘라내기
            Name=Name[0]+Name[1]+Name[2]+Name[3]+Name[4]+Name[5]+Name[6]+Name[7]+Name[8]+Name[9]+Name[10]+Name[11]+Name[12]+Name[13]+Name[14]+Name[15]+Name[16]+Name[17]+Name[18]+Name[19]+Name[20]+Name[21]+Name[22]+Name[23]+Name[24]+Name[25]+Name[26]+Name[27]+Name[28]+Name[29]+Name[30]+Name[31]
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

#파일 분석
Key=['라0', '라#0', '시0', '도1', '도#1', '레1', '레#1', '미1', '파1', '파#1', '솔1', '솔#1', '라1', '라#1', '시1', '도2', '도#2', '레2', '레#2', '미2', '파2', '파#2', '솔2', '솔#2', '라2', '라#2', '시2', '도3', '도#3', '레3', '레#3', '미3', '파3', '파#3', '솔3', '솔#3', '라3', '라#3', '시3', '도4', '도#4', '레4', '레#4', '미4', '파4', '파#4', '솔4', '솔#4', '라4', '라#4', '시4', '도5', '도#5', '레5', '레#5', '미5', '파5', '파#5', '솔5', '솔#5', '라5', '라#5', '시5', '도6', '도#6', '레6', '레#6', '미6', '파6', '파#6', '솔6', '솔#6', '라6', '라#6', '시6', '도7', '도#7', '레7', '레#7', '미7', '파7', '파#7', '솔7', '솔#7', '라7', '라#7', '시7', '도8']
Notes=['0.00', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08', '0.09', '0.10', '0.11', '1.00', '1.01', '1.02', '1.03', '1.04', '1.05', '1.06', '1.07', '1.08', '1.09', '1.10', '1.11', '2.00', '2.01', '2.02', '2.03', '2.04', '2.05', '2.06', '2.07', '2.08', '2.09', '2.10', '2.11', '3.00', '3.01', '3.02', '3.03', '3.04', '3.05', '3.06', '3.07', '3.08', '3.09', '3.10', '3.11', '4.00', '4.01', '4.02', '4.03', '4.04', '4.05', '4.06', '4.07', '4.08', '4.09', '4.10', '4.11', '5.00', '5.01', '5.02', '5.03', '5.04', '5.05', '5.06', '5.07', '5.08', '5.09', '5.10', '5.11', '6.00', '6.01', '6.02', '6.03', '6.04', '6.05', '6.06', '6.07', '6.08', '6.09', '6.10', '6.11']
Sheet=[]
Track=[]
Block=0
Time=0
NoChange=0
Drum=[]
for I in range(len(Midi)):
    LineX=Midi[I].split(" ")
    if LineX[0]=="트랙" : #트랙의 경우
        Play=0
        for J in range(len(Track)):
            if Track[J][0]!="BPM" and Track[J][0]!="LOG" : #추가된 노트 확인
                Play=1
        Track+=[["END",None,Time]]
        Sheet+=Track #트랙 리셋
        Track=[]
        Time=0
        if Play==1 :
            Block+=1
        if NoChange==2 :
            Drum+=str(Block)
        NoChange=0 #키 변경 차단
        if len(LineX)>1 :
            NoChange=1
    else : #노트의 경우?
        try:
            LineX[0]=float(LineX[0])
        except:
            for J in range(88):
                if NoChange==0 :
                    if LineX[0]==Key[J] and 0<=J+Pitch-3<=83 :
                        Track+=[[str(Block+1),Notes[J+Pitch-3],Time]]
                else :
                    if LineX[0]==Key[J] and 0<=J-3<=83 :
                        NoChange=2
                        Track+=[[str(Block+1),Notes[J-3],Time]]
            LineX[0]=list(LineX[0])
            if LineX[0]!=[] and LineX[0][0]=="#" :
                LineX[0][0]=""
                for J in range(len(LineX[0])-33):
                    LineX[0][len(LineX[0])-1-J]=""
                LineX[0]="".join(LineX[0])
                Track+=[["LOG",LineX[0],Time]]
        else:
            if LineX[0]>0 :
                Track+=[["BPM",LineX[0],Time]]
        finally:
            try:
                LineX[1]=float(LineX[1])
            except:
                Time+=0
            else:
                if LineX[1]>0 :
                    Time+=LineX[1]
Play=0 #트랙의 경우와 같음
for I in range(len(Track)):
    if Track[I][0]!="BPM" and Track[I][0]!="LOG" :
        Play=1
Track+=[["END",None,Time]]
Sheet+=Track
if Play==1 :
    Block+=1
if NoChange==2 :
    Drum+=str(Block)
print()
Sheet.sort(key=lambda x: x[2])

#분석한 파일을 로직 코드로 변환
Code=[]
#페이지 0
Track='setrate 100\nread x cell1 0\njump 10 notEqual x 0\nsensor a switch1 @enabled\njump 9 notEqual a 1\nset t1 @time\nwrite t1 cell1 2\nwrite 1 cell1 0\njump 11 always\nprint "'+Name+'\\n"\njump 20 equal x 0\ncontrol enabled switch1 0\nread t1 cell1 2\nset t2 @time\nop sub t t2 t1\nop div t t 10\nop idiv t t 1\nop div t t 100\nprint t\nprint "\\n"\nsensor a switch2 @enabled\njump 26 notEqual a 1\ncontrol enabled switch2 0\nread i cell1 1\nop add i i 11\njump 31 always\nsensor a switch3 @enabled\njump '+str(34+Block)+' notEqual a 1\ncontrol enabled switch3 0\nread i cell1 1\nop add i i 19\nop sub i i 10\njump 31 greaterThan i 9\nwrite i cell1 1\n'
if Block>963 :
    print("트랙 수가 너무 많아 일부를 제외하였습니다.\n")
    Block=963
for I in range(Block):
    NoChange=0
    for J in range(len(Drum)):
        if str(I+1)==Drum[J] :
            NoChange=1
    if NoChange==0 :
        Track+='control color block'+str(I+1)+' i\n'
    else :
        Track+='control color block'+str(I+1)+' 10\n'
Track+='print "[#2030D0]Made with "\nprint "[#FFFF00]Sheet2Logic 2"\nprintflush message1'
Code.append(Track)
#페이지 >=1
Tempo=120
Time=0
Play=0
Page=1
while True:
    Line=0
    Track='setrate 100\nread x cell1 0\njump 1 notEqual x '+str(Page)+'\n'
    while Line<996:
        if Sheet[Play][2]-Time>0 : #노트 간 간격
            Track+='wait '+str((60*(Sheet[Play][2]-Time))/(Speed*Tempo))+'\n'
            Line+=1
            Time=Sheet[Play][2]
        if Line==996 :
            break
        if Sheet[Play][0]=="BPM" : #템포 변경
            Tempo=Sheet[Play][1]
        elif Sheet[Play][0]=="LOG" : #위치 표시
            Track+='print "'+Sheet[Play][1]+'"\n'
            Line+=1
        elif Sheet[Play][0]=="END" : #마지막 노트
            if Sheet[Play][2]-Time>0 :
                Track+='wait '+str((60*(Sheet[Play][2]-Time))/(Speed*Tempo))+'\n'
                Line+=1
        else : #노트 연주
            Track+='control config block'+Sheet[Play][0]+' '+Sheet[Play][1]+'\n'
            Line+=1
        Play+=1
        if Play==len(Sheet) :
            break
    if Play==len(Sheet) : #모든 노트 연주됨
        Max=str(Page)
        Track+='write 0 cell1 0'
        Code.append(Track)
        break
    else : #아직 연주가 끝나지 않음
        Page+=1
        Track+='write '+str(Page)+' cell1 0'
        Code.append(Track)

#출력
print("완료! ("+str(Block)+" blocks)\n")
Page=0
while True :
    print("페이지 "+str(Page)+"/"+Max)
    with open(File+"로직.txt","w") as file:
        file.write(Code[Page])
    print("로직.txt 파일의 내용을 프로세서에 붙여넣으세요.\n프로세서를 모든 노트블록과 메모리 셀에 연결하세요.")
    if Page==0 :
        print("프로세서를 모든 스위치와 메모 블록에 연결하세요.\n\n엔터를 눌러 다음 페이지로 넘어갑니다.\n또는 페이지 번호를 직접 입력할 수 있습니다.")
    elif Page==int(Max) :
        print("\nend를 입력하면 프로그램을 종료합니다.")
    else :
        print("\n엔터를 눌러 다음 페이지로 넘어갑니다.")
    Name=input().strip()
    if Name=="end" : #페이지 이동
        break
    else :
        try:
            Name=int(Name)
        except:
            Page+=1
        else:
            Page=Name
        finally:
            if Page<0 or Page>int(Max) :
                Page=0
            print()
print("\n이용해주셔서 감사합니다!",end="")
exit(0)
