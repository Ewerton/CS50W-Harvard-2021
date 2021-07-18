/// If theres a file uploaded in the input, renders it an img control (imgElemID)
function PreviewUploadedImage(input, imgElemID) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#'+imgElemID)
                .attr('src', e.target.result)
                .width(250)
                .height(250);
        };

        reader.readAsDataURL(input.files[0]);
    }
}