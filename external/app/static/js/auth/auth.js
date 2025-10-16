import { hadleButtons } from './btnHandler.js';
import { applyPhoneMask } from './phoneMask.js';

document.addEventListener('DOMContentLoaded', async function() {
    console.log("Авторизация загружена");
    hadleButtons();
    applyPhoneMask();
});