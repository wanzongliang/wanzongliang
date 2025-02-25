def sort_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        lines = [line.strip() for line in lines]
        lines.sort()
        
        with open(filename, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write('    ' + line + '\n')
                
        print(f"{filename} 文件排序成功")
    
    except Exception as e:
        print(f"处理文件时出错: {e}")

sort_file_content('1.txt')
