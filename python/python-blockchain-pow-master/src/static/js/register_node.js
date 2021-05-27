function fetchNodes() {
    $.ajax({
        url: "/nodes/get",
        type: 'GET',
        success: function (response) {
            // Generate Nodes Table
            let nodes = response["nodes"];
            addNodes(nodes)
        },
        error: function (error) {
            handleError(error.responseText)
        }
    });
}

function addNodes(nodes) {
    nodes.sort(function (a, b) {
        let keyA, keyB;
        if (a.split(':')[0] === b.split(':')[0]) {
            keyA = a.split(':')[1];
            keyB = b.split(':')[1];
        }else{
            keyA = a.split(':')[0];
            keyB = b.split(':')[0];
        }
        if (keyA > keyB) return 1;
        if (keyA < keyB) return -1;
        return 0;
    });
    let $nodesElem = $('#nodes');
    $('#nodes').empty();
    for (let i = 0; i < nodes.length; i++) {
        let elem = `
            <hr>
            <div class="content is-small">
                <div class="is-size-6">` + nodes[i] + `</div>
            </div>
        `;
        $nodesElem.append(elem);
    }
}

$(function () {
    fetchNodes();

    $('#refresh_nodes').click(function (e) {
        e.preventDefault();
        fetchNodes();
    });

    $('#register_node').click(function (e) {
        e.preventDefault();
        let new_nodes = $('#register_node_form').serialize();
        $.ajax({
            url: '/nodes/register',
            type: 'POST',
            headers: {'Access-Control-Allow-Origin': '*'},
            dataType: 'json',
            data: new_nodes,
            success: function (response) {
                handleSuccess(response["message"])
                addNodes(response["total_nodes"])
            },
            error: function (error) {
                handleError(error.responseText)
            }
        });
    });
});