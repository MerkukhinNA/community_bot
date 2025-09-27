import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = './menu';
    });

    details = document.getElementById('details')

    document.querySelectorAll('input[name="event"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                console.log('Выбран ID:', this.id);
                details.innerHTML = `<label class="form-label d-block">Загрузка</label>`

                const data = {
                    question_id: this.id,
                }
        
                const api = '../api/v1/question/details'
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
                        details.innerHTML = `
                            <label class="form-label d-block">Текс: ${responseData.details.text}</label>
                            <label class="form-label d-block">Дата создания: ${responseData.details.date_create}</label>
                            <label class="form-label d-block">Ответ: ${responseData.details.answer}</label>
                            <label class="form-label d-block">Дата ответа: ${responseData.details.date_answer}</label>
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