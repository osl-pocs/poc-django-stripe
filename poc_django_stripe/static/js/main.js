function confirm_message(url, message) {
  if (confirm(message)) {
    window.location.replace(url);
  }
}
