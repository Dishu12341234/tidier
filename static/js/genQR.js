document.addEventListener('DOMContentLoaded', function() {
    let QRPs = document.getElementsByClassName('qr_p');

    for (let index = 0; index < QRPs.length; index++) {
        const element = QRPs[index];
        let data;

        try {
            // Try parsing the content as JSON
            data = JSON.parse(element.innerText);

            // Create new elements for latitude, longitude, and BinID
            let latP = document.createElement("p");
            latP.innerText = `Latitude: ${data['Lat']}`;

            let lonP = document.createElement("p");
            lonP.innerText = `Longitude: ${data['Lon']}`;

            let BinP = document.createElement("p");
            BinP.innerText = `BinID: ${data['BinID']}`;

            // Replace the original content with the new elements
            element.innerHTML = '';  // Clear the original content
            element.appendChild(BinP);
            element.appendChild(latP);
            element.appendChild(lonP);
        } catch (error) {
            console.error('Error parsing JSON:', error);
            // Handle the error, e.g., by displaying a message to the user
        }
    }
});