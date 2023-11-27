import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getStorage, ref, uploadBytes } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-storage.js";

const firebaseConfig = {
    apiKey: "AIzaSyBwV28WvuaYFGPGhW3pGv3nhZZq_gdVpcY",
    authDomain: "ku-hub-76621.firebaseapp.com",
    projectId: "ku-hub-76621",
    storageBucket: "ku-hub-76621.appspot.com",
    messagingSenderId: "493628516213",
    appId: "1:493628516213:web:b0af6e5f779ed07896953c",
    measurementId: "G-QDN5PB162J"
};

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

const fileInput = document.getElementById("id_display_photo"); // Update this ID to match your file input
const fileUploadForm = document.getElementById("profile-edit-form");
const submitButton = document.getElementById("button_save");

fileUploadForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const file = fileInput.files[0];

    if (file) {
        const cleanedFileName = cleanFileName(file.name);
        const fileref = ref(storage, 'profile/' + cleanedFileName);

        submitButton.disabled = true;
        submitButton.value = 'Uploading...';

        uploadBytes(fileref, file).then((result) => {
            alert("File uploaded successfully!");

            // Set the hidden input's value to the cleaned file name
            const displayPhotoUrlInput = document.getElementById("id_display_photo_url");
            displayPhotoUrlInput.value = cleanedFileName;

            fileUploadForm.submit();    // Submit the form after file upload
        }).catch((error) => {
            alert("Error during file upload: " + error.message);
            submitButton.disabled = false;
            submitButton.value = 'Save';
        });
    } else {
        fileUploadForm.submit();
    }
});


function cleanFileName(filename) {
    return filename.replace(/\s+/g, '_').replace(/[()]/g, '');
}