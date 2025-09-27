import { getUserId } from '../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('reserve-event-btn').addEventListener('click', function(event) {
        window.location.href = 'event/reserve';
    });
    document.getElementById('my-event-btn').addEventListener('click', function(event) {
        window.location.href = 'event/my';
    });
    document.getElementById('feedback-btn').addEventListener('click', function(event) {
        window.location.href = 'feedback/menu';
    });
    document.getElementById('admin-btn').addEventListener('click', function(event) {
        window.location.href = 'admin/menu';
    });
}