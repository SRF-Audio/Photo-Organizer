#!/usr/bin/osascript -l JavaScript

var Photos = Application("Photos");
var itemId = "{{mediaItemId}}";

function exportMediaItem(itemId) {
    var item = Photos.mediaItems.byId(itemId);
    if (item) {
        var exportPath = "./temp_photo_exports/" + item.filename();
        item.export({to: exportPath});
        return exportPath;
    } else {
        throw new Error("Media item not found.");
    }
}

try {
    var exportPath = exportMediaItem(itemId);
    return JSON.stringify({ path: exportPath });
} catch (e) {
    return JSON.stringify({ error: e.message });
}
