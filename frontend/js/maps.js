let usersFromDb = [];

function getData() {
  fetch("http://z2j.hqr.at/users", {})
    .then((res) => res.json())
    .then((res) => {
      console.log(res);
      usersFromDb = res;
    });
}

async function initMap() {
  geocoder = new google.maps.Geocoder();
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 8,
    center: { lat: 52, lng: 21 },
  });
  //return all markers
  await getData();
  await setMarkers(map);

  //return all users on Map
  usersInBounds = await createListOfUsersInBounds(map);
  // usersInBounds = await codeAddress(usersInBounds);

  //create divs with users
  await createListOfUsersOnLayout(usersInBounds);

  //change size of map and create new list
  await changeSizeOfMap(map);
}

// function which create list of markers
async function createListOfUsersInBounds(map) {
  let allMarkers = await setMarkers(map);
  usersInBounds = [];

  allMarkers.map((marker) => {
    if (map.getBounds().contains(marker.getPosition())) {
      if (usersInBounds.includes(marker)) {
      } else {
        usersInBounds.push(marker);
      }
    }
  });
  // }

  return usersInBounds;
}

async function checkIfMarkerIsInBounds(marker, usersInBounds) {
  if (map.getBounds().contains(marker.getPosition())) {
    if (usersInBounds.includes(marker)) {
    } else {
      usersInBounds.push(marker);
    }
  }
}

//function to create list of markers on layout
async function createListOfUsersOnLayout(usersInBounds) {
  //check filtering buttons
  if (be === true) {
    const markersOnMapAfterFiltering = Object.values(usersInBounds).filter((bar) => bar.stack.includes("be"));
    usersInBounds = markersOnMapAfterFiltering;
  } else if (fe === true) {
    const markersOnMapAfterFiltering = Object.values(usersInBounds).filter((bar) => bar.stack.includes("fe"));
    usersInBounds = markersOnMapAfterFiltering;
  }
  //create divs with data
  for (i = 0; i < usersInBounds.length; i++) {
    if (document.getElementById(usersInBounds[i].title) === null) {
      //create an element
      bar = document.createElement("div");
      bar.id = usersInBounds[i].stack + usersInBounds[i].title;
      bar.className = "user__bar";
      document.getElementsByClassName("user__bars")[0].appendChild(bar);
      //create elements inside
      let img = document.createElement("img");
      img.setAttribute("src", "img/discord.png");
      img.className = "discord__img";
      img.style.border = usersInBounds[i].icon === "img/blue-pin.png" ? "3px solid #2192ff;" : "3px solid #f0ff42";
      usersInBounds[i].icon === "img/blue-pin.png" ? "3px solid red" : "3px solid green";
      document.getElementsByClassName("user__bar")[i].appendChild(img);
      let name = document.createElement("p");
      let nameText = document.createTextNode(usersInBounds[i].title);
      name.appendChild(nameText);
      document.getElementsByClassName("user__bar")[i].appendChild(name);
      let city = document.createElement("p");
      city.style.fontWeight = "600";
      let cityText = document.createTextNode(usersInBounds[i].city_name);
      city.appendChild(cityText);
      document.getElementsByClassName("user__bar")[i].appendChild(city);
    }
  }
}
async function changeSizeOfMap(map) {
  await google.maps.event.addListener(map, "bounds_changed", async function () {
    document.querySelectorAll("div.user__bar").forEach((n) => n.remove());
    usersInBounds = await createListOfUsersInBounds(map);
    await createListOfUsersOnLayout(usersInBounds);
  });
}
// //change postal code to lat and lang
// async function codeAddress(addressesToCode) {
//   for (let i = 0; i < addressesToCode.length; i++) {
//     let user = addressesToCode[i];
//     let address = user.postal_code;
//     await geocoder.geocode({ address: address }, async function (results, status) {
//       if (status == "OK") {
//         lat = (results[0].geometry.bounds.Va.lo + results[0].geometry.bounds.Va.hi) / 2;
//         lng = (results[0].geometry.bounds.Ja.lo + results[0].geometry.bounds.Ja.hi) / 2;
//         city = results[0].geometry;
//         user.lat = lat;
//         user.lng = lng;
//         user.city = results[0].address_components[1].long_name;

//         return addressesToCode;
//       } else {
//         alert("Geocode was not successful for the following reason: " + status);
//         return [];
//       }
//     });
//   }
//   return addressesToCode;
// }

async function setMarkers(map) {
  const shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: "poly",
  };
  let allMarkers = [];
  usersFromDb.map((user) => {
    let marker = new google.maps.Marker({
      position: { lat: user.lat, lng: user.lng },
      map,
      icon: user.stack === "be" ? "img/yellow-pin.png" : "img/blue-pin.png",
      shape: shape,
      title: user.discord,
      city_name: user.city_name,
      stack: user.stack,
    });
    allMarkers.push(marker);

    const infowindow = new google.maps.InfoWindow({
      content: user.discord,
    });
    marker.addListener("click", () => {
      infowindow.open({
        anchor: marker,
        map,
      });
    });
  });
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
