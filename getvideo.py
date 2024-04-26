from googleapiclient.discovery import build
import json

# Thay thế 'YOUR_API_KEY_YOUTUBE' bằng khóa API của bạn
API_KEY_YOUTUBE = 'AIzaSyDDCzDua3KlgPPx6Nc7VyqZKtkHou_q6Vo'

# Tạo kết nối với API YouTube
youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)

def search_videos(query, max_results=10):
    # Thực hiện tìm kiếm video
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=max_results
    ).execute()

    # Lấy danh sách các video từ kết quả tìm kiếm
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append({
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId']
            })
    return videos

# Hỏi người dùng từ khóa tìm kiếm
search_query = input("Nhập từ khóa tìm kiếm trên YouTube: ")

# Sử dụng hàm search_videos để tìm kiếm video với từ khóa người dùng nhập
result = search_videos(search_query, max_results=5)
print(json.dumps(result, indent=2))
