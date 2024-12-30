document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".flash");
    flashMessages.forEach((msg) => {
      setTimeout(() => msg.remove(), 5000); // Remove flash messages after 5 seconds
    });
  });