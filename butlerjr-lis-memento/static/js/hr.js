/**
 * Created by fayelisifi on 11/11/14.
 */
var main = function() {
    console.log("Javascipt loaded successfully.");

    $(".delete-button").hover(
        function(){
            // Mouse in
            $(this).addClass("hover-button");

        },
        function(){
            // Mouse out
            $(this).removeClass("hover-button");
        }
    );

    $(".delete-button").click(
        function(){

        }
    );


    $(".edit-button").hover(
        function(){
            // Mouse in
            $(this).addClass("hover-button");

        },
        function(){
            // Mouse out
            $(this).removeClass("hover-button");
        }
    );
}

$(document).ready(main);