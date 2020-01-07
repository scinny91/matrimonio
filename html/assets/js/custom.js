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
    jQuery.ajax(
        {url: jQuery('#appserver').val() + "/add_guest",
        success: function(result){
                console.log('success')
                console.log(result)
                    jQuery('#inputs').append(result);
                    themeInit();
                    jQuery('.onchangeupdate').change(updateGuest);


        }
  });
}


function deleteGuest(){
    formData= new FormData();
    id_ospite = (this.id).split('_').pop()
    formData.append("id_ospite", id_ospite);
    $.ajax({
        url: jQuery('#appserver').val() + "/delete_guest/",
        type: "POST",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data){
            console.log(data)
            $("#riga_invitato_"+id_ospite).remove();
        }
      });
}



function updateGuest(){
    formData= new FormData();
    id_ospite = (this.id).split('_').pop()
    campo = this.name
    if (this.type === 'checkbox')
        valore = (jQuery('#'+this.id).is(':checked') ? 'S' : 'N')
    else
        valore = jQuery('#'+this.id).val()
    formData.append("id_ospite", id_ospite);
    formData.append("campo", campo);
    formData.append("valore", valore);
    $.ajax({
        url: jQuery('#appserver').val() + "/update_guest/",
        type: "POST",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data){
            console.log(data)
        }
      });
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
      formData.append("id_ospite", id_foto);
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
    jQuery('.delete_ospite').click(deleteGuest)
    jQuery('.onchangeupdate').change(updateGuest)

}


function logout()
{document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
window.location.href = jQuery('#appserver').val()
}

$(document).ready( Init() )