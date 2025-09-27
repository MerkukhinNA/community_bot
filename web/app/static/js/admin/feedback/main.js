import { hadleButtons } from './btnHandler.js';
import { getQuestions } from '../../common/callCommonApi.js';
import { generateQuestionsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    var responseData = await getQuestions('../../');
    const data = responseData.questions.map(item => ({
        id: item.question_id,
        status: item.status == 'created' ? 'о ожидании' : 'отвечен' ,
        text: item.text,
        date: item.date,
        user_name: item.user_name,
        checked: false
    }));
    
    generateQuestionsHTML(data, 'dynamic-container');
    hadleButtons()
});