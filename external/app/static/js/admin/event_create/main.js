import { hadleButtons } from './btnHandler.js';
import { applyDateMask } from './dateMask.js';
import { getCommunityes } from '../../common/callCommonApi.js';
import { generateCommunityHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    applyDateMask()

    var responseData = await getCommunityes('../../');
    const data = responseData.data.map(item => ({
        id: item.community_id,
        name: item.name,
        discription: item.discription,
        forSparkPark: item.for_spark_part,
        checked: true
    }));
    
    generateCommunityHTML(data, 'dynamic-container');
});