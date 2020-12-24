$(document).ready(function(){
    $(".submit").click(function(){
       if($(".last_name").val()==""){
           alert("성을 입력해주세요.");
           return false;
       }
        else if($(".first_name").val()==""){
            alert("이름을 입력해주세요.");
            return false;
        }
        else if($(".nikname").val()==""){
            alert("닉네임을 입력해주세요.");
            return false;
        }
        else if($(".email").val()==""){
            alert("아이디를 입력해주세요.");
            return false;
        }
        else if($(".pw").val()==""){
            alert("비밀번호를 입력해주세요.");
            return false;
        }
        else if($(".pw_check").val()==""){
            alert("비밀번호 확인을 입력해주세요.");
            return false;
        }
        else{
            var queryString = $("form[name=signForm]").serialize();

            $.ajax({
               type : 'post',
               url : '',
               data : queryString,
               dataType : 'json',
               error : function (xhr, status, error){
                   alert(error);
               } ,
                success : function (json){
                   for(var i in json){
                       if(Number(json[i])==0){
                           alert('아이디가 이미 사용중입니다.');
                       }
                       else if(Number(json[i])==1){
                            alert('닉네임이 이미 사용중입니다.');
                       }
                       else if(Number(json[i])==2){
                           alert('가입 완료!');
                            location.href="/";
                       }
                   }
                }
            });
       }
    });
});