/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
    const order = this.get_order()
    const order_lines = order.lines
    const categDiscount = {}
    console.log(order_lines,'order lines')


    for (const line of order_lines) {
         if (line.discount){
         const price = line.price_unit * line.qty;
         const discountPercent = line.discount;
         const discountAmount = price * (discountPercent/ 100);
         if (line.product_id.pos_categ_ids && line.product_id.pos_categ_ids.length > 0) {
            const category = line.product_id.pos_categ_ids[0];
            const categoryName = category.name
            const discountLimit = category.discount_limit

             if (categDiscount[categoryName]) {
                categDiscount[categoryName] += discountAmount;
            } else {
                categDiscount[categoryName] = discountAmount;
            }

             if (categDiscount[categoryName] > discountLimit) {
                    console.log("ALERT:", categoryName, "discount exceeded!");
                       await this.dialog.add(AlertDialog, {
                        title: _t("Discount Limit Exceeded"),
                        body: _t(
                            "The discount on product cannot exceed discount limit set inside category"
                        ),
                    });
                    return false;
                }

        }
         }
}
console.log(categDiscount,'DiscountMap')

        return super.pay();
    }
});
