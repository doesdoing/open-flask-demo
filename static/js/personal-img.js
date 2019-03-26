function chooseImg(file) {
    var file = file.files[0];
    if (!/image\/\w+/.test(file.type)) {
        alert('上传的不是图片');
        return false;
    } else {
        var imgSize = file.size;
        console.log(imgSize);
        if (imgSize > 1 * 1024 * 1024) {
            alert('上传的图片的大于1M,请重新选择');
            $(this).val('');
            return false;
        }else{
            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                var img = document.getElementById('img');
                img.src = this.result;
            };
        }
    }
}