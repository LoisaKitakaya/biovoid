const notificationBox = document.getElementById("flash-box");

const clearNotification = () => {
  notificationBox.remove();
};

setTimeout(clearNotification, 5000);

var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});

var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

const createNewUser = () => {
  const userForm = document.getElementById("user-form");
  userForm.submit();
};

const generateArt = () => {
  const generateForm = document.getElementById("generate-art-form");
  generateForm.submit();
};

const photoToArt = () => {
  const generateForm = document.getElementById("photo-to-art-form");
  generateForm.submit();
};

const imageVariation = () => {
  const generateForm = document.getElementById("image-variation-form");
  generateForm.submit();
};

const uploadImage = () => {
  const uploadForm = document.getElementById("image-upload-form");
  uploadForm.submit();
};

const downloadImage = (url, fileName) => {
  var link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", fileName);
  link.click();
};
