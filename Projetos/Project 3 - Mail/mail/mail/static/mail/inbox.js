// Global variable to record the current active view
var activeView = null;

document.addEventListener("DOMContentLoaded", function () {
	const btnInbox = document.querySelector("#inbox");
	btnInbox.addEventListener("click", function () {
		load_mailbox("inbox");
		animateCSS("#inbox-view", "fadeIn");
	});

	const btnSent = document.querySelector("#sent");
	btnSent.addEventListener("click", function () {
		load_mailbox("sent");
		animateCSS("#sent-view", "fadeIn");
	});

	const btnArchived = document.querySelector("#archived");
	btnArchived.addEventListener("click", function () {
		load_mailbox("archive");
		animateCSS("#archive-view", "fadeIn");
	});

	const btnCompose = document.querySelector("#compose");
	btnCompose.addEventListener("click", function () {
		compose_email();
		animateCSS("#compose-view", "fadeIn");
	});

	// By default we load the inbox
	animateCSS("#inbox-view", "fadeIn");
	load_mailbox("inbox");
});

function load_mailbox(mailbox) {
	// Toggles the button clicked as active
	ToggleButtonAsPressed(mailbox);

	// Hides all views, shows only the correct accordingly the clicked button and return the active view
	const activeView = ToggleView(mailbox);
	activeView.innerHTML = "";

	// Show the mailbox Header
	var mailBoxHeader = GetMailBoxHeader(mailbox);
	activeView.appendChild(mailBoxHeader);

	// query the backend about the mailbox selected
	fetch(`/emails/${mailbox}`)
		.then((response) => response.json())
		.then((emails) => {
			const containerDiv = GetContainerDiv();

			for (let email of emails) {
				// Compose the html to show the list of emails in the mailbox
				// A row with two columns, one for the email data, other for button actions on each email.
				const row = GetRowDivListEmails(email);

				// Uniquely identifying the row of each email
				row.id = "mail" + email.id;

				// Composing the row which shows the email
				const colEmail = GetColListEmail(email, 10);
				const colActions = GetColListEmailListActions(email, mailbox, 2);
				row.appendChild(colEmail);
				row.appendChild(colActions);
				containerDiv.appendChild(row);

				activeView.appendChild(containerDiv);

				// When the user click on the email, it will open the full mail
				// I am attaching the event to the first col to avoid trigger the load_email
				// function when the user clicks on "Archive" or "Mark As Read" button
				colEmail.addEventListener("click", () => load_email(email));

				//animateCSS("#" + row.id, "fadeInLeft");
			}

			UpdateUnreadMailCount(mailbox);
		});
}

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

function compose_email() {
	ToggleButtonAsPressed("compose");
	const activeView = ToggleView("compose");

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = "";
	document.querySelector("#compose-subject").value = "";
	document.querySelector("#compose-body").value = "";

	document.querySelector("#compose-form").onsubmit = () => {
		fetch("/emails", {
			method: "POST",
			body: JSON.stringify({
				recipients: document.querySelector("#compose-recipients").value,
				subject: document.querySelector("#compose-subject").value,
				body: document.querySelector("#compose-body").value,
			}),
		})
			.then((response) => response.json())
			.then(() => {
				load_mailbox("sent");
			});
		return false;
	};
}

function load_email(email) {
	const activeView = ToggleView("read");
	activeView.innerHTML = "";

	// fetch and display email
	fetch("/emails/" + `${email.id}`)
		.then((response) => response.json())
		.then((email) => {
			const containerDiv = GetContainerDiv();
			const mailWrapper = GetReadMailWrapperDiv();
			mailWrapper.innerHTML = `<h3>${email.subject}</h3>`;

			const row = GetRowDivReadEmail();
			const colEmail = GetColReadEmail(email, 10);
			const colActions = GetColListEmailReadActions(email, 2);

			row.appendChild(colEmail);
			row.appendChild(colActions);

			mailWrapper.appendChild(row);
			containerDiv.appendChild(mailWrapper);
			activeView.appendChild(containerDiv);
		});

	// mark email as read
	fetch("/emails/" + `${email.id}`, {
		method: "PUT",
		body: JSON.stringify({
			read: true,
		}),
	});
}

function GetMailBoxHeader(mailbox) {
	var container = GetContainerDiv();
	var row = GetRow();
	var col = GetCol(12);
	var content = document.createElement("div");
	addClass(content, "d-flex align-items-center");
	content.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
	content.innerHTML += "<span id='unreadCount" + mailbox + "' class='badge bg-secondary ms-3'></span>";

	col.appendChild(content);
	row.appendChild(col);
	container.appendChild(row);

	return container;
}

function UpdateUnreadMailCount(mailbox) {
	var count = document.querySelectorAll("#" + activeView.id + " .emailUnread").length;

	var elem = document.querySelector("#unreadCount" + mailbox);
	if (count == 0) {
		elem.textContent = " No email to read.";
	}

	if (count == 1) {
		elem.textContent = count + " unreaded email.";
	} else {
		elem.textContent = count + " unreaded emails.";
	}

	animateCSS("#" + elem.id, "heartBeat", "2");
}

