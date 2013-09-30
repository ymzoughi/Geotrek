$(".nav a").click(function(){
	$(".navbar .nav li a").removeClass("active");
	sliceTo($(this));
	$.scrollTo('#'+$(this).data("spy"), 500,{offset:-$('.navbar-fixed-top').height()});
	$(this).addClass("active");
});
$(window).scroll(function() {
	//var h = document.getElementsByTagName("H1");
	//console.log(h);
	//for (var i = 0; i < h.length; i++) {
	//	console.log (h[i].getBoundingClientRect().top);
			//console.log(h[i].id);
		//sliceTo($('[data-spy ='+h[i].id+']'));
	
	//}
	
//console.log(document.getElementById('h1'));
//console.log (h.getBoundingClientRect());
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