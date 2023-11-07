document.getElementById("id_tag_name").addEventListener("change", function() {
    var selected_tag = this.value;
    var file_upload = document.getElementById("file-upload-container");

    if (selected_tag === "Summary-Hub") {
        file_upload.style.display = "block";
    } else {
        file_upload.style.display = "none";
    }

});

document.getElementById("file-upload-form").addEventListener("change", function(event) {
    var file_input = document.getElementById("file-upload-input");
    var submit_button = document.getElementById("button_post");

    if (document.getElementById("file-upload-container").style.display === "block"
        && file_input.files.length === 0) {
        submit_button.disabled = true;
    } else {
        submit_button.disabled = false;
    }
});
