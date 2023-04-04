function addMe(form) {
  event.preventDefault();
  let nick = form.discord.value;
  let postal_code = form.postal_code.value;
  let stack = form.radiobutt.value;

  console.log(nick, postal_code, stack);

  fetch("http://z2j.hqr.at/users", {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
    method: "POST",
    body: JSON.stringify({
      discord: nick,
      zip_code: postal_code,
      stack: stack,
    }),
  }).then((res) => console.log(res));
}
