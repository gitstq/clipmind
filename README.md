<div align="center">

# 🧠 ClipMind

**Intelligent Terminal Clipboard History Manager**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Project Introduction

**ClipMind** is an intelligent terminal clipboard history manager designed for developers and power users. It automatically tracks your clipboard history, intelligently categorizes content types, and provides a beautiful TUI interface for quick search and retrieval.

**Core Value Proposition:**
- 🚀 **Never lose clipboard content again** - Automatic persistent storage
- 🧠 **Smart categorization** - Auto-detect URLs, code, JSON, emails, file paths
- ⚡ **Lightning-fast fuzzy search** - Find anything in milliseconds
- 🎯 **Zero dependencies** - Pure Python standard library, no bloat
- 💻 **Developer-first** - Vim-style keybindings, terminal-native workflow

**Differentiation from existing tools:**
Unlike GUI clipboard managers that require mouse interaction, ClipMind is entirely keyboard-driven and terminal-native. Unlike simple clipboard history tools, ClipMind provides intelligent content classification and persistent storage with JSON-based data format.

---

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📋 **Auto Capture** | Monitor clipboard changes in real-time |
| 🏷️ **Smart Classification** | Auto-detect text/code/URL/JSON/email/path |
| 🔍 **Fuzzy Search** | Lightning-fast content search with scoring |
| 🖥️ **Beautiful TUI** | Terminal UI with color-coded type icons |
| ⌨️ **Vim Bindings** | `j/k` navigation, `g/G` jump, `/` search |
| 💾 **Persistent Storage** | JSON-based history with configurable limits |
| 🌍 **Cross-Platform** | Windows, macOS, Linux native support |
| 🚫 **Zero Dependencies** | Only Python standard library |

---

### 🚀 Quick Start

#### Requirements
- Python 3.8 or higher
- Terminal with ANSI color support

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/ClipMind.git
cd ClipMind

# Install
pip install .

# Or install in development mode
pip install -e .
```

#### Usage

```bash
# Launch interactive TUI
clipmind

# Or use short alias
cm
```

**Keyboard Shortcuts:**
| Key | Action |
|-----|--------|
| `↑/k` | Move up |
| `↓/j` | Move down |
| `Enter` | Copy selected to clipboard |
| `/` | Search mode |
| `d` | Delete selected entry |
| `g` | Go to top |
| `G` | Go to bottom |
| `c` | Clear all history |
| `q` | Quit |

---

### 📖 Detailed Usage Guide

#### CLI Commands

```bash
# Add text to history
clipmind --add "Hello World"

# List recent entries
clipmind --list --limit 20

# Search history
clipmind --search "keyword"

# Filter by type
clipmind --list --type code

# Copy entry by index
clipmind --copy 0

# Delete entry by index
clipmind --delete 0

# Show statistics
clipmind --stats

# Monitor clipboard in background
clipmind --monitor

# Clear all history
clipmind --clear
```

#### Content Type Detection

ClipMind automatically classifies clipboard content:

| Icon | Type | Detection Pattern |
|------|------|-------------------|
| 📄 | Text | Default type |
| 💻 | Code | `def`, `class`, `import`, `function` |
| 🔗 | URL | `http://`, `https://`, `ftp://` |
| 📁 | Path | Existing file paths |
| 📋 | JSON | Valid JSON format |
| 📧 | Email | `user@domain.com` pattern |

---

### 💡 Design Philosophy & Roadmap

**Design Principles:**
1. **Terminal-native** - No GUI dependencies, works over SSH
2. **Zero dependencies** - Reduce supply chain attack surface
3. **Keyboard-first** - Optimize for developer workflow speed
4. **Intelligent defaults** - Auto-classify without configuration

**Roadmap:**
- [ ] Regex-based custom type rules
- [ ] Export/import history
- [ ] Encrypted storage option
- [ ] Plugin system for custom processors
- [ ] Integration with popular terminal multiplexers

---

### 📦 Packaging & Deployment

#### Build from Source

```bash
# Clean build
make clean

# Build distribution
make build

# Run tests
make test
```

#### Manual Installation

```bash
# Direct execution without installation
python -m clipmind
```

---

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit with conventional commits (`feat:`, `fix:`, `docs:`)
4. Push to your fork
5. Open a Pull Request

**Issue Reporting:**
- Use GitHub Issues for bug reports
- Include Python version and OS information
- Provide steps to reproduce

---

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="simplified-chinese"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**ClipMind** 是一款专为开发者和高级用户设计的智能终端剪贴板历史管理器。它自动追踪剪贴板历史，智能分类内容类型，并提供精美的 TUI 界面实现快速搜索和检索。

