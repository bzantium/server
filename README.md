# 할리스에서 만드는 삼행시봇 입니다.

## Install

```
pip install -r requirements.txt
```

## Branch 관리

```
git checkout -b "브랜치 이름"
git add .
git commit -m "커밋 메세지"
git push origin "브랜치 이름"
```

## Engines 관리

각자 생성한 모델을 engines에 등록해야합니다.
파일이름: 자기이름.py
```python
from .engine import Engine

# 메타클래스 Engine을 상속 받습니다.
# 추상 메소드인 activate을 구현합니다.
class MyEngine(Engine):
    def activate(text):
        '''
        args:
            - text <str>: str 타입의 글자 하나를 인자로 받습니다.

        return:
            - answer <str>: 딥러닝 모델로 생성한 문장을 str 타입으로 반환합니다
        '''
        answer = "딥러닝 모델로 생성한 문장을 만듭니다."

        return answer
```


## Zappa Setting 하는 법 (번외)
```
# pip가 버전 10이 되면서 변화된 부분을 zappa가 아직은 반영하지 못했습니다.
>> pip install pip==9.0.3
>> pip install zappa
>> pip install virtualenv

# zappa는 파이썬 가상환경에서 작업해야합니다.
# aws lambda 서비스는 기본적으로 파이썬 3.6과 2.7만 제공합니다.
# 따라서 가상환경도 3.6 or 2.7 (3.6 권장)으로 진행합니다.

# 파이썬 3.6 경로 파악
>> which python3.6
# 가상환경 생성
>> virtualenv --python=$파이썬3.6경로 venv
# 가상환경 실행
>> source venv/bin/actvaite
>> zappa init
# 이때 초기값 전부다 default로 설정
# zappa_settings.json 파일이 생성되는데 여기에서 local 환경에 따라 설정을 변경해줍니다.
>> zappa deploy # 첫번째 deploy
>> zappa update # 이후 수정이 있으면 update로 갱신
```
