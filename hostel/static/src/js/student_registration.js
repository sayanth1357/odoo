import {Interaction} from "@web/public/interaction";
import {registry} from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";


export class StudentRegistration extends Interaction {
    static selector = ".student_registration_form";
    dynamicContent = {
        "#rooms": {"t-on-change": this.onChangeRoom},
        "#autofill_info": {"t-on-change": this.autofillData},
    };
    async onChangeRoom() {
        this.room_data  = await rpc("/rpc/room_data", { room_id: this.el.querySelector("select[name='rooms']").value });
        const form = document.querySelector('form.student_registration_form');
        form.querySelector("div[class='room_details']").hidden = 0;
        form.querySelector("input[name='room_type']").value = this.room_data.room_type;
        if (this.room_data.facilities.length != 0){
             form.querySelector("div[class='room_facilities']").hidden = 0;
             form.querySelector("input[name='facilities']").value = this.room_data.facilities;
        }
        else{
             form.querySelector("div[class='room_facilities']").hidden = 1;
        }
        form.querySelector("input[name='rent']").value = this.room_data.rent;
        form.querySelector("input[name='total_rent']").value = this.room_data.total_rent;
        }

    async autofillData() {

        if(this.el.querySelector("input[name='autofill_info']").checked == true){
            this.room_data  = await rpc("/rpc/autofill_info", { uid: this.services.website_page.context.uid });
            this.el.querySelector("input[name='name']").value = this.room_data.name;
            this.el.querySelector("input[name='email']").value = this.room_data.email;
        }
        else{
            this.el.querySelector("input[name='name']").value = "";
            this.el.querySelector("input[name='email']").value = "";
        }

    }
    }

registry.category("public.interactions").add("hostel.student_registration.js", StudentRegistration);