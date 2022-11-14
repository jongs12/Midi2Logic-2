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
    except FileNotFoundError:
        print("그런 파일은 안 보이는데요, 다시 확인해 주시겠어요?")
    else:
        if len(Name)>32 : #긴 이름 잘라내기
            Name=list(Name)
            for I in range(32,len(Name)):
                Name[I]=""
            Name="".join(Name)
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
for I in range(len(Midi)):
    LineX=Midi[I].split(" ")
    if LineX[0]=="트랙" : #트랙의 경우
        Play=0
        for J in range(len(Track)):
            if Track[J][0]!="0" and Track[J][0]!=None : #추가된 노트 확인
                Play=1
        Track+=[[None,None,Time]]
        Sheet+=Track #트랙 리셋
        Track=[]
        Time=0
        if Play==1 :
            Block+=1
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
                        Track+=[[str(Block+1),Notes[J-3],Time]]
        else:
            if LineX[0]>0 :
                Track+=[["0",LineX[0],Time]]
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
    if Track[I][0]!="0" and Track[I][0]!=None :
        Play=1
Track+=[[None,None,Time]]
Sheet+=Track
if Play==1 :
    Block+=1
print()
Sheet.sort(key=lambda x: x[2])

#분석한 파일을 로직 코드로 변환
Code=[]
#페이지 0
Track='setrate 100\nread x cell1 0\njump '+str(28+Block)+' notEqual x 0\nsensor a switch1 @enabled\njump 10 notEqual a 1\ncontrol enabled switch1 0 0 0 0\nset t1 @time\nwrite t1 cell1 2\nwrite 1 cell1 0\njump '+str(28+Block)+' always\nsensor b switch2 @enabled\njump 18 notEqual b 1\ncontrol enabled switch2 0 0 0 0\nread i cell1 1\nop add i i 1\njump 17 lessThan i 10\nset i 0\nwrite i cell1 1\nsensor c switch3 @enabled\njump 26 notEqual c 1\ncontrol enabled switch3 0 0 0 0\nread i cell1 1\nop sub i i 1\njump 25 greaterThanEq i 0\nset i 9\nwrite i cell1 1\nprint "'+Name+'\\n"\nread i cell1 1\n'
for I in range(Block):
    Track+='control color block'+str(I+1)+' i 0 0 0\n'
Track+='jump '+str(37+Block)+' equal x 0\nread t1 cell1 2\nset t2 @time\nop sub t t2 t1\nop div t t 10\nop idiv t t 1\nop div t t 100\nprint t\nprint "\\n"\nprint "[#2030D0]Made with "\nprint "[#FFFF00]Midi2Logic"\nprintflush message1'
Code.append(Track)
#페이지 >=1
Tempo=1
Time=0
Play=0
Page=1
while True:
    Line=0
    Track='setrate 100\nread x cell1 0\njump 1 notEqual x '+str(Page)+'\n'
    while Line<996:
        if Sheet[Play][2]-Time>0 : #노트 간 간격
            Track+='wait '+str((60*(Sheet[Play][2]-Time))/Tempo)+'\n'
            Line+=1
            Time=Sheet[Play][2]
        if Line==996 :
            break
        if Sheet[Play][0]=="0" : #템포 변경
            Tempo=Sheet[Play][1]
        elif Sheet[Play][0]==None : #마지막 노트
            if Sheet[Play][2]-Time>0 :
                Track+='wait '+str((60*(Sheet[Play][2]-Time))/Tempo)+'\n'
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
if Block>960 :
    print("트랙 수가 너무 많습니다. 오류가 발생할 가능성이 있습니다.")
else :
    print("완료!",end=" ")
print("("+str(Block)+" blocks)\n")
Page=0
while True :
    print("페이지 "+str(Page)+"/"+Max)
    with open(File+"로직.txt","w") as file:
        file.write(Code[Page])
    print("로직.txt 파일의 내용을 프로세서에 붙여넣으세요.")
    print("프로세서를 모든 노트블록과 메모리 셀에 연결하세요.")
    if Page==0 :
        print("프로세서를 모든 스위치와 메모 블록에 연결하세요.")
    print()
    print("페이지 번호를 입력하세요. 비워두면 다음 페이지로 넘어갑니다. ")
    Name=input("end를 입력하면 프로그램을 종료합니다.")
    if Name=="end" : #페이지 이동
        print()
        break
    else :
        try:
            Name=int(Name)
        except:
            Page+=1
            if Page>int(Max) :
                Page=0
        else:
            if Name<0 or Name>int(Max) :
                Page+=1
            else :
                Page=Name
            if Page>int(Max) :
                Page=0
        finally:
            print("\n")
print("이용해주셔서 감사합니다!") 
exit(0)
