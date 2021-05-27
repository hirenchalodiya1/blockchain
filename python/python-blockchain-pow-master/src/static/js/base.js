function showElem($elem) {
    $elem.fadeIn();
    setTimeout(() => {
        $elem.fadeOut();
    }, 3000);
}

let $heroSuccessElem = $("#hero_success");
let $heroSuccessTextElem = $("#hero_success .subtitle");
let $heroFailureElem = $("#hero_failure");
let $heroFailureTextElem = $("#hero_failure .subtitle");

function handleError(error) {
    $heroFailureTextElem.text(error);
    showElem($heroFailureElem);
}

function handleSuccess(msg) {
    $heroSuccessTextElem.text(msg);
    showElem($heroSuccessElem);
}

$(document).ready(function () {

    $heroSuccessElem = $("#hero_success");
    $heroSuccessTextElem = $("#hero_success .subtitle");
    $heroFailureElem = $("#hero_failure");
    $heroFailureTextElem = $("#hero_failure .subtitle");

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    $('#mine').click(function () {
        $.ajax({
            url: '/mine',
            type: 'GET',
            headers: {'Access-Control-Allow-Origin': '*'},
            success: function (response) {
                handleSuccess("Mining Block " + response["block_number"] + " Successful");
                let $refreshButton = $('#refresh_messages')
                if ($refreshButton.length)
                    $refreshButton.click()
            },
            error: function (error) {
                if (error.responseText === "No unconfirmed transactions")
                    handleError("Mining Failed: No pending txns")
                else
                    handleError("Mining Failed: " + error.responseText)
            }
        })
    });

    $('#sync').click(function () {
        $.ajax({
            url: '/nodes/resolve',
            type: 'GET',
            headers: {'Access-Control-Allow-Origin': '*'},
            success: function (response) {
                handleSuccess(response);
                let $refreshButton = $('#refresh_messages')
                if ($refreshButton.length)
                    $refreshButton.click()
            },
            error: function (error) {
                handleError(error.responseText)
            }
        })
    });
});