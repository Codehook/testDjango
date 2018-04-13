// OAuth token and picker api config.
var pickerApiLoaded = false;
var oauthToken;
// Scope to use to access user's Drive items.
var scope = ['https://www.googleapis.com/auth/drive'];
// The Browser API key obtained from the Google Developers Console.
var developerKey;
// The Client ID obtained from the Google Developers Console. Replace with your own Client ID.
var clientId;
// Replace with your own App ID (Its the first number in your Client ID).
var appId;
// Initialize the Google Drive picker.
function initPicker(developerKeyIn, clientIdIn, appIdIn) {
    developerKey = developerKeyIn;
    clientId = clientIdIn;
    appId = appIdIn;
}
// Use the Google API Loader script to load the google.picker script.
function loadPicker() {
    gapi.load('auth', {
        'callback': onAuthApiLoad
    });
    gapi.load('picker', {
        'callback': onPickerApiLoad
    });
}
function onAuthApiLoad() {
    window.gapi.auth.authorize({
            'client_id': clientId,
            'scope': scope,
            'immediate': false
        },
        handleAuthResult);
}
function onPickerApiLoad() {
    pickerApiLoaded = true;
    createPicker();
}
function handleAuthResult(authResult) {
    if(authResult && !authResult.error) {
        oauthToken = authResult.access_token;
        createPicker();
    }
}
// Create and render a Picker object for searching images.
function createPicker() {
    if(pickerApiLoaded && oauthToken) {
        var view = new google.picker.DocsView(google.picker.ViewId.DOCS);
        view.setMode(google.picker.DocsViewMode.GRID);
        //view.setMimeTypes("image/png,image/jpeg,image/jpg");
        var picker = new google.picker.PickerBuilder()
            //.enableFeature(google.picker.Feature.NAV_HIDDEN)
            .enableFeature(google.picker.Feature.MULTISELECT_ENABLED)
            .setAppId(appId)
            .setOAuthToken(oauthToken)
            .addView(view)
            //.addView(new google.picker.Doc)
            //.addView(new google.picker.DocsUploadView())
            .setDeveloperKey(developerKey)
            .setCallback(pickerCallback)
            .build();
        picker.setVisible(true);
    }
}
// A simple callback implementation.
function pickerCallback(data) {
    if(data.action == google.picker.Action.PICKED) {
        var fileId = data.docs[0].id;
        $('#result').text(fileId);
        uploadFile(fileId);
    }
}
// Submit the form.
function uploadFile(fileId) {
    $('[name=file_id]').val(fileId);
    $('#hidden').submit();
}
