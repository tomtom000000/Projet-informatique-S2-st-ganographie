const ColorButtonNoSelect ="rgb(0, 123, 255)";
const ColorButtonSelect="rgb(0, 42, 255)";   
let Compteur_clic_carré_magique=0;
document.addEventListener("DOMContentLoaded", function() {
    hiddenMessage.style.display='none';
    caesarKey.style.display='none';
    audioFile.style.display='none';
    readMessage.style.backgroundColor=ColorButtonNoSelect;
    writeMessage.style.backgroundColor=ColorButtonNoSelect;
    
});

document.getElementById('writeMessage').addEventListener('click', function() {
    
    var fileInput = document.getElementById('audioFile');
    var messageInput = document.getElementById('hiddenMessage');
    var keyInput = document.getElementById('caesarKey');
    var file = fileInput.files[0];
    var message = messageInput.value;
    var key = keyInput.value;
    if (writeMessage.style.backgroundColor==ColorButtonNoSelect){
        writeMessage.style.backgroundColor=ColorButtonSelect;
        send.style.display='block';
        if(hiddenMessage.style.display=='none'){
            hiddenMessage.style.display='block';
        }
        if(caesarKey.style.display=='none'){
            caesarKey.style.display='block';
        }
        if(audioFile.style.display=='none'){
            audioFile.style.display='block';
        }
        if(readMessage.style.backgroundColor==ColorButtonSelect){
            readMessage.style.backgroundColor=ColorButtonNoSelect;
        }
    }else{
        writeMessage.style.backgroundColor=ColorButtonNoSelect;
        if(readMessage.style.backgroundColor==ColorButtonNoSelect){
            hiddenMessage.style.display='none';
            caesarKey.style.display='none';
            audioFile.style.display='none';
            send.style.display='none';
        } 
    }




});

document.getElementById('readMessage').addEventListener('click', function() {
    var fileInput = document.getElementById('audioFile');
    var keyInput = document.getElementById('caesarKey');
    var file = fileInput.files[0];
    var key = keyInput.value;
    if (readMessage.style.backgroundColor==ColorButtonNoSelect){
        readMessage.style.backgroundColor=ColorButtonSelect;
        send.style.display='block';
        if(hiddenMessage.style.display=='block')hiddenMessage.style.display='none';
        if(caesarKey.style.display=='none'){caesarKey.style.display='block';}
        if(audioFile.style.display=='none'){audioFile.style.display='block';}
        if(writeMessage.style.backgroundColor==ColorButtonSelect){writeMessage.style.backgroundColor=ColorButtonNoSelect;}
    }else{
        readMessage.style.backgroundColor=ColorButtonNoSelect;
        if(writeMessage.style.backgroundColor==ColorButtonNoSelect){
            hiddenMessage.style.display='none';
            caesarKey.style.display='none';
            audioFile.style.display='none';
            send.style.display='none';
        } 
    }
});


// Début fonction matrix.
const canvas = document.getElementById('matrixCanvas');
const context = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let katakana ='01';


const fontSize = 16;
const columns = canvas.width / fontSize;

const drops = Array.from({ length: columns }, () => 1);

function drawMatrix() {
    context.fillStyle = 'rgba(0, 0, 0, 0.05)';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "rgb(0,255,0)";
    
    context.font = `${fontSize}px monospace`;
    if(Compteur_clic_carré_magique%10==1)katakana = '12';
    if(Compteur_clic_carré_magique%10==2)katakana = '23';
    if(Compteur_clic_carré_magique%10==3)katakana = '34';
    if(Compteur_clic_carré_magique%10==4)katakana = '45';
    if(Compteur_clic_carré_magique%10==5)katakana = '56';
    if(Compteur_clic_carré_magique%10==6)katakana = '67';
    if(Compteur_clic_carré_magique%10==7)katakana = '78';
    if(Compteur_clic_carré_magique%10==8)katakana = '89';
    if(Compteur_clic_carré_magique%10==9)katakana = '¤#';
    if(Compteur_clic_carré_magique%10==0){
        katakana = '01';
    }
    for (let i = 0; i < drops.length; i++) {
        const text = katakana.charAt(Math.floor(Math.random() * katakana.length));
        context.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    }
}

setInterval(drawMatrix, 50);
// FIN fonction matrix.

//début carré magique 
function moveToRandomPosition(element) {
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    const elementWidth = element.offsetWidth;
    const elementHeight = element.offsetHeight;

    const randomX = Math.floor(Math.random() * (windowWidth - elementWidth));
    const randomY = Math.floor(Math.random() * (windowHeight - elementHeight));

    element.style.left = randomX + 'px';
    element.style.top = randomY + 'px';
}

document.addEventListener('DOMContentLoaded', function() {
    const carre = document.getElementById('carre');
    moveToRandomPosition(carre);

    carre.addEventListener('click', function() {
        Compteur_clic_carré_magique++;
        moveToRandomPosition(carre);
    });
});

//fin carré magique 


document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData();
            const audioFile = document.getElementById('audioFile').files[0];
            const hiddenMessage = document.getElementById('hiddenMessage').value;
            const caesarKey = document.getElementById('caesarKey').value;
            var readOrWrite = 0; // 1 => read, 0 => write
          
            if(writeMessage.style.backgroundColor==ColorButtonSelect){
                readOrWrite =0;
            }else if (readMessage.style.backgroundColor==ColorButtonSelect){
                readOrWrite=1;
            }
          
            formData.append('audioFile', audioFile);
            formData.append('hiddenMessage', hiddenMessage);
            formData.append('caesarKey', caesarKey);
            formData.append('readOrWrite',readOrWrite);
           
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                if (readOrWrite ==0){
                    const downloadLink = document.getElementById('downloadLink');
                    downloadLink.href = "/download/"+data.new_file_name;
                    
                    document.getElementById('downloadLink').style.display = 'block';
                }
                if(readOrWrite==1){
                    const cachmessage = data.message;
                    alert("le message caché est : "+cachmessage);
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
            
        });
