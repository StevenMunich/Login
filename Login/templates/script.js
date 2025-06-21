
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
                        item.innerText = msg;
                        list.appendChild(item);
                    });
                })
                .catch(error => console.error("Error:", error));
        }
