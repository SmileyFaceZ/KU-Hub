import { initializeApp } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import { getStorage, ref, uploadBytes } from "https://www.gstatic.com/firebasejs/10.6.0/firebase-storage.js";
import { firebaseConfig } from "./firebase-config.js";

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);

const fileUpload = document.getElementById("file-upload-input");
fileUpload.addEventListener("change", function(event) {
    const file = event.target.files[0];
    console.log(file);
    const fileref = ref(storage, file.name)
    uploadBytes(fileref, file)
        .then((result) => {
            alert("File uploaded successfully!");
    });
});

const fileref = ref(storage, file.name)

fileref.getDownloadURL().then(function(url) {
    document.getElementById("viewer").src = url;
}).catch(function(error) {
    console.error("Error getting download URL: ", error);
});
