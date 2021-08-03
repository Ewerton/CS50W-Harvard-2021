const home_url = "/"

$(document).ready(function () {
	// Handles the click to delete a post
	$(".deletePost").click(function (event) {
		var tweetId = $(this).data("tweetid");
		DeletePost(tweetId);
	});

	// Handles the click to edit a post
	$(".updatePost").click(function (event) {
		var tweetId = $(this).data("tweetid");
		UpdatePost(tweetId);
	});

	$(".newPost").click(function (event) {
		NewPost();
	});

	// Handles the click to edit a post
	$(".likePost").click(function (event) {
		var postId = $(this).data("postid");
		LikePost(postId);
	});

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
		},
		function () {
			// Removes the 'Unfollow' style
			if ($(this).html().includes("Unfollow")) {
				SetFollowingStyle($(this));
			}
		}
	);

	//reload_navbar();
	//reload_user_profile();
	//reload_who_to_follow();
});

function SetFollowStyle(elem) {
	// Applies the 'Following' style
	elem.css("background-color", "");
	elem.css("color", "#1DA1F2");
	removeClass(elem, "btn-primary");
	addClass(elem, "btn-outline-primary");
}

function SetFollowingStyle(elem) {
	// Applies the 'Following' style
	elem.html("Following");
	elem.css("color", "#FFF");
	elem.css("background-color", "#1DA1F2");
	removeClass(elem, "btn-outline-primary");
 	addClass(elem, "btn-primary");
}

function SetUnfollowStyle(elem) {
	// Applies the 'Unfollow' style
	elem.html("Unfollow");
	elem.css("background-color", "#CA2355");
	elem.css("color", "#FFF");
	removeClass(elem, "btn-outline-primary");
 	addClass(elem, "btn-primary");
	
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
				// Its following so i set the text and style to "Unfollow"
				btn.html("Following");
				SetFollowingStyle(btn);
			}
			if (data.operation === "unfollow") {
				// Its not following anymore so i set the text and style to the normal "Follow" text
				btn.html("Follow"); 
				SetFollowStyle(btn);
			}

			Reload_user_profile();
		},
		error: function (data) {
			console.log("Error: " + data.responseText);
		},
	});
}

function DeletePost(tweetId) {
	if (tweetId > 0) {
		Swal.fire({
			title: "Delete Tweet?",
			text: "This can’t be undone and it will be removed from your profile, the timeline of any accounts that follow you, and from Twitter search results.",
			showCancelButton: true,
			confirmButtonColor: "#e02460",
			confirmButtonText: "Delete",
		}).then((result) => {
			if (result.isConfirmed) {
				$.ajax({
					url: "/post/" + tweetId + "/del",
					type: "DELETE",
					success: function (data) {
						Swal.fire("Deleted!", "Your tweet has been deleted.", "success");
						//location.reload();
						window.location.href = home_url ; //reloads the home
					},
					error: function (data) {
						console.log("Error: " + data.responseText);
					},
				});
			}
		});
	}
}

function NewPost(tweetId) {
		$.ajax({
			url: "/post/save",
			type: "GET",
			success: function (data) {
				Swal.fire({
					html: data,
					showCancelButton: false, 
					showConfirmButton: false,
					showCloseButton: true
				  });
			},
	});
}

function UpdatePost(tweetId) {
	if (tweetId > 0) {
		$.ajax({
			url: "/post/" + tweetId + "/update",
			type: "GET",
			success: function (data) {
				Swal.fire({
					html: data,
					showCancelButton: false, 
					showConfirmButton: false,
					showCloseButton: true
				  });
			},
		});
	}
}

function LikePost(postId) {
	if (postId > 0) {
		$.ajax({
			url: "/post/" + postId + "/like/",
			type: "POST",
			data: { postid_to_like: postId },
			success: function (data) {
				if (data.operation === "liked") {
					SetLiked(postId);
				}
				if (data.operation === "unliked") {
					SetUnliked(postId);
				}
			},
			error: function (data) {
				console.log("Error: " + data.responseText);
			},
		});
	}
}

function SetLiked(postId){
	var likeIcon = $("#likeIcon"+postId);
	likeIcon.removeClass("far");
	likeIcon.addClass("fas");

	var likeCountSpan = $(".likeCount" + postId);
	likeCount = parseInt(likeCountSpan.text());
	likeCount ++;
	likeCountSpan.text(likeCount);
}

function SetUnliked(postId){
	var likeIcon = $("#likeIcon"+postId);
	likeIcon.removeClass("fas");
	likeIcon.addClass("far");

	var likeCountSpan = $(".likeCount" + postId);
	likeCount = parseInt(likeCountSpan.text());
	likeCount --;
	likeCountSpan.text(likeCount);
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
