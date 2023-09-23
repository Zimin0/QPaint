function openInfo() {
    oldHeadTitle.style.display = "none";
    newHeadTitle.style.display = "block";

    uploadInvite.style.display = "none";
    photoInfo.style.display = "flex";

    backBtn.style.display = "none";
    uploadBlock.style.display = "block";
}

function openCrop(event) {
    newHeadTitle.style.display = "none";
    colorsTitle.style.display = "flex";

    photoInfo.style.display = "none";
    cropBlock.style.display = "flex";

    uploadBlock.style.display = "none";

    let target = event.target;

    if (!FileReader) {
        alert('FileReader не поддерживается :(');
        return;
    }

    if (!target.files.length) {
        alert('Ничего не загружено!');
        return;
    }

    let fileReader = new FileReader();
    fileReader.onload = function () {
        cropImg.src = fileReader.result;

        cropper = new Cropper(cropImg, {
            aspectRatio: 30 / 40,
            viewMode: 1,
            dragMode: "move"
        });
    }

    fileReader.readAsDataURL(target.files[0]);
}


// Добавляет в input новый файл картинки // 
function sendCroppedImgAndSubmit(button) {
    // Обработка и обрезка изображения
    cropper.getCroppedCanvas({imageSmoothingEnabled: true}).toBlob((blob) => {
        var dt = new DataTransfer();
        var file = new File([blob], "cropped_photo.png", { type: 'image/png'}, 1);
        dt.items.add(file);
        var file_list = dt.files;
        var cropInput = document.getElementById("cropped-photo");
        cropInput.files = file_list;

        // Отправляем форму с задержкой в 3 секунды после обработки изображения
        setTimeout(function() {
            document.getElementById("upload-photo-form").submit();
        }, 50); 
    });

    // Скрываем текст кнопки и показываем объект загрузки
    displayLoadingAnimation(button);
}


// Отображает анимацию загрузки // 
function displayLoadingAnimation(button){
    button.style.display = "none";
    let loadingIcon = document.getElementById("loading-icon");
    loadingIcon.style.display = "inline-block"; // покажем объект загрузки
}


const oldHeadTitle = document.getElementById("old-header-title");
const newHeadTitle = document.getElementById("new-header-title");
const colorsTitle = document.getElementById("colors-title");

const uploadInvite = document.getElementById("upload-invite");
const photoInfo = document.getElementById("photo-info");
const cropBlock = document.getElementById("cropper-block");

const backBtn = document.getElementById("upload-back");
const uploadBlock = document.getElementById("upload-block");

newHeadTitle.style.display = "none";
colorsTitle.style.display = "none";
photoInfo.style.display = "none";
cropBlock.style.display = "none";
uploadBlock.style.display = "none";

const cropImg = document.getElementById('crop-img');

const cropInput = document.getElementById('cropped-photo');
cropInput.value = null;