import { getUserEvents } from '../../common/callCommonApi.js';
import { hadleButtons } from './btnHandler.js';
import { generateEventsHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    
    var responseData = await getUserEvents('../');
    const data = responseData.data.map(data => ({
        id: data.event_id,
        name: data.name,
        community: data.community,
        date: data.date,
        discription: data.discription,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});
