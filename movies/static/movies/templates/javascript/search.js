$(document).ready(function() {

    window.timestagger = 1000;
    window.timeref = Date.now();
    window.searchtext = $("#searchbox").val();

    function onsuccess(res) {
        $("#txtTopSearchHint").html(res);
        $(".ajaxaddmovie").click(function () {
            var selectedmovie = $(this).html();
            var linkto = $(this).attr("id");
            var cs = $("#current_selection");
            var current_selection_html = cs.html();
            var newelement = current_selection_html + window.sim_template.format({'linkto':linkto, 'selectedmovie':selectedmovie});
            cs.html(newelement);
            $(this).hide();
        });
    }

    //     Do ajax search and run the onsuccess() function
    function dosearch() {
        window.searchtext = $("#searchbox").val();
        $.ajax({
            url: "/mainsearch/?searchtext=" + window.searchtext,
            success: function (result) {
                onsuccess(result);
            }
        });
    }

    //  Interval function to stagger search
    var intervalID = setInterval(function () {
        if (window.searchtext != $("#searchbox").val()) {
            dosearch();
            window.timeref = Date.now();
        }
    }, window.timestagger);

    $(document).on("keyup", "#searchbox", function () {
        if (Date.now() > (window.timeref + window.timestagger)) {
            window.timeref = Date.now();
            dosearch();
        }
    });

});