## powerjob-work-python

```shell
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release


curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo systemctl enable docker

sudo systemctl start docker

```

## 根据dockerfile 生成 image


```shell
#get 镜像
sudo docker pull java-app/xpds-xcore:latest


 docker exec -it 3169fc4d7277 /bin/bash

#删除 镜像
 sudo docker rmi -f powerjob_work_python:v1

# build 新镜像
 sudo docker build -t powerjob_work_python:v1 .

#查看image
 sudo docker images

#运行 image
 #sudo docker run -it powerjob_work_python:v1

#查看运行中 容器
sudo docker ps

sudo docker run \
    -d --network=host \
    -v /home/yinyunlong/person/python_workspace/powerjob-work-python/resource/:/home/yinyunlong/person/python_workspace/powerjob-work-python/resource/ \
    -v /home/yinyunlong/person/python_workspace/powerjob-work-python/src/task/:/home/yinyunlong/person/python_workspace/powerjob-work-python/src/task/ \
    -it powerjob_work_python:v1


sudo docker run -d --network=host -v /home/yinyunlong/person/python_workspace/powerjob-work-python/resource/:/home/yinyunlong/person/python_workspace/powerjob-work-python/resource/ -v /home/yinyunlong/person/python_workspace/powerjob-work-python/src/task/:/home/yinyunlong/person/python_workspace/powerjob-work-python/src/task/ -it powerjob_work_python:v1 


#进入 container
sudo docker run -i -t powerjob_work_python:v1 /bin/bash

#停止容器

sudo docker stop  [container_id]

sudo docker inspect [container_id]

# 停止 容器的 always 设置
sudo docker update --restart=no [container_id]


redis安装说明-需要创建路径（/home/vimtech/tool/server/redis_5.0.14/data），配置好配置文件redis.conf，然后运行如下命令

sudo docker run -p 6379:6379 --name redis5.0.14 -v /home/yinyunlong/person/program/docker/redis/config/redis.conf:/etc/redis/redis.conf  -v /home/yinyunlong/person/program/docker/redis/data:/data  -d --restart=always redis:5.0.14 --appendonly yes 


sudo docker run --net=host -p 6300:6300 --name redis5.0.14 -v /data/prov/data/docker/redis/config/redis.conf:/etc/redis/redis.conf  -v /data/prov/data/docker/redis/data:/data  -d --restart=always redis:5.0.14 --appendonly yes 


```


## 生成 requirements.txt


```shell
#安装 requirements.txt 依赖
pip install -r requirements.txt

pip freeze > requirements.txt
```


## 生成 可执行文件
```shell
pyinstaller -F powerjob_worker.py
```

## docker compose 使用

```shell
#启动 compose 容器
sudo docker compose  up 

#后台 启动 compose 容器 -d
sudo docker compose  up -d

#停止 compose 容器
sudo docker compose down

#查看所有启动容器
sudo docker compose ps


sudo docker-compose -f docker-compose.yml up


sudo docker-compose -f /home/yinyunlong/person/python_workspace/powerjob-work-python/docker-compose.yml up -d

sudo docker-compose -f /home/yinyunlong/person/python_workspace/powerjob-work-python/docker-compose.yml down

```

## 清理所有停止运行的容器

```shell
sudo docker rm container_id

sudo docker container prune

sudo docker image prune

sudo docker volume prune

```

## 配置文件路径

/home/config/


