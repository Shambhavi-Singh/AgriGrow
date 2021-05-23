//basic animations
//title animation
$("#logo").mouseenter(() => {
  $("#logo").addClass(`woggleTop`);
  setTimeout(() => {
    $("#logo").removeClass(`woggleTop`);
  }, 1000);
});

//right-nav logic
let toggle_right_nav = true;
$(`#right-nav-switch`).click(() => {
  if (toggle_right_nav) {
    $("#right-nav-switch > img").css("float", "right");
    $(".hidden").removeClass("hidden");
    $(`#right-nav`).removeClass("slideOut");
    $(`#right-nav`).addClass("slideIn");
    $(`#right-nav`).css("width", "250px");
    $(`#right-nav-switch > img`).removeClass("flip-out");
    $(`#right-nav-switch > img`).addClass("flip");
    $(`#right-nav-switch > img`).css("transform", "rotateY(180deg)");
    toggle_right_nav = !toggle_right_nav;
  } else {
    setTimeout(() => {
      $("#right-nav > ul > li > span").addClass("hidden");
      $("#right-nav-switch > img").css("float", "left");
    }, 500);
    $(`#right-nav`).removeClass("slideIn");
    $(`#right-nav`).addClass("slideOut");
    $(`#right-nav`).css("width", "60px");
    $(`#right-nav-switch > img`).removeClass("flip");
    $(`#right-nav-switch > img`).addClass("flip-out");
    $(`#right-nav-switch > img`).css("transform", "rotateY(0deg)");
    toggle_right_nav = !toggle_right_nav;
  }
});

//welcome text logic:
const removeHiddenWelcomeMessage = () => {
  console.log("here");
  $(".tohide").addClass("fadeIn").removeClass("hidden");
};
const welcomeMessage = "Crop Recommender . System";
let atText = 0;
displayWelcomeMessage = () => {
  console.log(atText);
  if (welcomeMessage.charAt(atText) == ".")
    $("#welcome").html(`${$("#welcome").text()} <br>`);
  else
    $("#welcome").html(() => {
      return `${$("#welcome").html()}${welcomeMessage.charAt(atText)}`;
    });
  atText++;
  if (atText <= welcomeMessage.length) {
    setTimeout(displayWelcomeMessage, 60);
  } else {
    removeHiddenWelcomeMessage();
  }
};
$(window).ready(() => {
  displayWelcomeMessage();
});

$("#right-nav ul li").each((index, value) => {
  if (index == 0) return;
  $(`#right-nav ul li:nth-of-type(${index + 1})`).click(() => {
    atText = 0;
    $("#welcome").html("");
    $("section").css("display", "none");
    $(`#s${index}`).css("display", "block");
    if (index == 1) {
      displayWelcomeMessage();
    } else {
      $(".tohide").removeClass("fadeIn").addClass("hidden");
    }
    if (index == 2) {
      $("body").css("background-image", "url('images/instPage.jpg')");
      bubbly({
        colorStart: "hsla(360, 100%, 100%, 0.1)",
        colorStop: "hsla(360, 100%, 100%, 0.1)",
        blur: 1,
        compose: "source-over",
        bubbleFunc: () => `hsla(${Math.random() * 50}, 100%, 50%, .3)`,
        bubbles: Math.floor(($("body").height() + $("body").width()) * 0.015),
      });
    } else {
      $("canvas").remove("body > canvas");
      $("body").css("background-image", "url('images/homePage.jpg')");
    }
  });
});
