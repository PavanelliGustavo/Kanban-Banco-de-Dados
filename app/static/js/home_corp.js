let profile_modal = document.querySelector(".profile-modal");

function openProfileModal(){
    profile_modal.showModal();
}
function closeProfileModal(){
    profile_modal.close();
}

profile_modal.addEventListener("click", (event) => {
    const rect = profile_modal.getBoundingClientRect();
    const in_profile_modal =
        event.clientX >= rect.left &&
        event.clientX <= rect.right &&
        event.clientY >= rect.top &&
        event.clientY <= rect.bottom;

    if (!in_profile_modal) {
        closeProfileModal();
    }
});
