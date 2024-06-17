document.getElementById('search-btn').addEventListener('click', function() {
    const memberId = document.getElementById('member-id').value.trim();
    const messageElement = document.getElementById('message');
    const resultElement = document.getElementById('result');

    messageElement.style.display = 'none';
    resultElement.style.display = 'none';

    if (!/^[a-zA-Z0-9]+$/.test(memberId)) {
        messageElement.textContent = '半角英数字を入力してください';
        messageElement.style.display = 'block';
        document.getElementById('member-id').value = '';
        return;
    }

    fetch(`/search?memberId=${memberId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                messageElement.textContent = data.message;
                messageElement.style.display = 'block';
            } else {
                resultElement.textContent = `会員名: ${data.name}`;
                resultElement.style.display = 'block';
            }
        })
        .catch(error => {
            messageElement.textContent = 'エラーが発生しました';
            messageElement.style.display = 'block';
        });
});