function addMe(form) {
  event.preventDefault();
  let nick = form.discord.value;
  let postal_code = form.postal_code.value;
  let stack = form.radiobutt.value;
  console.log(nick, postal_code, stack);

  fetch("http://z2j.hqr.at/users", {
    headers: { "Content-Type": "application/json" },
    method: "POST",
    body: JSON.stringify({
      discord: nick,
      zip_code: postal_code,
      stack: stack,
    }),
  })
    .then((res) => {
      console.log(res);
      // console.log(res.body.getReader());
      return res.json();
    })

    .then((res) => {
      console.log(res.detail);
      if (res.detail !== undefined) {
        alert(res.detail);
      } else {
        console.log("wchodze tu");
        setTimeout(() => {
          form.submit();
        }, "1000");
      }
    });
}
