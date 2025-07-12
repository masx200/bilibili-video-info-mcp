# Bilibili 视频信息 MCP 服务器

这是一个基于 MCP (Model Context Protocol) 的服务器，可以获取 Bilibili 视频的字幕、弹幕和评论信息。

## 功能特点

- 支持获取 Bilibili 视频字幕列表
- 支持获取 Bilibili 视频弹幕内容
- 支持获取 Bilibili 视频热门评论
- 基于 FastMCP 框架，轻量化设计
- 通过环境变量配置 SESSDATA

## 使用方法

MCP 客户端配置
```json
{
    "mcpServers": {
        "bilibili-video-info-mcp": {
            "command": "uvx",
            "args": [
                "bilibili-video-info-mcp"
            ],
            "env": {
                "SESSDATA": "your valid sessdata"
            }
        }
    }
}
```

### 使用 MCP Inspector 调试

```bash
# 使用 npx 安装并运行 MCP Inspector
npx -y @modelcontextprotocol/inspector uv run mcp_server.py
```

这将启动 MCP Inspector 界面，您可以在浏览器中测试 MCP 工具。

## API 功能

### 1. 获取视频字幕列表

```json
{
  "name": "get_subtitles",
  "arguments": {
    "url": "https://www.bilibili.com/video/BV1x341177NN"
  }
}
```

### 2. 获取视频弹幕

```json
{
  "name": "get_danmaku",
  "arguments": {
    "url": "https://www.bilibili.com/video/BV1x341177NN"
  }
}
```

### 3. 获取视频评论

```json
{
  "name": "get_comments",
  "arguments": {
    "url": "https://www.bilibili.com/video/BV1x341177NN"
  }
}
```

## 集成到其他应用

MCP 服务器可以通过标准输入输出 (stdio) 与其他应用集成，也可以作为独立的 HTTP 服务运行。

### 在 AI 助手中使用

适用于 Claude、GPT 等 AI 助手的 MCP 集成，可以让 AI 助手获取 Bilibili 视频的字幕、弹幕和评论数据。

## 常见问题

### 1. 找不到 SESSDATA 怎么办？

1. 登录 Bilibili 网站
2. 打开浏览器开发者工具 (F12)
3. 进入 Application/Storage -> Cookies
4. 找到 SESSDATA 对应的值

### 2. 报错 "SESSDATA environment variable is required"

确保已经设置了环境变量：

```bash
export SESSDATA="你的SESSDATA值"
```

### 3. 视频链接支持哪些格式？

支持标准的 Bilibili 视频链接，例如：
- https://www.bilibili.com/video/BV1x341177NN
- https://b23.tv/xxxxx (短链接)
- 包含 BV 号的任何链接

## 许可证

MIT
