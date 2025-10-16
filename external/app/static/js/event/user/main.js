import { hadleButtons } from './btnHandler.js';
import { getUserVisits } from '../../common/callCommonApi.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    
    var responseData = await getUserVisits('../');
    const data = responseData.data.map(item => ({
        id: item.visit_id,
        name: item.event_name,
        discription: item.event_discription,
        date: item.date,
        community: item.community_name,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});