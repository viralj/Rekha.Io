function gup(name, url) {
    if (!url) url = location.href;
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(url);
    return results == null ? null : results[1];
}
$(document).ready(function () {
    var signupF = $('#_sf');    //signup form
    var loginF = $('#_lf');     //login form
    var signupB = $('#_sfb');    //signup button
    var loginB = $('#_lfb');     //login button

    var actionF = $('#action_form');

    var toggler = function (i) {
        /*
         * If signup button is clicked, add active class to signup button else add it to login class
         * */
        if (i == 1) {
            $(signupB).removeClass('_aha');
            $(loginB).addClass('_aha');

            $(actionF).html("").html($(loginF).html());

        } else {
            $(loginB).removeClass('_aha');
            $(signupB).addClass('_aha');
            $(actionF).html("").html($(signupF).html());
        }
    };

    /*
     * Default, we are showing sign up form if url does not have show login
     * */
    toggler(gup('_req') == "login" ? 1 : 0);

    $(signupB).on('click', function () {
        toggler(0);
    });

    $(loginB).on('click', function () {
        toggler(1);
    });
});