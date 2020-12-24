$(document).ready(function(){
    $(".logout").click(function(){
        $.ajax({
               type : 'post',
               url : 'logout/',
               data : '',
               dataType : 'json',
               error : function (xhr, status, error){
                   alert(error);
               } ,
                success : function (json){

                }
            });
    });
});