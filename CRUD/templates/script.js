function sendData() {
const inputValue = document.getElementById("userInput").value;
 fetch("http://127.0.0.1:5000/send", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: inputValue })
   })
   .then(response => response.json())
   .then(data => document.getElementById("sendResponse").innerText = data.message)
   .catch(error => console.error("Error:", error));
}

 function fetchData() {
     fetch("http://127.0.0.1:5000/get")
     .then(response => response.json())
     .then(data => {
          const list = document.getElementById("messagesList");
          list.innerHTML = "";
          data.messages.forEach(msg => {
            let item = document.createElement("li");
            item.innerText = `ID ${msg.id}: ${msg.text}`;
            list.appendChild(item);
            });
          }
     )//End Then
     .catch(error => console.error("Error:", error));
}

        function updateData() {
            
            const id = document.getElementById("updateId").value;
            const newText = document.getElementById("updateText").value;
            fetch(`http://127.0.0.1:5000/update/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: newText })
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error("Error:", error));

        }

        function deleteData() {
            const id = document.getElementById("deleteId").value;
            fetch(`http://127.0.0.1:5000/delete/${id}`, {
                method: "DELETE"
            })
            .then(response => response.json())
            .then(data => alert(data.message))
            .catch(error => console.error("Error:", error));
        }

function initializeDoc() {
    fetchData();
    document.getElementById("addButton").addEventListener("click", sendData);
    document.getElementById("getButton").addEventListener("click", fetchData);
    document.getElementById("updateButton").addEventListener("click", updateData);
    document.getElementById("deleteButton").addEventListener("click", deleteData);
}

window.addEventListener("load",initializeDoc, false)