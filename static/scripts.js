document.getElementById('search-btn').addEventListener('click', function() {
    console.log("検索ボタンがクリックされました");
    
    fetch('/static/messages.json')
        .then(response => response.json())
        .then(messages => {
            console.log("messages.jsonが読み込まれました:", messages);
            const memberId = document.getElementById('member-id').value.trim();
            const popupMessage = document.getElementById('popup-message');
            const popupContent = document.getElementById('popup-content');

            if (!popupMessage || !popupContent) {
                console.error("ポップアップ要素が見つかりません");
                return;
            }

            console.log("入力された会員ID:", memberId);

            if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
                console.log("無効な会員ID形式:", memberId);
                popupContent.textContent = messages.invalid_format;
                popupMessage.style.display = 'block';
                document.getElementById('member-id').value = '';
                return;
            }

            fetch(`/search?memberId=${memberId}`)
                .then(response => {
                    console.log("検索リクエストが送信されました:", response);
                    return response.json();
                })
                .then(data => {
                    console.log("検索結果が返されました:", data);
                    if (data.error) {
                        popupContent.textContent = `エラー：${data.message}`;
                    } else {
                        popupContent.textContent = `会員名：${data.name}`;
                    }
                    popupMessage.style.display = 'block';
                })
                .catch(error => {
                    console.error("検索リクエスト中にエラーが発生しました:", error);
                    popupContent.textContent = `${messages.error_occurred}：${error.message}`;
                    popupMessage.style.display = 'block';
                });
        })
        .catch(error => {
            console.error("messages.jsonの読み込み中にエラーが発生しました:", error);
        });

    // ● ポップアップを閉じるためのイベントリスナー
    document.getElementById('popup-message').addEventListener('click', function() {
        this.style.display = 'none';
    });
});