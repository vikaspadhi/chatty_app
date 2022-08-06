let username = JSON.parse(document.getElementById("username").textContent);
let userid = JSON.parse(document.getElementById("userid").textContent);
let msg_box = document.getElementById("msg_box");

let ws = new WebSocket(`ws://${window.location.host}/ws/sc/`);
ws.onopen = (event) => {
//   console.log("ws connected...");
};

ws.onclose = (event) => {
//   console.log("websocket disconnected...");
};

ws.onerror = (event) => {
//   console.log("Websocket error...", event);
};

let load_msg = (receiver) => {
  $.ajax({
    url: `/loadchat/${receiver}/`,
    success: function (response) {
      let messages = response.messages
      console.log(response)
    //   console.log(userid)
        document.getElementById("msg_box").innerHTML='';
      let msg = ``;
        messages.map((item)=>{
            if (item.sender_id == userid) {
              msg += `
    <div class="d-flex justify-content-end my-2">
                 <span class="border border-dark py-2 px-2 rounded" style="max-width: 50%;">
                    ${item.text}
                 </span> 
              </div>
  `;
            } else {
              msg += `
    <div class="d-flex justify-content-start my-2">
                 <span class="border py-2 px-2 rounded" style="max-width: 50%;">
                    ${item.text}
                 </span> 
              </div>
                `;
            }
        })
      
      document.getElementById("msg_box").innerHTML += msg;
      msg_box.scrollTop = msg_box.scrollHeight;
    },
  });
    
};

let receiver = localStorage.getItem("receiver");
if (receiver) {
  $("#input").removeAttr("disabled");
  let room_name = localStorage.getItem("room_name");
//   console.log(room_name)
  load_msg(room_name);
  let receiver_name = localStorage.getItem("receiver_name");
  document.getElementById("receiver_name").innerHTML=receiver_name;
}


let get_room_name=(number)=>{
    let room_name;
    $.ajax({
        url:`/getroom/${number}`,
        success:function(response){
            room_name = response.room_name
            localStorage.setItem("room_name", room_name);
            load_msg(room_name);
        }
    })
    
}

$(".user-item").click(function () {
    $(this).removeClass("bg-light")
  let receiver_name = $(this).html();
  localStorage.setItem('receiver_name',receiver_name)
  document.getElementById("receiver_name").innerHTML = receiver_name;

  let number = $(this).data("number");
  localStorage.setItem("receiver", number);

  $("#input").removeAttr("disabled");

  let data = { number: number, msg: "" };
  ws.send(JSON.stringify(data));
  get_room_name(number)
  
});


let send_msg = () => {
  let input = document.getElementById("input");
  let msg = input.value;
  let data = { msg: msg, number: localStorage.getItem("receiver") };
  ws.send(JSON.stringify(data));
  input.value = "";
};

let msg_input = document.getElementById("input");
msg_input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    send_msg();
  }
});


ws.onmessage = (event) => {
  chat_data = JSON.parse(event.data);
  console.log(chat_data);
  room_id = chat_data.room_name;
  localStorage.setItem("room_name", room_id);
    let msg = ``;
  if(chat_data.username == username)
  {
    msg += `
    <div class="d-flex justify-content-end my-2">
                 <span class="border border-dark py-2 px-2 rounded" style="max-width: 50%;">
                    ${chat_data.text}
                 </span> 
              </div>
  `;
  }
  else
  {
    msg += `
    <div class="d-flex justify-content-start my-2">
                 <span class="border py-2 px-2 rounded" style="max-width: 50%;">
                    ${chat_data.text}
                 </span> 
              </div>
  `;
  }
  document.getElementById("msg_box").innerHTML += msg;
//   active_id = `user_${chat_data.username}`;
//   document.getElementById(`${active_id}`).classList.add("bg-light");
  msg_box.scrollTop = msg_box.scrollHeight;
};

