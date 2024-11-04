const base_url = `${window.location.hostname}:${window.location.port}${window.location.pathname}`
const websocket = new WebSocket(`ws://${base_url}`)

websocket.onopen = function (event) {
    console.log('client connected')
    websocket.send('client says hi')
}
websocket.onmessage = function (event) {
    console.log('client event', event)
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

add_event_to_buttons()