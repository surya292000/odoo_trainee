/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";


patch(PosStore.prototype, {
     async pay() {
          if (this.config.pos_category_discount_enable){
              const currentOrder = this.get_order();
              for (const category of this.config.pos_categories_discount_ids){
                    let totalCategoryDiscount = 0;
                    for (const line of currentOrder.get_orderlines()) {
                        const product = line.get_product();
                        const product_categ_ids = product.pos_categ_ids.map(categ => categ.id)
                        if (product_categ_ids.includes(parseInt(category.category_id.id))){
                            const discount = line.get_discount();
                            totalCategoryDiscount += discount;
                        }
                    }
                    if(totalCategoryDiscount > category.pos_category_discount && category.pos_category_discount > 0){
                        this.dialog.add(AlertDialog, {
                           body: _t(`Not except discount, because allowed discount is ${category.pos_category_discount}%`),
                        });
                        return false;
                    }
              }

          }
          return super.pay();
    }
});
