import { getUserEvents } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    
    var responseData = await getUserEvents('../');
    const data = responseData.events.map(event => ({
        id: event.event_id,
        name: event.name,
        community: event.community,
        date: event.date,
        discription: event.discription,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});
