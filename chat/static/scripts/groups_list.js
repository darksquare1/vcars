const base_url = `${window.location.hostname}:${window.location.port}${window.location.pathname}`
const websocket = new WebSocket(`ws://${base_url}`)

websocket.onopen = function (event) {
    console.log('connection opened')
}
websocket.onmessage = function (event) {
    let message = JSON.parse(event.data)
    let type = message.type
    let data = message.data
    switch (type) {
        case "leave_group":
            leave_group_handler(data)
            break

        case "join_group":
            join_group_handler(data)
            break
    }

}

function add_event_to_buttons() {
    const buttons = document.querySelectorAll('.group-option')
    console.log(buttons)
    buttons.forEach(button => {
        button.addEventListener('click', send_event_message)
    })
}

function send_event_message(event) {
    const {target} = event;
    let group = target.value.split(" ")
    let group_uuid = group[1]
    let action = group[0]
    if (action === "open_group") {
        window.location.replace(`http://${window.location.hostname}:${window.location.port}/chat/group/${group_uuid}`)
    } else {
        let data = {
            "type": action,
            "data": group_uuid,
        }

        websocket.send(JSON.stringify(data))
    }
}

function leave_group_handler(uuid) {
    let leave_button = document.getElementById(`leave-${uuid}`)
    let open_button = document.getElementById(`open-${uuid}`)
    leave_button.remove()
    open_button.remove()
    let join_button = `<button id="join-${uuid}" class="group-option btn btn-success btn-sm" value="join_group ${uuid}">Join</button>`
    let dev_body = document.getElementById(uuid)

    dev_body.innerHTML += join_button
    add_event_to_buttons()
}


function join_group_handler(uuid) {
    let join_button = document.getElementById(`join-${uuid}`)
    join_button.remove()
    let leave_button = `<button id="leave-${uuid}" class="group-option btn btn-danger btn-sm me-2" value="leave_group ${uuid}">Leave</button>`
    let open_button = `<button id="open-${uuid}" class="group-option btn btn-primary btn-sm" value="open_group ${uuid}">Open</button>`
    let dev_body = document.getElementById(uuid)
    dev_body.innerHTML += leave_button
    dev_body.innerHTML += open_button
    add_event_to_buttons()
}

add_event_to_buttons()