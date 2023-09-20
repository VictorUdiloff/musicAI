
// Change Upload Section to Edit Section
let uploaddiv = document.getElementById("loadscreen")
let maindiv = document.getElementById("loadedscreen")
maindiv.style.display = "none"


var uploadedfile;
// Handle Audio Upload
const b = document.getElementById("fileupload")
b.addEventListener("change",function(){
    console.log(this.files);
    audiofile = this.files[0];
    uploaddiv.style.display = "none";
    maindiv.style.display = "inline";

    const formData = new FormData();
  formData.append('audiofile', audiofile);

  fetch('http://127.0.0.1:5000//upload', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      console.log('File uploaded:', data);
    })
    .catch(error => {
      console.error('Error uploading file:', error);
    });
})


// Put Song to Listening

let music = document.getElementById("originalsongpreview")
music.setAttribute("src",uploadedfile)


// Instruments/Bass display

instrumentsbass = document.getElementById("instrumentsbass")
instrumentsbutton = document.getElementById("instrumentsbutton")
instrumentsbutton.addEventListener("click",function(){
    voice.style.display="none";
    instrumentsbass.style.display="flex";
})

// Voice display

voice = document.getElementById("voice")
voicebutton = document.getElementById("voicebutton")
voicebutton.addEventListener("click",function(){
    instrumentsbass.style.display="none";
    voice.style.display="flex";
})