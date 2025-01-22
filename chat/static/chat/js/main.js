const roomName = JSON.parse(document.getElementById("room-name").textContent)
const username = JSON.parse(document.getElementById("user-name").textContent)
const conversation = document.getElementById('conversation');
const sendButton = document.querySelector("#send")
const inputField = document.querySelector("#comment")
var isRecord = false;
document.getElementById("hiddenInput").addEventListener('change', handleFileSelect, false)

function handleFileSelect(){
    var file = document.getElementById("hiddenInput").files[0]
    getbase64(file, file.type)
};

function getbase64(file, file_type){
    var type = file_type.split("/")[0]
    var reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function(){
        sendMessage(reader.result, type)
    }
}

navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {
        const hasMicrophone = devices.some(device => device.kind === 'audioinput');
        const startstop = document.getElementById("record");

        if (!hasMicrophone) {
            startstop.disabled = true;
            return;
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(mediaStreamObject) {
                const mediaRecorder = new MediaRecorder(mediaStreamObject);
                let isRecord = false;

                startstop.addEventListener('click', function(e) {
                    if (isRecord) {
                        startstop.style = "";
                        isRecord = false;
                        mediaRecorder.stop();
                    } else {
                        startstop.style = "color: red;";
                        isRecord = true;
                        mediaRecorder.start();
                    }
                });

                mediaRecorder.ondataavailable = function(event) {
                    const dataArray = event.data;
                    console.log("Audio data available:", dataArray);
                };

                mediaRecorder.onStop = function(e){
                    let audioData = new Blob(dataArray, {'type' : 'audio/mp3'})
                    dataArray = []
                    getbase64(audioData, audioData.type)
                }
            })
            .catch(function(error) {
                console.log('Error accessing media devices.', error);
            });
    })
    .catch(function(error) {
        console.log('Error enumerating devices.', error);
    });

function sendMessage(content, messageType="message") {
    fetch('/api/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            chat_room: roomName,
            user: username,
            content: content,
            message_type: messageType
        })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function loadMessages() {
    fetch(`/api/messages/?room_name=${roomName}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(displayMessage);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayMessage(data) {
    const message_type = data.message_type;
    let message = "";

    if (message_type === "message") {
        if (username === data.user) {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                        ${data.content}
                        </div>
                        <span class="message-time pull-right">
                        ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        } else {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            ${data.content}
                        </div>
                        <span class="message-time pull-right">
                            ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    } else if (message_type === "image") {
        if (username === data.user) {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                        <img width="250" height="250" src="${data.content}">
                        </div>
                        <span class="message-time pull-right">
                        ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        } else {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <img width="250" height="250" src="${data.content}">
                        </div>
                        <span class="message-time pull-right">
                            ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    } else if (message_type === "audio") {
        if (username === data.user) {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                            <audio controls>
                                <source src="${data.content}">
                            </audio>
                        </div>
                        <span class="message-time pull-right">
                        ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        } else {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <audio controls>
                                <source src="${data.content}">
                            </audio>
                        </div>
                        <span class="message-time pull-right">
                            ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    } else if (message_type === "video") {
        if (username === data.user) {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                            <video width="250" height="250" controls>
                                <source src="${data.content}">
                            </video>
                        </div>
                        <span class="message-time pull-right">
                        ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        } else {
            message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <video width="250" height="250" controls>
                                <source src="${data.content}">
                            </video>
                        </div>
                        <span class="message-time pull-right">
                            ${data.timestamp}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    }

    conversation.innerHTML += message;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

inputField.focus();
inputField.onkeyup = function(e) {
    if (e.keyCode === 13) {
        sendButton.click();
    }
};

sendButton.onclick = function() {
    const message = inputField.value;
    sendMessage(message, "message");
    inputField.value = "";
};

// Sayfa yüklendiğinde mevcut mesajları yükleyin
loadMessages();
