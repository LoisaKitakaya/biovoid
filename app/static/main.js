const clearNotification = () => {
  const notificationBox = document.getElementById("flash-box");
  notificationBox.remove();
};

var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

const createNewUser = () => {
  const userForm = document.getElementById("user-form");
  userForm.submit();
};
