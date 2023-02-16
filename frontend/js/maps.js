let usersWithCity = [
  ["#Magda2013", "Warszawa", "fe"],
  ["#Janek2921", "Piaseczno", "be"],
  ["#Marek2141", "Józefów", "fe"],
  ["#Jagoda2927", "Los Angeles", "fe"],
  ["#Bartek2191", "Grójec", "fe"],
  ["#Maciek2918", "Rybnik", "fe"],
];

async function initMap() {
  geocoder = new google.maps.Geocoder();
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 52, lng: 21 },
  });
  usersWithCord = await codeAddress(usersWithCity);
  //return all markers
  await setMarkers(map);
  //return all users on Map
  usersInBounds = await createListOfUsersInBounds(map);

  //create divs with users
  await createListOfUsersOnLayout(usersInBounds);

  //change size of map and create new list
  await changeSizeOfMap(map);
}

// function which create list of markers
async function createListOfUsersInBounds(map) {
  let allMarkers = await setMarkers(map);
  usersInBounds = [];
  for (let i = 0; i < allMarkers.length; i++) {
    if (map.getBounds().contains(allMarkers[i].getPosition())) {
      if (usersInBounds.includes(allMarkers[i])) {
        continue;
      } else {
        usersInBounds.push(allMarkers[i]);
      }
    }
  }
  return usersInBounds;
}

//function to create list of markers on layout
async function createListOfUsersOnLayout(usersOnMap) {
  //check filtering buttons
  if (be === true) {
    const markersOnMapAfterFiltering = Object.values(usersOnMap).filter((bar) => bar.stack.includes("be"));
    usersOnMap = markersOnMapAfterFiltering;
  } else if (fe === true) {
    const markersOnMapAfterFiltering = Object.values(usersOnMap).filter((bar) => bar.stack.includes("fe"));
    usersOnMap = markersOnMapAfterFiltering;
  }
  //create divs with data
  for (i = 0; i < usersOnMap.length; i++) {
    if (document.getElementById(usersOnMap[i].title) === null) {
      //create an element
      bar = document.createElement("div");
      bar.id = usersOnMap[i].stack + usersOnMap[i].title;
      bar.className = "user__bar";
      document.getElementsByClassName("user__bars")[0].appendChild(bar);
      //create elements inside
      let img = document.createElement("img");
      img.setAttribute("src", "img/discord.png");
      img.className = "discord__img";
      img.style.border = usersOnMap[i].icon === "img/blue-pin.png" ? "3px solid #2192ff;" : "3px solid #f0ff42";
      usersOnMap[i].icon === "img/blue-pin.png" ? "3px solid red" : "3px solid green";
      document.getElementsByClassName("user__bar")[i].appendChild(img);
      let name = document.createElement("p");

      let nameText = document.createTextNode(usersOnMap[i].title);
      name.appendChild(nameText);
      document.getElementsByClassName("user__bar")[i].appendChild(name);
      let city = document.createElement("p");
      city.style.fontWeight = "600";
      let cityText = document.createTextNode(usersOnMap[i].city);
      city.appendChild(cityText);
      document.getElementsByClassName("user__bar")[i].appendChild(city);
    }
  }
}
async function changeSizeOfMap(map) {
  await google.maps.event.addListener(map, "bounds_changed", async function () {
    document.querySelectorAll("div.user__bar").forEach((n) => n.remove());
    await createListOfUsersInBounds(map);
    await createListOfUsersOnLayout(usersInBounds);
  });
}
//change city to lat and lang
async function codeAddress(addressesToCode) {
  for (let i = 0; i < addressesToCode.length; i++) {
    let user = addressesToCode[i];
    let address = user[1];
    await geocoder.geocode({ address: address }, async function (results, status) {
      if (status == "OK") {
        lat = (results[0].geometry.bounds.Ya.lo + results[0].geometry.bounds.Ya.lo) / 2;
        lng = (results[0].geometry.bounds.Ma.lo + results[0].geometry.bounds.Ma.hi) / 2;
        user.splice(1, 0, lat);
        user.splice(2, 0, lng);
        return addressesToCode;
      } else {
        alert("Geocode was not successful for the following reason: " + status);
        return [];
      }
    });
  }
  return addressesToCode;
}

async function setMarkers(map) {
  const shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: "poly",
  };
  let allMarkers = [];

  for (let i = 0; i < usersWithCord.length; i++) {
    const user = usersWithCord[i];

    let marker = new google.maps.Marker({
      position: { lat: user[1], lng: user[2] },
      map,
      icon: user[4] === "be" ? "img/yellow-pin.png" : "img/blue-pin.png",
      shape: shape,
      title: user[0],
      city: user[3],
      stack: user[4],
    });

    allMarkers.push(marker);

    const infowindow = new google.maps.InfoWindow({
      content: user[0],
    });
    marker.addListener("click", () => {
      infowindow.open({
        anchor: marker,
        map,
      });
    });
  }
  return allMarkers;
}

//filtering list by buttons
let be = false;
let fe = false;

function activeClassForBtn(btn) {
  if (be) {
    btn = document.getElementById("be");
    btn.style.border = "2px solid red";
  } else if (fe) {
    btn = document.getElementById("fe");
    btn.style.border = "2px solid red";
  } else {
    btn = document.getElementById("be");
    btn.style.border = "";
    btn = document.getElementById("fe");
    btn.style.border = "";
  }
}
async function listFiltering(filter) {
  if (filter === "be") {
    be = !be;
  } else if (filter === "fe") {
    fe = !fe;
  }
  activeClassForBtn(filter);
}
window.initMap = initMap;
