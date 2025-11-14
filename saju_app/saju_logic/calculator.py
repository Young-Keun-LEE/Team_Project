# saju_logic/calculator.py (수정)
import time
from sajupy import calculate_saju
import random
# 모델 로드는 앱 실행 시 1번만 (기존과 동일)

# --- 1. 오행 매핑 테이블 (상수) ---
CHEONGAN_OHENG = {'甲': '목', '乙': '목', '丙': '화', '丁': '화', '戊': '토', '己': '토', '庚': '금', '辛': '금', '壬': '수', '癸': '수'}
JIJI_OHENG = {'寅': '목', '卯': '목', '巳': '화', '午': '화', '辰': '토', '戌': '토', '丑': '토', '未': '토', '申': '금', '酉': '금', '亥': '수', '子': '수'}
OHENG_MAP = {**CHEONGAN_OHENG, **JIJI_OHENG}

# --- 2. 일간 성향 매핑 테이블 (상수) ---
ILGAN_PERSONALITY = {
    '甲': "리더십이 강하고 진취적인 나무(甲목)",
    '乙': "유연하고 적응력이 뛰어난 풀(乙목)",
    '丙': "밝고 열정적인 태양(丙화)",
    '丁': "따뜻하고 섬세한 촛불(丁화)",
    '戊': "듬직하고 신뢰감 있는 큰 산(戊토)",
    '己': "포용력이 넓고 안정적인 논밭(己토)",
    '庚': "강하고 결단력 있는 바위(庚금)",
    '辛': "예리하고 반짝이는 보석(辛금)",
    '壬': "지혜롭고 유유히 흐르는 바다(壬수)",
    '癸': "총명하고 스며드는 이슬비(癸수)"
}
# --- 3. [수정] MBTI-유명인 매핑 테이블 (상수) ---
MBTI_CELEBRITY = { # 한 MBTI 당 여러 유명인 추가해서 그날 그날 바뀌게끔 추가 확장 가능
    'INFJ': 'RM (BTS)',
    'INFP': '아이유 (IU)',
    'INTJ': 'G-Dragon',
    'INTP': '티모시 샬라메',
    'ISFJ': '비욘세',
    'ISFP': '정국 (BTS)',
    'ISTJ': '강동원',
    'ISTP': '톰 크루즈',
    'ENFJ': '제니퍼 로렌스',
    'ENFP': '로버트 다우니 주니어',
    'ENTJ': '스티브 잡스',
    'ENTP': '라이언 레이놀즈',
    'ESFJ': '테일러 스위프트',
    'ESFP': '아델',
    'ESTJ': '엠마 왓슨',
    'ESTP': '도널드 트럼프'
}

