// Adapting search bar to selected CSS theme,
// when DOM is ready, or checkbox is clicked

adaptSearchBarTheme = function() {
    if ($('#darkSwitch').is(':checked')) {
        $('.search-bar').css({'background-color': 'var(--dark-background-variant)',
                              'color': 'var(--broken-white)'});
        $('.form-control').css({'border': '1px solid var(--dark-background-variant)',
                                'transition-duration': '0.01s'});
        }
    else {
        $('.search-bar').css({'background-color': 'white',
                              'color': 'black'});
        $('.form-control').css({'border': '1px solid var(--grey-variant-4)'});
        }
    };      

$(document).ready(function() {
    adaptSearchBarTheme();            
});

$('#darkSwitch').click(function() {
    adaptSearchBarTheme();
});