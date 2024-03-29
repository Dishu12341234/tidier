const fillUps = document.getElementsByClassName("fillUp");
const bars = document.getElementsByClassName("bar");
const BinIDs = document.getElementsByClassName("BinID");
const datas = document.getElementsByClassName("data");
const stats = document.getElementById("stats");

function deployBars() {
    for (let i = 0; i < fillUps.length - 1; i++) {
        const newBar = bars[i].cloneNode(true);
        newBar.style = bars[i].style;
        stats.appendChild(newBar);
    }
}

deployBars()

if (fillUps.length === 0) {
    stats.style.display = "none";
}

function updateFillDataBar() {
    for(let i = 0; i < fillUps.length; i++)
    {
        console.log(i);
    }
}

// for (let i = 0; i < fillUps.length; i++) {
//     let finalValue = parseInt(fillUps[i].innerHTML)
//     let currentFillUpValue = 1;
//     let fillInterval = setInterval(() => {
//         currentFillUpValue += 1;
//         datas[i].innerHTML = `${BinIDs[i].innerText}<br>${currentFillUpValue}%`
//         if (currentFillUpValue >= finalValue) {
//             clearInterval(fillInterval)
//         }
//     }, (1 / finalValue) * 1500)
// }

let currentFillUpValue = 1;
function updateBars() {
    for (let i = 0; i < fillUps.length; i++) {
        const perc = parseInt(fillUps[i].innerHTML);
        const finalVal = 430 + (perc / 100) * 430;
        const svg = bars[i].children[1];
        let fillUp = parseInt(BinIDs[i].parentElement.children[2].innerHTML)
        let BinID = BinIDs[i].parentElement.children[0].innerHTML
        console.log(fillUp);
        console.log(datas[i]);
        datas[i].innerHTML = `${BinID}<br>${fillUp}%`
        svg.style.transition = 'all 1.5s cubic-bezier(0.55, 1.26, 0, 1.09)'
        setTimeout(() => svg.style.strokeDashoffset = finalVal)//Some amount of delay is required
    }
}

updateBars();

function connectWebSocket() {
    const protocol = document.location.protocol === "https:" ? "wss:" : "ws:";
    const chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/bin/${Date.now()}/`);

    chatSocket.onopen = function (e) {
        console.log("Successfully connected to the WebSocket.");
        updateFillDataBar();
        setInterval(() => {
            const JSONData = {
                "type": "BinReload"
            };
            chatSocket.send(JSON.stringify(JSONData));
        }, 1000);
    };

    chatSocket.onclose = function (e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(() => {
            console.log("Reconnecting...");
            connectWebSocket();
        }, 2000);
    };

    chatSocket.onmessage = function (e) {
        const Bins = JSON.parse(e.data).bins;
        for (const binIndex in Bins) {
            const binID = Bins[binIndex].BinID;
            const bin = document.getElementById(binID);
            const newFillUp = Bins[binIndex].fillUp;
            const fillUp = bin.parentElement.children[2];
            fillUp.innerText = `${newFillUp}%`;

            const newRefreshStats = Bins[binIndex].refreshStats;
            const refreshStats = bin.parentElement.children[4];
            refreshStats.innerText = newRefreshStats;

            const newStatus = Bins[binIndex].status;
            const status = bin.parentElement.children[3];
            status.innerText = newStatus;
            datas[binIndex].innerHTML = `${BinIDs[binIndex].innerText}<br>${newFillUp}%`
        }
        updateBars();
    };

    chatSocket.onerror = function (err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    };
}

connectWebSocket();
