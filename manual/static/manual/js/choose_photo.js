function selectPhoto() {
    nextBtn.disabled = false;
}

const nextBtn = document.getElementById("photo-next");
nextBtn.disabled = true;

const radioBtns = document.getElementsByClassName("photo-radio");
for (let i = 0; i < radioBtns.length; i++) {
    radioBtns[i].checked = false;
}

// const choosePhotos = Array.from(document.getElementsByClassName("photo-img"));

// async function loadPhotos() {
//     let domain = "https://d0cb-91-238-229-3.ngrok-free.app";
//     let url = `${domain}/get-photos`;
//     let response = await fetch(url);
//     let photos = await response.json();

//     for(let i = 0; i < photos.length; i++) {
//         photos[i] = domain + "/" + photos[i];
//         choosePhotos[i].src = photos[i];
//         alert(choosePhotos[i].src);
//     }
// }

// loadPhotos();
