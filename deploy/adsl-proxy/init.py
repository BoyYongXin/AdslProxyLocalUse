import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootpath=str(curPath)
syspath=sys.path
depth = rootpath.count("\\") - 1
sys.path=[]
sys.path.append(rootpath)#将工程根目录加入到python搜索路径中
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[depth]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
#print(sys.path)