/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PosStore.prototype, {
    async pay() {
        const currentOrder = this.get_order();
        for (const line of currentOrder.get_orderlines()) {
            const product = line.get_product();
            const category = product.pos_categ_id; // single category of the product
            if (category && category.maximum_discount && category.maximum_discount > 0) {
                const discount = line.get_discount();
                if (discount > category.maximum_discount) {
                    await this.dialog.add(AlertDialog, {
                        title: _t("Discount Limit Exceeded"),
//                        body: _t(
//                            The discount on product "${product.display_name}" cannot exceed ${category.maximum_discount}%
//                        ),
                    });
                    return false;
                }
            }
        }
        return super.pay();
    }
});

