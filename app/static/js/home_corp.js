let profile_modal = document.querySelector(".profile-modal");
let drop_zone = document.getElementById("drop-zone");
let pfp_input = document.getElementById("pfp-input");
let user_input = document.getElementById('user_name');

function openProfileModal() {
    profile_modal.showModal();
}
function closeProfileModal() {
    profile_modal.close();
}

function detectDragOver() {
    drop_zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        drop_zone.classList.add('dragover');
    });
}

function detectDragLeave() {
    drop_zone.addEventListener('dragleave', () => {
        drop_zone.classList.remove('dragover');
    });
}

function openFileSelectorOnClick() {
    drop_zone.addEventListener("click", () => pfp_input.click())
}

function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        console.log(e.target.result);
        drop_zone.innerHTML = '<img src="' + e.target.result + '" class="profile-picture" />';
    };
    reader.readAsDataURL(file);
}

function showPreviewOnSelectedFile() {

    pfp_input.addEventListener('change', () => {
        const file = pfp_input.files[0];
        if (file) showPreview(file);
    });
}

function showPreviewOnDragedFile() {
    drop_zone.addEventListener('drop', (e) => {
        e.preventDefault();
        drop_zone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            pfp_input.files = e.dataTransfer.files;
            showPreview(file);
        }
    });
}

function sanitizeUserInput(value) {
    return value
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toUpperCase()
        .replace(/[^A-Z ]/g, '');
}

function dinamicalyFormatUserInput() {
    user_input.addEventListener('input', () => {
        const cleaned = sanitizeUserInput(user_input.value);

        if (cleaned !== user_input.value) {
            const pos = user_input.selectionStart;
            user_input.value = cleaned;
            user_input.setSelectionRange(pos, pos);
        }

        if (user_input.validity.patternMismatch) {
            user_input.setCustomValidity('Use apenas letras (A–Z) e espaços');
        } else {
            user_input.setCustomValidity('');
        }
    });
}

function formatPasteInput(inputEl) {
    inputEl.addEventListener('paste', async (e) => {
        e.preventDefault();

        let text = e.clipboardData && e.clipboardData.getData
            ? e.clipboardData.getData('text')
            : '';

        if (!text && navigator.clipboard && navigator.clipboard.readText) {
            try {
                text = await navigator.clipboard.readText();
            } catch (err) {
                console.error('Não foi possível ler a área de transferência:', err);
            }
        }

        const sanitized = sanitizeUserInput(text);
        const start = inputEl.selectionStart ?? inputEl.value.length;
        const end = inputEl.selectionEnd ?? inputEl.value.length;
        const value = inputEl.value;

        inputEl.value = value.slice(0, start) + sanitized + value.slice(end);

        const caret = start + sanitized.length;
        inputEl.setSelectionRange(caret, caret);
    });
}


openFileSelectorOnClick();
detectDragOver();
detectDragLeave();
showPreviewOnSelectedFile();
showPreviewOnDragedFile();
dinamicalyFormatUserInput()
formatPasteInput()