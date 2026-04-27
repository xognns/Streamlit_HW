import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="늬가 힙합을 알어?",
    page_icon="🎧",
)

# 제목과 소개
st.title('🎧늬가 힙합을 알어?🎧')
st.markdown('### 힙합에 대해서 얼마나 알고 있나요?')
st.markdown('2025404030 경태훈')


# 사이드바 
st.sidebar.header('사이드바 메뉴')
option = st.sidebar.selectbox(
    '원하는 기능 선택하셈',
    ['회원가입', '로그인', '퀴즈', '앱 정보']
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


@st.cache_data
def get_quiz_data():
    return [
        {
            'title': '1번 문제',
            'question': '힙합을 영어로 하면?',
            'options': ['heehop', 'hiphap', 'hiphop', 'hiphob'],
            'answer': 'hiphop',
        },
        {
            'title': '2번 문제',
            'question': '우리나라에서 진행한 힙합 오디션 프로그램은?',
            'options': ['미스터트롯', '쇼미더머니', '복면가왕', '프로듀스101'],
            'answer': '쇼미더머니',
        },
        {
            'title': '3번 문제',
            'question': '다음 중 한국 래퍼가 아닌 사람은?',
            'options': ['칸예 웨스트', '스윙스', '개코', '제네 더 질라'],
            'answer': '칸예 웨스트',
        },
        {
            'title': '4번 문제',
            'question': '랩에서 반복되는 소리로, 랩의 리듬감을 형성하는 이것은?',
            'options': ['플로우', '비트', '딜리버리', '라임'],
            'answer': '라임',
        },
    ]


# 회원가입
if option == '회원가입':

    st.title('회원가입')

    st.markdown('### 넌 누구냐.')

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input('이름', '홍길동')
        birthday = st.number_input('생년월일', min_value=19800101, max_value=20101231, value=20060322)
    with col2:
        schoolnumber = st.text_input('학번', '2025404030')
        major = st.selectbox('학과', 
                         ['정보융합학부', '소프트웨어학부', '컴퓨터정보공학부', '로봇학부'])
    
    st.markdown('### 뭘 듣느냐.')

    col3, col4 = st.columns(2)

    with col3:
        streamingapp = st.selectbox('사용중인 음악 스트리밍 앱은?', 
                         ['Melon music', 'Apple music', 'Spotify', 'Youtube music', '기타'])
        st.write(f'사용중인 앱: {streamingapp}')

    
    with col4:
        favsong = st.text_input('요즘 가장 좋아하는 음악(장르 상관 없이)', 'maybe baby')

        artist = st.text_input('아티스트', 'effie')

    if st.button('가입하기'):
        st.session_state.user = {
            'name': name,
            'birthday': birthday,
            'schoolnumber': schoolnumber,
            'major': major,
            'streamingapp': streamingapp,
            'favsong': favsong,
            'artist': artist,
        }
        st.session_state.logged_in = False
        st.success(f'{name}님, 회원가입이 완료되었습니다.')

elif option == '로그인':
    st.title('로그인')

    loginname = st.text_input('이름 확인', '홍길동', key='login_name')
    loginschoolnumber = st.text_input('학번 확인', '2025404030', key='login_schoolnumber')

    if st.button('로그인'):
        user = st.session_state.get('user')

        if user is None:
            st.warning('먼저 회원가입을 해주세요.')
        elif loginname == user['name'] and loginschoolnumber == user['schoolnumber']:
            st.session_state.logged_in = True
            st.success('로그인 성공!')
            st.write(f"{user['major']} {user['schoolnumber']} {user['name']}님 환영합니다.")
        else:
            st.session_state.logged_in = False
            st.error('로그인 실패')


# 퀴즈 기능
elif option == '퀴즈' :
    if not st.session_state.logged_in:
        st.warning('로그인해야 퀴즈에 접속할 수 있습니다.')
        st.info('사이드바에서 로그인 메뉴를 선택해서 먼저 로그인해주세요.')
    else:
        st.header('힙합 상식 퀴즈')

        quiz_data = get_quiz_data()
        quiz_tabs = st.tabs([quiz['title'].replace(' 문제', '') for quiz in quiz_data])
        score = 0
        answered_count = 0

        for index, quiz in enumerate(quiz_data):
            with quiz_tabs[index]:
                st.write(quiz['title'])
                st.write(f"### {quiz['question']}")
                quiz_answer = st.selectbox(
                    '답 선택',
                    ['선택하세요'] + quiz['options'],
                    key=f'quiz_answer{index + 1}',
                )

                if quiz_answer == '선택하세요':
                    st.info('답을 선택해주세요.')
                elif quiz_answer == quiz['answer']:
                    score += 1
                    answered_count += 1
                    st.success('정답입니다!')
                else:
                    answered_count += 1
                    st.error('오답입니다.')

        st.markdown('---')
        st.subheader('최종 결과')

        if answered_count < len(quiz_data):
            st.info(f'아직 {len(quiz_data) - answered_count}문제를 더 풀어야 합니다.')
        else:
            st.success(f'총 {len(quiz_data)}문제 중 {score}문제를 맞혔습니다.')

            if score == len(quiz_data):
                st.write('힙합 상식 만점입니다.')
            elif score >= len(quiz_data) // 2:
                st.write('기본적인 힙합 상식은 알고 있습니다.')
            else:
                st.write('힙합 상식을 조금 더 익혀보세요.')
    

else:
    st.header('앱 정보')
    st.info('이 앱은 당신의 힙합 교양 수준을 평가하기 위해 제작되었습니다.')
