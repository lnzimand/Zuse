html = """
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Chat</title>
    <style>
      body {
        font-family: Arial;
      }
      .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 75vw;
        margin: auto;
      }

      form {
        display: flex;
        flex-direction: column;
      }

      form input {
        margin: 1.5vh 0;
        line-height: 4vh;
      }

      form button {
        line-height: 4vh;
        border-radius: 0.5rem;
        box-shadow: 0px 0px 0px 2px #9fb4f2;
        background: linear-gradient(to bottom, #7892c2 5%, #476e9e 100%);
        background-color: #7892c2;
        border: 1px solid #4e6096;
        display: inline-block;
        cursor: pointer;
        color: #ffffff;
        font-family: Arial;
        font-size: 19px;
        padding: 0.4rem 0.5rem;
        text-decoration: none;
        text-shadow: 0px 1px 0px #283966;
      }

      form button:hover {
        background: linear-gradient(to bottom, #476e9e 5%, #7892c2 100%);
        background-color: #476e9e;
      }

      ul {
        list-style-type: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-right: 40px;
      }

      ul li {
        display: list-item;
        background: #7892c2;
        padding: 10px 10px;
        color: white;
        margin: 5px;
        flex-wrap: wrap;
      }

      ul li::marker {
        color: #7892c2;
      }

      #messages {
        justify-content: center;
      }

      li::before {
        content: "";
        display: block;
        width: 100%;
        height: 1rem;
        position: absolute;
        top: 0;
        left: 0;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>WebSocket Chat</h1>
      <form action="" onsubmit="sendMessage(event)">
        <input type="text" id="messageText" autocomplete="off" />
        <button>Send</button>
      </form>
      <ul id="messages"></ul>
    </div>
    <script>
      const ws = new WebSocket("ws://localhost:8000/ws-basic"); 

      ws.onmessage = (event) => {
        if (event.data.trim().length === 0) return
        const messages = document.getElementById("messages");
        const message = document.createElement("li");
        const content = document.createTextNode(event.data);

        message.appendChild(content);
        messages.appendChild(message);
      };

      const sendMessage = (event) => {
        const input = document.getElementById("messageText");

        ws.send(input.value);
        input.value = "";
        event.preventDefault();
      };
    </script>
  </body>
</html>
"""
