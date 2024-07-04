// グローバル変数としてポップアップ要素を定義
const popupMessage = document.getElementById('popup-message');
const popupContent = document.getElementById('popup-content');

// ポップアップを表示する関数
function showPopup(message) {
    popupContent.textContent = message;
    popupMessage.style.display = 'block';
    console.log("ポップアップが表示されました:", message);
}

// 検索ボタンのイベントリスナー
document.getElementById('search-btn').addEventListener('click', function() {
    console.log("検索ボタンがクリックされました");

    const memberId = document.getElementById('member-id').value.trim();

    if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
        showPopup("無効な会員ID形式です。半角英数字のみ使用可能です。");
        document.getElementById('member-id').value = '';
        return;
    }

    fetch(`/search?memberId=${memberId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showPopup(`エラー：${data.message}`);
            } else {
                showPopup(`会員名：${data.name}`);
            }
        })
        .catch(error => {
            console.error("検索リクエスト中にエラーが発生しました:", error);
            showPopup(`エラーが発生しました：${error.message}`);
        });
});

// 追加ボタンのイベントリスナー
document.getElementById('add-btn').addEventListener('click', function() {
    const memberId = document.getElementById('member-id').value.trim();
    const memberName = document.getElementById('member-name').value.trim();

    if (!memberId || !memberName) {
        showPopup("会員IDと会員名称は必須です。");
        return;
    }

    if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
        showPopup("無効な会員ID形式です。半角英数字のみ使用可能です。");
        return;
    }

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
            showPopup(`エラー：${data.message}`);
        } else {
            showPopup(`会員ID：${data.memberId}、会員名称：${data.memberName}が追加されました。`);
        }
    })
    .catch(error => {
        console.error("追加リクエスト中にエラーが発生しました:", error);
        showPopup(`エラーが発生しました：${error.message}`);
    });
});

// ポップアップを閉じるイベントリスナー
popupMessage.addEventListener('click', function() {
    this.style.display = 'none';
    console.log("ポップアップが閉じられました");
});