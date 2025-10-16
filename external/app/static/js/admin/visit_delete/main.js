import { hadleButtons } from './btnHandler.js';
import { getVisits } from '../../common/callCommonApi.js';
import { generateVisitsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()

    var responseData = await getVisits('../../');
    const data = responseData.data.map(item => ({
        visit_id: item.visit_id,
        user_name: item.user_name,
        user_last_name: item.user_last_name,
        user_phone: item.user_phone,
        community_name: item.community_name,
        event_name: item.event_name,
        event_discription: item.event_discription,
        date: item.date,
    }));
    
    generateVisitsHTML(data, 'dynamic-container');
});