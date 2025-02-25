def read_atoms(itp_file):
    """
    读取itp文件中的[atoms]部分，并将原子序号与名称映射存储到字典中。
    """
    with open(itp_file, 'r') as f:
        atom_mapping = {}
        reading_atoms = False
        for line in f:
            line = line.strip()
            if line.startswith(";") or not line:
                continue  # 跳过注释行和空行

            # 检查是否遇到 '[atoms]' 部分，并开始读取
            if '[ atoms ]' in line:
                reading_atoms = True
                continue  # 跳过 '[atoms]' 行

            # 检查是否遇到 '[bonds]' 部分，结束读取
            if reading_atoms and '[ bonds ]' in line:
                break  # 停止读取原子部分

            # 只在 [atoms] 部分读取
            if reading_atoms:
                parts = line.split()
                try:
                    atom_id = int(parts[0])  # 提取原子编号
                    atom_name = parts[4]  # 提取原子名称，第5列
                    atom_mapping[atom_id] = atom_name
                except ValueError as e:
                    print(f"无法处理行: {line}")
                    print(f"错误信息: {e}")

        return atom_mapping


def process_bonds_angles_dihedrals(itp_file, atom_mapping, output_file):
    """
    处理itp文件中的bonds、angles和dihedrals部分，将原子序号转换为原子名称并写入新文件。
    """
    with open(itp_file, 'r') as file, open(output_file, 'w') as output:
        reading_section = None  # 用于标记当前正在处理的部分（bonds/angles/dihedrals）

        for line in file:
            line = line.strip()  # 去除行首尾的空格和换行符
            if line.startswith(';') or not line:
                output.write(line + "\n")  # 写入注释行和空行
                continue  # 跳过注释行和空行

            # 识别并打印bonds、angles和dihedrals部分
            if '[ bonds ]' in line:
                reading_section = 'bonds'
                output.write(f"\n{line}\n")  # 写入该部分的标题
                continue
            elif '[ angles ]' in line:
                reading_section = 'angles'
                output.write(f"\n{line}\n")  # 写入该部分的标题
                continue
            elif '[ dihedrals ]' in line:
                reading_section = 'dihedrals'
                output.write(f"\n{line}\n")  # 写入该部分的标题
                continue

            # 处理bonds、angles和dihedrals的具体数据行
            if reading_section:
                parts = line.split()  # 将每行分割成部分
                try:
                    if reading_section == 'bonds':
                        # 对于bonds部分，处理前两个原子序号
                        atom_ids = list(map(int, parts[:2]))  # 提取前两个原子序号（原子编号）
                        atom_names = [atom_mapping.get(id, f'Unknown (ID {id})') for id in atom_ids]  # 获取原子名称
                        remaining_data = ' '.join(parts[2:])  # 获取剩余数据
                        output.write(f"{' '.join(atom_names)} {remaining_data}\n")
                    elif reading_section == 'angles':
                        # 对于angles部分，处理前三个原子序号
                        atom_ids = list(map(int, parts[:3]))  # 提取前三个原子序号
                        atom_names = [atom_mapping.get(id, f'Unknown (ID {id})') for id in atom_ids]  # 获取原子名称
                        remaining_data = ' '.join(parts[3:])  # 获取剩余数据
                        output.write(f"{' '.join(atom_names)} {remaining_data}\n")
                    elif reading_section == 'dihedrals':
                        # 对于dihedrals部分，处理四个原子序号
                        atom_ids = list(map(int, parts[:4]))  # 提取四个原子序号
                        atom_names = [atom_mapping.get(id, f'Unknown (ID {id})') for id in atom_ids]  # 获取原子名称
                        remaining_data = ' '.join(parts[4:])  # 获取剩余数据
                        output.write(f"{' '.join(atom_names)} {remaining_data}\n")
                except ValueError as e:
                    print(f"无法处理数据: {line}")
                    print(f"错误信息: {e}")
                    output.write(line + "\n")  # 若出错，直接写入原始行

# 主函数，负责读取文件并处理数据
def main(itp_file):
    try:
        # 读取原子信息并生成原子映射字典
        atom_mapping = read_atoms(itp_file)

        # 创建新的文件名（在原文件目录下加上 '_rn' 后缀）
        output_file = itp_file.replace('.itp', '_rn.itp')

        # 处理bonds、angles、dihedrals部分并写入新文件
        process_bonds_angles_dihedrals(itp_file, atom_mapping, output_file)
        print(f"处理完成，结果已写入: {output_file}")
    except Exception as e:
        print(f"发生错误: {e}")  # 捕获并打印错误

# 执行主函数
if __name__ == '__main__':
    itp_file = r"GM_graft.itp"  # 请替换为你的itp文件路径
    main(itp_file)

