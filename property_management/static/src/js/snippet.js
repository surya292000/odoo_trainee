/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}
publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector : '.categories_section',
    async willStart() {
        const result = await rpc('/get_product_categories', {});
        if(result){
            this.$target.empty().html(renderToElement('property_management.category_data', {result: result}))
        }
    },
//    start: function () {
//            const refEl = this.$el.find("#top_products_carousel")
//            const { products, categories, current_website_id, products_list} = this
//            const chunkData = chunk(property, 4)
//            refEl.html(renderToElement(property_management.category_data', {
//                products,
////                categories,
////                current_website_id,
////                products_list,
//                chunkData
//            }))
//        }
//    });
});
