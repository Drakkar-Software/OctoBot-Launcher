function load_template(template_url){
    const template_location = $("div[template='"+template_url+"']");
    $.ajax({
        url: template_url,
        beforeSend: function() {
            template_location.html("<i class='fa fa-circle-notch fa-spin'></i>");
        },
        success: function(data) {
           template_location.html(data);
           handle_route_button();
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

$(document).ready(function () {
    load_templates();
});
