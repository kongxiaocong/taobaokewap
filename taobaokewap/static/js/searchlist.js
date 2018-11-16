$(document).ready(function(){
   $(".sl-filter-section").click(function(){
        if($(this).children("aside:last-child").is(":visible")){
            $(this).children("aside:last-child").slideUp();
        }else{
            $(".sl-filter-options").hide();
            $(this).children("aside:last-child").slideDown();
        }
   });

    $("#sl-filter").click(function(){
        var currentLeft=100;
        var targetLeft=10;
        var timer=setInterval(function(){
            currentLeft-=2;
            if(currentLeft>=targetLeft){
                $("#sl-filter-aside,#sl-filter-fixed").css("left",currentLeft+"%");
            }else{
                $("#sl-filter-aside,#sl-filter-fixed").css("left",targetLeft+"%");
                $("#sl-filter-product-opacity").show();
                clearInterval(timer);
            }
        },1);
    });

    $("#sl-filter-product-opacity,#sl-filter-commit").click(function(){
        var currentLeft=10;
        var targetLeft=100;
        var timer=setInterval(function(){
            currentLeft+=2;
            if(currentLeft<=targetLeft){
                $("#sl-filter-aside,#sl-filter-fixed").css("left",currentLeft+"%");
            }else{
                $("#sl-filter-aside,#sl-filter-fixed").css("left",targetLeft+"%");
                $("#sl-filter-product-opacity").hide();
                clearInterval(timer);
            }
        },1);
    });

    $(".sl-filter-value-link").click(function(){
        if(this.className.indexOf("sl-filter-value-active")>-1){
            $(this).removeClass("sl-filter-value-active");
        }else{
            $(this).addClass("sl-filter-value-active");
        }
    });

    $(".sl-filter-product-header").click(function () {
        var ico=$(this).children("span:last-child");
        $(this).next().is(":visible") ? ico.html("&#xea51;") : ico.html("&#xea52;");
        $(this).next().slideToggle(100);
    });

    $(".sl-filter-options-item").click(function(){
        if(this.className.indexOf("sl-filter-options-active")>-1){
            $(this).removeClass("sl-filter-options-active");
        }else{
            $(this).addClass("sl-filter-options-active");
        }
    });

    $("#sl-header-right").click(function(){
        $("#global-header-aside").slideToggle(100);
    });
});