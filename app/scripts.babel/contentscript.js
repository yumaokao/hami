'use strict';
var DEBUG = false;
var STEPS = 4;

window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
if (window == top) {
	window.addEventListener('keyup', doKeyPress, false); //add the keyboard handler
}

function doKeyPress(e) {
    if (DEBUG)
        console.log('YMK in doKeyPress keyCode ' + e.keyCode);

	if (e.keyCode == 71) { 'g'
        var books = document.getElementsByClassName('box_in');
        /* if (books.length > 0) {
            var evt = mouseEvent('click');
            dispatchEvent(books[0], evt);
        } */
    } else if (e.keyCode == 78) {  // 'n'
        executeScript('turnPage( _PAGE_TYPE2 ? true : false);');
    } else if (e.keyCode == 80) {  // 'p'
        executeScript('turnPage( _PAGE_TYPE2 ? false : true);');
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

        var pages = getVariablesScript();
        var fancies = document.getElementsByClassName('viewer morning');
        var draggables = document.getElementsByClassName('ui-draggable');

        var current_page = parseInt(pages.current_page);
        var total_page = parseInt(pages.total_page);
        var viewer;
        var width_range = 0;
        var height_range = 0;
        var cur_left = 0;
        var cur_top = 0;

        if (DEBUG) {
            console.log('YMK current_page ' + current_page);
            console.log('YMK total_page ' + total_page);
        }

        if (fancies.length > 0 && draggables.length === total_page) {
            var fancy = fancies[0];
            viewer = draggables[current_page - 1];
            if (viewer.children.length > 0 && viewer.children[0].children.length > 0) {
                var img = viewer.children[0].children[0];
                if (img.tagName == 'IMG') {
                    width_range = parseInt(img.style.width) - fancy.offsetWidth;
                    height_range = parseInt(img.style.height) - fancy.offsetHeight;
                }
                cur_left = parseInt(viewer.style.left);
                cur_top = parseInt(viewer.style.top);
            }
        }


        switch (e.keyCode) {
            case 74:
                // cur_top = 0 - height_range;
                cur_top = cur_top - (height_range / STEPS);
                cur_top = cur_top > (0 - height_range) ? cur_top : (0 - height_range);
                break;
            case 75:
                // cur_top = 0;
                cur_top = cur_top + (height_range / STEPS);
                cur_top = cur_top > 0 ? 0 : cur_top;
                break;
            case 72:
                // cur_left = 0;
                cur_left = cur_left + (width_range / STEPS);
                cur_left = cur_left > 0 ? 0 : cur_left;
                break;
            case 76:
                // cur_left = 0 - width_range;
                cur_left = cur_left - (width_range / STEPS);
                cur_left = cur_left > (0 - width_range) ? cur_left : (0 - width_range);
                break;
        }

        if (DEBUG) {
            console.log('YMK set cur_left ' + cur_left);
            console.log('YMK set cur_top ' + cur_top);
        }

        viewer.style.left = cur_left + 'px';
        viewer.style.top = cur_top + 'px';
    }
}

function executeScript(text) {
    var ret = {};
    var script = document.createElement('script');
    script.id = '_hamibook-scroll'
    script.appendChild(document.createTextNode(text));
    (document.body || document.head || document.documentElement).appendChild(script);
    script.remove();
    return ret;
}

function getVariablesScript() {
    var ret = {};
    var script = document.createElement('script');
    script.id = '_hamibook-scroll'
    script.appendChild(document.createTextNode('var s = document.getElementById("_hamibook-scroll");'
                                               + 'if (s !== undefined) { s.setAttribute("_current_page", _CURRENT_PAGE); };'
                                               + 'if (s !== undefined) { s.setAttribute("_total_page", _TOTAL_PAGE); };'
                                               ));
    (document.body || document.head || document.documentElement).appendChild(script);

    // console.log('YMK in injectScript _current_page ' + script.getAttribute('_current_page'));
    // console.log('YMK in injectScript _total_page ' + script.getAttribute('_total_page'));

    ret.current_page = script.getAttribute('_current_page');
    ret.total_page = script.getAttribute('_total_page');

    script.remove();

    return ret;
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
