import os
import sys


def list_files(directory):
	"""打印目录中所有文件名（按字母排序）"""
	try:
		with os.scandir(directory) as entries:
			files = sorted(
				entry.name
				for entry in entries
				if entry.is_file()
			)
			
			if not files:
				print("该目录中没有文件")
				return
			
			print(f"\n目录 [ {directory} ] 中的文件列表：")
			for idx, filename in enumerate(files, 1):
				fl = filename.split(".")
				print("- [*{}*](./Chapters/{})".format(fl[0], filename))
	
	except FileNotFoundError:
		print(f"错误：目录不存在 - {directory}")
	except PermissionError:
		print(f"错误：无权限访问 - {directory}")


if __name__ == "__main__":
	# 获取目标目录路径
	target_dir = "../Chapters"
	
	# 验证路径有效性
	if not os.path.exists(target_dir):
		print(f"错误：路径不存在 - {target_dir}")
		sys.exit(1)
	
	if not os.path.isdir(target_dir):
		print(f"错误：这不是一个目录 - {target_dir}")
		sys.exit(1)
	
	# 执行文件列表打印
	list_files(target_dir)