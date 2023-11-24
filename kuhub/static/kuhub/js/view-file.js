import { initializeApp } from "https://www.gstatic.com/firebasejs/9.2.0/firebase-app.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/9.2.0/firebase-storage.js";
import firebaseConfig from "./config.js";

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

const fileUpload = document.getElementById("file-upload-input");

fileUpload.addEventListener("change", function(event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileref = ref(storage, file.name);
        uploadFileAndCreateViewButton(fileref, file);
    }
});

function uploadFileAndCreateViewButton(fileref, file) {
    uploadBytes(fileref, file)
        .then((snapshot) => {
            return getDownloadURL(snapshot.ref);
        })
        .then((downloadURL) => {
            console.log("File available at", downloadURL);
            createViewButton(downloadURL);
        })
        .catch((error) => {
            console.log("Error uploading file:", error);
        });
}

function createViewButton(downloadURL) {
    const button = document.createElement("button");
    button.textContent = "View File";
    button.addEventListener("click", function() {
        window.open(downloadURL, '_blank');
    });

    // Append the button to a specific element in your HTML
    // For example, append to the container of the file upload input
    fileUpload.parentNode.appendChild(button);
}
