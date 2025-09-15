import { getUserId } from '../../tgWebApp.js';

export function hadleButtons() {
    document.getElementById('back-btn').addEventListener('click', function(event) {
        window.location.href = '.././menu';
    });
}