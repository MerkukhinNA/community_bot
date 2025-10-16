import { getUserId } from '../../common/tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '../main-menu';
    });
    document.getElementById('create-btn').addEventListener('click', function(event) {
        window.location.href = './create';
    });
    document.getElementById('my-btn').addEventListener('click', function(event) {
        window.location.href = './my';
    });
}