**核心价值主张：**
- 🚀 **再也不丢失剪贴板内容** - 自动持久化存储
- 🧠 **智能分类** - 自动识别 URL、代码、JSON、邮箱、文件路径
- ⚡ **闪电般模糊搜索** - 毫秒级内容查找
- 🎯 **零依赖** - 纯 Python 标准库，无臃肿依赖
- 💻 **开发者优先** - Vim 风格快捷键，终端原生工作流

**与现有工具的差异化：**
与需要鼠标操作的 GUI 剪贴板管理器不同，ClipMind 完全基于键盘驱动且原生适配终端。与简单的剪贴板历史工具不同，ClipMind 提供智能内容分类和基于 JSON 的持久化存储。

---

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📋 **自动捕获** | 实时监控剪贴板变化 |
| 🏷️ **智能分类** | 自动识别文本/代码/URL/JSON/邮箱/路径 |
| 🔍 **模糊搜索** | 带评分的闪电般内容搜索 |
| 🖥️ **精美 TUI** | 带彩色类型图标的终端界面 |
| ⌨️ **Vim 快捷键** | `j/k` 导航、`g/G` 跳转、`/` 搜索 |
| 💾 **持久化存储** | 基于 JSON 的历史记录，可配置上限 |
| 🌍 **跨平台** | Windows、macOS、Linux 原生支持 |
| 🚫 **零依赖** | 仅使用 Python 标准库 |

---

### 🚀 快速开始

#### 环境要求
- Python 3.8 或更高版本
- 支持 ANSI 颜色的终端

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/ClipMind.git
cd ClipMind

# 安装
pip install .

# 或开发模式安装
pip install -e .
```

#### 使用

```bash
# 启动交互式 TUI
clipmind

# 或使用短别名
cm
```

**键盘快捷键：**
| 按键 | 操作 |
|------|------|
| `↑/k` | 向上移动 |
| `↓/j` | 向下移动 |
| `Enter` | 复制选中项到剪贴板 |
| `/` | 搜索模式 |
| `d` | 删除选中项 |
| `g` | 跳到顶部 |
| `G` | 跳到底部 |
| `c` | 清空所有历史 |
| `q` | 退出 |

---

### 📖 详细使用指南

#### CLI 命令

```bash
# 添加文本到历史
clipmind --add "Hello World"

# 列出最近条目
clipmind --list --limit 20

# 搜索历史
clipmind --search "关键词"

# 按类型筛选
clipmind --list --type code

# 按索引复制
clipmind --copy 0

# 按索引删除
clipmind --delete 0

# 显示统计
clipmind --stats

# 后台监控剪贴板
clipmind --monitor

# 清空所有历史
clipmind --clear
```

#### 内容类型检测

ClipMind 自动分类剪贴板内容：

| 图标 | 类型 | 检测规则 |
|------|------|----------|
| 📄 | 文本 | 默认类型 |
| 💻 | 代码 | `def`、`class`、`import`、`function` |
| 🔗 | 链接 | `http://`、`https://`、`ftp://` |
| 📁 | 路径 | 存在的文件路径 |
| 📋 | JSON | 有效 JSON 格式 |
| 📧 | 邮箱 | `user@domain.com` 格式 |

---

### 💡 设计思路与迭代规划

**设计理念：**
1. **终端原生** - 无 GUI 依赖，支持 SSH 远程使用
2. **零依赖** - 降低供应链攻击风险
3. **键盘优先** - 优化开发者工作流速度
4. **智能默认** - 无需配置即可自动分类

**迭代计划：**
- [ ] 基于正则的自定义类型规则
- [ ] 历史记录导出/导入
- [ ] 加密存储选项
- [ ] 自定义处理器插件系统
- [ ] 与主流终端复用器集成

---

### 📦 打包与部署指南

#### 从源码构建

```bash
# 清理构建
make clean

# 构建分发包
make build

# 运行测试
make test
```

#### 手动安装

```bash
# 无需安装直接运行
python -m clipmind
```

---

### 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 使用约定式提交 (`feat:`、`fix:`、`docs:`)
4. 推送到你的 Fork
5. 提交 Pull Request

**Issue 反馈：**
- 使用 GitHub Issues 提交 Bug 报告
- 包含 Python 版本和操作系统信息
- 提供复现步骤

---

### 📄 开源协议

本项目基于 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="traditional-chinese"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

**ClipMind** 是一款為開發者與進階使用者設計的智慧終端機剪貼簿歷史管理器。它自動追蹤剪貼簿歷史，智慧分類內容類型，並提供美觀的 TUI 介面實現快速搜尋與檢索。

