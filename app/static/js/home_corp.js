let profile_modal = document.querySelector(".profile-modal");
let drop_zone = document.getElementById("drop-zone");
let pfp_input = document.getElementById("pfp-input");

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

openFileSelectorOnClick();
detectDragOver();
detectDragLeave();
showPreviewOnSelectedFile();
showPreviewOnDragedFile();
