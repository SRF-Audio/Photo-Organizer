function retrieveAllMediaItems(Photos) {
  return Photos.mediaItems();
}

function processMediaItemsInBatches(mediaItems, batchSize = 500) {
  var mediaItemIDs = [];
  var errorIDs = []; // List to store IDs of items that caused errors
  var currentIndex = 0;
  var endIndex = Math.min(currentIndex + batchSize, mediaItems.length);

  while (currentIndex < mediaItems.length) {
    for (let i = currentIndex; i < endIndex; i++) {
      try {
        mediaItemIDs.push(mediaItems[i].id()); // Attempt to retrieve the ID
      } catch (err) {
        errorIDs.push(mediaItems[i].id()); // Add ID to error list if an error occurs
      }
    }

    // Update currentIndex to the next batch's start index
    currentIndex = endIndex;
    endIndex = Math.min(currentIndex + batchSize, mediaItems.length);
  }

  return { mediaItemIDs: mediaItemIDs, errorIDs: errorIDs };
}

function run() {
  var output = {
    mediaItems: [],
    errorItems: [],
  };

  try {
    var Photos = Application("Photos");
    Photos.activate(); // Ensure Photos is active
    var allMediaItems = retrieveAllMediaItems(Photos);
    var results = processMediaItemsInBatches(allMediaItems);
    output.mediaItems = results.mediaItemIDs;
    output.errorItems = results.errorIDs;
  } catch (err) {
    output.error = err.message;
  }

  console.log(JSON.stringify(output)); // Final output to stdout
}

run();
