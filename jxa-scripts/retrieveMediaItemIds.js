// console.log("Script loaded at:", new Date().toISOString());

var Photos = Application("Photos");
Photos.activate();

function retrieveAllMediaItems(Photos) {
  return Photos.mediaItems();
}

function processMediaItemsInBatches(mediaItems, batchSize = 500) {
  var mediaItemIDs = [];
  var errorIDs = [];
  var currentIndex = 0;
  var endIndex = Math.min(currentIndex + batchSize, mediaItems.length);

  while (currentIndex < mediaItems.length) {
    for (let i = currentIndex; i < endIndex; i++) {
      try {
        mediaItemIDs.push(mediaItems[i].id());
      } catch (err) {
        errorIDs.push(mediaItems[i].id());
      }
    }

    currentIndex = endIndex;
    endIndex = Math.min(currentIndex + batchSize, mediaItems.length);
  }

  return { mediaItemIDs: mediaItemIDs, errorIDs: errorIDs };
}

function run() {
  var output = {
    runId: new Date().toISOString(),
    mediaItems: [],
    errorItems: [],
  };

  try {
    var allMediaItems = retrieveAllMediaItems(Photos);
    var results = processMediaItemsInBatches(allMediaItems);
    output.mediaItems = results.mediaItemIDs;
    output.errorItems = results.errorIDs;
  } catch (err) {
    output.error = err.message;
  }

  // console.log(JSON.stringify(output));
  return JSON.stringify(output);
}

run();

// console.log("Script ended at:", new Date().toISOString());
