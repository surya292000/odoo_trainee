/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PropertyRentalLease = publicWidget.Widget.extend({
    selector: "#wrap",
    events: {
        "change #start_date": "_onChangeDates",
        "change #end_date": "_onChangeDates",
        "click .add_total_project": "_onClickAddMaterial",
        "click .remove_line": "_onClickRemoveLine",
        "click .custom_create": "_onClickSubmit",
        "change select[name='property_id']": "onChangeProperty",
        "change .property_name": "_onClickRow",
        "change .select_rental_type": "_onClickCalculate",
        "click #dismiss": "_onCloseClick",
    },

    init() {
        this._super(...arguments);
        this.orm = this.bindService("orm");
    },


    _getModal() {
        return {
            modal: this.$el.find("#modal_msg")[0],
            title: this.$el.find(".modal-title")[0],
        };
    },

    _showModalMessage(msgText) {
        const { modal, title } = this._getModal();
        if (modal && title) {
            title.innerHTML = msgText;
            modal.style.display = "block";
        } else {
            alert(msgText);
        }
    },

    _hideModal() {
        const { modal } = this._getModal();
        if (modal) modal.style.display = "none";
    },

    _onChangeDates() {
        const startInput = this.$el.find("#start_date");
        const endInput = this.$el.find("#end_date");
        const startDate = new Date(startInput.val());
        const endDate = new Date(endInput.val());
        const $daysCount = this.$el.find("#days_count");

        if (startDate > endDate) {
            this._showModalMessage("Choose Date Correctly");
            startInput.val("");
            endInput.val("");
            this.$el.find(".total_days").val("");
            return;
        }

        if (startDate && endDate) {
            const diffDays =
                Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;

            this.$el
                .find("#material_table tbody tr.property_order_line")
                .each(function () {
                    $(this).find('input[name="total_days"]').val(diffDays);
                });

            if ($daysCount.length) {
                $daysCount.text("Total Days : " + diffDays);
            }
        }
    },

    _onCloseClick() {
        const msgTitle = this.$el.find(".modal-title").text();
        if (msgTitle === "Choose Date Correctly") {
            this.$el.find("#start_date, #end_date").val("");
        }
        this._hideModal();
    },

    _onClickAddMaterial() {
        const startDate = new Date(this.$el.find("#start_date").val());
        const endDate = new Date(this.$el.find("#end_date").val());
        const diffDays =
            Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;

        const $rows = this.$el.find("#material_table tbody tr.property_order_line");
        const $newRow = $rows.first().clone();

        $newRow.removeClass("d-none property_order_line").addClass("property_order_line");
        $newRow.find("input, select").val("");
        $newRow.find(".owner, .amount, .sub_amount").text("");

        let valid = true;
        $rows.each((_, elem) => {
            const propertyVal = $(elem).find('select[name="property_id"]').val();
            if (!propertyVal) {
                this._showModalMessage("Fill the previous row");
//                $(elem).remove();
                valid = false;
            }
        });

        if (valid) {
            $newRow.insertBefore($rows.eq(0));
            $newRow.find('input[name="total_days"]').val(diffDays);
        }
    },

    _onClickRemoveLine(ev) {
        const $rows = this.$el.find("#material_table tbody tr");
        if ($rows.length > 1) {
            $(ev.target).closest("tr").remove();
        } else {
            alert("You must have at least one material entry.");
        }
    },

    async _onClickCalculate() {
        const data = await rpc("/property-property", {});
        const fromDate = new Date(this.$el.find("#start_date").val());
        const toDate = new Date(this.$el.find("#end_date").val());
        const type = this.$el.find(".select_rental_type").val();
        const totalDays = (toDate - fromDate) / 86_400_000;

        this.$el.find("#material_table tbody tr").each(function () {
            const propertyId = $(this).find("#property_id").val();
            if (!propertyId) return;

            const spanOwner = $(this).find(".owner");
            const spanAmount = $(this).find(".amount");
            const spanSubAmount = $(this).find(".sub_amount");

            spanOwner.text(data[propertyId].owner);

            if (type === "Rent") {
                spanAmount.text(data[propertyId].rent);
                spanSubAmount.text(data[propertyId].rent * totalDays);
            } else {
                spanAmount.text(data[propertyId].lease);
                spanSubAmount.text(data[propertyId].lease * totalDays);
            }
        });
    },

    async _onClickRow(ev) {
        const $row = $(ev.target).closest("tr");
        const fromDate = new Date(this.$el.find("#start_date").val());
        const toDate = new Date(this.$el.find("#end_date").val());
        const totalDays = (toDate - fromDate) / 86_400_000;
        const type = this.$el.find(".select_rental_type").val();

        const data = await rpc("/property-property", {});
        const propertyId = $row.find("#property_id").val();
        if (!propertyId) return;

        $row.find(".owner").text(data[propertyId].owner);

        if (type === "rent") {
            $row.find(".amount").text(data[propertyId].rent);
            $row.find(".sub_amount").text(data[propertyId].rent * totalDays);
        } else {
            $row.find(".amount").text(data[propertyId].lease);
            $row.find(".sub_amount").text(data[propertyId].lease * totalDays);
        }
    },

    async _onClickSubmit(ev) {
        ev.preventDefault();
        const startDate = this.$el.find("#start_date").val();
        const endDate = this.$el.find("#end_date").val();
        const type = this.$el.find(".select_rental_type").val();

        if (!startDate || !endDate) {
            this._showModalMessage("Date not provided");
            return;
        }

        const propertyIds = [];
        const data = [];

        this.$el.find("#material_table tbody tr.property_order_line").each((_, elem) => {
            const $row = $(elem);
            if ($row.hasClass("d-none")) return;

            const propertyId = $row.find("select[name='property_id']").val();
            const rentalType = $row.find("select[name='rental_type']").val();

            if (!propertyId) {
                this._showModalMessage("Completely fill property details");
                $row.remove();
                return;
            }

            data.push({ property_id: propertyId });
            propertyIds.push({ property: propertyId });
        });

        if (propertyIds.length === 0) {
            this._showModalMessage("Property not selected");
            return;
        }

        try {
            const result = await rpc("/material/submit", {
                start: startDate,
                end: endDate,
                type,
                data,
            });

            if (result.status === "success") {
                window.location.href = "/customer/success?lease_id=" + result.lease_id;
            } else {
                alert(result.message || "Submission failed");
            }
        } catch (error) {
            alert("Submission failed: " + error.message);
        }
    },

    onChangeProperty(ev) {
        const $selected = $(ev.target);
        const selectedValue = $selected.val();
        this.$el.find("#material_table tbody tr.property_order_line").each((_, elem) => {
            const $row = $(elem);
            if ($row[0] === $selected.closest("tr")[0] || $row.hasClass("d-none")) return;

            if ($row.find("select[name='property_id']").val() === selectedValue) {
                this._showModalMessage("Property already chosen");
                $selected.val("");
                $selected.closest("tr").find(".owner, .amount, .sub_amount").text("");
            }
        });
    },
});