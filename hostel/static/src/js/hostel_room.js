import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";
export function _chunk(array, size){
    const slice_result = [];
    for (let i=0; i< array.length; i +=size){
        slice_result.push(array.slice(i,i+size));
    }
    return slice_result;
}
export class HostelRoom extends Interaction {
    static selector = '.categories_section';

    async willStart(){
        this.result = await rpc('/hostel_room/get_room_data',{})
    }
    start(){
        if (this.result){
            const chunkData = _chunk(this.result['room_data'],4)
            chunkData[0].is_active = true
            $(this.el).empty().html(renderToElement('hostel.category_hostel_room_data', { chunkData}))
        }
    }

}

registry.category("public.interactions").add("hostel.hostel_room.js", HostelRoom)

