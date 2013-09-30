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