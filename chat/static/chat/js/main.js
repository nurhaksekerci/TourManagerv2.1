const roomName = JSON.parse(document.getElementById("room-name").textContent)
const username = JSON.parse(document.getElementById("user-name").textContent)
const conversation = document.getElementById('conversation');
const chatSocket = new WebSocket(
    (window.location.protocol === 'https:' ? 'wss://' : 'ws://') +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);
const sendButton = document.querySelector("#send")
const inputField = document.querySelector("#comment")
var isRecord = false;
document.getElementById("hiddenInput").addEventListener('change', handleFİleSelect, false)

function handleFİleSelect(){
    var file = document.getElementById("hiddenInput").files[0]
    getbase64(file, file.type)
};
function getbase64(file, file_type){
    var type = file_type.split("/")[0]
    var reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function(){
        chatSocket.send(JSON.stringify({
            "message_type" : type,
            "message" : reader.result
        }))
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
                    // Kayıt tamamlandığında veri işleme kodu buraya yazılabilir
                    const dataArray = event.data;
                    console.log("Audio data available:", dataArray);
                };

                mediaRecorder.onStop = function(e){
                    let audioData = new Blob(dataArray, {'type' : 'audio/mp3'})
                    dataArray=[]
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




chatSocket.onmessage=function(e){
    const data=JSON.parse(e.data)
    const message_type = data.message_type
    if(message_type === "message"){
        if(username === data.user){
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                        ${data.message}
                        </div>
                        <span class="message-time pull-right">
                        ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }else{
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            ${data.message}
                        </div>
                        <span class="message-time pull-right">
                            ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    }else if(message_type  === "image"){
        if(username === data.user){
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                        <img width="250" height="250" src="${data.message}">
                        </div>
                        <span class="message-time pull-right">
                        ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }else{
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <img width="250" height="250" src="${data.message}">
                        </div>
                        <span class="message-time pull-right">
                            ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    }else if(message_type  === "audio"){
        if(username === data.user){
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                            <audio controls>
                                <source src="${data.message}">
                            </audio>
                        </div>
                        <span class="message-time pull-right">
                        ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }else{
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <audio controls>
                                <source src="${data.message}">
                            </audio>
                        </div>
                        <span class="message-time pull-right">
                            ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    }else if(message_type  === "video"){
        if(username === data.user){
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                    <div class="sender">
                        <div class="message-text">
                            <video width="250" height="250" controls>
                                <source src="${data.message}">
                            </video>
                        </div>
                        <span class="message-time pull-right">
                        ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }else{
            var message = `
            <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            <video width="250" height="250" controls>
                                <source src="${data.message}">
                            </video>
                        </div>
                        <span class="message-time pull-right">
                            ${data.created_date}
                        </span>
                    </div>
                </div>
            </div>
            `;
        }
    }
    conversation.innerHTML += message;
};

chatSocket.onclose=function(e){
    console.error("Socket beklenmedik şekilde kapandı.")
};

inputField.focus()
inputField.onkeyup = function(e){
    if(e.keyCode === 13){
        sendButton.click()
    }
};

sendButton.onclick = function(){
    const message = inputField.value;
    chatSocket.send(JSON.stringify({
        "sender" : username,
        "message" : message,
        "message_type" : "message"
    }))
    inputField.value = "";
};