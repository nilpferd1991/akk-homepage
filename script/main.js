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

  // Add ClickHandler
  listObject.children("ul > li").click(function() {
    parent.css("text", $(this).html());
    parent.enter(); // TODO
    listObject.hide();
  });
  
  listObject.show();
}

function toType(id) {
  return "artists";
}



$(document).ready(function() {
	/*$.get("../php/main.php", function(data) {
	});*/
	
	
	$("input").focusin(function() {
		input = $(this);
    type = toType(input.id);
		$.get("../php/main.php", {action: "list", type: type, startswith: input.css("text")}, function(data) {
			items = $.parseJSON(data);
			fillList(input, items);
		});
	});
	
	$("input").focusout(function() {
		$("#list").hide();
	});

  // TODO
  $("input").enter(function() {
		input = $(this);
    type = toType(input.id);
		$.get("../php/main.php", {action: "list", type: "songs", where: input.css("text"), where_column: type }, function(data) {
		  songs = $.parseJSON(data);
		  var parent = $("#results_table");
		  parent.html("");
		  songs.forEach(function(song) {
			  parent.append(transformSongIntoDiv(song));
		  });
		});
  });
	
});
