import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '../main-menu';
    });
    document.getElementById('community-create-btn').addEventListener('click', function(event) {
        window.location.href = './community/create';
    });
    document.getElementById('community-delete-btn').addEventListener('click', function(event) {
        window.location.href = './community/delete';
    });
    document.getElementById('community-update-btn').addEventListener('click', function(event) {
        window.location.href = './community/update';
    });
    document.getElementById('event-create-btn').addEventListener('click', function(event) {
        window.location.href = './event/create';
    });
    document.getElementById('event-delete-btn').addEventListener('click', function(event) {
        window.location.href = './event/delete';
    });
    document.getElementById('visit-delete-btn').addEventListener('click', function(event) {
        window.location.href = './visit/delete';
    });
}