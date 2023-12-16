# WordPressUploader

WordPressUploader는 Python을 사용하여 WordPress 사이트에 게시글 및 미디어를 업로드하고, 게시글을 관리하는 도구입니다. 이 도구를 사용하면 프로그래매틱 방식으로 WordPress 사이트의 컨텐츠를 관리할 수 있습니다.

## 기능

- 게시글 업로드
- 미디어 파일 업로드
- 게시글 상태 변경 (예: draft, publish)
- 게시글 삭제
- 게시글 목록 조회

## 시작하기

이 섹션에서는 프로젝트를 로컬 환경에서 실행하기 위한 지침을 제공합니다.

### 필요 조건

이 프로젝트를 사용하기 위해서는 Python 3.x와 `requests` 라이브러리가 필요합니다.

### 설치

1. 프로젝트를 클론합니다.

   ```bash
   git clone https://github.com/joonheeu/wordpress-uploader.git
   cd wordpress-post-uploader
   ```
2. 필요한 라이브러리를 설치합니다.

   ```bash
   pip install -r requirements.txt
   ```
3. `.env` 파일을 생성하고 WordPress 사이트의 정보를 입력합니다.

   ```
   WP_SITE_URL='https://your-wordpress-url'
   WP_USERNAME='your_username'
   WP_PASSWORD='your_password'
   ```

### 사용 예제

```python
from wp_uploader import WordPressUploader

uploader = WordPressUploader()

# 게시글 업로드
uploader.upload_post("제목", "내용")

# 미디어 업로드
uploader.upload_media("path/to/image.jpg")

# 게시글 상태 변경
uploader.change_post_status(123, 'draft')  # 123은 게시글 ID

# 게시글 삭제
uploader.delete_post(123)

# 게시글 목록 조회
posts = uploader.get_posts()
print(posts)
```

## 기여하기

이 프로젝트에 기여하고 싶으신 분들은 아래 지침에 따라 기여할 수 있습니다.

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경 사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 열기

## 라이센스

이 프로젝트는 [MIT 라이센스](LICENSE)에 따라 사용이 허가되어 있습니다.

## 저자

- joonheeu - [GitHub 링크](https://github.com/joonheeu)
