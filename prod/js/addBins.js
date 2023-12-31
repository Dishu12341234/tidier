fetch('https://httpbin.org/ip')
    //jsonip.com
    .then(response => response.json())
    .then(data => {
        fetch(`https://ipapi.co/${data.origin}/json`).then(response => response.json()).then(
            data => {
                console.log(data.latitude);
                console.log(data.longitude);
                console.log(data.city);

                let city = document.getElementById("id_City");
                console.log(city);
                city.value = data.city
                document.getElementById("id_City").focus()
                document.getElementById("id_City").blur()
            }
        )
    }
    )
    .catch(error => console.error('Error fetching IP address:', error));
setTimeout(() => {
    const scanner = new Html5QrcodeScanner('reader', {
        qrbox: {
            width: 250,
            height: 250,
        },
        fps: 20,
    });

    scanner.render(success, () => null);
    function success(result) {
        console.log("Raw Result:", result); // Log the raw result to check its content
        document.getElementById('result').innerHTML = result;
        scanner.clear();

        try {
            let sanitizedResult = result.replace(/'/g, '"');
            id_qr_data.value = sanitizedResult;
            id_qr_data.focus()
        } catch (e) {
            console.error("Error parsing JSON:", e);
        }
    }
    function error(err) {
        console.error(err);
    }
}, 1000)

let inputs = document.querySelectorAll("input:not([type=\"submit\"])")
inputs.forEach((element) => {
    element.onfocus = element.oninput = () => {
        let lable = element.parentElement.children[0]
        if (element.value != "") {
            lable.style.marginTop = "-18px"
        }
        else {
            lable.style.marginTop = "0px"
        }
    }
})