from time import sleep


def readTxt():
    path = '/home/yinyunlong/person/1/'
    with open(path + "123.txt", "r") as f:
        data = f.readlines()
    i = 0
    for str in data:
        line = str.strip()
        if line != '':
            print(line)
            i = i + 1
            if (i % 10 == 0):
                sleep(5)


    print(data.__sizeof__())




if __name__ == '__main__':
    readTxt()