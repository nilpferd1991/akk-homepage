$.widget("custom.completion", {
	_create: function() {
		ownElement = this;
		this.element.autocomplete({
			source: function(request, responseFunction) {
				column = transformDivIDIntoColumnName($(this)[0].element);
				$.getJSON("../php/main.php", {action: "list", type: column, term: request.term},  responseFunction);
			},
			minLength: 0,
			select: function(event, ui) {
				ownElement._trigger("result", this, {value: ui.item.value});
			}
		}).keypress(function(event) {
			if(event.which == 13) {
				ownElement._trigger("result", this, {value: $(this).val()});
			}
		});
	}
});


function transformSongIntoDiv(song) {
	html = "<div class='result_row'>";
	html += "<div>" + song.title + "</div>";
	html += "<div>" + song.artist_name + "</div>";
	html += "<div>" + song.dance_name + "</div>";
	html += "</div>"
	return html;
}

function transformDivIDIntoColumnName(element) {
	id = $(element).parent().attr("id");
	if (id == "title_search") {
		return "songs";
	} else if (id == "artist_search") {
		return "artists";
	} else if (id == "dance_search") {
		return "dances";
	} 
}

function showResults(element, text) {
	$(".ui-autocomplete").hide();
	
	column = transformDivIDIntoColumnName(element);
	$.getJSON("../php/main.php", {action: "search", type: column, term: text}, function(data) {
		$("#results_table").html("");
		data.forEach(function(song) {
			$("#results_table").append(transformSongIntoDiv(song));
		});
	});
}

$(document).ready(function() {
	$("input").val("").completion({
		result : showResults
	});
	
	$("#clear_box").click(function() {
		$("input").val("");
		$("#results_table").html("");
	});
	
	$("#add_item").click(function(){
		
	});
});