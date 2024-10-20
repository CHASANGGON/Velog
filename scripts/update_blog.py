import feedparser
import git
import os

# 벨로그 RSS 피드 URL
rss_url = 'https://v2.velog.io/rss/yg9618'

# 로컬 깃허브 레포지토리 경로 (로컬 경로로 수정)
repo_path = '.'  # GitHub Actions에서 실행할 때는 현재 디렉토리를 사용

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 로컬 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
    file_name = entry.title
    file_name = file_name.replace('/', '-').replace('\\', '-')  # 슬래시와 백슬래시 대체
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # 파일이 이미 존재하지 않으면 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {entry.title}\n\n")
            file.write(f"{entry.description}\n")
            file.write(f"\n[Read more]({entry.link})")

        # 깃허브 커밋
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')

# 변경 사항을 깃허브에 푸시
origin = repo.remote(name='origin')
origin.push()
