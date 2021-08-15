# Airflow on mac



## 빠른 시작

https://airflow.apache.org/docs/apache-airflow/stable/start/local.html

```shell
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow

AIRFLOW_VERSION=2.1.2
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.1.2/constraints-3.6.txt
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname Kil \
    --lastname Jaeeun \
    --role Admin \
    --email rha3122@naver.com
# start the web server, default port is 8080
airflow webserver --port 8080 > webserver.log &

# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler > scheduler.log &

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page
```

* 이 명령을 실행하면 Aiflow가 `$AIRFLOW_HOME` 폴더를 생성하고, 기본적으로 `airflow.cfg` 파일을 생성해 빠르게 진행할 수 있다. 
* `$AIRFLOW_HOME/airflow.cfg`  또는 `Admin->Configuration` 메뉴의 ui에서 파일을 검사할 수 있다.
* 웹 서버의 PID 파일은 `systemd` 에 의해 시작된 경우, `$AIRFLOW_HOME/airflow-webserver.pid` 또는 `/run/airflow/webserver.pid`에 저장된다.



 

기본적으로 Airflow는 SQLite 데이터베이스를 이용합니다. 이 데이터베이스 백엔드를 사용하면, 병렬화가 불가능하므로, 상당히 빠르게 확장해야합니다. 태스크 인스턴스는 순차적으로만 실행되는 "Sequencial Executor"와 함께 작동합니다. 이 기능은 매우 제한적이지만 빠르게 시작하고 실행할 수 있으며 "UI" 및 명령줄 유틸리티를 둘러볼 수 있습니다.

> "Sequencial Executor" : 이 실행자는 한 번에 하나의 태스크 인스턴스만 실행하고 사용할 수 있음 디버깅을 위해. sqlite와 함께 사용할 수 있는 유일한 실행자이기도 하다. 



다음은 몇 가지 작업 인스턴스를 트리거하는 몇 가지 명령입니다. 아래 명령을 실행하면 "example_bash_operator" "DAG"에서 작업 변경 상태를 볼 수 있습니다.

```shell
# run your first task instance
airflow tasks run example_bash_operator runme_0 2015-01-01
# run a backfall over 2days
airflow dags backfill example_bash_operator \
		--start-date 2015-01-01 \
		--end-date 2015-01-02
```



---



## 튜토리얼

이 자습서에서는 첫 번째 파이프라인을 작성하는 동안 몇 가지 기본적인 Airflow 개념, 개체 및 사용법을 안내합니다.

### 파이프라인 정의 예

> Airflow/example_dags/tutorial.py

