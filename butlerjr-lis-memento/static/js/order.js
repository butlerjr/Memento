/**
 * Created by fayelisifi on 13/11/14.
 */
var main = function(){
    console.log("Javascipt loaded successfully.");
    $("#james-button").click(
        function(){
            console.log("James button clicked");
            $(".active-panel").removeClass("active-panel");
            $("#james-summary-panel").toggle("active-panel");
        }
    );


    $("#robouser-button").click(
        function(){
            console.log("James button clicked");
            $(".active-panel").removeClass("active-panel");
            $("#robouser-summary-panel").toggle("active-panel");
        }
    );
}

$(document).ready(main);