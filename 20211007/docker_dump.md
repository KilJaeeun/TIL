# Docker

* docker pull ubuntu
* docker images

* RUN
  * `docker run -it -d ubuntu`
    * `docker run -it -p 81:80 -d <new image name >` 
  * `docker ps`
* EXEC
  * `docker exec -it <container ID >  <program in the container>`
  * `exit`
* STOP
  * `docker stop <container id> ` // docker kill  container id
  * `docker kill <container id> ` 
  * `docker ps -a`
* REMOVE
  * `docker rm <container id> ` // remove container
  * `docker kill <container id>`
  * `docker ps -a`
* REMOVE
  * `docker rm <container id> ` // remove container
  * `docker rmi <image id > `// remove image



* COMMIT 
  * `docker commit <contiainer id > < new image name > `
  * `docker run -it -d <image name >`
  * `docker exec -it <container id> bash`



#### Docker File

* docker image 를 만들기 위해 내리는 command 를 모아둔 text 파일
  * docker build command를 사용해 docker 파일로부터 container 생성
* docker builld command 를 사용해 docker 파일로부터 container 생성
* docker command를 입력해 container를 수동으로 생성하는 대신에 docker 파일을 작성하고 이후에 build command로 모든 과정을 수행해 해당 container 생성

----

# Docker Compose vs Swarm

Compose 는 동일 호스트에서 두 개이상의 컨테이너를 운영

Swarm 은 컨테이너들을 cluster 하고 schedule 해서 전체 컨테이너 클러스터를 하나의 virtual 단일 컨테이너로 관리하고 각 컨테이너의 상태를 모니터링해서 컨테이너 수를 각 호스트에서 늘이거나 줄이면서 운영하는 도구이다.

swarm은 여러 호스트에서 다수의 컨테이너들을 운영, auto scaling 기능을 한다.



### 	creating a swarm cluster

* `docker swarm init --advertise-addr = <IP address>`
* `docker node ls` in master node



#### Deploy an app on docker swarm

Docker service = worker 노드에서 상당 기간 실행되는 docker container



#### Creating a service

`docker service create --name < service name > --replicas <# of replicas > -p < port mapping > <image name>`

`docker service ls`

`docker ps`

`docker rm -f <container id> ` 를 실행해 auto scaling 기능 확인 

`docker ps` 로 오토 스케일링 확인

`docker service scale <service name > = <# of service instances > ` 를 실행해 스케일 업, 다운



#### Removing a service

`docker service rm. serivce name>`





`docker swarm leave <on worker>`

`docker swarm leave --forcr (on master)`



----

# 쿠버네티스

* master components
  * API server
  * scheduler
  * control manager
  * etcd

* worker components
  * kubelet
    * container running 을 책임
  * kube-proxy
    * 각 노드의 network proxy
  * pod
    * 1개 이상 도커 컨테이너 포함

