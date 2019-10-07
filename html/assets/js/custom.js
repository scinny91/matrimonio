var transparentDemo = true;
var fixedTop = false;



$(window).scroll(function(e) {
    oVal = ($(window).scrollTop() / 170);
    $(".blur").css("opacity", oVal);
    
});

function handleError()
{
    console.error('Errore!!!')
}

function add_guest()
{
    var numero_raggiunto = jQuery('#numero_ospiti').val()
    jQuery.ajax(
        {url: jQuery('#appserver').val() + "/controller/",
        data: {'action': 'add_guest', 'index': numero_raggiunto},
        success: function(result){
            if (result.result)
                {
                    jQuery('#inputs').append(result.result);
                    jQuery('#numero_ospiti').val(parseInt(numero_raggiunto) +1);
                    //$('.switch')['bootstrapSwitch']();
                    //$("[data-toggle='switch']").wrap('<div class="switch" />').parent().bootstrapSwitch();
                    themeInit();

                }
  }});
}



function Init()
{
    jQuery('#add_guest').click(add_guest)
}



$(document).ready( Init() )