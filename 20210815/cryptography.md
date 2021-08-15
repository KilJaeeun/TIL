# cryptography

> python 과 cryptography 를 통해 대칭키 암호화하기

> python에서는 다양한 방법을 통해 암호화 관련 알고리즘을 구현할 수 있습니다. 그 중 cryptography 의 Fernet을 활용한, 대칭키 암호화 알고리즘을 해보려 합니다.



## 대칭키 암호화 방식

먼저 대칭키 암호화 방식(symmetric-key algorithm)은 암호화와 복호화에 같은 암호키를 사용하는 알고리즘입니다.

이에 암호화를 하는 측과 복호화를 하는 측이 암호키를 공유해야합니다. 공개키 암호화 방식에 비해 계산 속도가 빠르다는 장점이 있습니다.



```
from cryptography.fernet import Fernet
```

먼저 cryptography 에서 대칭키 암호화할 수 있는 Fernet을 Import gksek.

```
key = Fernet.generate_key()
```

`Fernet.generate_key()`를 통해 키를 하나 생성한다.

```
cipher_suit = Fernet(key)
cipher_text = cipher_suite.encrypt(b'A really secret message. Not for prying eyes.')
```

A really secret message. Not for prying eyes. 라는 바이트를 키로 암호화하고 복호화를 위한 토큰(cipher_text)를 생성합니다.

```
plaint_text = cipher_suite.decrypt(cipher_text)
```

위에서 만든 토큰과 키를 가지고 있다면 원래의 평문으로 복호화가 가능합니다.

```
print("encrypt_text:", cipher_text)
print("decrypt_text:", plain_text)
```

제대로 암호화 복호화가 이뤄졌는지 출력해보면 

```
encrypt_text : b'gAAAAABei9G1DxGCcZ2ReRkSQYYstjP81WybNAxK4i-3-Q2nygnryzzTo_JUWfHyaO-4XtVmztGjk0uBN_C57hLZ_DKNzWBGdqbQiNONEWql-yC-t0rKUCVfcfAAIQ4h21t7eZjXdM3-' 
decrypt_text : b'A really secret message. Not for prying eyes.'
```



---

### 참고 문헌

https://somjang.tistory.com/entry/Python-Python%EA%B3%BC-cryptography%EB%A5%BC-%ED%86%B5%ED%95%B4-%EB%8C%80%EC%B9%AD%ED%82%A4-%EC%95%94%ED%98%B8%ED%99%94-%ED%95%98%EA%B8%B0
