$(".nav a").click(function(){
	sliceTo($(this));
	$.scrollTo('#'+$(this).data("spy"), 500,{offset:-$('.navbar-fixed-top').height()})
});
$(window).scroll(function() {
	//var h = document.getElementsByTagName("H1");
	//for (var i = 0; i < h.length; i++) {
		//if (h[i].getBoundingClientRect().top<127 && h[i].getBoundingClientRect().top>25 ) {
			//console.log(h[i].id);
		//	sliceTo($('[data-spy ='+h[i].id+']'));
		//}
//	}
	
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
  			$(elm).css('color','##bdce12');
  	});
}