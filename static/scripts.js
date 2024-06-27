document.getElementById('search-btn').addEventListener('click', function() {
    fetch('/static/messages.json')
        .then(response => response.json())
        .then(messages => {
            const memberId = document.getElementById('member-id').value.trim();
            const popupMessage = document.getElementById('popup-message');
            const popupContent = document.getElementById('popup-content');

            if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
                popupContent.textContent = messages.invalid_format;
                popupMessage.style.display = 'block';
                document.getElementById('member-id').value = '';
                return;
            }

            fetch(`/search?memberId=${memberId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        popupContent.textContent = `エラー：${data.message}`;
                    } else {
                        popupContent.textContent = `会員名：${data.name}`;
                    }
                    popupMessage.style.display = 'block';
                })
                .catch(error => {
                    popupContent.textContent = `${messages.error_occurred}：${error.message}`;
                    popupMessage.style.display = 'block';
                });
        });

    // ● ポップアップを閉じるためのイベントリスナー
    document.getElementById('popup-message').addEventListener('click', function() {
        this.style.display = 'none';
    });
});