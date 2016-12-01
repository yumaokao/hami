'use strict';

window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
if (window == top) {
	window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
}

var trigger_key = 71; // g key
function doKeyPress(e) {
    console.log('YMK in doKeyPress keyCode ' + e.keyCode);
	if (e.keyCode == 71) { 'g'
        var books = document.getElementsByClassName('box_in');
        console.log('YMK get books ' + books.length);
        if (books.length > 1) {
            var evt = mouseEvent('click');
            dispatchEvent(books[0], evt);
        }
	} else if (e.keyCode == 72) { 'h'
        /*
         *      <IMG>
         *      |---------------|
         *      |               |
         *      |   <viewer>    |
         *      |     |----|    |
         *      |     |    |    |
         *      |     |----|    |
         *      |               |
         *      |---------------|
         */

        var fancies = document.getElementsByClassName('viewer morning');
        console.log('YMK fancies.length ' + fancies.length);
        if (fancies.length > 0) {
            var fancy = fancies[0];
            console.log('YMK get fancy.offsetWidth ' + fancy.offsetWidth);
            console.log('YMK get fancy.offsetHeight ' + fancy.offsetHeight);
        }

        var draggables = document.getElementsByClassName('ui-draggable');
        if (draggables.length > 0) {
            var viewer = draggables[0];
            if (viewer.children.length > 0 && viewer.children[0].children.length > 0) {
                var img = viewer.children[0].children[0];
                console.log('YMK get img ' + img.tagName);
                if (img.tagName == 'IMG') {
                    console.log('YMK get img.style.width ' + img.style.width);
                    console.log('YMK get img.style.height ' + img.style.height);
                }
            }
            console.log('YMK get viewer.style.left ' + viewer.style.left);
            console.log('YMK get viewer.style.top ' + viewer.style.top);
            /* console.log('YMK get viewer.offsetWidth ' + viewer.offsetWidth);
            console.log('YMK get viewer.offsetHeight ' + viewer.offsetHeight); */
        }



        /* thebook[0].style.left = 0;
        thebook[0].style.top = 0; */
    }
}

function mouseEvent(type) {
    var evt;
    if (typeof( document.createEvent ) == 'function') {
        evt = document.createEvent('MouseEvents');
        evt.initMouseEvent(type, true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
    }
    return evt;
}

function dispatchEvent(el, evt) {
    if (el.dispatchEvent) {
        el.dispatchEvent(evt);
    }
    return evt;
}
