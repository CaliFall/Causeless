import os
import re

def count_chinese_characters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
        count = len(chinese_chars)
        return count

def traverse_folder(folder_path):
    total = 0
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith('.md'):  # 只处理文本文件，你可以根据需要更改文件扩展名
                count = count_chinese_characters(file_path)
                print(f'{file_name} 中的汉字数量: {count}')
                total += count
    print(f'该文件夹中总共有 {total} 个汉字\n')


# 指定要遍历的文件夹路径
folder_path = ['../Chapters']
for folder in folder_path:
    print(folder+":")
    traverse_folder(folder)
