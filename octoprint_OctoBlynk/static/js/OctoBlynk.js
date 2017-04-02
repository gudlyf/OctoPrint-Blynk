/*
 * View model for OctoPrint-Blynk
 *
 * Author: Keith McDuffee
 * License: AGPLv3
 */
$(function() {
    function OctoblynkViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        OctoblynkViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        [ /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_OctoBlynk, #tab_plugin_OctoBlynk, ...
        [ /* ... */ ]
    ]);
});