**核心價值主張：**
- 🚀 **再也不會遺失剪貼簿內容** - 自動持久化儲存
- 🧠 **智慧分類** - 自動偵測 URL、程式碼、JSON、郵件、檔案路徑
- ⚡ **閃電級模糊搜尋** - 毫秒級內容查找
- 🎯 **零依賴** - 純 Python 標準函式庫，沒有臃腫依賴
- 💻 **開發者優先** - Vim 風格快捷鍵，終端機原生工作流程

**與現有工具的差異化：**
不同於需要滑鼠操作的 GUI 剪貼簿管理器，ClipMind 完全以鍵盤驅動且原生適配終端機。不同於簡單的剪貼簿歷史工具，ClipMind 提供智慧內容分類與基於 JSON 的持久化儲存。

---

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 📋 **自動捕獲** | 即時監控剪貼簿變化 |
| 🏷️ **智慧分類** | 自動偵測文字/程式碼/URL/JSON/郵件/路徑 |
| 🔍 **模糊搜尋** | 帶評分的閃電級內容搜尋 |
| 🖥️ **美觀 TUI** | 帶彩色類型圖示的終端機介面 |
| ⌨️ **Vim 快捷鍵** | `j/k` 導航、`g/G` 跳轉、`/` 搜尋 |
| 💾 **持久化儲存** | 基於 JSON 的歷史記錄，可配置上限 |
| 🌍 **跨平台** | Windows、macOS、Linux 原生支援 |
| 🚫 **零依賴** | 僅使用 Python 標準函式庫 |

---

### 🚀 快速開始

#### 環境需求
- Python 3.8 或更高版本
- 支援 ANSI 顏色的終端機

#### 安裝

```bash
# 複製倉庫
git clone https://github.com/gitstq/ClipMind.git
cd ClipMind

# 安裝
pip install .

# 或開發模式安裝
pip install -e .
```

#### 使用

```bash
# 啟動互動式 TUI
clipmind

# 或使用短別名
cm
```

**鍵盤快捷鍵：**
| 按鍵 | 動作 |
|------|------|
| `↑/k` | 向上移動 |
| `↓/j` | 向下移動 |
| `Enter` | 複製選中項目到剪貼簿 |
| `/` | 搜尋模式 |
| `d` | 刪除選中項目 |
| `g` | 跳到頂部 |
| `G` | 跳到底部 |
| `c` | 清空所有歷史 |
| `q` | 退出 |

---

### 📖 詳細使用指南

#### CLI 指令

```bash
# 新增文字到歷史
clipmind --add "Hello World"

# 列出最近項目
clipmind --list --limit 20

# 搜尋歷史
clipmind --search "關鍵字"

# 依類型過濾
clipmind --list --type code

# 依索引複製
clipmind --copy 0

# 依索引刪除
clipmind --delete 0

# 顯示統計
clipmind --stats

# 背景監控剪貼簿
clipmind --monitor

# 清空所有歷史
clipmind --clear
```

#### 內容類型偵測

ClipMind 自動分類剪貼簿內容：

| 圖示 | 類型 | 偵測規則 |
|------|------|----------|
| 📄 | 文字 | 預設類型 |
| 💻 | 程式碼 | `def`、`class`、`import`、`function` |
| 🔗 | 連結 | `http://`、`https://`、`ftp://` |
| 📁 | 路徑 | 存在的檔案路徑 |
| 📋 | JSON | 有效 JSON 格式 |
| 📧 | 郵件 | `user@domain.com` 格式 |

---

### 💡 設計理念與迭代規劃

**設計理念：**
1. **終端機原生** - 無 GUI 依賴，支援 SSH 遠端使用
2. **零依賴** - 降低供應鏈攻擊風險
3. **鍵盤優先** - 優化開發者工作流程速度
4. **智慧預設** - 不需設定即可自動分類

**迭代計劃：**
- [ ] 基於正規表示式的自訂類型規則
- [ ] 歷史記錄匯出/匯入
- [ ] 加密儲存選項
- [ ] 自訂處理器外掛系統
- [ ] 與主流終端機複用器整合

---

### 📦 打包與部署指南

#### 從原始碼建構

```bash
# 清理建構
make clean

# 建構分發套件
make build

# 執行測試
make test
```

#### 手動安裝

```bash
# 不需安裝直接執行
python -m clipmind
```

---

### 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/amazing-feature`)
3. 使用約定式提交 (`feat:`、`fix:`、`docs:`)
4. 推送到你的 Fork
5. 提交 Pull Request

**Issue 回報：**
- 使用 GitHub Issues 提交 Bug 報告
- 包含 Python 版本和作業系統資訊
- 提供重現步驟

---

### 📄 開源授權

本專案基於 MIT 授權開源 - 詳見 [LICENSE](LICENSE) 檔案。

---
