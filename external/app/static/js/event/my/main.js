import { getUserEventVisits } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    
    var responseData = await getUserEventVisits('../');
    const data = responseData.visits.map(visit => ({
        id: visit.visit_id,
        name: visit.event_name,
        community: visit.event_community,
        date: visit.event_date,
        discription: visit.event_discription,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});