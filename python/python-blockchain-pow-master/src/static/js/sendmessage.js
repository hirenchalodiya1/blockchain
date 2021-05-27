$(function () {
    $('#send_message').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/message/send',
            type: 'POST',
            headers: {'Access-Control-Allow-Origin': '*'},
            dataType: 'json',
            data: $('#send_message_form').serialize(),
            success: function (response) {
                document.getElementById("confirm_signature").value = response["signature"];
                $("#confirm_transaction_modal").toggleClass('is-active');
            },
            error: function (error) {
                handleError(error.responseText)
            }
        });
    });

    $("#button_confirm_transaction").click(function () {
        window.location.pathname = '/'
    });

    $('#confirm_transaction_modal .modal-background').click(() => {
        $("#confirm_transaction_modal").toggleClass('is-active');
    });

    $('.button_cancel_transaction').click(() => {
        $("#confirm_transaction_modal").toggleClass('is-active');
    });
});