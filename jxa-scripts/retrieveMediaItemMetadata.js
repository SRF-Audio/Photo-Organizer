#!/usr/bin/osascript -l JavaScript

var Photos = Application("Photos");

function retrieveAllMediaItems(Photos) {
  return Photos.mediaItems();
}

function processMediaItemsInBatches(mediaItems, batchSize = 500) {
  var mediaItemsData = [];
  var errorIDs = [];
  var currentIndex = 0;
  var endIndex = Math.min(currentIndex + batchSize, mediaItems.length);

  while (currentIndex < mediaItems.length) {
    for (let i = currentIndex; i < endIndex; i++) {
      try {
        var item = mediaItems[i];
        var mediaData = {
          _id: item.id(),
          name: item.name() || null,
          description: item.description() || null,
          keywords: item.keywords() || [],
          filename: item.filename() || null,
        };
        mediaItemsData.push(mediaData);
      } catch (err) {
        errorIDs.push(item.id());
      }
    }

    currentIndex = endIndex;
    endIndex = Math.min(currentIndex + batchSize, mediaItems.length);
  }

  return { mediaItemsData: mediaItemsData, errorIDs: errorIDs };
}

function retrieveMetaData() {
  var output = {
    runId: new Date().toISOString(),
    mediaItems: [],
    errorItems: [],
  };

  try {
    var allMediaItems = retrieveAllMediaItems(Photos);
    var results = processMediaItemsInBatches(allMediaItems);
    output.mediaItems = results.mediaItemsData;
    output.errorItems = results.errorIDs;
  } catch (err) {
    output.error = err.message;
  }

  console.log(JSON.stringify(output));
}

retrieveMetaData();
