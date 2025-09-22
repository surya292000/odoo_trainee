/** @odoo-module **/
import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";

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

   _onChangeDates: function() {
       const modal_div = this.el.querySelector('#modal_msg');
       const msg = this.el.querySelector('.modal-title');
       const startInput = this.el.querySelector('#start_date');
       const endInput = this.el.querySelector('#end_date');
       const start_date = new Date(startInput?.value || "");
       const end_date = new Date(endInput?.value || "");
       const total_days = this.el.querySelector('#days_count');

       if (start_date > end_date) {
           if (modal_div && msg) {
               msg.innerHTML = "Choose Date Correctly";
               modal_div.style.display = 'block';
           } else {
               alert("End Date must be after Start Date.");
           }
           if (endInput) endInput.value = "";
           if (startInput) startInput.value = "";
           Array.from(this.el.querySelectorAll('.total_days')).forEach(el => el.value = '');
           return;
       }
       else if (start_date && end_date) {
           const diffMs = end_date.getTime() - start_date.getTime();
           const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;

           Array.from(this.el.querySelectorAll('#material_table tbody tr.property_order_line')).forEach(function (row) {
               const td = row.querySelector('input[name="total_days"]');
               if (td) td.value = diffDays;
           });

           if (total_days) {
               total_days.textContent = 'Total Days : ' + diffDays;
           }
           console.log("Dates changed", startInput?.value, endInput?.value, diffDays);
       }
   },

   _onCloseClick: function() {
       const modal_div = this.el.querySelector('#modal_msg');
       const msg = this.el.querySelector('.modal-title');
       const startInput = this.el.querySelector('#start_date');
       const endInput = this.el.querySelector('#end_date');

       if (msg && msg.textContent == "Choose Date Correctly") {
           if (endInput) endInput.value = "";
           if (startInput) startInput.value = "";
           if (modal_div) modal_div.style.display = 'none';
       }
       else {
           if (modal_div) modal_div.style.display = 'none';
       }
   },

   _onClickAddMaterial: function (ev) {
       const modal_div = this.el.querySelector('#modal_msg');
       const msg = this.el.querySelector('.modal-title');
       const rows = Array.from(this.el.querySelectorAll('#material_table tbody tr.property_order_line'));
       const firstRow = this.el.querySelector('#material_table tbody tr.property_order_line');
       if (!firstRow) return;
       const new_row = firstRow.cloneNode(true);

       const startInput = this.el.querySelector('#start_date');
       const endInput = this.el.querySelector('#end_date');
       const start_date = new Date(startInput?.value || "");
       const end_date = new Date(endInput?.value || "");
       const total_days_elem = this.el.querySelector('#days_count');
       const diffMs = end_date.getTime() - start_date.getTime();
       const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;

       new_row.classList.remove('d-none');
       new_row.classList.remove('property_order_line');
       new_row.classList.add('property_order_line');
       Array.from(new_row.querySelectorAll('input, select')).forEach(el => {
           if (el.tagName === 'INPUT') el.value = '';
           else if (el.tagName === 'SELECT') el.selectedIndex = 0;
       });

       let shouldInsert = true;
       rows.forEach(elem => {
           const sel = elem.querySelector('select[name="property_id"]');
           const val = sel ? (sel.value || "") : "";
           if (val === null || val === "") {
               shouldInsert = false;
           }
       });

       if (!shouldInsert) {
           if (modal_div && msg) {
               msg.innerHTML = "Fill the previous row";
               modal_div.style.display = 'block';
           } else {
               alert("Fill the previous row");
           }
           return;
       }
       firstRow.parentNode.insertBefore(new_row, firstRow);
       const td_input = new_row.querySelector('input[name="total_days"]');
       if (td_input) td_input.value = diffDays;
       const ownerEl = new_row.querySelector('.owner'); if (ownerEl) ownerEl.textContent = " ";
       const amountEl = new_row.querySelector('.amount'); if (amountEl) amountEl.textContent = " ";
       const subAmountEl = new_row.querySelector('.sub_amount'); if (subAmountEl) subAmountEl.textContent = " ";
   },

   _onClickRemoveLine: function (ev) {
       const rows = this.el.querySelectorAll('#material_table tbody tr');
       if (rows.length > 1) {
           const tr = ev.target.closest('tr');
           if (tr) tr.remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },

   _onClickCalculate :  async function () {
       const data = await rpc('/property-property', {});
       const rows = Array.from(this.el.querySelectorAll('#material_table tbody tr'));
       const from_date = new Date(this.el.querySelector('#start_date')?.value || "");
       const to_date = new Date(this.el.querySelector('#end_date')?.value || "");
       const type = this.el.querySelector('.select_rental_type')?.value || "";
       const total_days = (to_date - from_date) / 86400000;

       rows.forEach(elem => {
           const property = elem.querySelector('#property_id')?.value || "";
           const span_owner = elem.querySelector('.owner');
           const span_amount = elem.querySelector('.amount');
           const span_sub_amount = elem.querySelector('.sub_amount');
           if (property && data[property]) {
               if (span_owner) span_owner.textContent = data[property].owner;
               if (type === 'Rent') {
                   if (span_amount) span_amount.textContent = data[property].rent;
                   if (span_sub_amount) span_sub_amount.textContent = data[property].rent * total_days;
               }
               else {
                   if (span_amount) span_amount.textContent = data[property].lease;
                   if (span_sub_amount) span_sub_amount.textContent = data[property].lease * total_days;
               }
           }
       });
   },

   _onClickRow : async function(ev){
       const current_row = ev.target.closest('tr');
       if (!current_row) return;
       const from_date = new Date(this.el.querySelector('#start_date')?.value || "");
       const to_date = new Date(this.el.querySelector('#end_date')?.value || "");
       const total_days = (to_date - from_date) / 86400000;
       const type = this.el.querySelector('.select_rental_type')?.value || "";
       const data = await rpc('/property-property', {});
       const property = current_row.querySelector('#property_id')?.value || "";
       const span_owner = current_row.querySelector('.owner');
       const span_amount = current_row.querySelector('.amount');
       const span_sub_amount = current_row.querySelector('.sub_amount');
       if (property && data[property]) {
           if (span_owner) span_owner.textContent = data[property].owner;
           if (type === 'rent') {
               if (span_amount) span_amount.textContent = data[property].rent;
               if (span_sub_amount) span_sub_amount.textContent = data[property].rent * total_days;
           }
           else {
               if (span_amount) span_amount.textContent = data[property].lease;
               if (span_sub_amount) span_sub_amount.textContent = data[property].lease * total_days;
           }
       }
   },

   _onClickSubmit: async function (ev) {
       ev.preventDefault();
       const modal_div = this.el.querySelector('#modal_msg');
       const msg = this.el.querySelector('.modal-title');
       const start_date = this.el.querySelector('#start_date')?.value || "";
       const end_date = this.el.querySelector('#end_date')?.value || "";
       const type = this.el.querySelector('.select_rental_type')?.value || "";
       const property_ids = [];
       let data = [];

       if (!start_date || !end_date) {
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

       Array.from(this.el.querySelectorAll('#material_table tbody tr.property_order_line')).forEach(row => {
           if (!row.classList.contains('d-none')) {
               const property_id = row.querySelector('select[name="property_id"]')?.value || "";
               const quantityStr = row.querySelector('input[name="total_days"]')?.value || "0";
               const quantity = parseInt(quantityStr, 10) || 0;
               const rental_type = row.querySelector('select[name="rental_type"]')?.value || "";

               data.push({
                   property_id: property_id,
               });

               if (!property_id) {
                   if (modal_div && msg) {
                       msg.innerHTML = "Completely fill property details";
                       modal_div.style.display = 'block';
                   } else {
                       alert("Completely fill property details");
                   }
                   row.remove();
                   ev.preventDefault();
               } else {
                   property_ids.push({ property: property_id });
               }
           }
       });

       if (property_ids.length == 0) {
           if (modal_div && msg) {
               msg.innerHTML = "Property not selected";
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
       const modal_div = this.el.querySelector('#modal_msg');
       const msg = this.el.querySelector('.modal-title');
       const selected_value = ev.target;
       const rows = Array.from(this.el.querySelectorAll('#material_table tbody tr.property_order_line'));

       rows.forEach(elem => {
           if (elem !== selected_value.closest('tr') && (!elem.classList.contains('d-none'))) {
               const otherVal = elem.querySelector('select[name="property_id"]')?.value || "";
               if (otherVal == selected_value.value) {
                   if (modal_div && msg) {
                       msg.innerHTML = "Property already chosen";
                       modal_div.style.display = 'block';
                   } else {
                       alert("Property already chosen");
                   }
                   selected_value.value = "";
                   const chRow = selected_value.closest('tr');
                   if (chRow) {
                       const own = chRow.querySelector('.owner'); if (own) own.textContent = "";
                       const amo = chRow.querySelector('.amount'); if (amo) amo.textContent = "";
                       const sub_amo = chRow.querySelector('.sub_amount'); if (sub_amo) sub_amo.textContent = "";
                   }
               }
           }
       });
   },
});
