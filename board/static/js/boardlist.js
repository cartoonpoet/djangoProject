$(document).ready(function(){
    $(".logout").click(function(){
        const token = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
               type : 'post',
               url : 'logout/',
               data : '',
                headers:{ "X-CSRFToken": token },
               dataType : 'json',
               error : function (xhr, status, error){
                   alert(error);
               } ,
                success : function (json){
                   if(Number(json['message'])==0){
                       location.href="/";
                   }
                }
            });
    });
});