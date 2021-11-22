function getKey(e) {
    var location = e.location;
    var selector;
    if (location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
        selector = ['[data-key="' + e.keyCode + '-R"]'];
    } else {
        var code = e.keyCode || e.which;
        selector = [
            '[data-key="' + code + '"]',
            '[data-char*="' +
                encodeURIComponent(String.fromCharCode(code)) +
                '"]',
        ].join(",");
    }
    return document.querySelector(selector);
}

function pressKey(char) {
    var key = document.querySelector(
        '[data-char*="' + char.toUpperCase() + '"]'
    );
    if (!key) {
        return console.warn("No key for", char);
    }
    key.setAttribute("data-pressed", "on");
    setTimeout(function () {
        key.removeAttribute("data-pressed");
    }, 200);
}

var h1 = document.querySelector("h1");
var originalQueue = h1.innerHTML;
var queue = h1.innerHTML;

function next() {
    var c = queue[0];
    queue = queue.slice(1);
    h1.innerHTML = originalQueue.slice(0, originalQueue.length - queue.length);
    pressKey(c);
    if (queue.length) {
        setTimeout(next, Math.random() * 200 + 50);
    }
}

h1.innerHTML = "&nbsp;";
setTimeout(next, 500);

document.body.addEventListener("keydown", function (e) {
    var key = getKey(e);
    if (!key) {
        return console.warn("No key for", e.keyCode);
    }

    key.setAttribute("data-pressed", "on");
});

document.body.addEventListener("keyup", function (e) {
    var key = getKey(e);
    key && key.removeAttribute("data-pressed");
});

function size() {
    var size = keyboard.parentNode.clientWidth / 90;
    keyboard.style.fontSize = size + "px";
    console.log(size);
}

var keyboard = document.querySelector(".keyboard");
window.addEventListener("resize", function (e) {
    size();
});
size();

function change(text) {
    var sentence = document.getElementById("text-input").value;

    console.log(typeof sentence);

    if (sentence.slice(-1) == " " || sentence.length == 0) {
        sentence += text;
        sentence += " ";
    } else {
        console.log("hey");
        sentence = sentence.substring(0, sentence.lastIndexOf(" "));
        if (sentence.length != 0) {
            sentence += " ";
        }
        sentence += text;
        sentence += " ";
    }

    document.getElementById("text-input").value = sentence;
    getword(sentence);
    document.getElementById("text-input").focus();
}

document.getElementById("box1").onclick = function () {
    const text = document.getElementById("box1").innerHTML;
    change(text);
};
document.getElementById("box2").onclick = function () {
    const text = document.getElementById("box2").innerHTML;
    change(text);
};
document.getElementById("box3").onclick = function () {
    const text = document.getElementById("box3").innerHTML;
    change(text);
};
