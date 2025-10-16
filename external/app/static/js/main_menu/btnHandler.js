import { getUserId } from '../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('create-event-btn').addEventListener('click', function(event) {
        window.location.href = 'event/create';
    });
    document.getElementById('user-event-btn').addEventListener('click', function(event) {
        window.location.href = 'event/user';
    });
    document.getElementById('feedback-btn').addEventListener('click', function(event) {
        window.location.href = 'feedback/menu';
    });
    document.getElementById('admin-btn').addEventListener('click', function(event) {
        window.location.href = 'admin/menu';
    });
}