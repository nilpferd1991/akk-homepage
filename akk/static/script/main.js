"use strict";

function transformSongIntoDiv(song) {

	var html = "<div class='ui-result_row'>";
	html += "<div><p>" + song.song_title + "</p></div>";
	html += "<div><p>" + song.artist_name + "</p></div>";
	html += "<div><p>" + song.dance_name + "</p></div>";
	html += "</div>";
	var newElement = $(html);

    newElement.click(function() {
        $("#edit_window").editWindow("show", song.song_id);
    });

	return newElement;
}

function transformDivIDIntoColumnName(element) {
	var id = $(element).parent().attr("class");
	if (id == "title_search") {
		return "songs";
	} else if (id == "artist_search") {
		return "artists";
	} else if (id == "dance_search") {
		return "dances";
	} else {
        return "search";
    }
}

function showResults(event, data) {
	$("#results_table").html("");

	var column = transformDivIDIntoColumnName(data.element);
    showResultsCallback(data.value, column)
}

function updateResults() {
    var value = $("#searchboxes").find(".search").completion("value");
    var column = "search";

    showResultsCallback(value, column);
}

function showResultsCallback(value, column) {
    $.getJSON("/db/completion", {type: column, term: value}, function(data) {
        $("#results_table").html("");
        data["results"].forEach(function(song) {
            $("#results_table").append(transformSongIntoDiv(song));
        });
    });
}

$(document).ready(function() {
	$("#searchboxes").find(".search").completion({
		result : showResults
	});
	
	$("#clear_button").click(function() {
		$("#searchboxes").find("input").val("");
		$("#results_table").html("");
	});

	var edit_window = $("#edit_window").editWindow({
	    updateSong: function(event, data) {
	        data.action = "update";
	        $.get("/db/update_song", data);
            updateResults();
	        console.log(data);
	    },
	    createNewSong: function(event, data) {
	        data.action = "add";
	        $.get("/db/add_song", data);
            updateResults();
	        console.log(data);
	    },
	    deleteSong: function(event, data) {
	        data.action = "delete";
	        $.get("/db/delete_song", data);
            updateResults();
            console.log(data);
	    },
        callback: function(event, data) {
            $.getJSON("/db/get_song", {songID: data.songID}, data.callback);
        }
	});

    $("#add_item").click(function() {
        $("#edit_window").editWindow("show");
    });
});