$(function() {
    $("textarea").val('');
    $("#certificate").hide().bind('click focus', function() { this.select(); } );
    $("#certform").submit(function(event) {
        event.preventDefault();
        $("#postgenerate").slideDown("slow");
        $.post("/generate", $(this).serialize(), function(data) {
            $("#certificate").val(data).fadeIn("slow");
            $('html, body').animate({
                scrollTop: $("#postgenerate").offset().top
            }, 1500);
        }, "text");
   });
});
