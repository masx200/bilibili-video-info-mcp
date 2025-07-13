import re
import requests
import xml.etree.ElementTree as ET
import os

def get_seesdata() -> str:
    """Get the Bilibili SESSDATA from environment variables"""
    seesdata = os.getenv("SESSDATA")
    if not seesdata:
        raise ValueError("SESSDATA environment variable is required")
    return seesdata

SESSDATA = get_seesdata()


# Bilibili API endpoints
API_GET_VIEW_INFO = "https://api.bilibili.com/x/web-interface/view"
API_GET_SUBTITLE = "https://api.bilibili.com/x/player/wbi/v2"
API_GET_DANMAKU = "https://api.bilibili.com/x/v1/dm/list.so"
API_GET_COMMENTS = "https://api.bilibili.com/x/v2/reply"

# Default Headers for requests
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Referer': 'https://www.bilibili.com/'
}

def _get_headers():
    headers = DEFAULT_HEADERS.copy()
    if SESSDATA:
        headers['Cookie'] = f'SESSDATA={SESSDATA}'
    return headers

def extract_bvid(url):
    # 先尝试直接从URL中提取BV号
    match = re.search(r'BV[a-zA-Z0-9_]+', url)
    if match:
        return match.group(0)
    
    # 如果是短链接（如b23.tv），则跟踪重定向获取完整URL
    if 'b23.tv' in url:
        try:
            response = requests.head(url, headers=_get_headers(), allow_redirects=True)
            if response.status_code == 200:
                # 获取最终重定向后的URL
                final_url = response.url
                match = re.search(r'BV[a-zA-Z0-9_]+', final_url)
                if match:
                    return match.group(0)
        except requests.RequestException as e:
            print(f"Error resolving short URL: {e}")
    
    return None

def get_video_basic_info(bvid):
    """Gets aid and cid for a given bvid."""
    headers = _get_headers()
    try:
        params_view = {'bvid': bvid}
        response_view = requests.get(API_GET_VIEW_INFO, params=params_view, headers=headers)
        response_view.raise_for_status()
        data_view = response_view.json()

        if data_view['code'] != 0:
            return None, None, {'error': 'Failed to get video info', 'details': data_view}

        video_data = data_view['data']
        return video_data.get('aid'), video_data.get('cid'), None
    except requests.RequestException as e:
        return None, None, {'error': f'Failed to fetch video details: {e}'}

def get_subtitles(aid, cid):
    """Fetches subtitles for a given aid and cid."""
    headers = _get_headers()
    subtitles = []
    try:
        params_subtitle = {'aid': aid, 'cid': cid}
        response_subtitle = requests.get(API_GET_SUBTITLE, params=params_subtitle, headers=headers)
        response_subtitle.raise_for_status()
        subtitle_data = response_subtitle.json()
        if subtitle_data.get('code') == 0 and subtitle_data.get('data', {}).get('subtitle', {}).get('subtitles'):
            for sub_meta in subtitle_data['data']['subtitle']['subtitles']:
                if sub_meta.get('subtitle_url'):
                    try:
                        subtitle_json_url = f"https:{sub_meta['subtitle_url']}"
                        response_sub_content = requests.get(subtitle_json_url, headers=headers)
                        response_sub_content.raise_for_status()
                        sub_content = response_sub_content.json()
                        subtitle_body = sub_content.get('body', [])
                        content_list = [item.get('content', '') for item in subtitle_body]
                        subtitles.append({
                            'lan': sub_meta['lan'],
                            'content': content_list
                        })
                    except requests.RequestException as e:
                        print(f"Could not fetch or parse subtitle content from {sub_meta.get('subtitle_url')}: {e}")
        return subtitles, None
    except requests.RequestException as e:
        return [], {'error': f'Could not fetch subtitles: {e}'}

def get_danmaku(cid):
    """Fetches danmaku for a given cid."""
    headers = _get_headers()
    danmaku_list = []
    try:
        params_danmaku = {'oid': cid}
        response_danmaku = requests.get(API_GET_DANMAKU, params=params_danmaku, headers=headers)
        danmaku_content = response_danmaku.content.decode('utf-8', errors='ignore')
        root = ET.fromstring(danmaku_content)
        for d in root.findall('d'):
            danmaku_list.append(d.text)
        return danmaku_list, None
    except (requests.RequestException, ET.ParseError) as e:
        return [], {'error': f'Failed to get or parse danmaku: {e}'}

def get_comments(aid):
    """Fetches comments for a given aid."""
    headers = _get_headers()
    comments_list = []
    try:
        params_comments = {'type': 1, 'oid': aid, 'sort': 2}  # sort=2 fetches hot comments
        response_comments = requests.get(API_GET_COMMENTS, params=params_comments, headers=headers)
        response_comments.raise_for_status()
        comments_data = response_comments.json()
        
        if comments_data.get('code') == 0 and comments_data.get('data', {}).get('replies'):
            for comment in comments_data['data']['replies']:
                if comment.get('content', {}).get('message'):
                    comments_list.append({
                        'user': comment.get('member', {}).get('uname', 'Unknown User'),
                        'content': comment['content']['message'],
                        'likes': comment.get('like', 0)
                    })
        return comments_list, None
    except requests.RequestException as e:
        return [], {'error': f'Failed to get comments: {e}'}
