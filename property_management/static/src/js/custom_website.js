/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from '@web/core/network/rpc';
console.log("tfd")
publicWidget.registry.PropertyRentalLease = publicWidget.Widget.extend({
   selector: "#wrap",
   events: {
       'change .operation': '_onChangeType',
       'change #start_date': '_onChangeDates',
       'change #end_date': '_onChangeDates',
       'click .add_total_project': '_onClickAddMaterial',
       'click .remove_line': '_onClickRemoveLine',
       'click .custom_create': '_onClickSubmit',

   },
   _onClickSubmit: async function (ev) {
    console.log('submit');
    console.log('sdfghjkl')
    ev.preventDefault();
    const property_ids = [];
    $('#material_table tbody tr.property_order_line').each(function () {
        const property_id = $(this).find('select[name="property_id"]').val();
        const quantityStr = $(this).find('input[name="total_days"]').val();
        const quantity = parseInt(quantityStr, 10) || 0;
        const rental_type = $(this).find('select[name="rental_type"]').val();
        property_ids.push({
            property: property_id,
            quantity: quantity,
            rental_type: rental_type,
        });
    });
    try {
         let result = await this.rpc("/material/submit", {
//            'rental_type': rental_type,
            'start_date': start_date,
            'end_date': end_date,
            'property_ids': property_ids
            // add other form fields here if needed
        });
        console.log(result, 'rpc result');

        if (result.success) {
            alert("Request submitted! ID: " + result.record_id);
        } else {
            alert("Submission failed");
        }
    } catch (error) {
        alert("Submission failed: " + error.message);
    }
},


   _onClickAddMaterial: function (ev) {
       console.log("gyduy")
       var $new_row = $('#material_table tbody tr.property_order_line:first').clone();
       $new_row.find('input, select').val('');  // Clear input values
       $new_row.appendTo('#material_table tbody');
//       console.log('console')
   },
   _onClickRemoveLine: function (ev) {
       console.log('dfghjkjb')
       if ($('#material_table tbody tr').length > 1) {
           $(ev.target).closest('tr').remove();
       } else {
           alert("You must have at least one material entry.");
       }
   },

   _onChangeDates: function () {
       console.log('date')
    const s = $('#start_date').val();
    const e = $('#end_date').val();
    if (!s || !e) {
        $('.total_days').val('');
        return;
    }
    const start = new Date(s);
    const end = new Date(e);
    if (end < start) {
        alert("End Date must be after Start Date.");
        $('.total_days').val('');
        return;
    }
    // difference in days (inclusive)
    const diffMs = end.getTime() - start.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1;
    // fill ALL rows with the computed days
    $('#material_table tbody tr.property_order_line').each(function () {
        $(this).find('input[name="total_days"]').val(diffDays);
//        this.$el.find()
        console.log("Dates changed", s, e, diffDays);
    });
  },

//    _onChangeDates: function (ev) {
//        // read global dates
//        const s = $('#start_date').val();
//        const e = $('#end_date').val();
//
//        // if either missing, clear values
//        if (!s || !e) {
//            $('input[name="total_days"]').val('');
//            $('#quantity_global').val('');
//            return;
//        }
//
//        // parse dates
//        const start = new Date(s);
//        const end = new Date(e);
//
//        // compute milliseconds difference (end - start)
//        const diffMs = end.getTime() - start.getTime();
//
//        if (diffMs < 0) {
//            alert("End Date must be the same or after Start Date.");
//            $('input[name="total_days"]').val('');
//            $('#quantity_global').val('');
//            return;
//        }
//
//        const msPerDay = 1000 * 60 * 60 * 24; // 86,400,000 ms
//        const diffDays = Math.floor(diffMs / msPerDay) + 1;
//
//        // set every row's total_days input
//        $('#material_table tbody tr.property_order_line').each(function () {
//            $(this).find('input[name="total_days"]').val(diffDays);
//        });
//
//        // set global quantity input (if you have one)
//        $('#quantity_global').val(diffDays);
//        },

//        },


//   _onChangeType: function (ev) {
//       var $row = $(ev.target).closest('tr');
//       if ('start_date' && 'end_date'){
//       console.log('sdfghj')
//       }
////       $row.find()
////       } else {
////           $row.find('.fields').prop('disabled', false);
////       }
//   }

////   _onChangeType: function (ev) {
////       var $row = $(ev.target).closest('tr');
////       if ($row.find('.operation').val() === "purchase order") {
////           $row.find('.fields').prop('disabled', true);
////       } else {
////           $row.find('.fields').prop('disabled', false);
////       }
////   }
});
