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