import json, os, re

# 从 config.json 读取配置信息
with open("config.json", "r", encoding="utf-8") as fconfig:
    config = json.load(fconfig)

work_dir = config["WorkDir"]
dest_dir = config["DestDir"]
gerber_custom = config["GerberCustom"]  # 使用 GerberCustom 作为规则
gerber_type = config["GerberType"]  # 使用 GerberType 作为文件类型
work_dir_files = os.listdir(work_dir)

if not dest_dir:
    dest_dir = os.path.join(work_dir, 'output')
if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)

# 创建 PCB 下单必读文档
with open(os.path.join(dest_dir, config["TextFileName"]), "w") as text_file:
    text_file.write(config["TextFileContent"])

# 选择一个特定的规则集，例如 'KiCad' 或 'AD'
selected_rule_set = gerber_custom[gerber_type]

# 对匹配到的文件进行重命名和添加头部信息
for key, value in selected_rule_set.items():
    match_file = None
    re_pattern = re.compile(pattern=value)

    for file_name in work_dir_files:
        if re_pattern.search(file_name):
            match_file = file_name
            break

    if match_file:
        # 找到文件，执行重命名和添加头部信息
        with open(os.path.join(work_dir, match_file), "r") as file:
            file_data = file.read()
        with open(os.path.join(dest_dir, config["FileName"][key]), "w") as file:
            file.write(config["Header"])
            file.write(file_data)
        print(key + " -> " + match_file)
    else:
        # 文件未找到，继续处理下一个
        print(key + " 文件未找到，跳过处理")
