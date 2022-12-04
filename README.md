# Midi2Logic 2

[개요]
---
미디 파일을 읽어서 [Mindustry](https://github.com/Anuken/Mindustry)의 모드 중 하나인 [Betamindy](https://github.com/sk7725/BetaMindy)의 노트블럭을 연주하는 로직 코드를 짜주는 [프로그램](https://github.com/jongs12/Midi2Logic)의 개선된 버전입니다.

이 프로그램을 사용하려면 [파이썬](https://github.com/python)과 [mido 모듈](https://github.com/mido/mido)(현재 1.2.10)이 필요합니다.
[이 글](https://foreverhappiness.tistory.com/25#%ED%99%98%EA%B2%BD%20%EB%B3%80%EC%88%98%20%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0)을 따라 파이썬과 pip을 설치한 다음 명령 프롬프트에 *pip3 install mido*라고 입력하면 mido 모듈이 설치됩니다.

**아직 개발 단계입니다.** 더 많은 기능들은 추후 추가할 예정입니다.

[사용법]
---
![2](https://user-images.githubusercontent.com/99316134/201531611-ce5914a9-5601-441d-8d86-816ad17120f0.PNG)

필요한 것들을 모두 설치한 후에 프로그램을 실행합니다.
프로그램이 설치된 곳과 같은 폴더에 있는 mid 파일의 이름을 입력합니다.

![3](https://user-images.githubusercontent.com/99316134/201531613-42c774d7-6bad-4d91-8b82-48322b34de98.PNG)

음정과 속도를 조절합니다. 음정은 0.5가 1음이며, 1옥타브는 6입니다. 속도는 배속으로 적용됩니다.
음수도 입력 가능합니다. 필요없다면 이 부분은 그냥 무시하셔도 됩니다.

![4](https://user-images.githubusercontent.com/99316134/201531614-00963a1f-5738-4a1c-be42-ace6120ae8b1.PNG)

변환이 끝나면 블록과 페이지 수를 표시합니다. 블록은 필요한 노트블록의 수, 페이지는 필요한 프로세서의 수입니다.

![5](https://user-images.githubusercontent.com/99316134/201531615-9ea85b8a-8c6b-47c0-a881-0078e0f12d87.PNG)

마찬가지로 프로그램이 설치된 곳과 같은 폴더에 로직.txt 파일이 생겨있을 겁니다.
확인은 조금 있다가 하고, 우선 민더를 켜 줍니다.

![7](https://user-images.githubusercontent.com/99316134/201531628-52994e37-81de-4e37-9113-ec4380f878cc.PNG)

편집기로 들어가서 midi.msav 파일을 불러와줍니다.

![8](https://user-images.githubusercontent.com/99316134/201531630-1d976157-999c-4808-8b4e-3237f90e6f90.PNG)

맵의 편집기를 열고, esc를 눌러서 인 게임 편집으로 가줍니다.

![9](https://user-images.githubusercontent.com/99316134/201531631-b822825e-16d7-4da6-add1-b8c3e5ce2f52.PNG)

맵 구성은 기본적으로 이렇게 되어 있습니다. 그냥 사용하셔도 되지만 필요하다면 수정해도 상관없습니다.

![10](https://user-images.githubusercontent.com/99316134/201531633-0e4ce713-9c7e-470c-9c7e-63b14817f852.PNG)

중요한 점은 프로세서 중 하나가 반드시 모든 노트블록과 스위치(3개), 메모 블록과 메모리 셀(각각 1개)에 연결되어 있어야 한다는 것입니다.

![6](https://user-images.githubusercontent.com/99316134/201531640-86387db4-35be-40c0-a451-8de067de5391.PNG)

그 후 아까 보았던 로직.txt 파일의 내용(0번 페이지)을 복사(Ctrl+ACV)해서 프로세서에 붙여넣어줍니다.

![11](https://user-images.githubusercontent.com/99316134/201531645-f17ebacd-7449-4f33-aeda-a7abc0c2a8c6.PNG)

나머지 프로세서는 노트블록과 메모리 셀에만 연결되어 있으면 됩니다.

![13](https://user-images.githubusercontent.com/99316134/201532444-2d8871c0-9de0-49f5-bbba-55e37b57d9b9.PNG)

다른 페이지를 불러와서 아까와 같이 복붙해줍시다.

![12](https://user-images.githubusercontent.com/99316134/201531647-4898761d-f98d-4001-b9bd-f3ac337d0efa.PNG)

다 했으면 ~~맵을 좀 꾸미고 나서~~ 저장하고 나와줍니다.

![1](https://user-images.githubusercontent.com/99316134/201531651-b2d498cd-3cbb-4863-a443-c975c2476aae.PNG)

사용자 지정 게임을 시작해서 감상하시면 됩니다.

[Sheet2Logic]
---
이것도 전작과 비슷합니다. 다만 아직 개발 단계이기 때문에 핵심적인 기능만 들어 있고, 몇 가지 간략화된 부분이 있습니다.

파일을 읽어서 프로세서 코드로 변환하는 것은 Midi2Logic과 비슷하지만, 읽는 파일이 mid가 아닌 txt 파일이라는 차이가 있습니다.
미디와 관련이 없기 때문에 mido 모듈은 필요없습니다.

txt 파일은 직접 작성해 주어야 합니다. ~~아니면 다른사람이 만든걸 가져오던가요.~~ 이때 인코딩은 반드시 UTF-8이어야 합니다.

![1](https://user-images.githubusercontent.com/99316134/201639352-1bb5153d-be5e-4abc-9de0-627661623b14.PNG)

악보는 '트랙'을 기준으로 나누어지며, 연주 시에는 모든 트랙이 동시에 재생됩니다.

트랙 뒤에 뭔가가 오면 해당 트랙의 노트는 악기가 10(드럼)으로 고정되며 음정 변환의 영향을 받지 않습니다.
이 기능은 프로세서에 코드를 처음 붙여넣었을 때 적용되지 않는데 악기를 한번 바꾸면 적용됩니다.

~~'쀒쀒!'은 그냥 예시입니다. 실제로는 띄어쓰기 빼고 뭐가 와도 상관없습니다.~~

트랙을 이루는 요소에는 노트와 템포가 있는데, 사진과 같이 노트는 계이름을 한글로 쓴 다음 음높이(옥타브)를 띄어쓰기 없이 입력합니다.
그 다음 한 칸 띄우고 몇 박자 동안 연주할 것인지(연주 후 몇 박자 동안 쉴 것인지) 입력합니다. 검은 건반의 계이름은 #만 지원합니다.
템포는 계이름이 올 자리에 대신 BPM을 입력하면 됩니다.

![2](https://user-images.githubusercontent.com/99316134/201640342-b106a095-5c6e-43d4-be67-0b3c69ae493a.PNG)

그 이후는 Midi2Logic과 같으므로 생략하겠습니다.

[Midi2Sheet]
---
이것도 Midi2Logic과 유사하지만, 로직 코드로 바로 변환하는 것이 아닌 Sheet2Logic과 연동 가능한 악보로 변환한다는 차이가 있습니다.
변환된 악보의 이름은 미디의 이름과 동일합니다.

아직 불안정하지만, 그래도 멀쩡히 작동은 하니(...) 업로드합니다.
