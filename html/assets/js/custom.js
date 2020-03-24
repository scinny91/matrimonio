var transparentDemo = true;
var fixedTop = false;



jQuery(window).scroll(function(e) {
    oVal = (jQuery(window).scrollTop() / 170);
    jQuery(".blur").css("opacity", oVal);
    
});

function add_guest()
{
    jQuery('.add_guest').html('<i class="fas fa-spinner"></i>')
    jQuery.ajax(
        {url: jQuery('#appserver').val() + "/add_guest/",
        success: function(result){
                jQuery('#inputs').append(result);
                themeInit();
                jQuery('.onchangeupdate').change(updateGuest);
                jQuery('.delete_ospite').click(deleteGuest)
                jQuery('.add_guest').html('Aggiungi partecipante')
        }
  });
}


function deleteGuest(){
    formData= new FormData();
    id_ospite = (this.id).split('_').pop()
    formData.append("id_ospite", id_ospite);
    jQuery("#riga_invitato_"+id_ospite).html('<i class="fas fa-spinner"></i>')
    jQuery.ajax({
        url: jQuery('#appserver').val() + "/delete_guest/",
        type: "POST",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data){
            jQuery("#riga_invitato_"+id_ospite).remove();
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

    if (this.name == 'mail')
    {
        if (!ValidateEmail(valore))
            {
                jQuery('#'+this.id).addClass('error')
                return
            }
             jQuery('#'+this.id).removeClass('error')

    }

    jQuery.ajax({
        url: jQuery('#appserver').val() + "/update_guest/",
        type: "POST",
        data: formData,
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(data){

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
      jQuery('#img_'+id_foto).attr("src", '../assets/img/loading.gif');
      formData.append("image", file, file_name);
      formData.append("id_ospite", id_foto);
      jQuery.ajax({
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

function login(){
    var formData = new FormData();
    var valore = jQuery('#hash').val()
    formData.append('hash_inserito', valore)
    console.log(formData)
    jQuery.ajax(
        {
        url: jQuery('#appserver').val() + "/check_login/",
        data: formData,
        type: "POST",
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        success: function(result){
                if (result == 'ok')
                {
                    jQuery('#div_hash').removeClass('has-error');
                    jQuery('#msg_hash').html('');
                    window.location.reload()
                }
                else
                {
                    jQuery('#div_hash').addClass('has-error')
                    jQuery('#msg_hash').html('Codice inserito non valido!');
                }


        }
    });
}

function enter_press(e)
 {
         if(e.which === 13){
            jQuery('#login').click()
         }
}

function ValidateEmail(mail)
{
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  {
    return (true)
  }
    return (false)
}


function Init()
{
    jQuery('.add_guest').click(add_guest)
    jQuery('.delete_ospite').click(deleteGuest)
    jQuery('.onchangeupdate').change(updateGuest)
    jQuery('#login').click(login)
    jQuery('#body_login').on('keypress', enter_press)

}


function logout()
{document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
window.location.href = jQuery('#appserver').val()
}

$(document).ready( Init() )