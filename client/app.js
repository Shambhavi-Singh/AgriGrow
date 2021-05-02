//basic animations
//title animation
$("#logo").mouseenter(()=>{$("#logo").addClass(`woggleTop`);setTimeout(()=>{$("#logo").removeClass(`woggleTop`)},1000)});



//right-nav logic
let toggle_right_nav=true;
$(`#right-nav-switch`).click(()=>{
    if(toggle_right_nav){
        $("#right-nav-switch > img").css("float","right");
        $(".hidden").removeClass("hidden");
        $(`#right-nav`).removeClass("slideOut");
        $(`#right-nav`).addClass("slideIn");
        $(`#right-nav`).css("width","230px");
        $(`#right-nav-switch > img`).removeClass("flip-out");
        $(`#right-nav-switch > img`).addClass("flip");
        $(`#right-nav-switch > img`).css("transform","rotateY(180deg)");
        toggle_right_nav = !toggle_right_nav;
    }
    else{
        
        setTimeout(()=>{$("#right-nav > ul > li > span").addClass("hidden");$("#right-nav-switch > img").css("float","left");},500);
        $(`#right-nav`).removeClass("slideIn");
        $(`#right-nav`).addClass("slideOut");
        $(`#right-nav`).css("width","60px");
        $(`#right-nav-switch > img`).removeClass("flip");
        $(`#right-nav-switch > img`).addClass("flip-out");
        $(`#right-nav-switch > img`).css("transform","rotateY(0deg)");
        toggle_right_nav = !toggle_right_nav;
    }   
});

//welcome text logic:
const welcomeMessage = "Crop Recommender . System";
let atText = 0;
displayWelcomeMessage = ()=>{
    if(welcomeMessage.charAt(atText)=='.') $("#welcome").html(`${$("#welcome").text()} <br>`);
    else $("#welcome").html(()=>{return `${$("#welcome").html()}${welcomeMessage.charAt(atText)}`});
    atText++;
    if($("#welcome").text().length<= welcomeMessage.length){
        setTimeout(displayWelcomeMessage,100);
    }
}
$(window).ready(()=>{displayWelcomeMessage()});

