function readJsonFromFile(url) {
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      onMessageArrived(data);
    })
    .catch(error => {
      console.error('Failed to fetch JSON:', error);
    });
}

function onMessageArrived(data) {
  console.log("Data Arrived:", data);
  if (document.getElementById("status") && document.getElementById("datetime")) {
    document.getElementById("status").innerHTML = data.traffic_status;
    console.log(data.traffic_status);
    document.getElementById("datetime").innerHTML = data.datetime;
    console.log(data.datetime);
  } else {
    console.error("HTML elements for displaying data not found.");
  }
}

// Usage
const jsonUrl = 'https://junctionkanshi.puritjess.com/traffic_data.json'; // Change this to the URL of your JSON file

// Set interval to fetch JSON every 3 sec
setInterval(() => {
  readJsonFromFile(jsonUrl);
}, 3000);

// Optionally perform an immediate fetch on page load
readJsonFromFile(jsonUrl);
