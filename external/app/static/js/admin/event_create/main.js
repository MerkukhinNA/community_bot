import { hadleButtons } from './btnHandler.js';
import { applyDateMask } from './dateMask.js';
import { getCommunityes } from '../../common/callCommonApi.js';
import { generateCommunityHTML } from '../../common/generateHTML.js';

document.addEventListener('DOMContentLoaded', async function() {
    hadleButtons()
    applyDateMask()

    var responseData = await getCommunityes('../../');
    const data = responseData.communityes.map(community => ({
        id: community.community_id,
        name: community.name,
        discription: community.discription,
        forSparkPark: community.for_spark_part,
        checked: true
    }));
    
    generateCommunityHTML(data, 'dynamic-container');
});