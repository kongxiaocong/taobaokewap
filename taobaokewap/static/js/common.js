/**
 * Created by liguanghua on 2018/6/21.
 */
$(document).ready(function(){
    //全局返回顶部
    var innerHeight=window.innerHeight;
    window.onscroll=function(){
        var scrollTop=document.body.scrollTop || document.documentElement.scrollTop;
        if(scrollTop>=innerHeight){
            $("#global-gotop").show();
        }else{
            $("#global-gotop").hide();
        }
    }
    $("#global-gotop").click(function(){
        var scrollTop=document.body.scrollTop || document.documentElement.scrollTop;
        var timer=setInterval(function(){
            scrollTop*=0.9;
            document.body.scrollTop = document.documentElement.scrollTop = scrollTop;
            if(scrollTop<1){
                document.body.scrollTop = document.documentElement.scrollTop = 0;
                clearInterval(timer);
            }
        },10);
    });

    //全局返回上一个页面
    $("#global-back").click(function(){
        history.back();
    });

    //全局切换radio
    $(".global-radio").click(function(){
        var $radioName=$(this).next().attr("name");
        var $radios=$("input[name='"+$radioName+"']");
        $radios.removeAttr("checked");
        $(this).next().attr("checked","true");

        $radios.each(function(){
            $(this).prev().removeClass("global-radio-active");
            $(this).parent().css("background-color","#fff");
        });
        $(this).addClass("global-radio-active");
        $(this).parent().css("background-color","#f7f7f7");
    });

    //全局头部菜单
    $("#global-header-menu").click(function(){
        $("#global-header-aside").slideToggle(100);
    });
});