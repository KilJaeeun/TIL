## 하둡의 필요성

* 급격이 늘어나느 데이터 처리. 시스템은 일반 하드웨어 처럼 내가 암것도 몰라도 쓸 수 있게 하고 싶음

### 문제점

* 분산 환경에서 연산 수행을 어떻게 할 것인가?
*  분산, 병렬 프로그램이 어렵다.
*  네트워크를 통한 데이터 복사는 오래 걸린다. 
* 장비 장애에 대한 대처도 필요하다. : 노드가 죽어도 끊임없이  데이터 저장

### 저장 인프라

* 신뢰도를 위한 여러번 파일 저장
* 전역 파일 네임 스페이스(global file namespace) 제공
* 분산 파일 시스템(distributed file system)
  * 구글: GFS
  * 하둡: HDFS



### 프로그래밍 모델

* 연산을 데이터가 있는 곳으로 전송
* 맵리듀스(MapReduce)
  * 구글의 연산, 데이터 변환 모델
  * 빅데이터를 우아하게 처리하는 방법

---

## HDFS

### 블록

* 한번에 읽고 쓸 수 있는 최대 데이터량(v1 기본 64M, v2: 기본 128M)
* 파일은 블록크기의 청크(chunk)로 쪼개져서 분산된 서버에 저장한다.(기본 3개 복제본을 저장함)

---

## 하둡 CLI
https://hadoop.apache.org/docs/r2.4.1/hadoop-project-dist/hadoop-common/FileSystemShell.html

| Command                                                      | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| hdfs dfs -mkdir mydir                                       | Create a directory (mydir) in hdfs                           |
| hdfs dfs -ls                                                | List files and directories in hdfs                           |
| hdfs dfs -cat mmyfile                                       | View a file content                                          |
| hdfs dfs -du                                                | check disk space usafe in hdfs                               |
| hdfs dfs -expunge                                           | empty trash on hdfs                                          |
| hdfs dfs -chgrp hadoop file1                                | change group membership of a file                            |
| hdfs dfs -chown huser file1                                 | change file ownership                                        |
| hdfs dfs -rm  file1                                         | delete a file in hdfs                                        |
| hdfs dfs -rmr mydir                                         | delete a directory or file in hdfs                           |
| hdfs dfs -copyFromLocal <source> <destination>              | copy from local filesystem to hdfs                           |
| hdfs dfs -copyToLocal <source> <destination>                | copy from hdfs ro. local filesystem                          |
| hdfs dfs -put <source> <destination>                        | copy from remote location to HDFS                            |
| hdfs dfs -get <source> <destination>                        | copy from hdfs to remote directory                           |
| hdfs dfs -mv file://data/fatafile /user/hduser/data         | move data file from local directory to                       |
| hdfs dfs - setrep -w 3 file 1                               | set the replication factor for file 1 to 3                   |
| hdfs dfs -getmerge mydir bigfile                            | Merge files in mydir directory and download it as one big file |
| hdfs dfs -text myfile                                       | display the content of the hdfs file                         |
| hdfs dfs distcp hddfs://192.168.0.8:8020/input hdfs://192.168.0.8:8020/output | copy data from one cluster to another using the cluster url  |

