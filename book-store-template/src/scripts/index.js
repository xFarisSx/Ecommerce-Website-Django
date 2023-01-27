import "../styles/index.scss";

// import Libraries
import "bootstrap";
import "../../node_modules/@fortawesome/fontawesome-free/js/all.js";
import Swiper from "../../node_modules/swiper";
import { Notyf } from "notyf";

window.bootstrap = require("bootstrap");
// Create an instance of Notyf
window.notyf = new Notyf({
  types: [
    {
      type: "error",
      icon: false,
      dismissible: true,
    },
    {
      type: "success",
      icon: false,
      dismissible: true,
    },
  ],
});

// init Swiper:
new Swiper(".main-slider", {
  pagination: {
    el: ".swiper-pagination",
    dynamicBullets: true,
  },
});

if (process.env.NODE_ENV === "development") {
  require("../index.html");
}

console.log("webpack starterkit");