```python
from datetime import timedelta
from textwrap import dedent

# The DAG object: we'll need this to instantiate a DAG
from airflow import DAG

# Operators: we need this to operate
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args={
  'owner':'airflow',
  'depends_on_past':False,
  'email':['airflow@example.com'],
  'email_on_failure':False,
  'email_on_retry':False,
  'retries':1,
  'retry_delay':timedelta(minutes=5),
  #"queue":"bash_queue",
  # "pool":"backfill",
  # "priority_weight":10,
  # "end_date":datetime(2016,1,1),
  #"wait_for_downstream":False,
  # "dag":dag,
  #"sla":timedelta(hours=2),
  # "execution_timeout":timedelta(seconds=300),
  #"on_failure_callback":some_function,
  # "on_success_callback":some_function,
  # "on_retry_callback":another_function,
  # "sla_miss_callback": yet_another_function,
  # "trigger_rule":"all_success"
}
with DAG(
'tutorial',
  default_args=default_args,
  description='A simple tutorial DAG',
  schedule_interval=timedelta(days=1),
  start_date= days_ago(2),
  tags=['example'],
) as dag:
  # t1, t2 , and t3 are examples of tasks created by instantiating operators
  t1 = BashOperator(
  	task_id='print_date',
    bash_command='date'
  )
  t2 = BashOperator(
  	task_id='sleep',
    depends_on_paste=False,
    bash_command='sleep 5',
    retries =3
  )
  t1.doc_md = dedent(
  """\
  #### Task Documentation
 	You can document your task using  the attributes `doc_md` (markdown),
 	`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets rendered in UI's Task Instances Detail page.
  ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
  """
  )
  dag.doc_md = __doc__ # providing that you have a docstring at beginning of the DAG
  dag.doc_md = """
  This is a documentation placed anywhere
  """ #  otherwise, type it like this
  template_command = dedent(
  """
  {% for i in range(5) %}
      echo "{{ ds  }}"
      echo "{{ macro.ds_add(ds, 7)  }}"
      echo "{{ ds  }}"
  {% endfor %}
  
  """
  )
  
  t3 = BashOperator(
    task_id='templated',
    depends_on_paste = False,
    bash_command = template_command, 
    params = {'my_param':'Parameter I passed in'}
  )
  
  t1 >> [t2, t3]
  
  
  
  

```



## DAG 정의 파일입니다.

머리를 감쌀 수 있는 한 가지는(처음에는 모든 사람에게 매우 직관적이지 않을 수 있음) 이 Airflow  Python 스크립트는 실제로  DAG 의 구조로 코드를 지정하는 구성 파일일 뿐입니다. 여기에 정의된 실제 작업은 이 스크립트의 컨텍스트와 다른 컨텍스트에서 실행됩니다. 

다른 작업은 다른 시점에 다른 작업자에서 실행됩니다. 즉, 이 스크립트를 사용해 작업 간에 교차 통신을 할 수 없습니다. 이를 위해 XComs 라는 고급 기능이 있다.

>  XComs  : https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html



사람들은 때떄로 DAG 정의 파일을 실제 데이터 처리를 수행할 수 있는 장소로 생각합니다. 하지만, 전혀 그렇지 않습니다. 스크립트의 목적은 DAG 개체를 정의하는  것입니다. 스케줄러가 주기적으로 실행하여 변경 사항이 있는 경우, 이를 반영하므로 빠르게  (분, 아닌 초) 평가해야합니다.





## 모듈 가져오기

Airflow 파이프라인은 Airflow DAG 개체를 정의하는 Python 스크립트일 뿐입니다. 필요한 라이브러리를 가져오는 것부터 시작하겠습니다.

```python
from datetime import timedelta
from textwrap import dedent


# The DAG object : we'll need to instantiate a DAG
from airflow import DAG

# Operators : we need this to operate
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
```

Python 및 Airflow가 모듈을 관리하는 방법에 대한 자세한 내용 은 [모듈 관리](https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html) 를 참조하세요.





## 기본 인수

우리는 DAG와 일부 작업을 만드려고 합니다. 각 작업의 생성자에 인수 집합을 명시적으로 전달하거나(중복될 수 있음) 기본 매개변수 사전을 정의할 수 있습니다. 작업을 생성할 때 사용할 수 있습니다.

```python
# These args will get passed on to each operator
# you can override them on a per-task basis during operator initialization
default_args={
  'owner':'airflow',
  'depends_on_past':False,
  'email':['airflow@example.com'],
  'email_on_failure':False,
  'email_on_retry':False,
  'retries':1,
  'retry_delay':timedelta(miniutes=5),
  # 'queue' :'bash_queue',
  # 'pool': 'backfill',
  # 'priority_weight':10,
  # 'end_date': datetime(2016, 1,1),
  # 'wait_for_downstream': False,
  # 'dag':dag,
  # 'sla': timedelta(hours=2),
  # 'execution_timeout':timedelta(seconds=300),
  # 'on_failure_callback':some_function,
  # 'on_success_callback': some_function,
  # 'on_retry_callback': another_function.
  # 'sla_miss_callback': yet_another_function.
  # 'triggering_rule':'all_success'
  
}
```

BaseOperator 의 매개변수와 매개변수의 기능에 대한 자세한 내용은 설명서를 참고하세요. `airflow.models.BaseOperator`

또한, 다른 용도로 사용되는 다양한 인수 집합을 쉽게 정의할 수 있습니다. 프로덕션 환경과 개발환경 간에 설정이 다른 경우를 예로 들 수 있습니다.



## DAG 인스턴스화

작업을 중첩할  DAG개체가 필요합니다. 여기에서 dag_id, DAG 고유 식별자 역할을 정의하는 문자열을 전달합니다. 또한, 방금 정의한 기본 정의한 기본 인수 사전을 전달 schedule_interval 하고  DAG 에 대해 1일을 정의합니다.

```python
# airflow/example_dags/tutorial.py
with DAG(
  'tutorial',
  default_args=default_args,
  description='A simple tutorial DAG',
  schedule_interval = timedelta(days=1),
  start_date = days_ago(2),
  tags=['example']
) as dag:
```



## 작업

작업은 연산자 개체를 인스턴스화할 때 생성됩니다. 연산자에서 인스턴스화된 개체를 작업이라합니다. 첫 번째 인수 task_id 는 작업의 고유 식별자 역할을 합니다.

```python
# example_dags/tutorial.py
t1 = BashOperator(
     task_id='print_data',
     bash_commands='date'
)

t2 = BashOperator(
     task_id='sleep',
     depends_on_past=False,
     bash_commands = 'sleep 5',
     retries =3
)
```

연산자별 인수 "bash_command"와 BaseOperator에서 상속된 모든 연산자 "retries"에 공통 인수의 혼합을 연산자의 생성자에게 전달하는 방법에 대해 알아 보십시오. 이것은 모든 생성자 호출에 대해 모든 인수를 전달하는 것보다 간단합니다. 또한 두 번째 작업에서는 재시도 매개 변수를 3으로 재정의합니다.



작업에 대한 우선 순위 규칙은 다음과 같다.

1. 명시적으로 전달된 인수
2. Default_args 사전에 존재한 값
3. 연산자의 기본값(있는 경우)

작업은 task_id, owner 및 인수를 포함하거나 상속해야합니다. 그렇지 않을 Airflow는 예외를 만들 것이다.



## Jinja로 템플릿하기

Airflow는 Jinja 템플릿의 기능을 활용하고, 파이프라인 작성자에게 내장 매개변수 및 매크로 세트를 제공합니다. Airflow는 또한 파이프라인 작성자가 자체 매개변수, 매크로 및 템플릿을 정의할 수 있는 후크를 제공합니다.

```python
templated_command = dedent(
"""
{% for i in range(5) %}
   echo "{{ ds }}"
   echo "{{ macros.ds_add(ds, 7)  }}"
   echo "{{ params.my_param }}"
{% endfor %}
"""
)

t3 = BashOperator(
	task_id='templated',
  depends_on_paste=False,
  bash_command = templated_command,
  params = {'my_param':'Parameter I passed in'}
)
```

* 블록에 templated_command 코드 논리가 포함되어 있고, 사용자 정의 매개변수를 참조합니다. 
* Params 의 후크는 BaseOperator 당신이 당신의 템플릿에 매개변수 및 / 또는 개체의 사전을 전달할 수 있습니다. 시간을 내어 매개변수 my_param가 템플릿에 전달되는 방식을 이해하십시오.
* 파일위치는 파이프라인 파일이 포함된 디렉토리에 상대적인 bash_command 인수 (예. Bash_command='templated_command.sh')로 파일을 전달할 수 있다.
  * 이것은 스크립트의 논리와 파이프라인 코드를 분리하고, 다른 언어로 구성된 파일에서  적절한 코드 강조 표시를 허용하고, 파이프라인을 구조화하는 일반적인 유연성과 같은 여러가지 이유로 바람직할 수 있습니다. `template_searchpath`로 DAG 생성자 호출에서 폴더위치를 가르키게 정의할 수 있다.
  * 동일한 DAG 생성자 호출 `user_defined_macros`을 이용해, 자신의 변수를 지정할 수 있도록 정의할 수 있다. 예를 들어 `dict(foo='bar')` 같이  인수에 전달해 템플릿에서  `{{ foo }} `  형태로 사용할 수 있다 . 
  * 또한, `user_defined_filters` 로 자신의 필터를 등록할 수 있다. 
    * 예를 들어 `dict(hello=lambda name: 'Hello %s'%name)`이 인수에 전달하면, 템플릿에서 `{{ 'world' | hello}}` 사용할 수 있다.
    * Jinja 문서에서 더 참조하자. https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html





## DAG 및  Tasks 추가

* DAG 또는 각 단일 Task에 대한 문서를 추가할 수 있다.  DAG 문서는 지금까지 마크다운, 일반텍스트, json, yaml 을 지원한다. 
* DAG 문서는 DAG 파일의 시작부분이나 아묵곳에서 문서 문자열로 작성할 수 있지만, 시작부분에 권장한다.

```python
t1.doc_md = dedent(
    """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

