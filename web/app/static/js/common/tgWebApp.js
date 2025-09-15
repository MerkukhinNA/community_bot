export function getUserId() {
    var userId = 666 // Это просто тестовые данные

    if (window.Telegram && window.Telegram.WebApp) {
        let tg = window.Telegram.WebApp;
        const user = tg.initDataUnsafe.user;

        if (user) {
            userId = user.id;  // user.id - это message.chat.id в python telebot
        }
    } 

    return userId
}

export function checkIsTgWebApp() {
    // Проверка на запуск сайта внутри телеграма (через Mini Apps)(нужно т.к. нету кастомной регистрации а многие функции требую идентифицировать пользователя, например ID)
    if (window.Telegram && window.Telegram.WebApp) {
        let tg = window.Telegram.WebApp;
        const user = tg.initDataUnsafe.user;
        
        if (user) {
            return true;
        } else {
            alert("не удалось получить данные о пользователе");
            return false;
        }
    } else {
        alert("сайт запущен вне 'Tg Mini Apps'");
        return false;
    }
}