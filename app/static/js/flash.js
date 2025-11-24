const flashes = document.querySelectorAll('.flash');
let offset = 80;
function offsetFlashMessages() {
    flashes.forEach(flash => {
        flash.style.position = 'fixed';
        flash.style.top = offset + 'px';
        flash.style.left = '20px';
        offset += flash.offsetHeight + 10;
    });
}

offsetFlashMessages()