"""
)

dag.doc_md = __doc__  # providing that you have a docstring at the beggining of the DAG
dag.doc_md = """
This is a documentation placed anywhere
"""  # otherwise, type it like this
```

![_images/task_doc.png](https://airflow.apache.org/docs/apache-airflow/stable/_images/task_doc.png)



## 종속성 설정

우리는 의존관계 없는  작업을 t1, t2 그리고 t3   가짖고 있다. 이들간 종속성을 정의할 수 있는 몇 가지 방법이다.

```python
#  t2는 t1 에 의존한다.
# 1. 
t1.set_downstream(t2) 
# 2. 
t2.set_upstream(t1)
# 3. bit 연산자로 체인을 표시할 수 있다.
t1 >> t2
# 4.
t2 << t1

# 5. 체이닝 의존관계 됨
t1  >> t2 >> t3

# 6.뭉태기로 전달해도됨
t1.set_downstream([t2,t3])
t1 >> [t2,t3]
[t2, t3] << t1
```

스크립트를 실행할때, Airflowsms DAG 에서 주기를 찾거나, 종속성이 두 번이상 참조될 때 예외를 발생시킨다.



## 요약

```python
from datetime import timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beggining of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
    """
    )

    t3 = BashOperator(
        task_id='templated',
        depends_on_past=False,
        bash_command=templated_command,
        params={'my_param': 'Parameter I passed in'},
    )

    t1 >> [t2, t3]
