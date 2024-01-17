var name = document.getElementById('chatroom-name').textContent;
var submitBtn = document.getElementById('submit-btn')
var dataInput = document.getElementById('data-input')
var user = document.getElementById('user').textContent.trim()
var dataBox = document.getElementById('data-box')

var socket = new WebSocket(`ws://${window.location.host}/ws/chat/${name}/`);
console.log(socket);

socket.onopen = function(e) {
    console.log('WebSocket connection opened.');
};

submitBtn.addEventListener('click', ()=> {
    var dataValue = dataInput.value
    socket.send(JSON.stringify({
        'message': dataValue,
        'sender': user,
    }));
})

socket.onmessage = function(e) {
    var { sender, message, color } = JSON.parse(e.data);

    dataBox.innerHTML += `<p style="background-color: ${color}">${sender}: ${message}</p>`;
};

socket.onclose = function(e) {
    console.log('WebSocket connection closed.');
};

socket.onerror = function(e) {
    console.error('WebSocket error:', e);
};

addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        document.getElementById('submit-btn').click();
        document.getElementById('data-input').value = '';
    }
});