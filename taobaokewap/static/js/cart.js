/**
 * Created by liguanghua on 2018/6/27.
 */
$(document).ready(function(){
    $(".cart-pdetail-num-increase").click(function(){
        var num=$(this).next().val();
        if(num<1000){
            num++;
            $(this).next().val(num);
        }else{
            alert("同一商品最多购买1000件");
        }
        calculatePrice(this);
        calculateTotalPrice();
    });
    $(".cart-pdetail-num-decrease").click(function(){
        var num=$(this).prev().val();
        if(num>=2){
            num--;
            $(this).prev().val(num);
        }else{
            alert("最少购买一件");
        }
        calculatePrice(this);
        calculateTotalPrice();
    });
    //脚本控制不会触发
    $(".cart-pdetail-num").on("input propertychange",function(){
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
        calculatePrice(this);
        calculateTotalPrice();
    });
    $(".cart-pdetail-num").focus(function(){
        this.select();
    });

    //计算每块商品价格
    function calculatePrice($this){
        var singlePrice=$($this).parent().prev().data("price");
        var num=$($this).parent().find("input").val();
        var totalPrice=(singlePrice*num).toFixed(2);
        $($this).parent().prev().html("￥"+totalPrice);
    }

    $(".cart-product-checkbox").click(function(){
        if($(this).hasClass("cart-product-checkbox-active")){
            $(this).removeClass("cart-product-checkbox-active");
            $(this).next().removeAttr("checked");
        }else{
            $(this).addClass("cart-product-checkbox-active");
            $(this).next().attr("checked","true");
        }
        updateParentCheckState(this);
        calculateTotalPrice();
    });

    //更新局部全选状态
    function updateParentCheckState($this){
        var $checkboxs=$($this).parent().parent().find("input[type='checkbox']");
        var isChecked=true;
        $checkboxs.each(function(){
            if(!$(this).attr("checked")){
                isChecked=false;
            }
        });
        if(isChecked){
            $($this).parent().parent().find(".cart-store-checkbox").addClass("cart-store-checkbox-active");
        }else{
            $($this).parent().parent().find(".cart-store-checkbox").removeClass("cart-store-checkbox-active");
        }
    }

    $(".cart-store-checkbox").click(function(){
        if($(this).hasClass("cart-store-checkbox-active")){
            $(this).removeClass("cart-store-checkbox-active");
            $(this).parent().siblings().find("input[type='checkbox']").removeAttr("checked");
            $(this).parent().siblings().find(".cart-product-checkbox").removeClass("cart-product-checkbox-active");
        }else{
            $(this).addClass("cart-store-checkbox-active");
            $(this).parent().siblings().find("input[type='checkbox']").attr("checked","true");
            $(this).parent().siblings().find(".cart-product-checkbox").addClass("cart-product-checkbox-active");
        }
        calculateTotalPrice();
    });

    $(".cart-delete").click(function(){
        var cartStore=$(this).parents(".cart-store");
        $(this).parents(".cart-store-product").remove();
        if(cartStore.children("article").length==0){
            cartStore.remove();
        }
        calculateTotalPrice();
    });

    //统计总价
    function calculateTotalPrice(){
        var totalPrice=0;
        var $checkboxs=$("input[type='checkbox']");
        $checkboxs.each(function(){
            if($(this).attr("checked")){
                totalPrice+=parseFloat($(this).parent().find(".cart-pdetail-price").html().substring(1));
            }
        });
        totalPrice=totalPrice.toFixed(2);
        $("#cart-total-price").html("￥"+totalPrice);
    }
    calculateTotalPrice();

});