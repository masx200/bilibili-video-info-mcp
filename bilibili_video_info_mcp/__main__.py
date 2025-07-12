"""
Bilibili Video Info MCP 服务器的入口点模块
可以通过 `python -m bilibili_video_info_mcp` 命令启动服务器
"""

from .server import run_server

def main():
    run_server(transport='stdio')

if __name__ == "__main__":
    main()
