import { getUserQuestions } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateUserQuestionsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    var responseData = await getUserQuestions('../');
    const data = responseData.questions.map(item => ({
        id: item.question_id,
        text: item.text,
        date_create: item.date,
        status: item.status == 'created' ? 'о ожидании' : 'отвечен' ,
        checked: false
    }));
    
    generateUserQuestionsHTML(data, 'dynamic-container');
    hadleButtons()
});