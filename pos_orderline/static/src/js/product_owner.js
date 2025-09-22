/** @odoo-module **/
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup() {
        super.setup(...arguments);
        this.product_owner_id = this.product_id.product_owner_id?.name || false;
    },

    getDisplayData() {
        const data = super.getDisplayData(...arguments);
        data.product_owner_id = this.product_owner_id || "";
        return data;
    },
});
