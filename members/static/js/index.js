let fillUps = document.getElementsByClassName("fillUp");
    let bars = document.getElementsByClassName("bar");
    let BinIDs = document.getElementsByClassName("BinID")
    let datas = document.getElementsByClassName("data");
    let bar1 = document.getElementById("s1")
    let stats = document.getElementById("stats")
    for (let i = 0; i < fillUps.length - 1; i++) {
        let newBar = bars[i].cloneNode(true);
        stats.appendChild(newBar);
    }
    if(fillUps.length == 0)
    {
        stats.style.display = "none"
    }
    function bar() {
        for (let i = 0; i < fillUps.length; i++) {
            let perc = parseInt(fillUps[i].innerHTML)
            let value = fillUps[i].innerHTML;
            let finalVal = 430 - (perc / 100) * 430
            datas[i].innerHTML = `${BinIDs[i].innerHTML}<br>${fillUps[i].innerHTML}`
            bars[i].children[1].style.strokeDashoffset = finalVal;
        }
    }
    bar(true)

    function connect() {
        let chatSocket = new WebSocket((document.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + `/ws/bin/${Date.now()}/`);

        chatSocket.onopen = function (e) {
            console.log("Successfully connected to the WebSocket.");
            setInterval(() => {
                let JSONData = ({
                    "type":"BinReload"
                })
                chatSocket.send(JSON.stringify(JSONData));
            }, 1000)
        };

        chatSocket.onclose = function (e) {
            console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
            setTimeout(function () {
                console.log("Reconnecting...");
                connect();
            }, 2000);
        };

        chatSocket.onmessage = function (e) {
            let Bins = JSON.parse(e.data).bins;
            for (let binIndex in Bins) {
                let binID = Bins[binIndex].BinID;
                let bin = document.getElementById(binID);
                let newFillUp = Bins[binIndex].fillUp;
                let fillUp = bin.parentElement.children[2]
                fillUp.innerText = `${newFillUp}%`

                let newRefreshStats = Bins[binIndex].refreshStats;
                let refreshStats = bin.parentElement.children[4]
                refreshStats.innerText = newRefreshStats

                let newStatus = Bins[binIndex].status
                let status = bin.parentElement.children[3]
                status.innerText = newStatus

                bar()
            }
        };

        chatSocket.onerror = function (err) {
            console.log("WebSocket encountered an error: " + err.message);
            console.log("Closing the socket.");
            chatSocket.close();
        };
    }

    connect();
