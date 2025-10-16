import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = './menu';
    });

    const dataContainer = document.getElementById('data-container')
    const answerContainer = document.getElementById('answer-container')
    const answer = document.getElementById('answer')
    var selectedQuestionId

    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();
        console.log('selectedQuestionId:', selectedQuestionId)

        const data = {
            user_chat_id: String(getUserId()),
            question_id: parseInt(selectedQuestionId),
            text: answer.value,
        }
        
        const api = '/api/v1/question/answer/create'
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
                selectedQuestionId = this.id
                console.log('selectedQuestionId:', selectedQuestionId)
                dataContainer.innerHTML = `<label class="form-label d-block">Загрузка</label>`

                const data = {
                    question_id: this.id,
                }
        
                const api = '../../api/v1/question/full'
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