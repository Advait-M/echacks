// jQuery to collapse the navbar on scroll
function sky(){
    if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
        $(".skyline").addClass("skyline-collapse");
    } else {
        $(".navbar-fixed-top").removeClass("top-nav-collapse");
        $(".skyline").removeClass("skyline-collapse");
        console.log("displayed skyline");
    }
}
function divHeight(){
    console.log("checked div heights");
    if ($(window).width() > 767) {
        var h1 = $('#how-img-1').css("height");
        var h2 = $('#how-img-2').css("height");
        var h3 = $('#how-img-3').css("height");
        var h4 = $('#chal-img-1').css("height");
        var h5 = $('#chal-img-2').css("height");
    }
    else {
        var h1 = $('#how-child-1').css("height");
        var h2 = $('#how-child-2').css("height");
        var h3 = $('#how-child-3').css("height");
        var h4 = $('#chal-child-1').css("height");
        var h5 = $('#chal-child-2').css("height");
    }
    console.log("div heights: " + h1 + ", " + h2 + ", " + h3 + ", " + h4 + ", " + h5);
    if (h1 != "0px"  && h2 != "0px" && h3 != "0px" && h4 != "0px" && h4 != "1px" && h5 != "0px" && h5 != "1px"){
        document.getElementById('how-div-1').style.height = h1;
        document.getElementById('how-div-2').style.height = h2;
        document.getElementById('how-div-3').style.height = h3;
        document.getElementById('chal-div-1').style.height = h4;
        document.getElementById('chal-div-2').style.height = h5;
        clearInterval(divTimer);
    }
}
divTimer = setInterval(divHeight, 200);
function link(s){
    if (s){
        document.getElementById('modal-h').innerHTML = "Challenge 1";
        document.getElementById('modal-i').src = "css/img/c1.pdf";
    }
    else{
        document.getElementById('modal-h').innerHTML = "Challenge 2";
        document.getElementById('modal-i').src = "css/img/c2.pdf";
    }
}
$(window).scroll(function() {
    sky();
});

$(function() {
    $('a.page-scroll').bind('click', function(event) {
        $('html, body').stop().animate({
            scrollTop: ($($(this).attr('href')).offset().top - 50)
        }, 800, 'easeInOutExpo');
        event.preventDefault();
    });
});
$(function() {
    $('.navbar-collapse ul li a').bind('click', function(event) {
        if ($(window).width() < 768) {
            // Closes the Responsive Menu on Menu Item Click
            $('.navbar-toggle').click();
        }
    });
});
$( window ).on("resize", function() {
    divHeight();
});
