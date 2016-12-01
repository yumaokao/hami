'use strict';


var HAS_EVENT_KEY_SUPPORT = KeyboardEvent.prototype.hasOwnProperty('key');
console.log('HAS_EVENT_KEY_SUPPORT + ' + HAS_EVENT_KEY_SUPPORT);

window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
if (window == top) {
    console.log('YMK in window == top');
	window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
}

var trigger_key = 71; // g key
function doKeyPress(e) {
    console.log('YMK in doKeyPress keyCode ' + e.keyCode);
	if (e.keyCode == trigger_key){
        var books = document.getElementsByClassName('box_in');
        console.log('YMK get books ' + books.length);
        if (books.length > 1) {
            var evt = mouseEvent('click');
            dispatchEvent(books[0], evt);
        }
	} else if (e.keyCode == trigger_key + 1) {
        var thebook = document.getElementsByClassName('ui-draggable');
        console.log('YMK get thebook[0].style.left ' + thebook[0].style.left);
        console.log('YMK get thebook[0].style.top ' + thebook[0].style.top);
        thebook[0].style.left = 0;
        thebook[0].style.top = 0;
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
