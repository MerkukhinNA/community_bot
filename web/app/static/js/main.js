import { checkIsTgWebApp } from './common/tgWebApp.js';
import { checkUser } from './common/callCommonApi.js';

document.addEventListener('DOMContentLoaded', async function() {
    // if (!checkIsTgWebApp()) {
    //     return;
    // }

    if (await checkUser()) {         
        window.location.href = 'main-menu';
    } else {
        window.location.href = 'auth';
    }
});