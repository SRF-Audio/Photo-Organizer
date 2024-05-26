#!/usr/bin/osascript -l JavaScript

var Photos = Application("Photos");
var itemId = "{{mediaItemId}}";

function exportMediaItem(itemId) {
  try {
    var item = Photos.mediaItems.byId(itemId);
    if (item) {
      var exportPath = "/Users/stephenfroeber/GitHub/Photo-Organizer/jxa-scripts/temp_photo_exports/";
      Photos.export([item], { to: Path(exportPath) });
      return JSON.stringify({ path: exportPath + item.filename()});
    } else {
      throw new Error("Media item not found.");
    }
  } catch (e) {
    return JSON.stringify({ error: e.message });
  }
}

exportMediaItem(itemId);
