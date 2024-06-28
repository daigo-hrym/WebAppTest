document.getElementById('search-btn').addEventListener('click', function() {
    console.log("検索ボタンがクリックされました");

    fetch('/static/messages.json')
        .then(response => {
            console.log("messages.jsonが読み込まれました:", response);
            return response.json();
        })
        .then(messages => {
            console.log("messages.jsonの内容:", messages);
            const memberId = document.getElementById('member-id').value.trim();
            const messageElement = document.getElementById('message');
            const resultElement = document.getElementById('result');

            if (!messageElement || !resultElement) {
                console.error("メッセージまたは結果表示用の要素が見つかりません");
                return;
            }

            console.log("入力された会員ID:", memberId);

            messageElement.style.display = 'none';
            resultElement.style.display = 'none';

            if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
                console.log("無効な会員ID形式:", memberId);
                messageElement.textContent = messages.invalid_format;
                messageElement.style.display = 'block';
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
                        messageElement.textContent = `エラー：${data.message}`;
                        messageElement.style.display = 'block';
                    } else {
                        resultElement.textContent = `会員名：${data.name}`;
                        resultElement.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error("検索リクエスト中にエラーが発生しました:", error);
                    messageElement.textContent = `${messages.error_occurred}：${error.message}`;
                    messageElement.style.display = 'block';
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