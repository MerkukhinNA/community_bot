import { getUserId } from './tgWebApp.js';

export function checkUser(localPath='') {
    const data = {
        chat_id: String(getUserId()),
    }
    
    const api = localPath + 'api/v1/users/check';
    console.log(`Отправленные данные на "${api}":`, data);
    // Возвращаем Promise
    return fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData));
        return responseData['success'];
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return false;
    });
}

export function getUserEvents(localPath='') {
    const data = {
        chat_id: String(getUserId()),
    }
    
    const api = localPath + 'api/v1/user/events'
    console.log(`Отправленные данные на "${api}":`, data);
    return fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getUserVisits(localPath='') {
    const data = {
        chat_id: String(getUserId()),
    }
    
    const api = localPath + 'api/v1/users/visits'
    console.log(`Отправленные данные на "${api}":`, data);
    return fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getEvents(localPath='') {
    const api = localPath + 'api/v1/events'
    return fetch(api, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json', 
        },
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getCommunityes(localPath='') {
    const api = localPath + 'api/v1/communityes'
    return fetch(api, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json', 
        },
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getVisits(localPath='') {
    const api = localPath + 'api/v1/visits'
    return fetch(api, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json', 
        },
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getUserQuestions(localPath='') {
    const data = {
        chat_id: String(getUserId()),
    }
    
    const api = localPath + 'api/v1/user/questions'
    console.log(`Отправленные данные на "${api}":`, data);
    return fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}

export function getQuestions(localPath='') {
    const data = {
    }
    
    const api = localPath + 'api/v1/question/shorts'
    console.log(`Отправленные данные на "${api}":`, data);
    return fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(responseData => {
        console.log("Ответ от сервера: " + JSON.stringify(responseData, null, 2));
        return responseData
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return "err: " + error
    });
}