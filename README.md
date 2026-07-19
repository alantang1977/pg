<div align="center">
  <img src="https://raw.githubusercontent.com/alantang1977/X/main/Pictures/SuperMAN.png" alt="logo"/>
  <h1 align="center">IPTV 直播源聚合项目</h1>
</div>

<div align="center">
  所有资源均来自于各路大神无私分享，如有侵权，请联系删除。所有以任何方式查看本仓库内容的人或直接或间接使用本仓库内容的使用者都应仔细阅读此声明。本仓库管理者保留随时更改或补充此免责声明的权利。一旦使用、复制、修改了本仓库内容，则视为您已接受此免责声明。
</div>
<br>

<p align="center">
  <a href="https://github.com/alantang1977/pg/releases">
    <img src="https://img.shields.io/github/v/release/alantang1977/pg" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-%20%3D%203.12-47c219" />
  </a>
  <a href="https://github.com/alantang1977/pg/releases">
    <img src="https://img.shields.io/github/downloads/alantang1977/pg/total" />
  </a>
  <a href="https://github.com/alantang1977/pg">
    <img src="https://img.shields.io/github/stars/alantang1977/pg" />
  </a>
  <a href="https://github.com/alantang1977/pg/fork">
    <img src="https://img.shields.io/github/forks/alantang1977/pg" />
  </a>
</p>

## 项目简介

本项目是一个IPTV直播源自动聚合工具，通过收集网络上公开的直播源，自动进行分类整理、去重、黑白名单过滤，生成高质量的直播源列表。

### 主要功能

- **多源聚合**: 从多个公开直播源地址获取数据
- **自动分类**: 按央视频道、卫视频道、地方台等分类整理
- **黑白名单**: 自动过滤失效源，保留优质源
- **繁简转换**: 自动将繁体频道名转为简体
- **多格式输出**: 支持 TXT 和 M3U 两种格式
- **自动更新**: 通过 GitHub Actions 定时自动更新

### 更新频率（北京时间）

| 内容 | 更新时间 |
| ---- | ---- |
| 直播源 | 每日 04:00 |
| 黑白名单 | 每周五 00:00 |

## 直播源下载

| 格式 | 完整版 | 精简版 | 其他 |
| ---- | ---- | ---- | ---- |
| TXT | [live.txt](https://raw.githubusercontent.com/CCSH/IPTV/refs/heads/main/live.txt) | [live_lite.txt](https://raw.githubusercontent.com/CCSH/IPTV/refs/heads/main/live_lite.txt) | [others.txt](https://raw.githubusercontent.com/CCSH/IPTV/refs/heads/main/others.txt) |
| M3U | [live.m3u](https://raw.githubusercontent.com/CCSH/IPTV/refs/heads/main/live.m3u) | [live_lite.m3u](https://raw.githubusercontent.com/CCSH/IPTV/refs/heads/main/live_lite.m3u) | - |

## 项目结构

```
.
├── main.py                          # 主程序：直播源聚合处理
├── assets/
│   ├── urls.txt                     # 直播源URL列表
│   ├── config.txt                   # 配置文件
│   ├── corrections_name.txt         # 频道名称纠错表
│   └── whitelist-blacklist/
│       ├── main.py                  # 黑白名单检测脚本
│       ├── whitelist_manual.txt     # 手动白名单
│       ├── whitelist_auto.txt       # 自动生成白名单
│       ├── blacklist_manual.txt     # 手动黑名单
│       ├── blacklist_auto.txt       # 自动生成黑名单
│       └── blackhost_count.txt      # 黑名单主机统计
├── 主频道/                          # 主频道名称字典
│   ├── 央视频道.txt
│   ├── 卫视频道.txt
│   ├── 体育频道.txt
│   └── ...
├── 地方台/                          # 地方台名称字典
│   ├── 北京频道.txt
│   ├── 上海频道.txt
│   ├── 广东频道.txt
│   └── ...
├── js/                              # JavaScript 影视源脚本
├── py/                              # Python 影视源脚本
├── lib/                             # 库文件和资源
├── jsm.json                         # JS模式配置文件
├── py.json                          # PY模式配置文件
└── .github/workflows/               # GitHub Actions 工作流
    ├── main.yml                     # 每日直播源更新
    └── whitelist-blacklist.yml      # 每周黑白名单更新
```

## 本地使用

### 环境要求

- Python 3.12+
- 依赖包：`opencc-python-reimplemented`

### 安装依赖

```bash
pip install opencc-python-reimplemented
```

### 运行主程序

```bash
python main.py
```

运行后会生成以下文件：
- `live.txt` - 完整版直播源（TXT格式）
- `live_lite.txt` - 精简版直播源（TXT格式）
- `live.m3u` - 完整版直播源（M3U格式）
- `live_lite.m3u` - 精简版直播源（M3U格式）
- `others.txt` - 未分类的其他源

### 运行黑白名单检测

```bash
python assets/whitelist-blacklist/main.py
```

运行后会在 `assets/whitelist-blacklist/` 目录下生成更新后的黑白名单文件。

## 配置说明

### 添加自定义源

编辑 `assets/urls.txt` 文件，每行添加一个直播源URL，支持 TXT 和 M3U 格式。

### 频道名称纠错

编辑 `assets/corrections_name.txt` 文件，格式为：
```
正确名称,错误名称1,错误名称2,...
```

### 手动黑白名单

- 白名单：编辑 `assets/whitelist-blacklist/whitelist_manual.txt`
- 黑名单：编辑 `assets/whitelist-blacklist/blacklist_manual.txt`

格式：
```
频道名称,频道地址
```

## 版本更新日志

### v2.0.0 (2026-07-19)

- **修复**: 修复黑白名单脚本中 `split_url` 函数的bug（错误地追加原行而非新行）
- **优化**: 升级 GitHub Actions 版本（checkout v2→v4, setup-python v2→v5）
- **优化**: Python 版本统一为 3.12
- **优化**: 增加 git commit 前的变更检查，避免空提交
- **优化**: 黑白名单工作流调整为每周四 UTC 16:00（北京时间周五 00:00）运行
- **文档**: 完善 README.md，添加项目结构、使用说明、配置说明等

### v1.0.0

- 初始版本
- 支持多源聚合
- 支持自动分类
- 支持黑白名单过滤
- 支持繁简转换
- 支持 TXT 和 M3U 格式输出

## 致谢

直播源来源于：[https://github.com/CCSH/IPTV](https://github.com/CCSH/IPTV)

感谢所有公开分享直播源的大神们！写代码不易，有能力的请关注、点赞、打赏作者。

## 相关工具

在线MD5文件哈希计算工具：[https://tool.hiofd.com/file-md5-online/](https://tool.hiofd.com/file-md5-online/)

## 免责声明

1. 本项目所有资源均来自网络，仅供学习交流使用
2. 请勿用于商业用途
3. 如有侵权，请联系删除
4. 使用本项目内容所产生的一切后果由使用者自行承担

[回到顶部](#readme)
