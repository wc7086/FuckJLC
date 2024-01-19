import json, os, re, shutil, sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import windnd

# 创建主窗口
root = tk.Tk()
root.title("GUI Window")

# 获取屏幕尺寸以及窗口尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 330
window_height = 330

# 计算屏幕中央的坐标
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

# 设置窗口的大小和位置
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# 禁止窗口的宽度和高度调整（固定窗口大小）
root.resizable(False, False)

# 文件拖放
def dragged_files(folder_path):
    input_entry.delete(0, tk.END)
    input_entry.insert(0, folder_path[0])

# 配置所有列的权重为1，使其可以扩展
for col in range(3):
    root.grid_columnconfigure(col, weight=1)

# 配置所有行的权重为1，使其可以扩展
for row in range(4):  # 现在有4行
    root.grid_rowconfigure(row, weight=1)

# 定义打开文件的函数
def browse_input():
    input_folder_path = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_folder_path)

# 定义浏览文件的函数
def browse_output():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def on_select(event):
    # 获取选中的值
    print("选中:", config.get())

def load_config():
    try:
        with open("config.json", "r", encoding="utf-8") as json_file:
            config_data = json.load(json_file)

        # 获取 WorkDir 和 DestDir，确保它们是字符串
        work_dir = str(config_data.get("WorkDir", ""))
        dest_dir = str(config_data.get("DestDir", ""))

        # 更新输入框的值
        input_entry.delete(0, tk.END)
        input_entry.insert(0, work_dir)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, dest_dir)

        # 从 GerberCustom 获取下拉框的选项
        gerber_custom_options = list(config_data["GerberCustom"].keys())
        config["values"] = gerber_custom_options

        # 设置默认选项
        default_gerber_type = config_data.get("GerberType", gerber_custom_options[0] if gerber_custom_options else "")
        config.set(default_gerber_type)
    except Exception as e:
        custom_print(f"读取配置文件时出错: {e}")

def modify_files(work_dir, dest_dir, gerber_type, header, text_file_name, text_file_content, file_names, gerber_custom):
    work_dir_files = os.listdir(work_dir)

    if not dest_dir:
        dest_dir = os.path.join(work_dir, 'output')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(os.path.join(dest_dir, text_file_name), "w") as text_file:
        text_file.write(text_file_content)

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
            with open(os.path.join(work_dir, match_file), "r") as file:
                file_data = file.read()
            with open(os.path.join(dest_dir, file_names[key]), "w") as file:
                file.write(header)
                file.write(file_data)
            custom_print(key + " -> " + match_file)
        else:
            custom_print(key + " 文件未找到，跳过处理")

def save_to_json_and_run_modify():
    try:
        clear_output()
        # 读取现有的配置
        with open("config.json", "r", encoding="utf-8") as json_file:
            config_data = json.load(json_file)

        # 从 GUI 获取数据并更新配置
        config_data["WorkDir"] = input_entry.get()
        config_data["DestDir"] = output_entry.get()
        config_data["GerberType"] = config.get()

        # 将更新后的数据写回 config.json
        with open("config.json", "w", encoding="utf-8") as json_file:
            json.dump(config_data, json_file, indent=4, ensure_ascii=False)

        # 调用 modify_files 函数
        modify_files(
            config_data["WorkDir"],
            config_data["DestDir"],
            config_data["GerberType"],
            config_data["Header"],
            config_data["TextFileName"],
            config_data["TextFileContent"],
            config_data["FileName"],
            config_data["GerberCustom"]
        )
    except Exception as e:
        custom_print(f"保存配置并运行修改时出错: {e}")

# 创建自定义打印函数
def custom_print(text):
    output_text.insert(tk.END, text + "\n")  # 在文本框的末尾添加文本
    output_text.see(tk.END)  # 自动滚动到最新的文本

# 创建清空输出框内容的函数
def clear_output():
    output_text.delete("1.0", tk.END)

def get_resource_path(relative_path):
    """ 获取资源的绝对路径。用于 PyInstaller 打包后资源的访问 """
    try:
        # PyInstaller 创建的临时文件夹的路径
        base_path = sys._MEIPASS
    except Exception:
        # 正常执行时的路径
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def copy_config_to_current_dir():
    config_filename = "config.json"
    temp_config_path = get_resource_path(config_filename)
    current_dir_config_path = os.path.join(os.getcwd(), config_filename)

    if not os.path.isfile(current_dir_config_path):
        # 如果当前目录下没有 config.json，则从临时目录复制
        shutil.copy(temp_config_path, current_dir_config_path)

# 创建下拉框
config_label = tk.Label(root, text="配置文件", anchor="e")
config_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
config = ttk.Combobox(root, state="readonly")
config.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

# 绑定选择事件
# config.bind("<<ComboboxSelected>>", on_select)

# 创建输入框和其标签
input_label = tk.Label(root, text="Gerber 文件夹", anchor="e")
input_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
input_entry = tk.Entry(root, width=18)
input_entry.grid(row=1, column=1, padx=5, pady=5)

# 创建输出框和其标签
output_label = tk.Label(root, text="输出文件夹", anchor="e")
output_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
output_entry = tk.Entry(root, width=18)
output_entry.grid(row=2, column=1, padx=5, pady=5)

# 创建浏览输入文件夹按钮
browse_input_button = tk.Button(root, text="浏览文件夹", command=browse_input)
browse_input_button.grid(row=1, column=2, padx=5, pady=5)

# 创建浏览输出文件夹按钮
browse_output_button = tk.Button(root, text="浏览文件夹", command=browse_output)
browse_output_button.grid(row=2, column=2, padx=5, pady=5)

# 创建一个按钮，使其填满最后一行的所有单元格
# 我们使用columnspan=3来跨越三列
fill_button = tk.Button(root, text="Fuck JLC", command=save_to_json_and_run_modify)
fill_button.grid(row=3, column=0, padx=5, pady=5, columnspan=3, sticky="nsew")

# 创建输出框
output_text = tk.Text(root, height=10)  # 设置输出框的高度
output_text.grid(row=4, column=0, columnspan=3, sticky="ew")

copy_config_to_current_dir()

load_config()

windnd.hook_dropfiles(root, func=dragged_files)

# 运行主循环
root.mainloop()
