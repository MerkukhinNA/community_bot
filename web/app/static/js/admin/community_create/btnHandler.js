import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '.././menu';
    });

    const communityName = document.getElementById('community-name');
    const communityDiscription = document.getElementById('community-discription');
    const question = document.getElementById('question-yes-btn');  // Самый простой способ - просто проверять чек одной из кнопок
    
    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();  // Скрыть модальное окно

        const data = {
            name: communityName.value,
            discription: communityDiscription.value,
            for_spark_part: question.value,
        }
        
        const api = '/api/v1/community/create'
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
            console.log("Ответ от сервера: " + JSON.stringify(responseData));
            if (responseData['success']) {
                console.log("Ответ от сервера: " + JSON.stringify(responseData));
                window.location.href = '.././menu';
            } else {
                alert("Ответ от сервера: " + JSON.stringify(responseData));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
}