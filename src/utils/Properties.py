import os

from src.utils import tools_utils


class Properties:

    def __init__(self, file_name):
        self.file_name = file_name

    def getProperties(self):
        try:
            pro_file = open(self.file_name, 'r', encoding='utf-8')
            properties = {}
            for line in pro_file:
                if line.find('=') > 0:
                    strs = line.replace('\n', '').split('=')
                    properties[strs[0]] = strs[1]
        except Exception as e:
            raise e
        else:
            pro_file.close()
        return properties

pro = Properties(tools_utils.project_path()+'resource/config/param.properties').getProperties()

if __name__ == '__main__':

    pro = Properties(tools_utils.project_path()+'resource/config/param.properties')

    print(pro.getProperties())