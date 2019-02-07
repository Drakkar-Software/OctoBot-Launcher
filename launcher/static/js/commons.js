function load_template(template_url){
    const template_location = $("div[template='"+template_url+"']");
    $.ajax({
        url: template_url,
        beforeSend: function() {
            template_location.html("<div class='my-2'><h5>Loading data <i class='fa fa-circle-notch fa-spin'></i></h5></div>");
        },
        error: function() {
           template_location.html("<div class='my-2'>This service is temporary unavailable.</div>");
           handle_route_button();
        },
        success: function(data) {
           template_location.html(data);
           handle_route_button();
        },
        complete: function() {
           const spinner = $(".fa-sync", template_location.parent());
            if (spinner.hasClass("fa-spin")){
                spinner.removeClass("fa-spin");
            }
        }
    });
}

function load_templates(){
    $("div[template]").each(function () {
        load_template($(this).attr('template'));
    });
}


function handle_route_button(){
    $(".btn").click(function(){
        const button = $(this);
        if (button[0].hasAttribute('route')){
            const command = button.attr('route');
            const origin_val = button.text();
            let refreshIntervalId;
            $.ajax({
                url: command,
                beforeSend: function() {
                    button.html("<i class='fa fa-circle-notch fa-spin'></i>");
                    refreshIntervalId = setInterval(function () {
                        get_progress(button);
                    }, 100);
                },
                complete: function() {
                   clearInterval(refreshIntervalId);
                   button.html(origin_val);
                   load_template(button.closest("div[template]").attr("template"));
                }
            });
         }
    });
}

function get_progress(element) {
    const body = element.closest(".card-body");
    const progress = body.find(".progress");
    const progress_bar = progress.find(".progress-bar");

    // show progress if not
    if (progress.is(':hidden')){
        progress.show();
    }

    $.ajax({
        url: "/progress",
        error: function() {
           console.log("An error occurred when updating progress.");
        },
        success: function(data) {
            progress_bar.css("width", data + "%").attr("aria-valuenow", data);
        }
    });
}

function animate_sync(){
    $(".fa-sync").click(function(){
        if (!$(this).hasClass("fa-spin")){
            $(this).addClass("fa-spin");
        }
    });
}

$(document).ready(function () {
    load_templates();
    animate_sync();
});
