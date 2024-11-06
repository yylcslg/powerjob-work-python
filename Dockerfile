FROM python:3.11.4

WORKDIR /home
WORKDIR config
WORKDIR ../powerjob-work-python/src
WORKDIR ../
WORKDIR log
WORKDIR ../


COPY requirements.txt ./
COPY worker.py ./

#RUN pip install  -r requirements.txt
#解决速度慢问题
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip3 install  -r requirements.txt


COPY src /home/powerjob-work-python/src
COPY resource/config/param.properties /home/config

WORKDIR /home/powerjob-work-python/

CMD [ "python", "powerjob_worker.py" ]
