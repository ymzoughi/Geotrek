$( document ).ready(function() {
  // Handler for .ready() called.
  //alert ("test");
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
