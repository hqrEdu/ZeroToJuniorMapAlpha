function addMe(form) {
  event.preventDefault();
  let nick = form.discord.value;
  let city = form.city.value;
  let stack = form.backend.checked;
  let stack2 = form.frontend.checked;

  console.log(nick, city, stack, stack2);
}
