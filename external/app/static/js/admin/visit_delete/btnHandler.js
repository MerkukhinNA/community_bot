export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '.././menu';
    });
    document.getElementById('confirm-btn').addEventListener('click', function(event) {
        bootstrap.Modal.getInstance(document.getElementById('confirm-modal')).hide();
        const selectedBtn = document.querySelector('input[name="event"]:checked');
        console.log('selected id', selectedBtn.id);

        const data = {
            visit_id: parseInt(selectedBtn.id),
        }
        
        const api = '../../api/v1/visit/delete'
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
            window.location.href = '.././menu';
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
}