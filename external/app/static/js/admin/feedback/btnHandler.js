import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = './menu';
    });

    const dataContainer = document.getElementById('data-container')
    const answerContainer = document.getElementById('answer-container')
    const answer = document.getElementById('answer')
    var selectedFeedbackId

    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();
        console.log('selectedFeedbackId:', selectedFeedbackId)

        const data = {
            chat_id: String(getUserId()),
            feedback_id: parseInt(selectedFeedbackId),
            text: answer.value,
        }
        
        const api = '/api/v1/feedback/answer/create'
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
                window.location.reload()
            } else {
                alert("Ответ от сервера: " + JSON.stringify(responseData));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
    document.querySelectorAll('input[name="event"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                console.log('Выбран ID:', this.id)
                selectedFeedbackId = this.id
                console.log('selectedFeedbackId:', selectedFeedbackId)
                dataContainer.innerHTML = `<label class="form-label d-block">Загрузка</label>`

                const data = {
                    feedback_id: this.id,
                }
        
                const api = '../../api/v1/feedback'
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
                        console.log("Ответ от сервера: " + JSON.stringify(responseData))
                        answerContainer.classList.remove('d-none');  // Сделать видимым убрав класс скрытности

                        dataContainer.innerHTML = `
                            <label class="form-label d-block">Текс: ${responseData.data.text}</label>
                            <label class="form-label d-block">Дата создания: ${responseData.data.date_create}</label>
                            <label class="form-label d-block">ФИО пользователя: ${responseData.data.user_name}</label>
                            <label class="form-label d-block">Контакт пользователя: ${responseData.data.user_contact}</label>
                            <label class="form-label d-block">Ответ:  ${responseData.data.answer}</label>
                            <label class="form-label d-block">Дата ответа: ${responseData.data.date_answer}</label>
                        `;
                    } else {
                        alert("Ответ от сервера: " + JSON.stringify(responseData));
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
            }
        });
    });
}