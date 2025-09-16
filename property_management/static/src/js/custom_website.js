/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";
import { renderToElement } from "@web/core/utils/render";
import { useRef, useState } from "@odoo/owl";

//console.log("tfd")

publicWidget.registry.PropertyRentalLease = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'change #start_date': '_onChangeDates',
       'change #end_date': '_onChangeDates',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
       'click .custom_create': '_onClickSubmit',
       'change select[name="property_id"]': 'onChangeProperty',
       'change .property_name': '_onClickRow',
       'change .select_rental_type': '_onClickCalculate',
       'click #dismiss': '_onCloseClick',
   },

   init() {
       this._super(...arguments);
       this.orm = this.bindService("orm");
   },

   setup() {
       super.setup();
       this.location = useService("message");
   },

   _onChangeDates: function() {
       var modal_div = this.el.querySelector('#modal_msg');
       var msg = this.el.querySelector('.modal-title');
       var start_date = new Date($('#start_date').val())
       var end_date = new Date($('#end_date').val())
       var total_days = this.$el.find('#days_count');

       if (start_date > end_date) {
           if (modal_div && msg) {
               msg.innerHTML = "Choose Date Correctly"
               modal_div.style.display = 'block';
           } else {
               alert("End Date must be after Start Date.");
           }
           $('#end_date').val("");
           $('#start_date').val("");
           $('.total_days').val('');
           return;
       }
       else if (start_date && end_date) {
           const diffMs = end_date.getTime() - start_date.getTime();
           const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;

           $('#material_table tbody tr.property_order_line').each(function () {
               $(this).find('input[name="total_days"]').val(diffDays);
           });

           if (total_days.length) {
               total_days.text('Total Days : ' + diffDays);
           }
           console.log("Dates changed", $('#start_date').val(), $('#end_date').val(), diffDays);
       }
   },

   _onCloseClick: function() {
       var modal_div = this.el.querySelector('#modal_msg');
       var msg = this.el.querySelector('.modal-title');
       var start_date = $('#start_date')
       var end_date = $('#end_date')

       if (msg && msg.textContent == "Choose Date Correctly") {
           end_date.val("")
           start_date.val("")
           if (modal_div) modal_div.style.display = 'none';
       }
       else {
           if (modal_div) modal_div.style.display = 'none';
       }
   },

   _onClickAddMaterial: function (ev) {
       var modal_div = this.el.querySelector('#modal_msg');
       var msg = this.el.querySelector('.modal-title');
       var rows = $('#material_table tbody tr.property_order_line');
       var $new_row = $('#material_table tbody tr.property_order_line:first').clone();
       var start_date = new Date($('#start_date').val())
       var end_date = new Date($('#end_date').val())
       var total_days = this.$el.find('#days_count');
       const diffMs = end_date.getTime() - start_date.getTime();
       const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;

       $new_row.removeClass('d-none')
       $new_row.removeClass('property_order_line');
       $new_row.addClass('property_order_line');
       $new_row.find('select[name="property_id"]').val("")
       $new_row.find('input, select').val('');  // Clear input values

       rows.each(function(index, elem){

           if($(elem).find('select[name="property_id"]').val() == null || $(elem).find('select[name="property_id"]').val() == ""){
               if (modal_div && msg) {
                   msg.innerHTML = "Fill the previous row";
                   modal_div.style.display = 'block';
               } else {
                   alert("Fill the previous row");
               }
               elem.remove();
           }
           else{
               $new_row.insertBefore(rows.eq(0));
               $new_row.insertBefore(rows.eq(0)).find('input[name="total_days"]').val(diffDays);
               $new_row.insertBefore(rows.eq(0)).find('.owner').text(" ");
               $new_row.insertBefore(rows.eq(0)).find('.amount').text(" ");
               $new_row.insertBefore(rows.eq(0)).find('.sub_amount').text(" ");
               console.log($new_row.insertBefore(rows.eq(0)),'hhhhhhhhhhhhhhhhhhhhh')

           }
       });
   },

   _onClickRemoveLine: function (ev) {
        if ($('#material_table tbody tr').length > 1) {
           $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },

   _onClickCalculate :  async function () {
           const data = await rpc('/property-property', {})
            var $table = this.$el.find('#material_table tbody tr')
            var from_date = new Date(this.$el.find('#start_date').val())
            var to_date = new Date(this.$el.find('#end_date').val())
            var type = this.$el.find('.select_rental_type').val();
            var total_days = (to_date - from_date) / 86_400_000;
            $table.each(function(index, elem){
                var property = $(elem).find('#property_id').val()
                var span_owner = $(elem).find('.owner');
                var span_amount = $(elem).find('.amount');
                var span_sub_amount = $(elem).find('.sub_amount')
                if (property){
                console.log('hai')
                    span_owner.text(data[property].owner);
                    if(type=='Rent'){
                        span_amount.text(data[property].rent);
                        span_sub_amount.text(data[property].rent * total_days);
                         }
                    else{
                        span_amount.text(data[property].lease)
                        span_sub_amount.text(data[property].lease * total_days)}
                }
            })
           },

   _onClickRow : async function(ev){
           var current_row = $(ev.target)
           console.log(current_row,'current ')
           var from_date = new Date(this.$el.find('#start_date').val())
           var to_date = new Date(this.$el.find('#end_date').val())
           var total_days = (to_date - from_date) / 86_400_000;
           var type = this.$el.find('.select_rental_type').val();
           const data = await rpc('/property-property', {})
           console.log(data, 'data')
           var property = current_row.closest('tr').find('#property_id').val()
                var span_owner = current_row.closest('tr').find('.owner');
                var span_amount = current_row.closest('tr').find('.amount');
                var span_sub_amount = current_row.closest('tr').find('.sub_amount');
                if (property){
                    span_owner.text(data[property].owner);
                    if(type=='rent'){
                        span_amount.text(data[property].rent);
                        span_sub_amount.text(data[property].rent * total_days)
                         }
                        else{
                             span_amount.text(data[property].lease)
                             span_sub_amount.text(data[property].lease * total_days)}
                }
           },
   _onClickSubmit: async function (ev) {
       ev.preventDefault();
       var modal_div = this.el.querySelector('#modal_msg');
       var msg = this.el.querySelector('.modal-title');
       var start_date = $('#start_date').val();
       var end_date = $('#end_date').val();
       var type =  this.$el.find('.select_rental_type').val();
       const property_ids = [];
       let data =[];
       if(start_date.length==0 || end_date.length==0){
           if (modal_div && msg) {
               msg.innerHTML = "Date not provided";
               modal_div.style.display = 'block';
           } else {
               alert("Date not provided");
           }
           ev.preventDefault();
           ev.stopPropagation();
           return;
       }
       $('#material_table tbody tr.property_order_line').each(function () {
           if(!$(this)[0].classList.contains('d-none')){
               let row = $(this);
               const property_id = row.find('select[name="property_id"]').val();
               console.log('property_id',property_id)
               const quantityStr = row.find('input[name="total_days"]').val();
               const quantity = parseInt(quantityStr, 10) || 0;
               const rental_type = row.find('select[name="rental_type"]').val();
               console.log(rental_type,'rentalllllllllllllllll')

               data.push({
               property_id: property_id,
               })
               console.log('data',data)

               if (property_id == null || property_id == ""){
               console.log('propppppp')
                   if (modal_div && msg) {
                       msg.innerHTML = "Completely fill property details"
                       modal_div.style.display = 'block';
                   } else {
                       alert("Completely fill property details");
                   }
                   row.remove();
                   ev.preventDefault();
               }
               else{
                   property_ids.push({
                       property: property_id,
//                       quantity: quantity,
                   });
               }
           }
       });
       console.log('neyhdbedbu',property_ids)
       if(property_ids.length == 0){
           if (modal_div && msg) {
               msg.innerHTML = "Property not selected"
               modal_div.style.display = 'block';
           } else {
               alert("Property not selected");
           }
           ev.preventDefault();
           return;
       }

       try {
            let result = await rpc("/material/submit", {
                start: start_date,
                end: end_date,
                type: type,
                data: data,
            });
            console.log(result, 'rpc result');

            if (result.status === "success") {
                window.location.href = "/customer/success?lease_id";
            } else {
                alert(result.message || "Submission failed");
            }
        } catch (error) {
            alert("Submission failed: " + error.message);
        }

   },

   onChangeProperty: async function(ev) {
       var modal_div = this.el.querySelector('#modal_msg');
       var msg = this.el.querySelector('.modal-title');
       var selected_value = $(ev.target);
       var $table = $('#material_table tbody tr.property_order_line')

       $table.each(function(index, elem){
           if(elem !== selected_value.closest('tr')[0] && (!elem.classList.contains('d-none'))){
               if($(elem).find('select[name="property_id"]').val() == selected_value.val()){
                   if (modal_div && msg) {
                       msg.innerHTML = "Property already chosen"
                       modal_div.style.display = 'block';
                   } else {
                       alert("Property already chosen");
                   }
                   selected_value.val("")
                   selected_value.closest('tr').find('.owner').text("")
                   selected_value.closest('tr').find('.amount').text("")
                   selected_value.closest('tr').find('.sub_amount').text("")
               }
           }
       });
   },
});