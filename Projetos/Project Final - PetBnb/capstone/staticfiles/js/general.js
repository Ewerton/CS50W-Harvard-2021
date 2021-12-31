(function ($) {
	"use strict";

	/*======== 0 PRELOADER ========*/
	$(window).on("load", function () {
		$("#preloader").fadeOut(500);
	});

	/*======== 1. MENUZORD ========*/
	var menuzord = $("#menuzord");
	if (menuzord.length != 0) {
		menuzord.menuzord({
			indicatorFirstLevel: "",
			indicatorSecondLevel: "",
			align: "right",
		});
	}

	/*======== 2. NAVBAR ========*/
	$(window).on("load", function () {
		$(".scrolling").on("click", function (e) {
			e.preventDefault();
			e.stopPropagation();
			$(".navbar-collapse").removeClass("show");
			var target = $(this).attr("href");
			$(target).velocity("scroll", {
				duration: 800,
				offset: -50,
				easing: "easeOutExpo",
				mobileHA: false,
			});
		});

		var header_area = $(".header");
		var main_area = header_area.find(".nav-menuzord");
		var zero = 0;
		var navbarSticky = $(".navbar-sticky");

		$(window).scroll(function () {
			var st = $(this).scrollTop();
			if (st > zero) {
				navbarSticky.addClass("navbar-scrollUp");
			} else {
				navbarSticky.removeClass("navbar-scrollUp");
			}
			zero = st;

			if (main_area.hasClass("navbar-sticky") && ($(this).scrollTop() <= 600 || $(this).width() <= 300)) {
				main_area.removeClass("navbar-scrollUp");
				main_area.removeClass("navbar-sticky").appendTo(header_area);
				header_area.css("height", "auto");
			} else if (!main_area.hasClass("navbar-sticky") && $(this).width() > 300 && $(this).scrollTop() > 600) {
				header_area.css("height", header_area.height());
				main_area.addClass("navbar-scrollUp");
				main_area.css({ opacity: "0" }).addClass("navbar-sticky");
				main_area.appendTo($("body")).animate({ opacity: 1 });
			}
		});

		$(window).trigger("resize");
		$(window).trigger("scroll");
	});

	/*======== 3. SELECTRIC ========*/
	var selectLocation = $(".select-location");
	if (selectLocation.length !== 0) {
		ApplySeletric(selectLocation);
	}

	function ApplySeletric(elem) {
		elem.selectric({
			arrowButtonMarkup: '<div class="arrow-button"><i class="fa fa-angle-down" aria-hidden="true"></i></div>',
		});
	}

	/*======== 4. TOOLTIP ========*/
	var dataTooltip = $('[data-toggle="tooltip"]');
	if (dataTooltip !== 0) {
		dataTooltip.tooltip();
	}

	/*======== 6. OWL CAROSEL ========*/
	//Popular Listing
	// var populerListing = $(".popular-listing");
	// if (populerListing.length !== 0) {
	// 	populerListing.owlCarousel({
	// 		loop: true,
	// 		autoplay: true,
	// 		lazyLoad: true,
	// 		margin: 30,
	// 		dots: false,
	// 		nav: true,
	// 		navText: [
	// 			'<i class="fas fa-chevron-left " aria-hidden="true"></i>',
	// 			'<i class="fas fa-chevron-right" aria-hidden="true"></i>',
	// 		],
	// 		responsive: {
	// 			320: {
	// 				slideBy: 1,
	// 				items: 1,
	// 			},
	// 			768: {
	// 				slideBy: 1,
	// 				items: 2,
	// 			},
	// 			992: {
	// 				slideBy: 1,
	// 				items: 3,
	// 			},
	// 		},
	// 	});
	// }
	// Testimonial
	// var testimonial = $(".testimonial");
	// if (testimonial.length !== 0) {
	// 	testimonial.owlCarousel({
	// 		center: true,
	// 		loop: true,
	// 		autoplay: true,
	// 		autoplayTimeout: 6000,
	// 		smartSpeed: 1000,
	// 		// rtl: true, //For RTL
	// 		responsive: {
	// 			320: {
	// 				slideBy: 1,
	// 				items: 1,
	// 			},
	// 			768: {
	// 				slideBy: 1,
	// 				items: 1,
	// 			},
	// 			992: {
	// 				slideBy: 1,
	// 				items: 3,
	// 			},
	// 		},
	// 	});
	// }
	// Brand Slider
	// var brandSlider = $(".brand-slider");
	// if (brandSlider.length != 0) {
	// 	brandSlider.owlCarousel({
	// 		loop: true,
	// 		margin: 28,
	// 		autoplay: true,
	// 		autoplayTimeout: 6000,
	// 		autoplayHoverPause: true,
	// 		nav: true,
	// 		navText: [
	// 			'<i class="fas fa-chevron-left " aria-hidden="true"></i>',
	// 			'<i class="fas fa-chevron-right" aria-hidden="true"></i>',
	// 		],
	// 		dots: false,
	// 		smartSpeed: 500,
	// 		// rtl: true, //For RTL
	// 		responsive: {
	// 			320: {
	// 				slideBy: 1,
	// 				items: 1,
	// 			},
	// 			768: {
	// 				slideBy: 1,
	// 				items: 3,
	// 			},
	// 			992: {
	// 				slideBy: 1,
	// 				items: 4,
	// 			},
	// 		},
	// 	});
	// }

	// Listing Details
	var listingDetails = $(".listing-details-carousel");

	if (listingDetails.length !== 0) {
		listingDetails.each(function () {
			var itemsQty = this.childElementCount;
			console.log(itemsQty);

			var qtd320 = 1; // always 1

			//For 768 pixels the quantity will be 4 or less than this when needed
			var qtd768 = 3;
			if (itemsQty < 3) {
				qtd768 = itemsQty; // 3 or less than this when needed
			}

			// For 992 pixels the quantity will be 4 or less than this when needed
			var qtd992 = 4;
			if (itemsQty < 4) {
				qtd992 = itemsQty;
			}

			$(this).owlCarousel({
				loop: true,
				autoplay: true,
				autoplayTimeout: 6000,
				autoplayHoverPause: true,
				items: itemsQty,
				nav: true,
				navText: [
					'<i class="fas fa-chevron-left " aria-hidden="true"></i>',
					'<i class="fas fa-chevron-right" aria-hidden="true"></i>',
				],
				dots: false,
				responsive: {
					320: {
						slideBy: 1,
						items: qtd320,
						// nav: false,
					},
					768: {
						slideBy: 1,
						items: qtd768,
					},
					992: {
						slideBy: 1,
						items: qtd992,
					},
				},
			});
		});
	}

	// Blog Carousel
	// var blogCarousel = $(".blog-carousel");
	// if (blogCarousel.length !== 0) {
	// 	blogCarousel.owlCarousel({
	// 		loop: true,
	// 		autoplay: true,
	// 		autoplayTimeout: 6000,
	// 		autoplayHoverPause: true,
	// 		items: 1,
	// 		nav: true,
	// 		navText: [
	// 			'<i class="fas fa-chevron-left " aria-hidden="true"></i>',
	// 			'<i class="fas fa-chevron-right" aria-hidden="true"></i>',
	// 		],
	// 		dots: false,
	// 	});
	// }

	/*======== 7. COUNTER-UP ========*/
	var counter = $("#counter");
	if (counter.length !== 0) {
		var a = 0;
		$(window).scroll(function () {
			var oTop = counter.offset().top - window.innerHeight;
			if (a === 0 && $(window).scrollTop() > oTop) {
				$(".counter-value").each(function () {
					var $this = $(this),
						countTo = $this.attr("data-count");
					$({
						countNum: $this.text(),
					}).animate(
						{
							countNum: countTo,
						},
						{
							duration: 5000,
							easing: "swing",
							step: function () {
								$this.text(Math.floor(this.countNum));
							},
							complete: function () {
								$this.text(this.countNum);
							},
						}
					);
				});
				a = 1;
			}
		});
	}

	/*======== 8. BANNER ========*/
	// City Banner
	// var city_slider = $("#rev_slider_17_1");
	// if (city_slider.length !== 0) {
	// 	$("#rev_slider_17_1")
	// 		.show()
	// 		.revolution({
	// 			sliderType: "standard",
	// 			sliderLayout: "fullwidth",
	// 			dottedOverlay: "none",
	// 			delay: 9000,
	// 			navigation: {
	// 				onHoverStop: "off",
	// 			},
	// 			responsiveLevels: [1240, 1025, 778, 480],
	// 			visibilityLevels: [1240, 1025, 778, 480],
	// 			gridwidth: [1240, 1025, 778, 480],
	// 			gridheight: [600, 500, 450, 500],
	// 			lazyType: "smart",
	// 			shadow: 0,
	// 			spinner: "off",
	// 			stopLoop: "off",
	// 			stopAfterLoops: -1,
	// 			stopAtSlide: -1,
	// 			shuffle: "off",
	// 			autoHeight: "off",
	// 			disableProgressBar: "on",
	// 			hideThumbsOnMobile: "off",
	// 			hideSliderAtLimit: 0,
	// 			hideCaptionAtLimit: 0,
	// 			hideAllCaptionAtLilmit: 0,
	// 			debugMode: false,
	// 			fallbacks: {
	// 				simplifyAll: "off",
	// 				nextSlideOnWindowFocus: "off",
	// 				disableFocusListener: false,
	// 			},
	// 		});
	// }
	// Auto Mobile
	// var autoMobile = $("#rev_slider_14_1");
	// if (autoMobile.length !== 0) {
	// 	$("#rev_slider_14_1")
	// 		.show()
	// 		.revolution({
	// 			sliderType: "standard",
	// 			sliderLayout: "fullwidth",
	// 			dottedOverlay: "none",
	// 			delay: 9000,
	// 			navigation: {
	// 				onHoverStop: "off",
	// 			},
	// 			responsiveLevels: [1240, 1025, 778, 480],
	// 			visibilityLevels: [1240, 1025, 778, 480],
	// 			gridwidth: [1170, 992, 750, 450],
	// 			gridheight: [700, 700, 650, 550],
	// 			lazyType: "smart",
	// 			shadow: 0,
	// 			spinner: "off",
	// 			stopLoop: "off",
	// 			stopAfterLoops: -1,
	// 			stopAtSlide: -1,
	// 			shuffle: "off",
	// 			autoHeight: "off",
	// 			disableProgressBar: "on",
	// 			hideThumbsOnMobile: "off",
	// 			hideSliderAtLimit: 0,
	// 			hideCaptionAtLimit: 0,
	// 			hideAllCaptionAtLilmit: 0,
	// 			debugMode: false,
	// 			fallbacks: {
	// 				simplifyAll: "off",
	// 				nextSlideOnWindowFocus: "off",
	// 				disableFocusListener: false,
	// 			},
	// 		});
	// }

	/*======== 9. NEW CAR FILTERING ========*/
	// init Isotope
	var grid = $(".grid");
	if (grid.length != 0) {
		var $grid = grid.isotope({
			itemSelector: ".element-item",
			layoutMode: "fitRows",
		});
		// filter functions
		var filterFns = {
			// show if number is greater than 50
			numberGreaterThan50: function () {
				var number = $(this).find(".number").text();
				return parseInt(number, 10) > 50;
			},
			// show if name ends with -ium
			ium: function () {
				var name = $(this).find(".name").text();
				return name.match(/ium$/);
			},
		};

		// bind filter button click
		$("#filters").on("click", "button", function () {
			var filterValue = $(this).attr("data-filter");
			// use filterFn if matches value
			filterValue = filterFns[filterValue] || filterValue;
			$grid.isotope({ filter: filterValue });
		});

		// bind sort button click
		$("#sorts").on("click", "button", function () {
			var sortByValue = $(this).attr("data-sort-by");
			$grid.isotope({ sortBy: sortByValue });
		});

		// change is-checked class on buttons
		$(".button-group").each(function (i, buttonGroup) {
			var $buttonGroup = $(buttonGroup);
			$buttonGroup.on("click", "button", function () {
				$buttonGroup.find(".is-checked").removeClass("is-checked");
				$(this).addClass("is-checked");
			});
		});
		// layout Isotope after each image loads
		$grid.imagesLoaded().progress(function () {
			$grid.isotope("layout");
		});
	}

	/*======== 10.  RATING ========*/
	var ratingDefault = $(".add-rating-default");
	if (ratingDefault.length != 0) {
		ApplyRateYoDefault(ratingDefault);
	}

	function ApplyRateYoDefault(elem) {
		elem.rateYo({
			starWidth: "20px",
			//precision: 1,
			fullStar: true,
			spacing: "5px",
			starSvg:
				'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"/></svg>',

			onInit: function (rating, rateYoInstance) {
				console.log("RateYo initialized! with " + rating);
			},
			onSet: function (rating, rateYoInstance) {
				console.log("Rating is set to: " + rating);
			},
			// To get the current rating value
			//$(".add-rating-default").rateYo("rating")
		});
	}

	var readRatingDefault = $(".read-rating-default");
	if (readRatingDefault.length != 0) {
		ApplyRateYoMini(readRatingDefault);
	}

	function ApplyRateYoMini(elem) {
		elem.rateYo({
			starWidth: "12px",
			fullStar: true,
			spacing: "5px",
			readOnly: true,
			starSvg:
				'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"/></svg>',
		});
	}

	/*======== 11. DATERANGEPICKER ========*/
	var singleCalender = $(".single-date");
	if (singleCalender.length !== 0) {
		singleCalender.daterangepicker({
			singleDatePicker: true,
			opens: "left",
		});
	}
	var singleCalender = $(".single-date-left");
	if (singleCalender.length !== 0) {
		singleCalender.daterangepicker({
			singleDatePicker: true,
			// showDropdowns: true
		});

		singleCalender.val("");
	}
	var doubleCalender = $(".double-date");
	if (doubleCalender.length !== 0) {
		doubleCalender.daterangepicker({
			opens: "left",
		});
	}

	/*======== 12. QUANTITY ========*/
	// var incrBtn = $(".incr-btn");
	// if (incrBtn.length !== 0) {
	// 	$(".incr-btn").on("click", function (e) {
	// 		var newVal;
	// 		var $button = $(this);
	// 		var oldValue = $button.parent().find(".quantity").val();
	// 		$button.parent().find(".incr-btn[data-action=decrease]").removeClass("inactive");
	// 		if ($button.data("action") === "increase") {
	// 			newVal = parseFloat(oldValue) + 1;
	// 		} else {
	// 			// Don't allow decrementing below 1
	// 			if (oldValue > 1) {
	// 				newVal = parseFloat(oldValue) - 1;
	// 			} else {
	// 				newVal = 0;
	// 				$button.addClass("inactive");
	// 			}
	// 		}
	// 		$button.parent().find(".quantity").val(newVal);
	// 		e.preventDefault();
	// 	});
	// }

	/*======== 13. SIMPLE TIMER ========*/
	// var simple_timer = $(".simple_timer");
	// if (simple_timer.length != 0) {
	// 	simple_timer.syotimer({
	// 		year: 2021,
	// 		month: 9,
	// 		day: 9,
	// 		hour: 20,
	// 		minute: 30,
	// 	});
	// }

	/*======== 14. TOOLTIP ========*/
	var tooltip = $('[data-toggle="tooltip"]');
	if (tooltip.length != 0) {
		tooltip.tooltip();
	}

	/*======== 15. CLOSE BUTTON ========*/
	// var closeBtn = $(".close-btn");
	// if (closeBtn.length !== 0) {
	// 	closeBtn.click(function () {
	// 		$(this).parent().hide();
	// 	});
	// }

	/*======== 16. FORM CHECK READONLY ========*/
	// var formGroupCustom = $(".form-check-readonly");
	// if (formGroupCustom.length !== 0) {
	// 	var input = formGroupCustom.find(".form-check-input");

	// 	input.change(function () {
	// 		var formControl = $(this).parent().parent().find(".form-control");

	// 		if ($(this).prop("checked") === false) {
	// 			formControl.attr("readonly", true);
	// 		}
	// 		if ($(this).prop("checked") === true) {
	// 			formControl.removeAttr("readonly");
	// 		}
	// 	});
	// }


	// My Listing
	var tblServerReservations = $("#tblServerReservations");
	if (tblServerReservations.length !== 0) {
		tblServerReservations.DataTable({
			// language: {
			// 	paginate: {
			// 		previous: "Prev",
			// 	},
			// },
			paging: false,
			orderClasses: false,
			info: false,
			lengthChange: false,
			searching: false,
			//aoColumnDefs: [{ bSortable: false, aTargets: [-2, -1 ] }],
			columnDefs: [{ targets: [0, 1, 2, 3], sortable: false, orderable: false }],
			responsive: true,
			order: [[1, "desc "]],
		});
	}

	var tblBookingDetail = $("#tblBookingDetail");
	if (tblBookingDetail.length !== 0) {
		tblBookingDetail.DataTable({
			paging: false,
			orderClasses: false,
			info: false,
			lengthChange: false,
			searching: false,
			autoWidth: false,
			//aoColumnDefs: [{ bSortable: false, aTargets: [-2, -1 ] }],
			columnDefs: [
				{ targets: [0, 1, 2], sortable: false, orderable: false },
				{ targets: [0], width: "60% " },
			],
			//responsive: true,
			order: [[1, "desc "]],
		});
	}

	/*======== 17. REPLY BUTTON ========*/
	// var replyWrapper = $(".reply-wrapper");
	// if (replyWrapper.length !== 0) {
	// 	$(".btn-reply").on("click", function () {
	// 		// Shows the textarea and the reply button
	// 		$(this).parent().find($(".form-reply")).addClass("show");
	// 	});
	// }

	/*======== 17. SUBMIT REPLY BUTTON ========*/
	// var replyWrapper = $("button[name='submitReply']");
	// if (replyWrapper.length !== 0) {
	// 	$("button[name='submitReply']").on("click", function () {
	// 		var reviewId = $(this).data("reviewid");
	// 		console.log("clicou submitReply do review " + reviewId);
	// 		//PostReply(reviewId);
	// 	});
	// }

	

	/*======== 17. SUBMIT REVIEW BUTTON ========*/
	var btnSendReview = $("button[name='sendReview']");
	if (btnSendReview.length !== 0) {
		$("button[name='sendReview']").on("click", function () {
			var userReviewing = $(this).data("userreviewing");
			var userReviewed = $(this).data("userreviewed");
			var reviewText = $('textarea[name="txtReview"]').val();
			var bookingId = $("select[name='dates_review']").val();
			var number_of_stars = $(".add-rating-default").rateYo("rating");

			PostReview(userReviewing, userReviewed, reviewText, bookingId, number_of_stars);

			console.log(
				"clicou Send Review. UserReviewing: " +
					userReviewing +
					" UserReviewed: " +
					userReviewed +
					" ReviewText: " +
					reviewText +
					" BookingId: " +
					bookingId +
					" NumberOfStars: " +
					number_of_stars
			);
		});
	}

	/*======== 17. DELETE REVIEW BUTTON ========*/
	var deleteReviewButton = $("button[name='deleteReview']");
	if (deleteReviewButton.length !== 0) {
		$("button[name='deleteReview']").on("click", function () {
			var reviewId = $(this).data("reviewid");
			var userReviewed = $(this).data("userreviewed");
			console.log("clicou deleteReviewReply " + reviewId);
			console.log("User to reload: " + userReviewed);
			DeleteReview(reviewId, userReviewed);
		});
	}

	function DeleteReview(reviewId, userReviewed) {
		Swal.fire({
			title: "Are you sure?",
			showDenyButton: true,
			confirmButtonText: "Yes",
			denyButtonText: "No",
		}).then((result) => {
			if (result.isConfirmed) {
				$.ajax({
					url: "/booking/review/delete/" + reviewId + "/",
					method: "DELETE",
					data: {
						reviewId: reviewId,
						userReviewed: userReviewed,
					},
					success: function (response) {
						console.log(response);
						Reload_Reviews(userReviewed);
					},
					error: function (error) {
						console.log(error);
					},
				});
			} else if (result.isDenied) {
				//Swal.fire("Changes are not saved", "", "info");
			}
		});
	}

	function PostReview(userReviewing, userReviewed, reviewText, bookingId, number_of_stars) {
		if (reviewText.length <= 0) {
			Swal.fire({
				title: "Error!",
				text: "You need to write some review.",
				icon: "error",
				confirmButtonText: "OK",
			});
			return;
		}

		if (number_of_stars <= 0) {
			Swal.fire({
				title: "Error!",
				text: "You need to rate it from 1 to 5 stars.",
				icon: "error",
				confirmButtonText: "OK",
			});
			return;
		}

		if (userReviewing && userReviewed && bookingId && number_of_stars) {
			if (reviewText.length > 0) {
				$.ajax({
					url: "/booking/review/" + bookingId + "/",
					type: "POST",
					data: {
						userReviewing: userReviewing,
						userReviewed: userReviewed,
						reviewText: reviewText,
						bookingId: bookingId,
						number_of_stars: number_of_stars,
					},
					success: function (data) {
						// Reload the reviews section
						Reload_Reviews(userReviewed);
					},
					error: function (data) {
						console.log("Error: " + data.responseText);
					},
				});
			}
		}
	}

	function Reload_Reviews(userReviewed) {
		var reviews = $(".reviews_wrapper");

		if (reviews.length > 0) {
			$.ajax({
				url: "/booking/review/list/" + userReviewed,
				type: "GET",
				success: function (data) {
					reviews.html(data);

					// Reseting the review textarea
					$('textarea[name="txtReview"]').val("");

					// Resetting the Booking Date
					$("select[name='dates_review']").val();

					// Resetting the rating stars
					$(".add-rating-default").rateYo("rating", 0);

					// reapplying the DropDown styles
					var selectLocation = $(".select-location");
					if (selectLocation.length !== 0) {
						ApplySeletric(selectLocation);
					}

					// reapplying the rating styles
					var ratingDefault = $(".add-rating-default");
					if (ratingDefault.length != 0) {
						ApplyRateYoDefault(ratingDefault);
					}

					var readRatingDefault = $(".read-rating-default");
					if (readRatingDefault.length != 0) {
						ApplyRateYoMini(readRatingDefault);
					}

					// reattaching the click event to the reply button
					// $(".btn-reply").on("click", function () {
					// 	// Shows the textarea and the reply button
					// 	$(this).parent().find($(".form-reply")).addClass("show");
					// });

					// reattaching the click event to the delete button
					$("button[name='deleteReview']").on("click", function () {
						var reviewId = $(this).data("reviewid");
						var userReviewed = $(this).data("userreviewed");
						console.log("clicou deleteReviewReply " + reviewId);
						console.log("User to reload: " + userReviewed);
						DeleteReview(reviewId, userReviewed);
					});
				},
			});
		}
	}

	/*======== Secondary Navbar Active Link ========*/
	//$(document).ready(function() {
	jQuery(function () {
		var url = RemoveSlashAtEnd(window.location.href);

		var target = url.split("/");
		var target = RemoveEmptyElementsFromArray(target);
		var urlTarget = "/" + target.slice(-3).join("/"); // "/dashboard/something/something"

		$(".navbar-nav li a").each(function () {
			var linkUrl = RemoveSlashAtEnd($(this).attr("href"));

			if (linkUrl === urlTarget) {
				$(this).removeClass("active");
				$(this).removeClass("active").addClass("active");
			}
		});
	});
})(jQuery);

