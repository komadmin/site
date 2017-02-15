document.addEventListener("DOMContentLoaded", function() {
    $(document).on("click", ".setting_button", function () {
        console.log("working");
        var buttontype = $(this).data('type');
        var buttonvalue = $(this).data('value');
        $.ajax({
            url: "/settingbutton/",
            method: "POST",
            data: {
                type: buttontype,
                value: buttonvalue
            },
            success: function (result) {
                // $('this').html(result);
                location.reload();
                console.log("Button: " + buttontype + " = " + buttonvalue);
            }
        });
    });
});