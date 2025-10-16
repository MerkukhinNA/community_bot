import { getUserVisits } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    
    var responseData = await getUserVisits('../');
    const data = responseData.data.map(data => ({
        id: data.visit_id,
        name: data.event_name,
        community: data.event_community,
        date: data.event_date,
        discription: data.event_discription,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});