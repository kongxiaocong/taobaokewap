/**
 * Created by liguanghua on 2018/5/29.
 * param
 * id 控件索引
 * width 宽度
 * sliderTime 图片滑动时间
 * autoplayIntervalTime 自动播放间隔时间
 */
function pictureSwitching(id,width,sliderTime,autoplayIntervalTime) {

    //获取页面元素
    var psc = document.getElementById("ps"+id+"-container");
    var img = document.getElementById("ps"+id+"-img-wrapper");
    var imgs = img.getElementsByTagName("img");
    var prev = document.getElementById("ps"+id+"-prev");
    var next = document.getElementById("ps"+id+"-next");
    var btns = document.getElementById("ps"+id+"-index-wrapper").getElementsByTagName("a");

    //计算图片个数
    var num=btns.length;

    //初始化样式布局
    psc.style.width = width + "px";
    img.style.width = width * (num + 2) + "px";
    img.style.left = "-" + width + "px";
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].style.width = width + "px";
    }

    //计算间隔偏移
    var intervalTime = 1, totalTime = sliderTime, intervalOffset, totalOffset = width;//定义间隔时间、总的时间、间隔偏移量、总的偏移量
    intervalOffset = Math.floor(intervalTime * totalOffset / totalTime);//计算间隔偏移量，考虑除不尽的情况

    //定时器stopID
    var timer = 0, autoplayTimer = 0, timer2 = 0;

    //下一张
    next.onclick = function () {
        if (timer > 0 || timer2 > 0) return;//事件防干扰

        var left = img.offsetLeft;//当前偏移值
        var validLeft = left - width;//目标偏移值（往负方向移动）
        var nextSwitchWidth = "-" + width * (num + 1);//循环切换触发点

        timer = setInterval(function () {
            left = left - intervalOffset;
            if (left >= validLeft) {
                img.style.left = left + "px";
                if (img.offsetLeft == validLeft) {//刚好达到边界值
                    activeBtnColor();
                    clearInterval(timer);
                    timer = 0;
                }
            } else {
                img.style.left = validLeft + "px";
                activeBtnColor();
                clearInterval(timer);
                timer = 0;
            }
            if (img.offsetLeft == nextSwitchWidth) {//切换到第一张
                img.style.left = "-" + width + "px";
                activeBtnColor();
            }
        }, intervalTime);
    }

    //上一张
    prev.onclick = function () {
        if (timer > 0 || timer2 > 0) return;//事件防干扰

        var left = img.offsetLeft;//当前偏移值
        var validLeft = left + width;//目标偏移值（往正方向移动）
        var prevSwitchWidth = 0;//循环切换触发点

        timer = setInterval(function () {
            left = left + intervalOffset;
            if (left <= validLeft) {
                img.style.left = left + "px";
                if (left == validLeft) {
                    activeBtnColor();
                    clearInterval(timer);
                    timer = 0;
                }
            } else {
                img.style.left = validLeft + "px";
                activeBtnColor();
                clearInterval(timer);
                timer = 0;
            }
            if (img.offsetLeft == prevSwitchWidth) {//切换到最后一张
                img.style.left = "-" + num * width + "px";
                activeBtnColor();
            }
        }, intervalTime);
    }

    //悬停按钮切换
    for (var i = 0; i < btns.length; i++) {
        btns[i].onmouseover = function () {
            if (timer > 0 || timer2 > 0) return;//事件防干扰

            var index = this.getAttribute("data-index");//获取悬停按钮的索引
            var left = img.offsetLeft;//获取当前偏移值
            var validLeft = "-" + index * width;//计算目标偏移量
            var intervalTime2 = 1, totalTime2 = sliderTime, intervalOffset2, totalOffset2;
            for (var i = 0; i < btns.length; i++) {
                if (btns[i].className == "ps-index-on") {
                    var activeIndex = btns[i].getAttribute("data-index");
                    break;
                }
            }
            if (index > activeIndex) {//切换后面的图片
                totalOffset2 = width * (index - activeIndex);
                intervalOffset2 = Math.floor(intervalTime2 * totalOffset2 / totalTime2);
                timer2 = setInterval(function () {
                    left = left - intervalOffset2;
                    if (left >= validLeft) {
                        img.style.left = left + "px";
                        if (left == validLeft) {
                            activeBtnColor();
                            clearInterval(timer2);
                            timer2 = 0;
                        }
                    } else {
                        img.style.left = validLeft + "px";
                        activeBtnColor();
                        clearInterval(timer2);
                        timer2 = 0;
                    }
                }, intervalTime2);
            } else if (index < activeIndex) {//切换前面的图片
                totalOffset2 = width * (activeIndex - index);
                intervalOffset2 = Math.floor(intervalTime2 * totalOffset2 / totalTime2);
                timer2 = setInterval(function () {
                    left = left + intervalOffset2;
                    if (left <= validLeft) {
                        img.style.left = left + "px";
                        if (left == validLeft) {
                            activeBtnColor();
                            clearInterval(timer2);
                            timer2 = 0;
                        }
                    } else {
                        img.style.left = validLeft + "px";
                        activeBtnColor();
                        clearInterval(timer2);
                        timer2 = 0;
                    }
                }, intervalTime2);
            }
        }
    }

    //自动播放
    function autoplay(){
        autoplayTimer = setInterval(next.onclick, autoplayIntervalTime);
    }
    autoplay();

    //鼠标悬停停止自动播放
    img.onmouseover = function () {
        clearInterval(autoplayTimer);
    }

    //鼠标移开开启自动播放
    img.onmouseout = function () {
        autoplay();
    }

    //激活按钮颜色
    function activeBtnColor() {
        var left = img.offsetLeft;
        var activeIndex = Math.abs(left / width) - 1;
        for (var i = 0; i < btns.length; i++) {
            if (i == activeIndex) {
                btns[i].className = "ps-index-on";
                document.getElementsByTagName("header")[0].style.backgroundColor = btns[i].getAttribute("data-color");
            } else {
                btns[i].className = "ps-index-off";
            }
        }
    }

    //移动端触摸事件
    var startpos,endpos;
    psc.ontouchstart=function(e){
        startpos={startX:e.changedTouches[0].pageX , startY:e.changedTouches[0].pageY};
    }
    psc.ontouchmove=function(e){
        e.preventDefault();//阻止滚动默认行为
    }
    psc.ontouchend=function(e){
        endpos={endX: e.changedTouches[0].pageX , endY: e.changedTouches[0].pageY};
        if(Math.abs(endpos.endY-startpos.startY) > Math.abs(endpos.endX-startpos.startX) && endpos.endY-startpos.startY<0){
            //bottom to top
        }else if(Math.abs(endpos.endY-startpos.startY) > Math.abs(endpos.endX-startpos.startX) && endpos.endY-startpos.startY>0){
            //top to bottom
        }else if(Math.abs(endpos.endY-startpos.startY) < Math.abs(endpos.endX-startpos.startX) && endpos.endX-startpos.startX<0){
            //right to left
            next.onclick();
        }else{
            //left to right
            prev.onclick();
        }
    }

}
