import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = './menu';
    });

    const question = document.getElementById('question');
    
    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();

        const data = {
            user_chat_id: String(getUserId()),
            text: question.value
        }
        
        const api = '../api/v1/question/create'
        console.log(`Отправленные данные на "${api}":`, data);
        fetch(api, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(responseData => {
            if (responseData['success']) {
                console.log("Ответ от сервера: " + JSON.stringify(responseData));
                window.location.href = './menu';
                alert("Вопрос отправлен");

            } else {
                alert("Ответ от сервера: " + JSON.stringify(responseData));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
}