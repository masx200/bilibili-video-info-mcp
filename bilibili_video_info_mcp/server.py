"""
Bilibili视频信息MCP服务器的核心模块
"""

from mcp.server.fastmcp import FastMCP
from . import bilibili_api

# 创建 FastMCP 服务器实例，命名为 BilibiliVideoInfo
mcp = FastMCP("BilibiliVideoInfo", dependencies=["requests"])

@mcp.tool(
    annotations={
        "title": "获取视频字幕",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def get_subtitles(url: str) -> list:
    """获取B站视频的字幕内容
    
    Args:
        url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
        
    Returns:
        列表形式的字幕内容，按语言分组
    """
    bvid = bilibili_api.extract_bvid(url)
    if not bvid:
        return [f"错误: 无法从 URL 提取 BV 号: {url}"]
    
    aid, cid, error = bilibili_api.get_video_basic_info(bvid)
    if error:
        return [f"获取视频信息失败: {error['error']}"]
    
    subtitles, error = bilibili_api.get_subtitles(aid, cid)
    if error:
        return [f"获取字幕失败: {error['error']}"]
    
    if not subtitles:
        return ["该视频没有字幕"]
    
    return subtitles

@mcp.tool(
    annotations={
        "title": "获取视频弹幕",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def get_danmaku(url: str) -> list:
    """获取B站视频的弹幕内容
    
    Args:
        url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
        
    Returns:
        列表形式的弹幕内容
    """
    bvid = bilibili_api.extract_bvid(url)
    if not bvid:
        return [f"错误: 无法从 URL 提取 BV 号: {url}"]
    
    aid, cid, error = bilibili_api.get_video_basic_info(bvid)
    if error:
        return [f"获取视频信息失败: {error['error']}"]
    
    danmaku, error = bilibili_api.get_danmaku(cid)
    if error:
        return [f"获取弹幕失败: {error['error']}"]
    
    if not danmaku:
        return ["该视频没有弹幕"]
    
    return danmaku

@mcp.tool(
    annotations={
        "title": "获取视频评论",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
async def get_comments(url: str) -> list:
    """获取B站视频的热门评论
    
    Args:
        url: B站视频链接，例如 https://www.bilibili.com/video/BV1x341177NN
        
    Returns:
        列表形式的热门评论
    """
    bvid = bilibili_api.extract_bvid(url)
    if not bvid:
        return [f"错误: 无法从 URL 提取 BV 号: {url}"]
    
    aid, cid, error = bilibili_api.get_video_basic_info(bvid)
    if error:
        return [f"获取视频信息失败: {error['error']}"]
    
    comments, error = bilibili_api.get_comments(aid)
    if error:
        return [f"获取评论失败: {error['error']}"]
    
    if not comments:
        return ["该视频没有热门评论"]
    
    return comments

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bilibili Video Info MCP Server")
    parser.add_argument('transport', nargs='?', default='stdio', choices=['stdio', 'sse', 'streamable-http'],
                        help='Transport type (stdio, sse, or streamable-http)')
    args = parser.parse_args()
    mcp.run(transport=args.transport)