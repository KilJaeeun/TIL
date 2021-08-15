# Airflow API에 대한 자습서

이 자습서는 일반 airflow 자습서 기반으로 특히 airflow 2.0 의 일부로 도입된 taskflow api 패러다임 사용해 데이터 파이프라을 작성하는데 중점을 두고 이를 기존 패러다임을 사용해 작성된 DAG 와 대조 합니다.



여기에서 선택한 데이터 파이프라인은 추출, 변환 및 로드에 대한 세 가지 개별 작업이 있는 간단한 ETL 패턴한다.

## "Taskflow API" ETL 파이프라인 예

다음은 Taskflow API 패러다임을 사용하는 매우 간단한 ETL 파이프라인입니다. 자세한 설명은 아래에 나와 있습니다.

```python
# tutorial_taskflow_api_etl.py
import json

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

# 이러한 인수는 각 연산자에게 전달됩니다.
# 연산자를 초기화하는 동안 태스크별로 이러한 항목을 재정의할 수 있습니다.

default_args ={
  'owner':'airflow'
}
@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['example'])
def tutorial_taskflow_api_etl():
  """
    ### TaskFlow API Tutorial Documentation
   	이것은 다음의 용도를 보여주는 간단한 ETL 데이터 파이프라인 예제입니다.
    추출, 변환 및 로드에 대해 세 가지 간단한 작업을 사용하는 TaskFlow API입니다.
    Flow TaskFlow API 튜토리얼과 함께 제공되는 설명서가 있습니다.
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
	"""
  @task
  def extract():
    """
    #### Extract task
    나머지 데이터 파이프라인에 대해 데이터를 준비하는 간단한 추출 작업입니다. 
    이 경우 하드 코딩된 JSON 문자열에서 데이터를 읽어 시뮬레이션합니다.
    """
    data_string ='{"1001":301.27, "1002":433.21, "1003":502.22}'
    order_data_dict = json.loads(data_string)
    return order_data_dict
  
  
  @task(multiple_output=True)
	def transform(order_data_dict: dict):
    """
    #### Transform task
		주문 데이터 집합을 가져와 총 주문 값을 계산하는 간단한 변환 작업입니다.
    """
    total_order_value = 0
    for value in order_data_dict.values():
      total_order_value +=value
      
    return {"total_order_value":total_order_value}

	@task()
  def load(total_order_value : float):
    """
    #### Load Task
    변환 작업의 결과를 가져와서 최종 사용자 검토에 저장하는 대신 인쇄하는 단순 로드 작업입니다.
    """
		print(f"Total order value is : {total_order_value:.2f}")
	order_data = extract()
	order_summary = transform(order_data)
  load(order_sumary["total_order_value"])
 

tutorial_etl_dag = tutorial_taskflow_api_etl()

```



## DAG 정의 파일입니다.

이 파일이 처음 보는  DAG 파일의 경우, 이 python 스크립트는 flowflow 에 의해 해석되며 
데이터 파이프라인에 대한 구성 파일이 됩니다. DAG 파일에 대한 전체 소개를 보려면 DAG 구조와 정의를 광범위하게 다루는 핵심 flowFlow 튜토리얼을 참고하십시오.





## DAG 인스턴스화

우리는 업무 간의 의존성을 가지고 업무의 집합인 DAG를 만들고 있습니다. 이는 매우 간단한 정의입니다. 다시 시도하거나 복잡한 예약 없이 Airflow로 DAG를 설정하기만 하면 되기 때문입니다. 이 예에서는 아래와 같이 python 함수 이름이 DAG 식별자 역할을 하는 `@dag` decorator를 사용하여 이 DAG를 만들고 있습니다.

```python
@dag(default_args=default_args, schedule_interval = None, start_date=days_ago(2), tag=['example'])
def tutorial_taskflow_api_etl():
  """
  ### TaskFlow API Tutorial Documentation
  이것은 다음의 용도를 보여주는 간단한 ETL 데이터 파이프라인 예제입니다.
    추출, 변환 및 로드에 대해 세 가지 간단한 작업을 사용하는 TaskFlow API입니다.
    Flow TaskFlow API 튜토리얼과 함께 제공되는 설명서는 다음과 같습니다.
    위치했다
  """
```



## Tasks

이 데이터 파이프라인에서는 `@task`를 리용ㅇ해 파이썬 함수를 기반으로 태스크가 생성된다. 함수 이름은 태스크의 고유 식별자로 사용된다.

```python
@task()
def extract():
  """
  #### Extract task
  나머지 데이터 파이프라인에 대해 데이터를 준비하는 간단한 추출 작업입니다. 
  이 경우 하드 코딩된 JSON 문자열에서 데이터를 읽어와서 시뮬레이션합니다.
  """
  data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

  order_data_dict = json.loads(data_string)
  return order_data_dict
```

