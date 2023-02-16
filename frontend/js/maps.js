let usersWithCity = [
  ["#Magda2013", "Warszawa", "fe"],
  ["#Janek2921", "Piaseczno", "be"],
  ["#Marek2141", "Józefów", "fe"],
  ["#Jagoda2927", "Los Angeles", "fe"],
  ["#Bartek2191", "Grójec", "fe"],
  ["#Maciek2918", "Rybnik", "fe"],
];

let geocoder;
let map;
let usersWithCord = [];
let markerList = [];
let markersOnMap = [];

async function initMap() {
  geocoder = new google.maps.Geocoder();
  let latlng = new google.maps.LatLng(52, 31);
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 52, lng: 21 },
  });

  usersWithCord = await codeAddress(usersWithCity);
  markerList = await setMarkers(map, markerList);

  // function which create list of markers
  async function createListOfUsers(markerList, markersOnMap) {
    markersOnMap = [];

    for (let i = 0; i < markerList.length; i++) {
      if (map.getBounds().contains(markerList[i].getPosition())) {
        if (markersOnMap.includes(markerList[i])) {
          continue;
        } else {
          markersOnMap.push(markerList[i]);
        }
      }
    }
    createListOfUsersOnLayout(markersOnMap);
    return markersOnMap;
  }

  //function to create list of markers on layout
  async function createListOfUsersOnLayout(markersOnMap) {
    for (i = 0; i < markersOnMap.length; i++) {
      if (document.getElementById(markersOnMap[i].title) === null) {
        //create an element
        bar = document.createElement("div");
        bar.id = markersOnMap[i].stack + markersOnMap[i].title;
        bar.className = "user__bar";
        document.getElementsByClassName("user__bars")[0].appendChild(bar);
        //create elements inside
        let img = document.createElement("img");
        img.setAttribute("src", "img/discord.png");
        img.className = "discord__img";
        img.style.border = markersOnMap[i].icon === "img/blue-pin.png" ? "3px solid #2192ff;" : "3px solid #f0ff42";
        markersOnMap[i].icon === "img/blue-pin.png" ? "3px solid red" : "3px solid green";
        document.getElementsByClassName("user__bar")[i].appendChild(img);
        let name = document.createElement("p");

        let nameText = document.createTextNode(markersOnMap[i].title);
        name.appendChild(nameText);
        document.getElementsByClassName("user__bar")[i].appendChild(name);
        let city = document.createElement("p");
        city.style.fontWeight = "600";
        let cityText = document.createTextNode(markersOnMap[i].city);
        city.appendChild(cityText);
        document.getElementsByClassName("user__bar")[i].appendChild(city);
      }
    }
  }

  //initialization of list
  createListOfUsers(markerList, markersOnMap);
  //markers which should be on list after zooming
  async function changeSizeOfMap(map, markerList, markersOnMap) {
    await google.maps.event.addListener(map, "bounds_changed", async function () {
      document.querySelectorAll("div.user__bar").forEach((n) => n.remove());
      createListOfUsers(markerList, markersOnMap);
      createListOfUsersOnLayout(markersOnMap);
    });
  }
  changeSizeOfMap(map, markerList, markersOnMap);
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

async function setMarkers(map, markerList) {
  const shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: "poly",
  };

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

    markerList.push(marker);

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
  return markerList;
}

//sorting list by buttons
async function listFiltering(filter) {
  let bars = document.querySelectorAll("div.user__bar");
  const result = Object.values(bars).filter((bar) => !bar.id.includes(filter));
  console.log(result);
  for (let i = 0; i < result.length; i++) {
    console.log(result[i].id);
    let el = document.getElementById(result[i].id);
    el.remove();
  }

  window.initMap = initMap;
}
