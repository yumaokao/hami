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
        // console.log('YMK get books ' + books.length);
        if (books.length > 1) {
            var evt = mouseEvent('click');
            dispatchEvent(books[0], evt);
        }
    } else if (e.keyCode == 78) {  // 'n'
        // turnPage( _PAGE_TYPE2 ? false : true);
        injectScript();
    } else if (e.keyCode == 80) {  // 'p'
        // turnPage( _PAGE_TYPE2 ? true : false);
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

        // console.log('YMK _CURRENT_PAGE ' + _CURRENT_PAGE);
        // console.log('YMK _TOTAL_PAGE' + _TOTAL_PAGE);

        var fancies = document.getElementsByClassName('viewer morning');
        console.log('YMK fancies.length ' + fancies.length);
        if (fancies.length > 0) {
            var fancy = fancies[0];
            console.log('YMK get fancy.offsetWidth ' + fancy.offsetWidth);
            console.log('YMK get fancy.offsetHeight ' + fancy.offsetHeight);
        }

        var draggables = document.getElementsByClassName('ui-draggable');
        console.log('YMK draggables.length ' + draggables.length);
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
            case 74:
                cur_top = 0 - height_range;
                break;
            case 75:
                cur_top = 0;
                break;
            case 76:
                cur_left = 0 - width_range;
                break;
        }

        viewer.style.left = cur_left + 'px';
        viewer.style.top = cur_top + 'px';

        /* thebook[0].style.left = 0;
        thebook[0].style.top = 0; */
    }
}

function injectScript() {
    var script = document.createElement('script');
    script.id = '_hamibook-scroll'
    script.appendChild(document.createTextNode('console.log(_CURRENT_PAGE); console.log(_TOTAL_PAGE);'
                                               + 'var s = document.getElementById("_hamibook-scroll");'
                                               + 'if (s !== undefined) { s.setAttribute("_current_page", _CURRENT_PAGE); };'
                                               + 'if (s !== undefined) { s.setAttribute("_total_page", _TOTAL_PAGE); };'
                                               ));
    (document.body || document.head || document.documentElement).appendChild(script);

    console.log('YMK in injectScript _current_page ' + script.getAttribute('_current_page'));
    console.log('YMK in injectScript _total_page ' + script.getAttribute('_total_page'));

    script.remove();
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
