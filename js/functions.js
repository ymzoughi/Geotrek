$( document ).ready(function() {
  $( ".animated-text-1").animate({
    left: "+=1100",
  }, 500, function() {
    // Animation complete.
  });
  $( ".animated-text-2").animate({
    left: "+=1386",
  }, 700, function() {
    // Animation complete.
  });
  $( ".animated-text-3").animate({
    left: "+=1486",
  }, 800, function() {
    // Animation complete.
  });
  $(".fancy").fancybox();
  $( window ).resize(function() {
  		//alert ("test");
  		var widthCarousel = $("#carousel-example-generic1").width();
  		var withIndicator = $("#carousel-example-generic1 .carousel-indicators").width();
  		var left = (widthCarousel/2)-(withIndicator/2);
  		console.log(left);
  		//$('.carousel-indicators').css('left',left+'px');
  });
  $(".nav a").click(function(){
	$(".navbar .nav li a").removeClass("active");
	sliceTo($(this));
	$.scrollTo('#'+$(this).data("spy"), 500,{offset:-$('.navbar-fixed-top').height()});
	$(this).addClass("active");
});
$(window).scroll(function() {
});
function sliceTo(elm)
{
	var To = $(elm).offset().left;
	var width = $(elm).width();
	$('.top-bar').animate({
    	'left': To+15,
    	'width':width,
  		},"slow", function() {
  			//$(elm).css('color','#bdce12');
  	});
}
});
