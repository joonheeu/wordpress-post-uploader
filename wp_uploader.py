from typing import List, Union
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

class WordPressUploader:
    def __init__(self, site_url: str, username: str, password: str):
        self.site_url = site_url
        self.auth = HTTPBasicAuth(username, password)

    def send_request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, auth=self.auth, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"요청 중 오류 발생: {e}")
            return None

    def upload_post(self, title: str, content: str, slug: str, featured_media_id: int=None, categories: List[Union[int, str]]=['미분류'], tags: List[Union[int, str]]=[], status='publish'):
        api_url = f'{self.site_url}/wp-json/wp/v2/posts'

        categories_ids = [self.ensure_category(cat) for cat in categories]
        tags_ids = [self.ensure_tag(tag) for tag in tags]

        post_data = {
            'title': title, 
            'content': content, 
            'slug': slug,
            'featured_media': featured_media_id,
            'comment_status': 'closed',
            'ping_status': 'closed',
            'categories': categories_ids,
            'tags': tags_ids,
            'status': status,
        }
        return self.send_request('POST', api_url, json=post_data)

    def upload_media(self, file_path_or_image_url: str, slug: str, title: str, alt: str, description: str, caption: str = '', upload_format = 'webp'):
        arguments = {
            'title': title,
            'alt_text': alt,
            'slug': slug,
            'caption': caption,
            'description': description,
        }
        api_url = f'{self.site_url}/wp-json/wp/v2/media'
        filename = slug.replace("-", "_")
            
        if file_path_or_image_url.startswith('http'):
            converted_image = self.download_and_convert_image(file_path_or_image_url, format=upload_format)
            files = { 'file': (f'{filename}.{upload_format}', converted_image, f'image/{upload_format}') }
            return self.send_request('POST', api_url, files=files, data=arguments)
        else:
            file_path = file_path_or_image_url
            with open(file_path, 'rb') as file:
                files = { 'file': (os.path.basename(file_path), file, f'image/{upload_format}') }
                return self.send_request('POST', api_url, files=files, data=arguments)

    def download_and_convert_image(self, image_url, format='webp'):
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            converted_image = BytesIO()
            image.save(converted_image, format=format)
            converted_image.seek(0)
            return converted_image
        else:
            raise Exception(f'이미지 다운로드 실패: 상태 코드 {response.status_code}')

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

    def add_category(self, name: str):
        """
        WordPress에 새로운 카테고리를 추가합니다.
        """
        api_url = f'{self.site_url}/wp-json/wp/v2/categories'
        category_data = {'name': name}
        return self.send_request('POST', api_url, json=category_data)

    def get_category(self, name: str):
        """
        주어진 이름의 카테고리 ID를 검색합니다.
        """
        api_url = f'{self.site_url}/wp-json/wp/v2/categories?search={name}'
        response = self.send_request('GET', api_url)
        if response and len(response) > 0:
            return response[0]['id']  # 첫 번째 일치 항목의 ID를 반환
        return None

    def add_tag(self, name: str):
        """
        WordPress에 새로운 태그를 추가합니다.
        """
        api_url = f'{self.site_url}/wp-json/wp/v2/tags'
        tag_data = {'name': name}
        return self.send_request('POST', api_url, json=tag_data)

    def get_tag(self, name: str):
        """
        주어진 이름의 태그 ID를 검색합니다.
        """
        api_url = f'{self.site_url}/wp-json/wp/v2/tags?search={name}'
        response = self.send_request('GET', api_url)
        if response and len(response) > 0:
            return response[0]['id']  # 첫 번째 일치 항목의 ID를 반환
        return None
    
    def ensure_category(self, name_or_id):
        """
        주어진 이름 또는 ID에 해당하는 카테고리가 있는지 확인하고,
        없으면 새로 생성합니다.
        """
        if isinstance(name_or_id, int):
            return name_or_id  # 이미 ID인 경우
        category_id = self.get_category(name_or_id)
        if category_id is not None:
            return category_id
        new_category = self.add_category(name_or_id)
        return new_category['id']

    def ensure_tag(self, name_or_id):
        """
        주어진 이름 또는 ID에 해당하는 태그가 있는지 확인하고,
        없으면 새로 생성합니다.
        """
        if isinstance(name_or_id, int):
            return name_or_id  # 이미 ID인 경우
        tag_id = self.get_tag(name_or_id)
        if tag_id is not None:
            return tag_id
        new_tag = self.add_tag(name_or_id)
        return new_tag['id']

if __name__ == '__main__':
    # 사용 예시
    uploader = WordPressUploader()
    # uploader.upload_post("새로운 게시글", "이것은 게시글의 내용입니다.")
    # uploader.upload_media("https://thumbnail11.coupangcdn.com/thumbnails/remote/212x212ex/image/retail/images/9254191159793527-75868827-c3ec-4444-baae-9a4782c4942e.jpg")
    uploader.upload_media("./serendipity-logo-white.png")
    # uploader.change_post_status(123, 'draft')  # 123은 게시글 ID
    # uploader.delete_post(123)
    # posts = uploader.get_posts()
    # print(posts)
