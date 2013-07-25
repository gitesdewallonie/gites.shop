jQuery(document).ready(function($) {

    var fields = ['first_line', 'second_line', 'city', 'country', 'postal_code'];

    $("#form\\.ship_same_billing").bind('click', function(e) {
        if ($(this).attr('checked')) {
            $("#mailing-address label").addClass("disabled");
            $.each(fields, function(idx, value) {
                billFieldName = "form\\.bill_" + value;
                shipFieldName = "form\\.ship_" + value;
                if ($("#" + billFieldName).val().length == 0) {
                    originalValue = $("#" + shipFieldName).val();
                    $("#" + billFieldName).val(originalValue);
                }
            });
        }
        else {
            $("#mailing-address label").removeClass("disabled");
        }
    });

    if ($("#form\\.ship_same_billing").prop('checked')) {
        $("#mailing-address label").addClass("disabled");
        $("#mailing-address input").attr("disabled", "disabled");
        $("#mailing-address select").attr("disabled", "disabled");
    }

});
