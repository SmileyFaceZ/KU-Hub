document.getElementById("id_tag_name").addEventListener("change", function() {
    var selectedTag = this.value;
    var fileUploadContainer = document.getElementById("file-upload-container");

    if (selectedTag === "Summary-Hub") {
        fileUploadContainer.style.display = "block";
    } else {
        fileUploadContainer.style.display = "none";
    }
});