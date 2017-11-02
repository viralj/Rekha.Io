function gup(name, url) {
    if (!url) url = location.href;
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    let regexS = "[\\?&]" + name + "=([^&#]*)";
    let regex = new RegExp(regexS);
    let results = regex.exec(url);
    return results == null ? null : results[1];
}
$(document).ready(function () {
    $('.modal').modal();

    let signupF = $('#_sf');    //signup form
    let loginF = $('#_lf');     //login form
    let signupB = $('#_sfb');    //signup button
    let loginB = $('#_lfb');     //login button

    let actionF = $('#action_form');

    let toggler = function (i) {
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