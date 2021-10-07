# Tutorial on the Taskflow API

이 자습서는 일반 Airflow 자습서를 기반으로 하며 특히 Airflow 2.0의 일부로 도입된 Taskflow API 패러다임을 사용하여 데이터 파이프라인을 작성하는 데 중점을 두고 이를 기존 패러다임을 사용하여 작성된 DAG와 대조합니다.



여기에서 선택한 데이터 파이프라인은 추출, 변환 및 로드에 대한 세 가지 개별 작업에 있는 간단한  ETL 패턴입니다.



##  Taskflow API ETL 파이프라인의 예	

```python
import json

from airflow.decorators
```





----

# airflow란?

https://dydwnsekd.tistory.com/27?category=897626



### airflow 란?

airflow는 airbnb 에서 개발한 워크플로우 스케줄링, 모니터링 도구로 현재 apache 프로젝트가 되었다.

airflow는 DAG(Directed Acyclic Graph)라는 개념으로 동작하는데 python으로 DAG를 작성하고 순서를 정의할 수 있다.
현재도 활발한 개발이 이뤄지고 있다.

빅데이터를 활용하는 많은 곳에서 활용하는 비슷한 도구에는 oozie 가 있다.



### airflow의 특성

* Dynamic : airflow pipeline(동작 순서, 방식)을 python 을 이용해 구성하기 떄문에 동적인 구성이 가능
* Extensible: python을 이용해 operator, executor을 사용해 사용자 환경에 맞게 확장 사용 가능
* Elegant: 간결하고 명시적이며, jinja template를 이용해 parameter를 이용해 데이터를 전달하고 파이프라인을 생성하는 것이 가능
* Scalable: 분산 구조와 메시지큐를 이용해 scale out 과 워커간 협업을 지원





### airflow architecture



architecture에서 보는 것과 같이 airflow는 scheduler, webserver, worker, metaDB 로 구성된다.

* webserver: DAG, user, connection, com, variable 관리를 할 수 있는 UI 제공
* Scheduler: 모든 작업과 DAG 를 관리하고 실행시키는 역할, postgreSQL , MySQL 8 이상의 버전에서  HA 기능까지제공
  * **HA**는 관리자가 없을지라도**, 운영 서버**의 장애를 모니터링해 **대기 서버**가 처리할 수 있도록 함으로써 중단 없이 서비스를 제공하는 역할을 한다.

* Executor:  worker의 동작 방식에 대해 정의를 하는 부분으로 local, sequential, celery 등 다양한 executor 방식을 제공
* metaDB: 실행중인 데이터 파이프라인에 대한 메타 데이터를 저장



### airflow 

Airflow webserver에서는 다양한 기능을 제공하지만, 여기서는 일단 DAGs를 볼 수 있는 UI만 확인해보자.
airflow DAGs를 볼 수 있는 화면으로 각각 DAG에 대한 실행, 삭제, 실행 log 등의 기록을 살펴볼 수 있다.

* https://airflow.apache.org/docs/apache-airflow/stable/ui.html : ui/ 스크린샷

## Airflow 구성

지난 포스트에서 Airflow가 무엇인지 간단하게 알아보았다

이번 포스트에서는 Airflow에서 알아야 할 용어들과 기본 개념에 대해서 알아보도록 하자

### DAG (Directed Acyclic Graph)

지향성 비순환 그래프로 지난 포스트에서도 간단하게 언급이 되었는데

python으로 작성하고 순서를 정해 하나의 workflow형식으로 동작한다

DAG는 아래와 같은 그림으로 표시할 수 있으며, 각 노드들은 task로 DAG가 실행되는 순서를 파악할 수 있다.

더보기

 



![img](https://blog.kakaocdn.net/dn/cqxvaV/btq1V1KLwBX/ggzyZ4vktxgjafkviJ2Lr0/img.png)https://en.wikipedia.org/wiki/Directed_acyclic_graph



### Task

하나의 작업 단위를 Task 라고 하며 하나  또는 여러 개의 task 를 이용해 하나의 DAG를 생성하게 된다.

Task 간에는 순서를 지정할 수 있고, <<, >> 를 통해 간단하게 지정하는 것이 가능하다.

Task 는 Operator 로 만들 수 있으며, python code를 실행시키기 위한  PythonOperator, Bash command를 실행시키기 위한 BashOperator 등이 제공된다.

```
with DAG('my_dag', start_date=datetime(2016, 1, 1)) as dag:
    task_1 = DummyOperator('task_1')
    task_2 = DummyOperator('task_2')

    # task_1을 실행한 후 task_2 실행
    task_1 >> task_2 # Define dependencies
```



### Operator

Operator는 Task 를 만들기 위해 사용되는 Airflow class인데 위에서 언급한 BashOperator,, PythonOperator 등을 제외한 외부 서비스들과 연동을 위한 Operator들이 제공되며 args를 이용해 어떻게 동작할 지 정ㅇ의할 수 ㅣㅇㅆ다.

Operator의 종류는 아래의 링크에서 더 자세히 확인할 수 있다

[airflow.apache.org/docs/stable/_api/airflow/operators/index.html](https://airflow.apache.org/docs/stable/_api/airflow/operators/index.html)

[airflow.apache.org/docs/](https://airflow.apache.org/docs/)

제공된 Operator뿐만 아니라 Operator을 생성하는 것도 가능하다







----



