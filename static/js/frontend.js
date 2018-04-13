/**
 * Controls the floating menu
 */
$(".breakpoint").visibility({
    once: !1,
    onBottomPassed: function() {
        $(".fixed.menu").transition("fade in");
    },
    onBottomPassedReverse: function() {
        $(".fixed.menu").transition("fade out");
    }
});

/**
 * Controls the side bar
 */
$(".ui.sidebar").sidebar("attach events", ".toc.item");
