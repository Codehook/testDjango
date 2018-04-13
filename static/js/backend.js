/**
 * These will execute on load
 */
$('.message .close').click(function() {
    $(this).closest('.message').transition('fade');
});
$('a.sidebar-toggle').click(function() {
    $('.ui.sidebar').sidebar('toggle');
});
$('.ui.accordion').accordion();
$('.ui.checkbox').checkbox();
$('.ui.dropdown').dropdown();
