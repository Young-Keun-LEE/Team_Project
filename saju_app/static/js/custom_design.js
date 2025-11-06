document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.querySelector('.design-gallery');

    // 이 스크립트는 'design-gallery'가 있는 페이지에서만 실행
    if (!gallery) {
        return;
    }

    // API URL은 템플릿의 data 속성에서 가져옴
    const apiUrl = gallery.dataset.setActiveUrl;

    // 갤러리 전체에 이벤트 리스너를 한 번만 등록 (이벤트 위임)
    gallery.addEventListener('click', (event) => {
        // 클릭된 요소가 'apply-btn' 클래스를 가졌는지 확인
        const button = event.target.closest('.apply-btn');
        
        if (button) {
            const designId = button.dataset.designId;
            if (designId) {
                applyDesign(designId, button);
            }
        }
    });

    /**
     * 디자인 적용 API를 호출하고 UI를 업데이트하는 함수
     * @param {string} designId - 적용할 디자인의 ID
     * @param {HTMLElement} button - 클릭된 '적용하기' 버튼
     */
    async function applyDesign(designId, button) {
        
        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // TODO: CSRF 토큰이 필요하면 헤더에 추가
                },
                body: JSON.stringify({ design_id: designId })
            });

            const data = await response.json();

            if (data.success) {
                // 1. (UI) 기존에 '적용됨' 상태였던 카드를 찾아서 '적용하기'로 되돌림
                const oldActiveCard = gallery.querySelector('.design-card.active');
                if (oldActiveCard) {
                    oldActiveCard.classList.remove('active');
                    const oldButton = oldActiveCard.querySelector('.design-button');
                    if (oldButton) {
                        oldButton.classList.remove('active');
                        oldButton.classList.add('apply-btn'); // 'apply-btn' 클래스 추가
                        oldButton.textContent = '적용하기';
                        oldButton.disabled = false;
                    }
                }

                // 2. (UI) 방금 클릭한 카드를 '적용됨' 상태로 변경
                const newCard = button.closest('.design-card');
                newCard.classList.add('active'); // 테두리 활성화
                
                button.classList.remove('apply-btn');
                button.classList.add('active'); // 버튼 스타일 변경
                button.textContent = '✔️ 적용됨';
                button.disabled = true;

            } else {
                alert(data.error || '디자인 적용에 실패했습니다.');
            }
        } catch (error) {
            console.error('디자인 적용 중 오류:', error);
            alert('네트워크 오류가 발생했습니다.');
        }
    }
});