function EndsWith(str, suffix) {
	return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function RemoveSlashAtEnd(str) {
	if (EndsWith(str, "/")) {
		return str.substring(0, str.length - 1);
	}
	return str;
}

function RemoveEmptyElementsFromArray(array) {
	return array.filter(function (el) {
		if (el != null) {
			if (el != "") {
				return el;
			}
		}
	});
}

/**** FUNÇÕES UTILITARIAS ****/

/**
 * Adiciona uma classe CSS á um elemento ou lista de elementos
 * @param  {any} elem o elemento que receberá a classe CSS
 * @param  {string} clazz a classe CSS a ser adicionada
 */
function AddClass(elem, clazz) {
	if (elem && clazz) {
		if (EhColecao(elem)) {
			for (let i = 0; i < elem.length; i++) {
				if (!ElemHasClass(elem[i], clazz)) {
					elem[i].classList.add(clazz);
				}
			}
		} else {
			if (!ElemHasClass(elem, clazz)) {
				elem.classList.add(clazz);
			}
		}
	}
}

/**
 * Remove uma classe CSS de um elemento ou lista de elementos
 * @param  {any} elem elemento que terá a classe removida
 * @param  {string} clazz a classe CSS que será removida
 */
function RemoveClass(elem, clazz) {
	if (elem && clazz) {
		if (EhColecao(elem)) {
			for (let i = 0; i < elem.length; i++) {
				if (ElemHasClass(elem[i], clazz)) {
					elem[i].classList.remove(clazz);
				}
			}
		} else {
			if (ElemHasClass(elem, clazz)) {
				elem.classList.remove(clazz);
			}
		}
	}
}

/**
 * Verifica se um elemento possui determinada classe CSS
 * @param  {any} elem elemento que será avaliado
 * @param  {string} clazz o nome da classe CSS a ser verificada
 */
function ElemHasClass(elem, clazz) {
	return new RegExp("( |^)" + clazz + "( |$)").test(elem.className);
}

/**
 * Verifica se um objeto possui determinada propriedade
 * @param  {any} elem elemento que será avaliado
 * @param  {string} prop o nome da propriedade a ser verificada
 */
function ElementoPossuiPropriedade(elem, prop) {
	if (elem && prop) {
		return prop in elem;
	}
	return false;
}

/**
 * Verifica se um objeto é uma coleção (Array, HTMLCollection, etc)
 * @param  {any} elem elemento que será avaliado
 */
function EhColecao(elem) {
	if (Array.isArray(elem)) return true;

	if (elem instanceof HTMLCollection) return true;

	return ElementoPossuiPropriedade(elem, "length");
}
