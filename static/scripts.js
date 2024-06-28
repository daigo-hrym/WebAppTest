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
            const popupMessage = document.getElementById('popup-message'); // ● 追加: ポップアップ要素の取得
            const popupContent = document.getElementById('popup-content'); // ● 追加: ポップアップ要素の取得

            if (!messageElement || !resultElement || !popupMessage || !popupContent) { // ● 変更: ポップアップ要素の存在確認
                console.error("メッセージまたは結果表示用の要素が見つかりません");
                return;
            }

            console.log("入力された会員ID:", memberId);

            messageElement.style.display = 'none';
            resultElement.style.display = 'none';

            if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
                console.log("無効な会員ID形式:", memberId);
                popupContent.textContent = messages.invalid_format; // ● 変更: ポップアップにメッセージを表示
                popupMessage.style.display = 'block'; // ● 変更: ポップアップを表示
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
                        popupContent.textContent = `エラー：${data.message}`; // ● 変更: ポップアップにエラーメッセージを表示
                        popupMessage.style.display = 'block'; // ● 変更: ポップアップを表示
                    } else {
                        popupContent.textContent = `会員名：${data.name}`; // ● 変更: ポップアップに検索結果を表示
                        popupMessage.style.display = 'block'; // ● 変更: ポップアップを表示
                    }
                })
                .catch(error => {
                    console.error("検索リクエスト中にエラーが発生しました:", error);
                    popupContent.textContent = `${messages.error_occurred}：${error.message}`; // ● 変更: ポップアップにエラーメッセージを表示
                    popupMessage.style.display = 'block'; // ● 変更: ポップアップを表示
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