"use strict";

function capitalizeFirstLetter (string) {
	return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

$.widget("custom.editWindow", {
    currentSongID: -1,

    _create: function() {
        var ownElement = this.element;
        ownElement.html('<div><p>Song name: </p><div id="title_input" class="title_search"></div></div>' +
			'<div><p>Artist name: </p><div id="artist_input" class="artist_search"></div></div>' +
			'<div><p>Dance name: </p><div id="dance_input" class="dance_search"></div></div>' +
			'<div><p>Rating: </p><div id="rating_input" class="rating"></div></div>' +
			'<div><p>Notes: </p><div id="notes_input" class="notes"></div></div>' +
			'<div>' +
            '    <div></div>' +
            '    <div><button id="submit_button" class="button">Save</button>' +
            '        <button id="cancel_button" class="button">Cancel</button></div>' +
            '</div>');


        ownElement.find("[class$=search]").completion({autoFocus: false});
        ownElement.find(".rating").rating();
        ownElement.find(".notes").notes();
        ownElement.find(".button").button();

        ownElement.find("#cancel_button").click(function() { ownElement.editWindow("hide") });
        ownElement.find("#submit_button").click(function() { ownElement.editWindow("save") });

        this.hide();
    },

    show: function (songID) {
        if(songID != undefined) {
            this.currentSongID = songID;
        } else {
            this.currentSongID = -1;
        }

        this.loadSong();

        var ownElement = this.element;
        ownElement.parent().show();
    },

    hide: function() {
        this.currentSongID = -1;
        var ownElement = this.element;
        ownElement.parent().hide();
    },

    save: function() {
        var ownElement = this.element;

        var title = ownElement.find("#title_input").completion("value");
        var artist = ownElement.find("#artist_input").completion("value");
        var dance = ownElement.find("#dance_input").completion("value");
        var rating = ownElement.find("#rating_input").rating("value");
        var notes = ownElement.find("#notes_input").notes("value");

        if(this.currentSongID == -1) {
            this._trigger("createNewSong", null, {title: title, artist: artist, dance: dance, rating: rating, notes: notes});
        } else {
            this._trigger("updateSong", null, {songID: this.currentSongID, title: title, artist: artist, dance: dance, rating: rating, notes: notes});
        }

        this.hide();
    },

    reset: function() {
        var ownElement = this.element;

        ownElement.find("[class$=search]").completion("reset");
        ownElement.find(".rating").rating("reset");
        ownElement.find(".notes").notes("reset");
    },

    loadSong: function() {
        if(this.currentSongID == -1) {
            this.reset();
        } else {
            // TODO
        }
    }
});


$.widget("custom.completion", {
	options: {
		autoFocus: true
	},
	_create: function() {
        var ownElement = this;
		ownElement.element.html("<input/>");
        var inputElement = ownElement.element.children("input");

		inputElement.attr("type", "text");
		inputElement.attr("placeholder", capitalizeFirstLetter(transformDivIDIntoColumnName(inputElement)) + "...");
		inputElement.addClass("ui-completion");
		inputElement.autocomplete({
			autoFocus: this.options.autoFocus,
			source: function(request, responseFunction) {
				var column = transformDivIDIntoColumnName($(this)[0].element);
				$.getJSON("../php/main.php", {action: "list", type: column, term: request.term},  responseFunction);
			},
			minLength: 1,
			select: function(event, ui) {
				ownElement._trigger("result", ownElement, {value: ui.item.value, element: this});
			}
		});
		if(this.options.autoFocus == false) {
			inputElement.keypress(function(event) {
				if(event.keyCode == 13) {
					$(this).autocomplete("close");
					$(".ui-complete").hide();
					ownElement._trigger("result", ownElement, {value: "value", element: this});
				}
			});
		}
	},

	reset: function() {
	    var inputElement = this.element.children("input");
	    inputElement.val("");
	},

	value: function() {
	    var inputElement = this.element.children("input");
	    return inputElement.val();
	}
});

$.widget("custom.rating", {
    options: {
        length: 5,
        data: 0
    },

    currentStatus: 0,
    data: 0,

	_create: function() {
        var ownElement = this;
        ownElement.data = ownElement.options.data;

        // Add images
        var length = ownElement.options.length;
        ownElement.element.html("<div></div>");
        var inputElement = ownElement.element.find("div");
        inputElement.addClass("ui-rating");
        for(var i = 0; i < length; i++) {
            inputElement.append("<img src='../img/stars.png'/>");
        }

        // Add handlers

        ownElement.update(ownElement.data);

        var images = inputElement.find("img");
        images.hover(function() {
            ownElement.update(images.index(this) + 1);
        }).click(function() {
            ownElement.data = images.index(this) + 1;
        });
        ownElement.element.mouseleave(function() {
            ownElement.update(ownElement.data);
        });
	},
    update: function(number) {
        var ownElement = this;
        var images = ownElement.element.find("div > img");
        if(number > ownElement.currentStatus) {
            images.slice(ownElement.currentStatus, number).animate({"background-color": "black"}, 50);
            ownElement.currentStatus = number;
        } else if(number < ownElement.currentStatus) {
            images.slice(number, ownElement.currentStatus).animate({"background-color": "lightgray"}, 50);
            ownElement.currentStatus = number;
        }
    },

    reset: function() {
        this.data = 0;
        this.update(0);
    },

    value: function() {
        return this.currentStatus;
    }
});

$.widget("custom.notes", {
    _create: function() {
        var ownElement = this;
        ownElement.element.html('<textarea></textarea>');
        var inputElement = ownElement.element.find("textarea");
        inputElement.addClass("ui-notes");
        inputElement.attr("placeholder", "Notes...");
    },

    reset: function() {
        var inputElement = this.element.find("textarea");
        inputElement.val("");
    },

    value: function() {
        var inputElement = this.element.find("textarea");
        return inputElement.val();
    }
});