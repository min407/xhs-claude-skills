<div align="center">

# 小红书创作者工具箱·转obsidian

面向小红书内容创作者的 Claude Code skills + 本地剪藏服务

[![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-7C3AED)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

中文 | [English](README_EN.md)

</div>

---

这个仓库提供两套能力：

1. `skills/`：给 Claude Code 用的 skill，适合提取、批量整理、分析、做封面。
2. `service/`：一个本地 HTTP 服务，适合做“一键剪藏”。

如果你是小白，可以直接看 [docs/小白使用说明.md](docs/小白使用说明.md)。

## 适合谁

- 想把小红书内容沉淀成可检索资料的人
- 想做选题拆解、内容分析、封面生成的小红书博主
- 想把浏览器里的帖子一键保存到本地知识库的人

## 你可以做什么

| 能力 | 命令/入口 | 说明 |
|:--|:--|:--|
| 单条提取 | `/xhs <链接>` | 把单条小红书帖子提取为 Markdown |
| 批量提取 | `/xhs-batch <多个链接>` | 批量整理多个帖子 |
| 内容分析 | `/xhs-analyze [关键词]` | 总结、对比、提炼你已保存的内容 |
| 封面生成 | `/xhs-cover <标题文案>` | 生成小红书风格封面图 |
| 本地剪藏 | `service/server.py` | 通过浏览器书签或 curl 一键保存当前帖子 |

## 快速开始

### 方式 A：在 Claude Code 里使用

1. 安装插件

```bash
/plugin marketplace add chenxiachan/xhs-claude-skills
/plugin install rednote-to-obsidian@chenxiachan-xhs-claude-skills
```

2. 准备 cookies

- 打开 Chrome 并登录小红书
- 打开开发者工具的 `Console`
- 导出 cookies 到 `~/cookies.json`

3. 开始使用

```bash
/xhs https://www.xiaohongshu.com/explore/...
/xhs-batch <链接1> <链接2>
/xhs-analyze
/xhs-cover 爆款标题文案
```

默认输出目录：

```text
~/Documents/Obsidian Vault/xhs
```

### 方式 B：启动本地服务

如果你更想做“打开帖子后点一下就保存”，用本地服务更合适。

```bash
cd service
python3 server.py
```

启动后测试：

```bash
curl http://127.0.0.1:7895/health
```

剪藏接口：

```bash
curl "http://127.0.0.1:7895/clip?url=https://www.xiaohongshu.com/explore/..."
```

服务详细说明见 [service/README.md](service/README.md)。

## Cookies 怎么准备

在 Chrome 的小红书页面打开 Console，运行：

```javascript
copy(JSON.stringify(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return {
    name,
    value: rest.join('='),
    domain: '.xiaohongshu.com',
    path: '/',
    expires: Date.now() / 1000 + 86400 * 30,
    size: name.length + rest.join('=').length,
    httpOnly: false,
    secure: false,
    session: false,
    priority: 'Medium',
    sameParty: false,
    sourceScheme: 'Secure',
    sourcePort: 443
  };
})))
```

然后把复制结果保存为：

```text
~/cookies.json
```

## 隐私与安全

- cookies 只保存在你自己的电脑上，不需要上传到任何服务端
- 仓库默认忽略 `cookies.json`、日志、缓存、临时音视频文件
- 请不要把你自己的笔记库、截图、运行日志一起提交到 git

## 项目结构

```text
xhs-claude-skills/
├── .claude-plugin/plugin.json
├── docs/
│   └── 小白使用说明.md
├── service/
│   ├── README.md
│   ├── clipper.py
│   └── server.py
└── skills/
    ├── xhs/
    ├── xhs-batch/
    ├── xhs-analyze/
    └── xhs-cover/
```

## 常见提醒

- 如果提示 404 或抓取失败，优先怀疑 cookies 过期
- 本地服务更适合“快速保存”，复杂的视频转录建议用 Claude Code 的 `/xhs`
- 如果你的 Obsidian 路径不一样，可以在本地服务中设置环境变量 `XHS_OUTPUT_DIR`
