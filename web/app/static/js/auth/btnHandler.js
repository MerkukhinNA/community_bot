import { getUserId } from '../common/tgWebApp.js';

export function hadleButtons() {
    const firstName = document.getElementById('first-name');
    const middleName = document.getElementById('middle-name');
    const lastName = document.getElementById('last-name');
    const companyName = document.getElementById('company-name');
    const phone = document.getElementById('phone-mask');
    const question = document.getElementById('work-question-yes-btn');  // Самый простой способ - просто проверять чек одной из кнопок
    
    document.getElementById('complete-btn').addEventListener('click', function(event) {
        event.target.style.display = "none"

        // Создаем данные для api
        const data = {
            chat_id: String(getUserId()),
            name: firstName.value,
            last_name: middleName.value + " " + lastName.value,
            company: companyName.value,
            phone: phone.value,
            work_in_spark_park: question.checked,
        }
        
        // Отправляем данные на api бэкенда
        const api = 'api/v1/users/create'
        console.log(`Отправленные данные на "${api}":`, data);
        fetch(api, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Указываем, что отправляем данные в формате JSON
            },
            body: JSON.stringify(data), // Эти данные будут переданы в аргументы функции, которую декарирует FastApi
        })
        .then(response => response.json())
        .then(responseData => {
            if (responseData['success']) {
                console.log("Ответ от сервера: " + JSON.stringify(responseData));
                window.location.href = 'main-menu';
            } else {
                event.target.style.display = "inline-block"; // Снова показать кнопку после получения ответа от сервера
                alert("Ответ от сервера: " + JSON.stringify(responseData));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
}