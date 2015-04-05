function transformSongIntoDiv(song) {
	html = "<div class='result_row'>";
	html += "<div>" + song.title + "</div>";
	html += "<div>" + song.artist_name + "</div>";
	html += "<div>" + song.dance_name + "</div>";
	html += "</div>"
	return html;
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
	
	
	$("input").autocomplete({
		source: function(request, responseFunction) {
			$.getJSON("../php/main.php", {action: "list", type: "dances", term: request.term},  responseFunction);
		}
	});	
});