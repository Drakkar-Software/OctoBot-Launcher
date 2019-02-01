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
            $.ajax({
                url: command,
                beforeSend: function() {
                    button.html("<i class='fa fa-circle-notch fa-spin'></i>");
                },
                complete: function() {
                   button.html(origin_val);
                }
            });
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
