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
            name = $(this).find(".name").html();
            entityKey = $(this).find(".entity-key").html();
            $("#delete-confirmation-modal #name").html(name);
            $("#delete-confirmation-modal input[name=entity_key]").val(entityKey).prop("disabled", false);
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