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
        {url: jQuery('#appserver').val() + "/add_guest",
        success: function(result){
                console.log('success')
                    jQuery('#inputs').append(result);
                    jQuery('#numero_ospiti').val(parseInt(numero_raggiunto) +1);
                    themeInit();


        }
  });
}

function save_guest(){
    var lista_dati = new Array()
    var lista_campi = ['nome_ospite', 'albergo', 'bambino', 'viaggio', 'menu', 'note']

    var rows_html = jQuery('#inputs').children()
    rows_html.each(
        function(element) {
          var row_index = (this.id).replace('riga_invitato#','')
          var object = {}
          for (i=0; i<lista_campi.length; i++)
          {
            object[lista_campi[i]] = jQuery('#'+lista_campi[i]+'_'+row_index).val()
            console.log('#'+lista_campi[i]+'_'+row_index)
          }
          object.id_ospite = row_index
          object.url_img_user = jQuery('#img_'+row_index).attr('src')
          lista_dati.push(object)
        }
    )
    console.log(lista_dati)
    jQuery.ajax(
        {
        url: jQuery('#appserver').val() + "/save_guest/",
        type: "POST",
        data: {'lista_valori': JSON.stringify(lista_dati)},
        success: function(result){
            console.log(result)
            if (result.result)
                {
                  console.log('ciao')
                }
  }});



}


function uploadFile(input){
  var file = input.files[0];
  var file_name = input.id
  file_name += '.'+ file.name.split('.').pop();
  id_foto = file_name.replace('foto_','').split('.')
  id_foto = id_foto[0]

  if(file != undefined){
    formData= new FormData();
    if(!!file.type.match(/image.*/)){
      jQuery('#img_'+id_foto).attr("src", 'assets/img/loading.gif');
      formData.append("image", file, file_name);
      $.ajax({
        url: jQuery('#appserver').val() + "/save_image/",
        type: "POST",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data){
            console.log(data)

            console.log('#img_'+id_foto)
            jQuery('#img_'+id_foto).attr("src", data);
        }
      });
    }else{
      console.error('Not a valid image!');
    }
  }else{
    console.log('Input something!');
  }
}



function Init()
{
    jQuery('#add_guest').click(add_guest)
    jQuery('#save_guest').click(save_guest)

}



$(document).ready( Init() )