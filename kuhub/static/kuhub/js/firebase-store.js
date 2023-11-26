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

const fileUploadForm = document.getElementById("file-upload-form");
const fileInput = document.getElementById("file-upload-input");
const submitButton = document.getElementById("button_post");

function cleanFileName(filename) {
    // Replace spaces with underscores and remove parentheses
    return filename.replace(/\s+/g, '_').replace(/[()]/g, '');
}

fileUploadForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const file = fileInput.files[0];
    if (file) {
        console.log(file);

        // Clean the file name
        const cleanedFileName = cleanFileName(file.name);
        console.log(cleanedFileName);

        // Use the cleaned file name for the Firebase storage reference
        const fileref = ref(storage, 'summary-file/' + cleanedFileName);

        submitButton.disabled = true;
        submitButton.value = 'Uploading...';

        uploadBytes(fileref, file).then((result) => {
            alert("File uploaded successfully!");
            fileUploadForm.submit();
        }).catch((error) => {
            alert("Error during file upload: " + error.message);
            submitButton.disabled = false;
            submitButton.value = 'Post';
        });
    } else {
        alert("No file selected!");
    }
});


