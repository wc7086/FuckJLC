# FuckJLC

核心代码源自 https://github.com/acha666/FuckJLC

将其他EDA软件的gerber转换为立创EDA格式的脚本

# Usage

## 命令行版本`modify.py`

首先查看`config.yaml`，修改工作目录等配置信息，选择适合你的规则

然后运行脚本，在输出目录中查看处理完成的gerber

最后复制钻孔文件

``` shell
# yum/apt/brew/scoop/winget install python
pip install json
python modify.py
```

# 文件结构

* `modify.py` 脚本主文件
* `config.yaml` 通用配置信息

## GUI版本`gui.py`

1. 下载 [Release](https://github.com/wc7086/fuckself/releases) 中的 [FKJLC_win-x64.zip](https://github.com/wc7086/fuckself/releases/download/v0.1.0/FKJLC_win-x64.zip) 解压后直接运行，有概率误报

2. 运行目录中的`gui.py`

```shell
pip install json
python gui.py
```



# 提示

目前仅对有限格式的gerber做适配，其他软件请发Issue并附带目录结构或者自力更生PR

脚本并未严格测试，仅给各位提供一个绕过检测的思路，保险起见仍建议各位手动进行修改

由于钻孔文件格式千奇百怪，脚本**不处理钻孔文件**，脚本完成后你需要手动复制钻孔文件

作者并没有仔细研究嘉立创的判定规则，目前看来凑合能用，就这样吧

作者不为使用脚本造成的任何后果负责

欢迎一切 新功能/bug/建议/对线/改错字 Issue/PR

# 工作原理

脚本将会将你的gerber重命名为立创EDA的命名格式，并在gerber文件的头部添加立创EDA的注释信息

除此之外，脚本不会做任何处理

**低调使用**