```





```
python ~/airflow/dags/tutorial.py
```

스크립트에서 예외가 발생하지 않으면 크게 잘못한 것이 없고 Airflow 환경이 어느 정도 건전하다는 의미입니다.

----


## 명령줄 메타데이터 유효성 검사

```
# db 초기화
airflow db init

# print the list of active DAGs
airflow dags list

# prints the list of tasks in the "tutorial" DAG
airflow tasks list tutorial

# print the hierarchy of tasks in the "tutorial" DAG
airflow tasks list tutorial --tree
```



## 테스트

특정 날짜에 실제 작업 인스턴스를 실행해 테스트해보자. 이 컨텍스트에 지정된 날짜를 `execution_date` 라고 한다. 이겅은 물리적으로 지금(또는 종속성이 충족되는 즉시)실행되지만, 특정 날짜 및 시간에 작업 또는 dag를 실행하는 스케줄러를 시뮬레이션하는 논리적 날짜입니다.

```shell
#command layout: command subcommand dag_id task_id date

# testing print_date
airflow tasks testtutorial print_date 2015-06-01

# testing sleep
airflow tasks test tutorial sleep 2015-06-01
```



이제 이전에 템플릿으로 무엇을 했는지 기억합니까? 다음 명령을 실행해 이 템플릿이 어떻게 렌더링되고 실행되는지 확인하세요.

```shell
# testing templated
airflow tasks test tutorial templated 2015-06-01
```



그러면 이벤트의 자세한 로그가 표시되고 궁극적으로 bash 명령이 실행되고 결과가 인쇄됩니다.

이 명령은 작업 인스턴스를 로컬에서 실행하고, 로그를 stdout(화면)으로 출력하고, 종속성을 신경쓰지 않으며, 상태(실행 중, 성공, 실패 등)를 데이터베이스에 전달하지 않습니다. 단일 작업 인스턴스를 테스트할 수 있습니다. 

```shell
airflow tasks test
```



## 백필(Backfill)

모든 것이 잘 돌아가는 것이 같으니 백필을 실행해 보겠습니다. `backfill`  종속성을 존중하고 로그를 파일로 내보내고 데이터베이스와 대화하여 상태를 기록합니다. 웹서버가 가동 중인 경우 진행상황을 추적할 수 있습니다. 백필이 진행됨에 따라 진행상황을 시각적으로 추적하려는 경우 웹 서버를 시작합니다. 

```shell
airflow webserver
```

 `depends_on_paste=True` 를 사용한 경우,개별 작업 인스턴스는 이전 작업 인스턴스의 성공 여부에 따라 달라진다.`exertion_date==start_date` 작업 인스턴스가 생성되지 않으므로 이 종속성을 무시합니다.



`depends_on_past=True` 를 사용할 때, `wait_for_downstream=True` 또한 사용하고 싶을 수 있다. `depends_on_past=True` 는 태스크 인스턴스가 이전 task_instance의 성공에 의존하게 하고, 태스크 인스턴스가 이전 `wait_for_downstream=True` 태스크 인스턴스의 바로 다운스트림인 모든 태스크 인스턴스가 성공할 때까지 기다리게한다.



이 컨텍스트 날짜 범위는 이 날짜의 작업 인스턴스로 실행 일정 `start_date`이고`end_date`입니다.

```shell
# optional , start a webserver  in debug mode in the background
# airflow webserver --debug &

# start your backfill on a date range
airflow dags backfill tutorial \
	--start-date 2015-06-01 \
	--end-date 2015-06-07
```









----

## 참고 문헌

* https://yogae.tistory.com/32
* https://bcho.tistory.com/1184

* https://airflow.apache.org/docs/apache-airflow/stable/start/local.html
* https://zzsza.github.io/data/2018/01/04/airflow-1/








