function formatTime(time) {
    let d = new Date(time);
    return ('0' + d.getDate()).slice(-2) +
        '/' + ('0' + d.getMonth()).slice(-2) +
        '/' + (d.getFullYear()) +
        ' ' + ('0' + d.getHours()).slice(-2) +
        ':' + ('0' + d.getMinutes()).slice(-2) +
        ':' + ('0' + d.getSeconds()).slice(-2)
}

function fetchMessages() {
    $.ajax({
        url: "/transactions",
        type: 'GET',
        success: function (response) {
            // Generate Messages Table
            let transactions = response["transactions"];
            let transactions_length = response["length"];
            let messages = [];
            for (let i = 0; i < transactions_length; i++) {
                let transaction = transactions[i]
                let message = transaction["data"]
                messages.push(JSON.parse(message))
            }
            addMessages(messages)
        },
        error: function (error) {
            handleError(error.responseText)
        }
    });
}

function addMessages(messages) {
    messages.sort(function (a, b) {
        let keyA = new Date(a.timestamp),
            keyB = new Date(b.timestamp);
        // Compare the 2 dates
        if (keyA > keyB) return -1;
        if (keyA < keyB) return 1;
        return 0;
    });

    let $messagesElem = $('#message_forum');
    $messagesElem.empty();
    for (let i = 0; i < messages.length; i++) {
        let elem = `
            <hr>
            <div class="content is-small">
                <div class="is-size-5">` + messages[i]['msg'] + `</div>
                <div class="is-flex" style="justify-content: space-between">
                    <div class="is-size-7">Sent By: ` + messages[i]['sender_name'] + `</div>
                    <div class="is-size-7">` + formatTime(messages[i]['timestamp']) + `</div>
                </div>
            </div>
        `;
        $messagesElem.append(elem);
    }
}

$(function () {
    $('#refresh_messages').click(() => {
        fetchMessages();
    });

    $.ajax({
        url: "/transactions",
        type: 'GET',
        success: function (response) {
            fetchMessages();
        },
        error: function (error) {
            handleError(error.responseText)
        }
    });
});