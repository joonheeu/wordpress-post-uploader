import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from dotenv import load_dotenv
import os

class WordPressUploader:
    def __init__(self):
        load_dotenv()
        self.site_url = os.getenv('WP_SITE_URL')
        self.username = os.getenv('WP_USERNAME')
        self.password = os.getenv('WP_PASSWORD')
        self.auth = HTTPBasicAuth(self.username, self.password)

    def send_request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, auth=self.auth, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"요청 중 오류 발생: {e}")
            return None

    def upload_post(self, title, content, status='publish'):
        api_url = f'{self.site_url}/wp-json/wp/v2/posts'
        post_data = {'title': title, 'content': content, 'status': status}
        return self.send_request('POST', api_url, json=post_data)

    def upload_media(self, file_path):
        api_url = f'{self.site_url}/wp-json/wp/v2/media'
        headers = {'Content-Disposition': f'attachment; filename={os.path.basename(file_path)}'}
        with open(file_path, 'rb') as file:
            return self.send_request('POST', api_url, headers=headers, data=file)

    def change_post_status(self, post_id, new_status):
        api_url = f'{self.site_url}/wp-json/wp/v2/posts/{post_id}'
        post_data = {'status': new_status}
        return self.send_request('POST', api_url, json=post_data)

    def delete_post(self, post_id):
        api_url = f'{self.site_url}/wp-json/wp/v2/posts/{post_id}'
        return self.send_request('DELETE', api_url)

    def get_posts(self, per_page=10, page=1):
        api_url = f'{self.site_url}/wp-json/wp/v2/posts?per_page={per_page}&page={page}'
        return self.send_request('GET', api_url)

if __name__ == '__main__':
    # 사용 예시
    uploader = WordPressUploader()
    uploader.upload_post("새로운 게시글", "이것은 게시글의 내용입니다.")
    uploader.upload_media("/path/to/your/image.jpg")
    uploader.change_post_status(123, 'draft')  # 123은 게시글 ID
    uploader.delete_post(123)
    posts = uploader.get_posts()
    print(posts)
