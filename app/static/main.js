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

const data = {
  id: "cc93759d-7a58-41b7-b4af-d764af3f3df2",
  invoice: {
    invoice_id: "Y6BOV7Y",
    state: "PENDING",
    provider: "M-PESA",
    charges: "0.00",
    net_amount: 1.0,
    currency: "KES",
    value: "1.00",
    account: "254725131828",
    api_ref: "Direct Bill (API Request)",
    mpesa_reference: None,
    host: "41.90.56.51",
    failed_reason: None,
    failed_code: None,
    failed_code_link: "https://intasend.com/troubleshooting",
    created_at: "2023-03-01T16:27:58.135101+03:00",
    updated_at: "2023-03-01T16:27:58.135119+03:00",
  },
  customer: {
    customer_id: "0VVB4G0",
    phone_number: "254725131828",
    email: None,
    first_name: None,
    last_name: None,
    country: None,
    zipcode: None,
    provider: "M-PESA",
    created_at: "2023-03-01T14:31:12.171327+03:00",
    updated_at: "2023-03-01T14:31:12.171352+03:00",
  },
  payment_link: None,
  customer_comment: None,
  refundable: False,
  created_at: "2023-03-01T16:27:58.148903+03:00",
  updated_at: "2023-03-01T16:27:58.148920+03:00",
};