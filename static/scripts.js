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
            const popupMessage = document.getElementById('popup-message');
            const popupContent = document.getElementById('popup-content');

            if (!messageElement || !resultElement || !popupMessage || !popupContent) {
                console.error("メッセージまたは結果表示用の要素が見つかりません");
                return;
            }

            console.log("入力された会員ID:", memberId);

            messageElement.style.display = 'none';
            resultElement.style.display = 'none';

            if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
                console.log("無効な会員ID形式:", memberId);
                popupContent.textContent = messages.invalid_format;
                popupMessage.style.display = 'block';
                console.log("ポップアップを表示します: 無効な会員ID形式");
                document.getElementById('member-id').value = '';
                console.log("ポップアップが表示されました: 無効な会員ID形式", popupMessage.style.display);
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
                        popupMessage.style.display = 'block';
                        console.log("ポップアップを表示します: エラー", data.message);
                    } else {
                        popupContent.textContent = `会員名：${data.name}`;
                        popupMessage.style.display = 'block';
                        console.log("ポップアップを表示します: 会員名", data.name);
                    }
                    console.log("ポップアップが表示されました: 検索結果", popupMessage.style.display);
                })
                .catch(error => {
                    console.error("検索リクエスト中にエラーが発生しました:", error);
                    popupContent.textContent = `${messages.error_occurred}：${error.message}`;
                    popupMessage.style.display = 'block';
                    console.log("ポップアップを表示します: エラー", error.message);
                    console.log("ポップアップが表示されました: エラー", popupMessage.style.display);
                });
        })
        .catch(error => {
            console.error("messages.jsonの読み込み中にエラーが発生しました:", error);
        });

    // ポップアップを閉じるためのイベントリスナー
    document.getElementById('popup-message').addEventListener('click', function() {
        this.style.display = 'none';
        console.log("ポップアップが閉じられました");
    });
});

★
document.getElementById('add-btn').addEventListener('click', function() {
    const memberId = document.getElementById('member-id').value.trim();
    const memberName = document.getElementById('member-name').value.trim();
    const popupMessage = document.getElementById('popup-message');
    const popupContent = document.getElementById('popup-content');

    // 簡単な入力検証
    if (!memberId || !memberName || !/^[a-zA-Z0-9]+$/.test(memberId)) {
        popupContent.textContent = "無効な入力です。会員IDは半角英数字、会員名称は必須です。";
        popupMessage.style.display = 'block';
        return;
    }

    // データ送信
    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ memberId, memberName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            popupContent.textContent = `エラー：${data.message}`;
        } else {
            popupContent.textContent = `会員ID：${data.memberId}、会員名称：${data.memberName}が追加されました。`;
        }
        popupMessage.style.display = 'block';
    })
    .catch(error => {
        popupContent.textContent = `エラーが発生しました：${error.message}`;
        popupMessage.style.display = 'block';
    });
});

document.getElementById('popup-message').addEventListener('click', function() {
    this.style.display = 'none';
});