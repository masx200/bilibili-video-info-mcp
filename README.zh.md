# MCP Server for Bilibili Video Info

[![English](https://img.shields.io/badge/language-English-blue.svg)](./README.md) [![中文](https://img.shields.io/badge/language-中文-red.svg)](./README.zh.md)

Bilibili MCP Server，可以获取根据视频 url 获取视频的字幕、弹幕和评论信息。

## 使用方法

MCP Server 支持三种通信方式：
1. **stdio**
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

2. **sse**（服务器发送事件）
在 sse 模式下运行 bilibili-video-info-mcp
``` bash
cp .env.example .env
uvx run --env .env bilibili-video-info-mcp sse
```
然后配置你的mcp客户端
```json
{
    "mcpServers": {
        "bilibili-video-info-mcp": {
            "url": "http://{your.ip.address}:$PORT$/sse"
        }
    }
}
```

3. **streamable-http**（HTTP流式传输）
在 streamable-http 模式下运行 bilibili-video-info-mcp
``` bash
cp .env.example .env
uvx run --env .env bilibili-video-info-mcp streamable-http
```
然后配置你的mcp客户端
```json
{
    "mcpServers": {
        "bilibili-video-info-mcp": {
            "url": "http://{your.ip.address}:$PORT$/mcp"
            }
        }
    }
}
```

## MCP 工具列表

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
