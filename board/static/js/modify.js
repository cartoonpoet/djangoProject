$(document).ready(function(){
    $(".upload-hidden1").on('change', function(fileValue){
        if(window.FileReader){
            var files=$('input[name="file"]')[0].files;
            if(files.length>5){
                alert("파일은 5개까지만 추가할 수 있습니다.");
                return false;
            }
            filename = files[0].name;
            for(var i=1; i<files.length; i++){
                filename += ', '+files[i].name;
            }
            //filename = $(this)[0].files[0].name;
        }
        else {
           filename = $(this).val().split('/').pop().split('\\').pop();
        }
        $(this).siblings('.upload1').val(filename);
    });
    $(".cancel").click(function(){
       location.href = '../';
    });
    $(".post_edit").click(function (){
        // var xhttp = new XMLHttpRequest();
        // var csrf_token = $('[name=csrfmiddlewaretoken]').val();
        // xhttp.open("PUT", "", true);
        // xhttp.setRequestHeader('X-CSRFToken', csrf_token);
        // xhttp.onload = () => {
        //     if(xhttp.status == 200){
        //         let result = xhttp.response;
        //         alert(result);
        //         return result;
        //     }
        //     else{
        //         alert("ERROR"+this.status);
        //     }
        // };
        // xhttp.send();
        // return false;
    })
});