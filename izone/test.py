# 文件名: izone -> test
# 创建时间: 2020/7/4 8:28
import os


def test_getenv():
	# 获取环境变量
	print(os.getenv('IZONE_REDIS_HOST', '127.0.0.1'))
	
	print("debug: ", os.getenv('IZONE_DEBUG', 'True').upper() == 'TRUE')
	
	
	print("start test getenv() function:\n")
	
	print(os.getenv("SystemRoot"))          #-- 系统根目录
	print(os.getenv("WoXiaXieDe"))          #-- 我乱写的
	print(os.getenv("ALLUSERSPROFILE"))     #-- 所有“用户配置文件”的位置
	print(os.getenv("alluserSpRoFilE"))     #-- 所有“用户配置文件”的位置
	print(os.getenv("COMPUTERNAME"))        #-- 计算机的名称
	
	print("\n")
	
	print(os.getenv("COMSPEC"))             #-- 命令行解释器可执行程序的准确路径
	print(os.getenv("HOMEDRIVE"))           #-- 连接到用户主目录的本地工作站驱动器号
	print(os.getenv("HOMEPATH"))            #-- 用户主目录的完整路径
	print(os.getenv("NUMBER_OF_PROCESSORS"))#-- 安装在计算机上的处理器的数目
	print(os.getenv("OS"))                  #-- 操作系统的名称
	
	print("\n")
	
	print(os.getenv("PROCESSOR_LEVEL"))     #-- 计算机上安装的处理器的型号
	print(os.getenv("PATHEXT"))             #-- 连接到用户主目录的本地工作站驱动器号
	print(os.getenv("PROCESSOR_REVISION"))  #-- 处理器修订号的系统变量
	print(os.getenv("TEMP"))                #-- 临时目录
	print(os.getenv("SYSTEMDRIVE"))         #-- 系统根目录的驱动器


if __name__ == '__main__':
	test_getenv()
