export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = './menu';
    });

    const dataContainer = document.getElementById('data-container')

    document.querySelectorAll('input[name="event"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                console.log('Выбран ID:', this.id);
                dataContainer.innerHTML = `<label class="form-label d-block">Загрузка</label>`

                const data = {
                    question_id: parseInt(this.id),
                }
        
                const api = '../api/v1/question/full'
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
                        dataContainer.innerHTML = `
                            <label class="form-label d-block">Текс: ${responseData.data.text}</label>
                            <label class="form-label d-block">Дата создания: ${responseData.data.date_create}</label>
                            <label class="form-label d-block">Ответ: ${responseData.data.answer}</label>
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