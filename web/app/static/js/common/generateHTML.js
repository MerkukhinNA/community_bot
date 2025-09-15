export function generateCommunityHTML(data, elementId) {
    const container = document.getElementById(elementId);
    let html = '';
    
    data.forEach(data => {
        html += `
            <input type="radio" id="${data.id}" class="btn-check" 
                   name="event" 
                   autocomplete="off" ${data.checked ? 'checked' : ''}>
            <label class="btn btn-outline-primary" for="${data.id}">
                Сообщество: ${data.name}
                <br><small>Описание: ${data.discription}</small>
                <br><small>Для "Искра-Парк": ${data.forSparkPark ? 'да' : 'нет'}</small>
            </label>
        `;
    });
    
    container.innerHTML += html;
}

export function generateVisitsHTML(data, elementId) {
    const container = document.getElementById(elementId);
    let html = '';
    
    data.forEach(data => {
        html += `
            <input type="radio" id="${data.visit_id}" class="btn-check" 
                   name="event" 
                   autocomplete="off" ${data.checked ? 'checked' : ''}>
            <label class="btn btn-outline-primary" for="${data.visit_id}">
                Пользователь: ${data.user_name} ${data.user_last_name}
                <br><small>Телефон: ${data.user_phone}</small>
                <br><small>Собщество: ${data.community_name}</small>
                <br><small>Событие: ${data.event_name}</small>
                <br><small>Описание события: ${data.event_discription}</small>
                <br><small>Дата: ${data.event_date}</small>
            </label>
        `;
    });
    
    container.innerHTML += html;
}

export function generateEventHTML(data, elementId) {
    const container = document.getElementById(elementId);
    let html = '';
    
    data.forEach(data => {
        html += `
            <input type="radio" id="${data.id}" class="btn-check" 
                   name="event" 
                   autocomplete="off" ${data.checked ? 'checked' : ''}>
            <label class="btn btn-outline-primary" for="${data.id}">
                Событие: ${data.name}
                <br><small> Сообщество: ${data.community}</small>
                <br><small>Дата: ${data.date}</small>
                <br><small> Описание: ${data.discription}</small>
            </label>
        `;
    });
    
    container.innerHTML += html;
}