# --- 4.MBTI 유명인 이미지 URL 매핑 테이블 ---
MBTI_CELEBRITY_IMAGES = {
    
    'INFJ': 'RM.jpg',
    'INFP': 'IU.jpg',
    'INTJ': 'G-Dragon.jpg',
    'INTP': 'Timothée_Chalamet.jpg',
    'ISFJ': 'Beyoncé.jpg',
    'ISFP': 'Jeon_Jungkook.jpg',
    'ISTJ': 'Kang_Dong-won.jpg',
    'ISTP': 'Tom_Cruise.jpg',
    'ENFJ': 'Jennifer_Lawrence.jpg',
    'ENFP': 'Robert_Downey_Jr.jpg',
    'ENTJ': 'Steve_Jobs.jpg',
    'ENTP': 'Ryan_Reynolds.jpg',
    'ESFJ': 'Taylor_Swift.jpg',
    'ESFP': 'Adele.jpg',
    'ESTJ': 'Emma_Watson.png',
    'ESTP': 'Donald_J._Trump.jpg'
}
# --- 5. 퍼스널 컬러 테이블 매일 랜덤하게 매칭 ---
RANDOM_COLOR_PALETTE = [
    {'name': '선셋 오렌지', 'code': '#f4a261'},
    {'name': '코랄 핑크', 'code': '#e76f51'},
    {'name': '오션 블루', 'code': '#264653'},
    {'name': '포레스트 그린', 'code': '#2a9d8f'},
    {'name': '선샤인 옐로우', 'code': '#e9c46a'},
    {'name': '라벤더 그레이', 'code': '#a5a5c5'},
    {'name': '딥 퍼플', 'code': '#800080'},
    {'name': '로얄 네이비', 'code': '#000080'},
    {'name': '버건디 레드', 'code': '#800020'}
]
def analyze_saju(birth_datetime):
    """
    sajupy로 사주를 계산하고, 성향, MBTI를 계산하여 반환
    """
    year = birth_datetime.year
    month = birth_datetime.month
    day = birth_datetime.day
    hour = birth_datetime.hour
    minute = birth_datetime.minute
    
    print(f"분석 요청: {birth_datetime}")
    
    try: # 라이브러리가 성공적으로 계산했는지 확인
        saju_result = calculate_saju(
            year=year, month=month, day=day, hour=hour, minute=minute,
            city="Seoul", use_solar_time=True
        )
    except Exception as e:
        print(f"사주 계산 오류: {e}")
        return None
    
    # 1. sajupy 결과에서 8개의 글자(팔자) 추출
    year_ganji = saju_result.get('year_pillar', '')
    month_ganji = saju_result.get('month_pillar', '')
    day_ganji = saju_result.get('day_pillar', '')
    hour_ganji = saju_result.get('hour_pillar', '')

    if not all([year_ganji, month_ganji, day_ganji, hour_ganji]):
        return None

    # 8개 글자를 리스트로 변환 (예: '庚午' -> ['庚', '午'])
    all_chars = list(year_ganji) + list(month_ganji) + list(day_ganji) + list(hour_ganji)
    
    # 2. 오행 점수(개수) 계산
    oheng_scores = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
    for char in all_chars:
        oheng = OHENG_MAP.get(char)
        if oheng:
            oheng_scores[oheng] += 1

    # 3. 일간(나 자신) 추출
    ilgan = day_ganji[0]
    

    # --- 4. 기본 성향 분석 ---
    personality_desc = ILGAN_PERSONALITY.get(ilgan, "알 수 없음")

    # --- 5. MBTI 추론 로직 ---
    mbti = ""

    # E/I (외향/내향)
    if ilgan in ['甲', '丙', '戊', '庚', '壬']:
        mbti += "E"
    else:
        mbti += "I"

    # S/N (감각/직관)
    # (수정) scores -> oheng_scores
    if oheng_scores.get('금', 0) + oheng_scores.get('토', 0) > oheng_scores.get('수', 0) + oheng_scores.get('목', 0):
        mbti += "S"
    else:
        mbti += "N"

    # T/F (사고/감정)
    # (수정) scores -> oheng_scores
    if oheng_scores.get('금', 0) > oheng_scores.get('화', 0):
        mbti += "T"
    else:
        mbti += "F"

    # J/P (판단/인식)
    # (수정) scores -> oheng_scores
    if oheng_scores.get('토', 0) > oheng_scores.get('수', 0):
        mbti += "J"
    else:
        mbti += "P"

    # --- 6. MBTI 및 퍼스널 컬러 생성 ---
    
    # 6-1. MBTI로 유명인 매칭 (없을 경우 '알 수 없음' 반환)
    celebrity_name = MBTI_CELEBRITY.get(mbti, '유명인 정보 없음') 

    # 6-2. 랜덤 컬러 코드 생성 (예: #f4a261) -> 성향별 매칭아니고 매일 랜덤하게 변경
    selected_color = random.choice(RANDOM_COLOR_PALETTE)
    color_name = selected_color['name']
    color_code = selected_color['code']
    
    # 6-3. MBTI로 유명인 이미지 URL 매칭
    celebrity_image_file = MBTI_CELEBRITY_IMAGES.get(mbti, 'default_celeb.png')
    
    # 3가지 정보를 포함한 딕셔너리 반환
    analysis_data = {
        'mbti': mbti,
        'personality_desc': personality_desc,
        'celebrity': celebrity_name,
        'color_name': color_name,             
        'color_code': color_code,
        'celebrity_image_filename': celebrity_image_file
    }
    
    return analysis_data