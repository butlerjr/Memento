/**
 * Created by fayelisifi on 11/11/14.
 */
function equalHeight(group) {
    var tallest = 0;
    group.each(function() {
        var thisHeight = $(this).height();
        if(thisHeight > tallest) {
            tallest = thisHeight;
        }
    });
    group.each(function() { $(this).height(tallest); });
}

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

    $(".edit-button").click(
        function(){
            var caption = $(this).parent();
            var pricechangemenu = $(this).parent().next();
            var price = caption.find('text').text();
            price = price.replace("$","")
            caption.slideToggle();
            pricechangemenu.slideToggle();
            var pricebox = pricechangemenu.find('#mySpinbox');
            pricebox.spinbox('value', price);
        }
    );

    $(".save-button").click(
        function(){
            var caption = $(this).parent().prev();
            var pricechangemenu = $(this).parent();
            var pricebox = pricechangemenu.find('#mySpinbox');
            var price = pricebox.spinbox('value');
            price = "$" + price + ".0";
            $(caption).find('text').text(price);
            caption.slideToggle();
            pricechangemenu.slideToggle();
        }
    );

    $(".cancel-button").click(
        function(){
            $(this).parent().prev().slideToggle();
            $(this).parent().slideToggle();
        }
    );

    $(".save-button").hover(
        function(){
            // Mouse in
            $(this).addClass("hover-button");

        },
        function(){
            // Mouse out
            $(this).removeClass("hover-button");
        }
    );

    $(".cancel-button").hover(
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