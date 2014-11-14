/**
 * Created by fayelisifi on 13/11/14.
 */
var main = function(){
    console.log("Javascipt loaded successfully.");
    $(".customer-button").click(
        function(){

            var buttonid = $(this).attr('id');
            console.log("Button clicked:" + buttonid);
            var panelid = buttonid.replace("-button", "-panel");
            console.log("Panelid:" + panelid);

            if ($('#' + panelid).hasClass("active-summary-panel")){
                console.log("The panel is currently displayed");
                $('#' + panelid).toggle('400', function() {
                    $(this).toggleClass("active-summary-panel");
                });

                $('#initial-panel').toggle('400', function() {
                    $(this).toggleClass("active-summary-panel");
                });
            } else {
                console.log("The panel is not currently displayed");
                $(".active-summary-panel").toggle('400', function() {
                    $(this).toggleClass("active-summary-panel");
                });
                $('#' + panelid).toggle('400', function() {
                    $(this).toggleClass("active-summary-panel");
                });
            }
        }
    );

}

$(document).ready(main);