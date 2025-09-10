/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';
publicWidget.registry.MaterialRequest = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'change .operation': '_onChangeType',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
//       'click .custom_create': '_onClickSubmit',
   },
//   _onClickSubmit: async function (ev) {
//       ev.preventDefault();
//       var employee_id = $('#customer').val();
//       var date = $('#date').val();
//       var material_order_ids = [];
//       $('#material_table tbody tr.material_order_line').each(function () {
//           let product = $(this).find('select[name="product"]').val();
//           let quantity = $(this).find('input[name="quantity"]').val();
//           let operation = $(this).find('select[name="operation"]').val();
//           let source = $(this).find('select[name="source"]').val();
//           let destination = $(this).find('select[name="destination"]').val();
//           material_order_ids.push({
//               'material': product,
//               'quantity': quantity,
//               'operation_id': operation,
//               'source': source || null,
//               'destination': destination || null
//           });
//       });
//       // Log data before sending
//       console.log({
//           'employee_id': employee_id,
//           'date': date,
//           'material_order_ids': material_order_ids
//       });
//       try {
//           let response = await rpc('/material/submit', {
//               employee_id: employee_id,
//               date: date,
//               material_order_ids: material_order_ids
//           });
//           console.log('Response:', response);
//           alert('Material request submitted successfully!');
//       } catch (error) {
//           console.error('Error:', error);
//           alert('Failed to submit the material request.');
//       }
//},

   _onClickAddMaterial: function (ev) {
       var $new_row = $('#material_table tbody tr.property_order_line:first').clone();
       $new_row.find('input, select').val('');  // Clear input values
       $new_row.appendTo('#material_table tbody');
   },
   _onClickRemoveLine: function (ev) {
       if ($('#material_table tbody tr').length > 1) {
           $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },
   _onChangeType: function (ev) {
       var $row = $(ev.target).closest('tr');
       if ($row.find('.operation').val() === "purchase order") {
           $row.find('.fields').prop('disabled', true);
       } else {
           $row.find('.fields').prop('disabled', false);
       }
   }
});