변환 및 로드 태스크는 위에 표시된 추출 태스크와 동일한 방식으로 생성된다.







## DAG의 주 흐름

```python
order_data = extract()
order_summary = transform(order_data)
load(order_summary["total_order_value"])
```





이제 이 흐름을  DAG로 실행하려면 python 함수를 호출하면 된다.

```python
tutorial_etl_dag = tutorial_taskflow_api_etl()
```











## 2.0 이전에 DAG 를 작성해야했던 방법

```python
import json
from textwrap import dedent

# The DAG object; DAG 를 인스턴스화 하기위해 필요함.
from airflow import DAG
# Operators: we need this to operate
from airflow.operators.python import PythonOperator
from airflow.utils.date import days_ago

# 이러한 인수는 각 연산자에게 전달됩니다.
# 연산자를 초기화하는 동안 작업별로 재지정할 수 있습니다.
default_args={
  'owner':'airflow'
}
with DAG(
    'tutorial_etl_dag',
    default_args=default_args,
    description='ETL DAG tutorial',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    dag.doc_md = __doc__
    def extract(**kwargs):
        ti = kwargs['ti']
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        ti.xcom_push('order_data', data_string)
    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='extract', key='order_data')
        order_data = json.loads(extract_data_string)

        total_order_value = 0
        for value in order_data.values():
            total_order_value += value

        total_value = {"total_order_value": total_order_value}
        total_value_json_string = json.dumps(total_value)
        ti.xcom_push('total_order_value', total_value_json_string)
    def load(**kwargs):
        ti = kwargs['ti']
        total_value_string = ti.xcom_pull(task_ids='transform', key='total_order_value')
        total_order_value = json.loads(total_value_string)

        print(total_order_value)
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> transform_task >> load_task

    
```

위와 같은 모든 가공은 새로운 기류 2.0 dag에서도 이루어지고 있지만, 이 모든 것은 DAG 개발자로부터 추상화되었다.

Transform 태스크는 다음과 같으므로 별도로 검토하여 자세히 살펴보도록 하자. 데이터 파이프라인 중간에. 기류 1.x에서 이 작업은 다음과 같이 정의된다.





## 가상 환경에서 Taskflow API 사용

기류 2.0.3을 기준으로 Taskflow API를 다음과 같이 사용할 수 있다. 가상 환경 이 추가된 기능은 훨씬 더 많은 것을 가능하게 할 것이다. Taskflow API에 대한 포괄적인 사용 사례 범위(이에 국한되지 않음) 공기 흐름 작업자의 패키지 및 시스템 라이브러리.

가상 환경에서 공기 흐름 태스크를 실행하려면 전환하십시오. `@task` 에 대한 장식가. `@task.virtualenv` 장식가 그 `@task.virtualenv` 실내 장식가에서는 사용자 지정 라이브러리로 새로운 가상 환경을 만들 수 있다. 그리고 당신의 기능을 실행할 수 있는 다른 파이톤 버전도 있다.

```python
@task.virtualenv(
    use_dill=True,
    system_site_packages=False,
    requirements=['funcsigs'],
)
def extract():
    """
    #### Extract task
    A simple Extract task to get data ready for the rest of the data
    pipeline. In this case, getting data is simulated by reading from a
    hardcoded JSON string.
    """
    data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

    order_data_dict = json.loads(data_string)
    return order_data_dict

```



## 다중 출력 추론

업무 또한 받아쓰기를 이용해 여러 출력을 추론할 수 있다.

```python
@task
def identity_dict(x:int, y:int)-> Dict[str,int]:
  return {"x": x, "y": y}
```

타이핑을 사용해 Dict 기능 반환 유형에 대해 ,multiple_outputs 매개 변수는 자동으로 true 로 설정됩니다.

참고로 수동으로 설정할 경우, multiple_outputs 매개변수 추론이 비활성되며 매개변수 값이 사용됩니다.



## 일반 태스크에서 장식된 태스크



```python
@task()def extract_from_file():  """  #### Extract from file task  파일의 데이터를 팬더 데이터 프레임으로 읽어 나머지 데이터 파이프라인에 사용할 데이터를 준비하는 간단한 추출 작업  """    order_data_file = '/tmp/order_data.csv'    order_data_df = pd.read_csv(order_data_file)file_task = FileSensor(task_id='check_file', filepath='/tmp/order_data.csv')order_data = extract_from_file()file_task >> order_data
```

위의 코드 블록에서 새로운 파이톤 기반 작업은 다음과 같이 정의된다. `extract_from_file` 어떤 것 알려진 파일 위치에서 데이터를 읽는다. 메인 DAG에서 새로운 기능 `FileSensor` 태스크는 이 파일을 검사하도록 정의된다. 부디 참고하세요 이 작업이 파일을 기다리는 센서 작업인지 확인하십시오. 마지막으로 이 센서 태스크와 파이선 기반 태스크 간의 종속성이 지정된다.