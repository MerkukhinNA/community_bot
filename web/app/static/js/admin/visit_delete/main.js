import { hadleButtons } from './btnHandler.js';
import { getVisits } from '../../common/callCommonApi.js';
import { generateVisitsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()

    var responseData = await getVisits('../../');
    const data = responseData.visits.map(visit => ({
        visit_id: visit.visit_id,
        user_name: visit.user_name,
        user_last_name: visit.user_last_name,
        user_phone: visit.user_phone,
        community_name: visit.community_name,
        event_name: visit.event_name,
        event_discription: visit.event_discription,
        event_date: visit.event_date,
    }));
    
    generateVisitsHTML(data, 'dynamic-container');
});