import { getUserFeedbacks } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateUserQuestionsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    var responseData = await getUserFeedbacks('../');
    const data = responseData.data.map(item => ({
        id: item.feedback_id,
        text: item.text,
        date_create: item.date,
        status: item.status == 'created' ? 'о ожидании' : 'отвечен' ,
        checked: false
    }));
    
    generateUserQuestionsHTML(data, 'dynamic-container');
    hadleButtons()
});