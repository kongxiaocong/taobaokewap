/**
 * Created by liguanghua on 2018/6/22.
 */
window.onload=function(){
    //初始化元素尺寸
    var width=window.innerWidth;
    var imgWrapper=document.getElementById("slider-img-wrapper");
    var imgs=document.getElementsByClassName("slider-img");
    var imgNum=imgs.length;
    imgWrapper.style.width=width*imgNum+"px";
    for(var i=0;i<imgNum;i++){
        imgs[i].style.width=width+"px";
    }
    var currentNum=document.getElementById("slider-current-num");
    var totalNum=document.getElementById("slider-total-num");
    totalNum.innerHTML=imgNum;

    //触摸滑动
    var slider=document.getElementById("slider");
    var startpos,endpos;
    var timer=0;
    slider.ontouchstart=function(e){
        startpos={startX:e.changedTouches[0].pageX , startY:e.changedTouches[0].pageY};
    }
    slider.ontouchmove=function(e){
        e.preventDefault();//阻止滚动默认行为
    }
    slider.ontouchend=function(e){
        endpos={endX: e.changedTouches[0].pageX , endY: e.changedTouches[0].pageY};
        if(Math.abs(endpos.endY-startpos.startY) > Math.abs(endpos.endX-startpos.startX) && endpos.endY-startpos.startY<0){
        }else if(Math.abs(endpos.endY-startpos.startY) > Math.abs(endpos.endX-startpos.startX) && endpos.endY-startpos.startY>0){
        }else if(Math.abs(endpos.endY-startpos.startY) < Math.abs(endpos.endX-startpos.startX) && endpos.endX-startpos.startX<0){
            //right to left
            if(timer>0) return;
            var stopLeft="-"+width*(imgNum-1);
            var currentLeft=imgWrapper.offsetLeft;
            if(currentLeft!=stopLeft){
                var targetLeft=currentLeft-width;
                timer=setInterval(function(){
                    currentLeft-=5;
                    if(currentLeft<targetLeft){//值不合法，拉回边界
                        imgWrapper.style.left=targetLeft+"px";
                        currentNum.innerHTML=Math.abs(targetLeft/width)+1;
                        clearInterval(timer);
                        timer=0;
                    }else{//值合法，允许赋值
                        imgWrapper.style.left=currentLeft+"px";
                    }
                },1);
            }
        }else{
            //left to right
            if(timer>0) return;
            var stopLeft=0;
            var currentLeft=imgWrapper.offsetLeft;
            if(currentLeft!=stopLeft){
                var targetLeft=currentLeft+width;
                timer=setInterval(function(){
                    currentLeft+=5;
                    if(currentLeft>targetLeft){//值不合法，拉回边界
                        imgWrapper.style.left=targetLeft+"px";
                        currentNum.innerHTML=Math.abs(targetLeft/width)+1;
                        clearInterval(timer);
                        timer=0;
                    }else{//值合法，允许赋值
                        imgWrapper.style.left=currentLeft+"px";
                    }
                },1);
            }
        }
    }
}