import { hadleButtons } from './btnHandler.js';
import { getEvents } from '../../common/callCommonApi.js';
import { generateEventsHTML } from '../../common/generateHTML.js';
import { getUserVisits } from '../../common/callCommonApi.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()

    var responseData = await getEvents('../../');
    const data = responseData.data.map(item => ({
        id: item.event_id,
        name: item.name,
        discription: item.discription,
        date: item.date,
        community: item.community,
        checked: true
    }));
    
    generateEventsHTML(data, 'dynamic-container');
});