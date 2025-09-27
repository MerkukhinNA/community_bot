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