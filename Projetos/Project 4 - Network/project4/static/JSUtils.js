$(document).ready(function () {
	// Handles the click to Follow a User
	$("button[name='btnFollow']").click(function (event) {
		var useridToFollow = $(this).data("useridtofollow");
		var loggedUserId = $(this).data("loggeduserid");
		FollowUser(useridToFollow, loggedUserId);
	});

	// Toggles the style of the Follow button when the mouse hovers over it
	$("button[name='btnFollow']").hover(
		function () {
			if ($(this).html().includes("Following")) {
				SetUnfollowStyle($(this));
			}
			if ($(this).html().includes("Follow")) {
				SetFollowStyle($(this));
			}
		},
		function () {
			// Removes the 'Unfollow' style
			if ($(this).html().includes("Unfollow")) {
				SetUnfollowingStyle($(this));
			}
			if ($(this).html().includes("Follow")) {
				SetFollowStyle($(this));
			}
		}
	);

	//reload_navbar();
	//reload_user_profile();
	//reload_who_to_follow();
});

function SetFollowStyle(elem) {
	// Applies the 'Following' style
	//elem.html("Follow");
	elem.css("background-color", "");
}

function SetUnfollowingStyle(elem) {
	// Applies the 'Following' style
	elem.html("Following");
	elem.css("background-color", "");
}

function SetUnfollowStyle(elem) {
	// Applies the 'Unfollow' style
	elem.html("Unfollow");
	elem.css("background-color", "#CA2355");

}

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

function Reload_user_profile() {
	$.ajax({
		url: "/get_profilecard",
		type: "GET",
		success: function (data) {
			$(".profilecard_placeholder").html(data);
		},
	});
}

function Reload_navbar() {}

function Reload_who_to_follow() {
	$.ajax({
		url: "/get_whotofollow",
		type: "GET",
		success: function (data) {
			$(".whotofollow_placeholder").html(data);
		},
	});
}

function FollowUser(userIdToFollow) {
	var btn = $("button[data-useridtofollow='" + userIdToFollow + "']");
	$.ajax({
		url: "/follow_unfollow",
		type: "POST",
		data: { user_id_to_follow: userIdToFollow },
		success: function (data) {
			if (data.operation === "follow") {
				btn.html("Following"); // Its following so i set the text to "Unfollow"
			}
			if (data.operation === "unfollow") {
				btn.html("Follow"); // Its not following so i set the text to the normal "Follow" text
			}
		},
		error: function (data) {
			console.log("Error: " + data.responseText);
		},
	});
}




/**** Utilities function ****/
function addClass(elem, clazz) {
	if (!elemHasClass(elem, clazz)) {
		elem.className += " " + clazz;
	}
}

function removeClass(elem, clazz) {
	if (elemHasClass(elem, clazz)) {
		elem.classList.remove(clazz);
	}
}

function elemHasClass(elem, clazz) {
	return new RegExp("( |^)" + clazz + "( |$)").test(elem.className);
}
