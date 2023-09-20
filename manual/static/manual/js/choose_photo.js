function selectPhoto() {
    nextBtn.disabled = false;
}

const nextBtn = document.getElementById("photo-next");
nextBtn.disabled = true;

const radioBtns = document.getElementsByClassName("photo-radio");
for (let i = 0; i < radioBtns.length; i++) {
    radioBtns[i].checked = false;
}

const choosePhotos = Array.from(document.getElementsByClassName("photo-img"));

// let url = `https://example_url`;
// let response = await fetch(url);

// let photos = await response.json();

// for(let i = 0; i < photos.lenght; i++) {
//      choosePhotos[i].src = photos[i];
// }