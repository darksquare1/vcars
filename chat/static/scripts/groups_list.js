const base_url = `${window.location.hostname}:${window.location.port}${window.location.pathname}`
console.log(base_url)
const websocket = new WebSocket(`ws://${base_url}`)

websocket.onopen = function(event){
    console.log('client connected')
    websocket.send('client says hi')
}
websocket.onmessage = function (event){
    console.log('client event', event)
}
