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
	} else if (e.keyCode == 72 || e.keyCode == 74 || e.keyCode == 75 || e.keyCode == 76) {  // 'hjkl'
        /*
         *      <IMG>
         *      |---------------|
         *      |               |
         *      |    <fancy>    |
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

        var viewer;
        var width_range = 0;
        var height_range = 0;
        var cur_left = 0;
        var cur_top = 0;
        if (fancies.length > 0 && draggables.length > 0) {
            var fancy = fancies[0];
            viewer = draggables[0];
            if (viewer.children.length > 0 && viewer.children[0].children.length > 0) {
                var img = viewer.children[0].children[0];
                if (img.tagName == 'IMG') {
                    width_range = parseInt(img.style.width, 10) - fancy.offsetWidth;
                    console.log('YMK img.style.width ' + img.style.width);
                    console.log('YMK fancy.offsetWidth ' + fancy.offsetWidth);
                    console.log('YMK width_range ' + width_range);
                    height_range = parseInt(img.style.height, 10) - fancy.offsetHeight;
                }
                cur_left = viewer.style.left;
                cur_top = viewer.style.top;
            }
        }


        switch (e.keyCode) {
            case 72:
                // cur_left = cur_left + width_range / 10;
                cur_left = 0;
                break;
            case 76:
                cur_left = 0 - width_range;
                break;
        }

        console.log('YMK set viewer.style.left ' + cur_left);
        viewer.style.left = cur_left + 'px';
        // viewer.style.top = 0;

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
