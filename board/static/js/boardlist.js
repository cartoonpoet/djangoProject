$(document).ready(function(){
    $(".searching").click(function(){
        if($(".contents").val() == ""){
            alert('검색어를 입력하세요.');
            return false;
        }
        else{
            $("form").submit();
        }
    })
});