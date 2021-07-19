$(document).ready(function () {
	// $(".testAjax").click(function () {
	// 	reload_user_profile();
	// });

	//reload_navbar();
	//reload_user_profile();
	//reload_who_to_follow();
});

/// If theres a file uploaded in the input, renders it an img control (imgElemID)
function PreviewUploadedImage(input, imgElemID) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$("#" + imgElemID)
				.attr("src", e.target.result)
				.width(250)
				.height(250);
		};

		reader.readAsDataURL(input.files[0]);
	}
}

function reload_user_profile() {
	$.ajax({
		url: "/get_profilecard",
		type: "GET",
		success: function (data) {
			$(".profilecard_placeholder").html(data);
		},
	});
}

function reload_navbar() {}

function reload_who_to_follow() {
    $.ajax({
		url: "/get_whotofollow",
		type: "GET",
		success: function (data) {
			$(".whotofollow_placeholder").html(data);
		},
	});
}
