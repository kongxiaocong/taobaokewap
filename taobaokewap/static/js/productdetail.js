/**
 * Created by liguanghua on 2018/6/17.
 */
$(document).ready(function(){
    $(".pd-nav-title").click(function(){
        if(this.className.indexOf("pd-nav-active")==-1){
            $(".pd-nav-title").removeClass("pd-nav-active");
            $(this).addClass("pd-nav-active");
            $(".pd-nav-detail").hide();
            $(this).children(".pd-nav-detail").show();
        }
    });

    $(".pd-param-option-link").click(function(){
        if(this.className.indexOf("pd-param-option-checked")>-1){
            $(this).removeClass("pd-param-option-checked");
        }else{
            $(this).addClass("pd-param-option-checked");
        }
    });

    $(".pd-number-add").click(function(){
        var num=$(this).next().val();
        if(num<1000){
            num++;
            $(this).next().val(num);
        }else{
            alert("同一商品最多购买1000件");
        }
    });

    $(".pd-number-cut").click(function(){
        var num=$(this).prev().val();
        if(num>=2){
            num--;
            $(this).prev().val(num);
        }else{
            alert("最少购买一件");
        }
    });

    $(".pd-number-input").focus(function(){
        this.select();
    });

    //脚本控制不会触发
    $(".pd-number-input").on("input propertychange",function(){
        var num=$(this).val();
        if(/^[1-9][0-9]*$/.test(num)){
            if(num>=1 && num<=1000){
                $(this).val(num);
            }else if(num>1000){
                $(this).val(1000);
                alert("数量越界");
            }else{
                $(this).val(1);
                alert("数量越界");
            }
        }else{
            $(this).val(1);
            alert("数量必须是正整数");
        }
    });
});