$(function () {
    $('#generate_wallet').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/wallet/new',
            type: 'POST',
            headers: {'Access-Control-Allow-Origin': '*'},
            dataType: 'json',
            data: $('#generate_wallet_form').serialize(),
            success: function (response) {
                $('#generate_wallet_form').hide();
                $("#username").val(response['username']);
                document.getElementById("private_key").innerHTML = response['private_key'];
                document.getElementById("public_key").innerHTML = response['public_key'];
                document.getElementById("keys").style.display = "block";
            },
            error: function (error) {
                handleError(error.responseText)
            }
        });
    });
});