# TypeLedger

**简体中文** | [English](./README.md)

一个安静、注重隐私的 Windows 输入统计工具，用来理解你的每日产出、输入节奏和周效率。

TypeLedger 在本机后台运行，常驻系统托盘，只记录汇总输入指标。它帮助你看清自己是否正在形成稳定的写作或编码节奏，同时不会保存你输入的具体内容。

```text
本地优先。不需要账号。不保存原始输入文本。
```

## 快速了解

| 项目 | 说明 |
| --- | --- |
| 平台 | Windows 桌面 |
| 适合人群 | 写作者、开发者、研究者、学生、知识工作者 |
| 界面语言 | 英文和简体中文 |
| 数据 | 本地汇总指标 |
| 隐私 | 不保存原始输入文本、剪贴板内容或截图 |
| 打包方式 | PyInstaller Windows 绿色版 |

## 快速入口

- [English README](./README.md)
- [从源码运行](#从源码运行)
- [打包 Windows 应用](#打包-windows-应用)
- [发布检查清单](./docs/release-checklist.md)

## 它能帮你理解什么

TypeLedger 主要围绕几个实际问题设计：

- 我今天到底有没有真正写东西或写代码？
- 这一周比上一周更高效吗？
- 产出变多是因为工作更久，还是因为效率更高？
- 我通常在一天中的哪个时间段输入最多？
- 我的长期写作或编码节奏有没有变得更稳定？

## 核心功能

| 模块 | 能力 |
| --- | --- |
| 每日统计 | 净字符数、键盘输入、粘贴字符、退格次数、准确率估算 |
| 会话节奏 | 当前会话、上一会话、会话时长、最近活跃情况 |
| 速度估算 | 基于最近键盘输入估算 CPM 和 WPM |
| 周效率 | 周产出、活跃时长、活跃效率、较上周和目标的对比 |
| 历史记录 | 每日记录、近 30 天趋势、小时分布、CSV 导出 |
| 系统托盘 | 后台运行、托盘菜单、快速打开设置和历史记录 |
| 本地化 | 支持英文和简体中文界面 |

## 隐私模型

TypeLedger 只保存汇总数字。

它会记录输入字符数、粘贴字符数、退格次数、会话时长、小时统计和周汇总等指标。它不会保存原始输入文本、剪贴板内容、窗口标题、网站地址、文件名、截图或按键序列。

应用在你的 Windows 本机运行，不需要云账号。

## 下载和使用

从 [GitHub Releases](https://github.com/Yijian6/type-ledger/releases) 下载最新绿色版：

```text
TypeLedger-windows-portable.zip
```

然后：

1. 解压到你信任的文件夹。
2. 运行 `TypeLedger.exe`。
3. 如果主窗口启动后隐藏了，请从系统托盘打开。

当前版本还没有代码签名。Windows SmartScreen 或安全软件可能会提示风险，因为应用需要使用全局键盘钩子来统计按键数量。这是本地输入统计工具常见的情况。TypeLedger 不会保存你输入的具体内容。

开发者也可以使用下面的源码运行方式。

## 从源码运行

要求：

- Windows
- Python 3.11+

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## 打包 Windows 应用

安装开发依赖：

```powershell
.venv\Scripts\pip install -r requirements-dev.txt
```

打包绿色版应用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_windows.ps1
```

输出文件：

```text
dist\TypeLedger\TypeLedger.exe
dist\TypeLedger-windows-portable.zip
```

## 本地数据

TypeLedger 的本地数据保存在：

```text
%APPDATA%\TypeRecord\
```

文件夹名称继续使用 `TypeRecord`，是为了兼容早期版本的数据。

主要文件：

- `data\daily_counts.json`
- `config\settings.json`
- `data\logs\type_record.log`

## 开发

运行测试：

```powershell
python -m pytest
```

运行代码检查：

```powershell
ruff check .
```

## 当前状态

TypeLedger 仍然是早期阶段的个人效率工具。当前重点是可靠性、本地优先隐私、干净的 Windows 打包，以及更完整的中英文用户体验。

## 许可证

当前还没有声明许可证。如果要更大范围发布或接受外部贡献，建议先补充许可证。
