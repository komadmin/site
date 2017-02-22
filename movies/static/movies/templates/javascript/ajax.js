$(document).ready(function() {
console.log("ajax.js loaded");
//     Set global variables.
    window.timestagger = 1000;
    window.timeref = Date.now();
    window.searchtext = $("#searchbox").val();
    window.sim_template = $("#sim_template").html();

//     String format function
    if (!String.prototype.format) {
        String.prototype.format = function() {
            var str = this.toString();
            if (!arguments.length)
                return str;
            var args = typeof arguments[0],
                args = (("string" == args || "number" == args) ? arguments : arguments[0]);
            for (var arg in args)
                str = str.replace(RegExp("\\{" + arg + "\\}", "gi"), args[arg]);
            return str;
        }
    }

//     Could alternatively load this from a template file
//     console.log(window.sim_template);

    $(document).on("click", ".submit_button", function () {
        thisbutton = $(this);
        linkto = thisbutton.siblings(".addcomment").attr("id");
        $.ajax({
            url: "{% url 'movies:addsimilar_ajax' %}",
            method: "POST",
            data: {
                linkfrom: linkfrom,
                linkto: linkto,
                reason: $(this).siblings(".sim_comment").val()
            },
            success: function (result) {
                $("#simlist ul").html(result);
                thisbutton.parent().html("Your suggestion has been sent"); // need to replace with "Your suggestion has been saved".
                console.log("Suggestion sent successfully");
            },
            error: function (result) {
                console.log(result)
                }
        });
    });


    $(document).on("click", ".simlist_voteup", function() {
        var simid = $(this).data("simid");
        console.log("simid " + simid);
        $.ajax({
            url: "/votesimilar/",
            method: "GET",
            data: {
                simid: simid,
                vote: "1"
            },
            success: function (result) {
                $("#" + simid + " .simlist_nvotes").html(result);
            },
            error: function (result) {
                console.log(result)
                var win=window.open("/votesimilar/?vote=1&simid=" + simid);
            }
        });
    });


    function isEmpty(str) {
        return (!str || 0 === str.length);
    }

    function framereplace(ytid, movid) {
        framecode = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{{ytid}}" frameborder="0" allowfullscreen></iframe>';
        rendered = Mustache.render(framecode, {ytid: ytid});
        popup = $('#popup' + movid);
        popup.popup({
            opacity: 0.3,
            transition: 'all 0.3s'
        });
        popup.popup('show');
        popup.html(rendered);
    }

    $(document).on("click", ".movlist_youtubebutton", function() {
        console.log("Youtube Button Clicked");
        var ytid = $(this).data('ytid');
        var movid = $(this).data('movid');

        if (isEmpty(ytid)) {
            $.ajax({
                url: "/gettrailer/",
                method: "GET",
                data: {movid: movid},
                dataType: "json",
                success: function (result) {
                    console.log(result);
                    ytid = result.ytid;
                }
            }).then(framereplace(ytid, movid)); // needs to happen after
        } else {
            framereplace(ytid, movid);
        }
    });

    state = "down";
    $(document).on("click", ".simlist_watched", function() {
        butid = $(this).data("buttonid");
        pos = $(this).position();
        popup = $("[data-linkto*=" + butid + "]");
        popup.css({position: 'absolute', bottom: pos.top + 40, left: pos.left - 125});
        if (state == 'down') {
            popup.show();
            popup.animate({height: 125},100);
            state = "up";
        } else {
            popup.animate({height: 0},100);
            state = "down";
        }
    });

    selected_button = 0;
    $(document).on("click", ".movlist_rate_button", function() {
        var el = $(this);
        var rating = el.data("movrate");
        var movid = el.data("movid");
        var opcomment = $('#opcomment-' + movid).val();
                $.ajax({
                    url: "{% url 'movies:ratesuggestion' %}",
                    method: "GET",
                    data: {
                        movid: movid,
                        rating: rating,
                        opcomment: opcomment
                    },
                    success: function (result) {
                        console.log(result);
                        el.css({"background-color": "white"})
                        if (selected_button != 0) {
                            $(".rate" + selected_button).css({backgroundColor: ""});
                        }
                    },
                    error: function (result) {
                        console.log(result);
                        window.location.replace("{% url 'movies:ratesuggestion' %}?movid=" + movid + "&rating=1");
                        }
                });
    });


    $(document).on("click", ".movlist_seenit", function() {
        var el = $(this);
        var movid = el.data("movid");
            $.ajax({
                url: "/markasseen/",
                method: "POST",
                data: {
                    movid: movid
                },
            success: function (result) {
                if (result == "marked") {
                    console.log(result);
                    el.css({"background-color": "green"})
                } else {
                    if (result == "unmarked") {
                        console.log(result);
                        el.css({"background-color": "grey"})
                    }
                }
            }
        });
    });


});