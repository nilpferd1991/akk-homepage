function capitalizeFirstLetter (string) {
	return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

$.widget("custom.completion", {
	_create: function() {
		ownElement = this;
		ownElement.element.html("<input></input>")
		inputElement = ownElement.element.children("input");
		
		inputElement.attr("type", "text");
		inputElement.attr("placeholder", capitalizeFirstLetter(transformDivIDIntoColumnName(inputElement)) + "...");
		inputElement.addClass("ui-completion");
		inputElement.autocomplete({
			source: function(request, responseFunction) {
				column = transformDivIDIntoColumnName($(this)[0].element);
				$.getJSON("../php/main.php", {action: "list", type: column, term: request.term},  responseFunction);
			},
			minLength: 0,
			select: function(event, ui) {
				ownElement._trigger("result", none, {value: ui.item.value});
			}
		}).keypress(function(event) {
			if(event.which == 13) {
				ownElement._trigger("result", ownElement, {value: $(this).val()});
			}
		});
	}
});


function transformSongIntoDiv(song) {
	html = "<div class='ui-result_row'>";
	html += "<div>" + song.title + "</div>";
	html += "<div>" + song.artist_name + "</div>";
	html += "<div>" + song.dance_name + "</div>";
	html += "</div>"
	return html;
}

function transformDivIDIntoColumnName(element) {
	id = $(element).parent().attr("class");
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
	
	console.log("kh");
	
	column = transformDivIDIntoColumnName(element);
	$.getJSON("../php/main.php", {action: "search", type: column, term: text}, function(data) {
		$("#results_table").html("");
		data.forEach(function(song) {
			$("#results_table").append(transformSongIntoDiv(song));
		});
	});
}

$(document).ready(function() {
	$("#searchboxes > [class$=search]").completion({
		result : showResults
	});
	
	$("#clear_button").click(function() {
		$("#searchboxes input").val("");
		$("#results_table").html("");
	});
	
	$("#edit_window").find("[class$=search]").completion();
});