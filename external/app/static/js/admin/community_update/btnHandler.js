import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '.././menu';
    });

    const communityName = document.getElementById('name');
    const communityDiscription = document.getElementById('discription');
    const question = document.getElementById('question-yes-btn');

    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();
        const selectedCommunityBtn = document.querySelector('input[name="event"]:checked');
        console.log('selectedCommunityBtn = ', selectedCommunityBtn.id);
            
        const data = {
            community_id: parseInt(selectedCommunityBtn.id),
            name: communityName.value,
            discription: communityDiscription.value,
            question: question.checked,
        }
        
        const api = '/api/v1/community/update'
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