/**
 * Created by liguanghua on 2018/6/24.
 */
$(document).ready(function(){
    $("#i-search").focus(function(){
        $("#i-search-page").show();
        $("#i-spage-input").focus();
    });
    $("#i-spage-cancel").click(function(){
        $("#i-search-page").hide();
    });
});