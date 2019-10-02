$(function(){
	$('#search').keyup(function(){
		// ajax call
		$.ajax({
			type:"POST",
			url:"/newhome/search",
			data:{
				'search_text' : ('#search').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success :searchSuccess,
			dataType:'html'
		});
	});
});

function searchSuccess(data,textStatuc,jqXHR){
	$('#livesearch').html(data)
}
