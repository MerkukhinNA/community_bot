import { hadleButtons } from './btnHandler.js';
import { getEvents } from '../../common/callCommonApi.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()

    var responseData = await getEvents('../../');
    const data = responseData.events.map(visit => ({
        id: visit.visit_id,
        name: visit.name,
        community: visit.community,
        date: visit.date,
        discription: visit.discription,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});