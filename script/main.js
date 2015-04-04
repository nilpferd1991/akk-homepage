function transformSongIntoDiv(song) {
	html = "<div class='result_row'>";
	html += "<div>" + song.title + "</div>";
	html += "<div>" + song.artist_name + "</div>";
	html += "<div>" + song.dance_name + "</div>";
	html += "</div>"
	return html;
}

function fillList(parent, listElements) {
	listObject = $("#list");		
	html = "<ul>"; 
	listElements.forEach(function(element) {
		html += "<li>" + element + "</li>";
	});
	
	html += "</ul>";
	
	listObject.html(html);
	listObject.css("width", parent.outerWidth());
	listObject.css("top", parent.offset().top + parent.outerHeight() + 5);
	listObject.css("left", parent.offset().left);
	listObject.show();
}

$(document).ready(function() {
	/*$.get("../php/main.php", function(data) {
		songs = $.parseJSON(data);
		var parent = $("#results_table");
		parent.html("");
		songs.forEach(function(song) {
			parent.append(transformSongIntoDiv(song));
		});
	});*/
	
	
	$("input").focusin(function() {
		input = $(this);
		$.get("../php/main.php", function(data) {
			artists = $.parseJSON(data);
			fillList(input, artists);
		});
	});
	
	$("input").focusout(function() {
		$("#list").hide();
	});
	
});