/**** Whole page toggles ****/

// Apply a CSS class to show which view in selected
function ToggleButtonAsPressed(mailbox) {
	removeClass(document.querySelector("#inbox"), "active");
	removeClass(document.querySelector("#sent"), "active");
	removeClass(document.querySelector("#archived"), "active");
	removeClass(document.querySelector("#compose"), "active");

	var buttonToActivate = null;
	switch (mailbox) {
		case "inbox":
			buttonToActivate = document.querySelector("#inbox");
			break;
		case "compose":
			buttonToActivate = document.querySelector("#compose");
			break;
		case "sent":
			buttonToActivate = document.querySelector("#sent");
			break;
		case "archive":
			buttonToActivate = document.querySelector("#archived");
			break;
	}

	addClass(buttonToActivate, "active");
}

// Toggles between diferent views
function ToggleView(mailbox) {
	// Hide o all views
	document.querySelector("#inbox-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "none";
	document.querySelector("#sent-view").style.display = "none";
	document.querySelector("#archive-view").style.display = "none";
	document.querySelector("#read-view").style.display = "none";

	// Show only one view.
	switch (mailbox) {
		case "inbox":
			activeView = document.querySelector("#inbox-view");
			break;
		case "compose":
			activeView = document.querySelector("#compose-view");
			break;
		case "sent":
			activeView = document.querySelector("#sent-view");
			break;
		case "archive":
			activeView = document.querySelector("#archive-view");
			break;
		case "read":
			activeView = document.querySelector("#read-view");
			break;
		default:
			activeView = document.querySelector("#inbox-view");
	}

	activeView.style.display = "block";
	return activeView;
}

/**** Generic Bootstrap elements craeation ****/

// Gets a <div class='container'>
function GetContainerDiv() {
	const containerDiv = document.createElement("div");
	containerDiv.setAttribute("class", "container");
	return containerDiv;
}

// Gets a <div class='row'>
function GetRow() {
	const rowDiv = document.createElement("div");
	rowDiv.setAttribute("class", "row ");
	return rowDiv;
}

// Gets a <div class='col-md-SIZE'>
function GetCol(size) {
	const colDiv = document.createElement("div");
	addClass(colDiv, "col-md-" + size);
	return colDiv;
}

/**** Elements for the "List Mails" in some mailbox ****/

// Gets a div which hosts each email in a list of emails
function GetRowDivListEmails(email) {
	const rowDiv = GetRow();
	addClass(rowDiv, "mail_row shadow");

	if (!email.read) {
		addClass(rowDiv, "emailUnread");
	}

	return rowDiv;
}

// Gets a div which hosts each email contents in a list of emails
function GetColListEmail(email, size) {
	const colDivConteudo = GetCol(size);
	addClass(colDivConteudo, "colDivEmail");

	colDivConteudo.innerHTML += "From: " + email.sender + "<br />";
	colDivConteudo.innerHTML += "Subject: " + email.subject + "<br />";
	colDivConteudo.innerHTML += email.timestamp + "<br />";

	return colDivConteudo;
}

//Gets a div which hosts the action buttons for each email in a list of emails
function GetColListEmailListActions(email, mailbox, size) {
	const colDivActions = GetCol(size);
	addClass(colDivActions, "colDivActions");

	colDivActions.appendChild(GetBtnReadUnread(email, mailbox));

	colDivActions.appendChild(GetBtnArchive(email, mailbox));

	return colDivActions;
}

//Gets a div which hosts the "Mark as Read/Unread" button for each email in a list of emails
function GetBtnReadUnread(email, mailbox) {
	const elementWrapper = GetRow();
	addClass(elementWrapper, "float-end");

	const btnReadUnread = document.createElement("button");
	btnReadUnread.id = "btnReadUnread" + email.id;

	elementWrapper.appendChild(btnReadUnread);

	// Styling the initial state of the button.
	ApplyReadUnreadStylingToButton(email, btnReadUnread);

	// Add the click to archive the mail
	btnReadUnread.addEventListener("click", () => {
		fetch("/emails/" + `${email.id}`, {
			method: "PUT",
			body: JSON.stringify({
				read: !email.read,
			}),
		}).then(() => {
			// I will just "hack" this property to avoid querying the backend again,
			email.read = !email.read;
			ApplyReadUnreadStylingToButton(email, btnReadUnread);

			var elemRow = document.querySelector("#mail" + email.id);
			ApplyReadUnreadStylingToEmailRow(email, elemRow);

			UpdateUnreadMailCount(mailbox);
			//load_mailbox(mailbox);
		});
	});

	return elementWrapper;
}

function ApplyReadUnreadStylingToButton(email, button) {
	if (email.read) {
		// Styling the read/unread button
		removeClass(button, "btn-outline-success");
		addClass(button, "btn btn-sm btn-outline-secondary");
		button.textContent = "Mark as Unread";
	} else {
		// Styling the read/unread button
		removeClass(button, "btn-outline-secondary");
		addClass(button, "btn btn-sm btn-outline-success");
		button.textContent = "Mark as Read";
	}
}

function ApplyReadUnreadStylingToEmailRow(email, elemRow) {
	//Styling and animating the row
	if (email.read) {
		removeClass(elemRow, "emailUnread");
		animateCSS("#" + elemRow.id, "flipInX");
	} else {
		addClass(elemRow, "emailUnread");
		animateCSS("#" + elemRow.id, "flipOutX");
	}
}

//Gets a div which hosts the "Archive" button for each email in a list of emails
function GetBtnArchive(email, mailbox) {
	const elementWrapper = GetRow();
	addClass(elementWrapper, "float-end");

	if (mailbox === "inbox" || mailbox === "archive") { // Sent mails cant be archived!		
		const archiveButton = document.createElement("button");
		archiveButton.textContent = email.archived ? "Unarchive" : "Archive";
		addClass(archiveButton, "btn btn-sm btn-outline-danger");

		// Add the click to archive the mail
		archiveButton.addEventListener("click", () => {
			// Apply some animation to the item
			var name = "#mail" + email.id;
			animateCSS(name, "fadeOutRight");

			fetch("/emails/" + `${email.id}`, {
				method: "PUT",
				body: JSON.stringify({
					archived: !email.archived,
				}),
			}).then(() => {
				load_mailbox(mailbox);
			});
		});

		elementWrapper.appendChild(archiveButton);
	}

	return elementWrapper;
}

/**** Elements for the "Read Email" view ****/

//Gets a div which hosts the whole email item in a list of emails
function GetReadMailWrapperDiv() {
	const div = document.createElement("div");
	addClass(div, "readmail_wrapper shadow");
	return div;
}

//Gets a row div which hosts the email being readed
function GetRowDivReadEmail() {
	const rowDiv = GetRow();
	rowDiv.setAttribute("class", "row readmail_row");
	return rowDiv;
}

//Gets a col div which hosts the email being readed
function GetColReadEmail(email, size) {
	const colDivConteudo = GetCol(size);
	addClass(colDivConteudo, "colReadEmail");

	colDivConteudo.innerHTML += "<b>From: </b>" + email.sender + "<br />";
	colDivConteudo.innerHTML += "<b>Recipients: </b>";
	for (let recipient of email.recipients) {
		colDivConteudo.innerHTML += recipient;
	}
	colDivConteudo.innerHTML += "<br />";
	colDivConteudo.innerHTML += "<b>Sent on: </b>" + email.timestamp + "<br />";

	const bodyDiv = document.createElement("div");
	addClass(bodyDiv, "mail_body");
	bodyDiv.innerHTML += email.body + "<br />";
	colDivConteudo.appendChild(bodyDiv);

	return colDivConteudo;
}

//Gets a col div which hosts buttons Actions (currently only the reply button) for the email being readed
function GetColListEmailReadActions(email, size) {
	const colDivActions = GetCol(size);
	addClass(colDivActions, "colDivActions");

	colDivActions.appendChild(GetBtnReply(email));

	return colDivActions;
}

//Gets a div which hosts "Reply" button for the email being readed
function GetBtnReply(email) {
	const elementWrapper = GetRow();
	addClass(elementWrapper, "float-end");

	const btnReply = document.createElement("button");
	addClass(btnReply, "btn btn-primary");
	btnReply.textContent = "Reply";

	btnReply.addEventListener("click", () => {
		compose_email(); // when clicked, will show the compose email view

		// prefill the email for the Reply
		document.querySelector("#compose-recipients").value = email.sender;
		document.querySelector("#compose-subject").value =
			email.subject.slice(0, 4) == "Re: " ? "Re: " + email.subject.slice(4) : "Re: " + email.subject;
		document.querySelector("#compose-body").value =
			"On " + email.timestamp + " " + email.sender + " wrote " + email.body;
	});

	elementWrapper.appendChild(btnReply);
	return elementWrapper;
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

// Apply animations using the animate.css
const animateCSS = (element, animation, duration = "0", prefix = "animate__") =>
	// We create a Promise and return it
	new Promise((resolve, reject) => {
		const animationName = `${prefix}${animation}`;
    const animationDuration = `${prefix}delay-${duration}s`;
		const node = document.querySelector(element);

		node.classList.add(`${prefix}animated`, animationName);
		if (duration != "0") {
			node.classList.add(`${prefix}animated`, animationDuration);
		}
    
		// When the animation ends, we clean the classes and resolve the Promise
		function handleAnimationEnd(event) {
			event.stopPropagation();
			node.classList.remove(`${prefix}animated`, animationName);
      if (duration != "0") {
        node.classList.remove(`${prefix}animated`, animationDuration);
      }
			resolve("Animation ended");
		}

		node.addEventListener("animationend", handleAnimationEnd, { once: true });
	});
